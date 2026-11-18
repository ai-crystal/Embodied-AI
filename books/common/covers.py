# -*- coding: utf-8 -*-
"""系列封面生成：一套版式，按 book.json 里的 cover 配置换图、换色、换文案。

用法（一般由 books/build/figures.py 调用）：
    python books/common/covers.py --book books/intro

输出（写进该册 images/）：
    cover.jpg      正封（含书名，用于 PDF 与 README）
    backcover.jpg  封底
    cover-art.jpg  无字的同款背景（docsify 封面页用，避免书名叠两遍）
"""
import argparse
import base64
import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent          # books/common
ROOT = HERE.parent.parent                       # 仓库根
ART = ROOT / "_private" / "art"

W, H = 794, 1123


def data_uri(name):
    p = ART / name
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return "data:%s;base64,%s" % (mime, base64.b64encode(p.read_bytes()).decode())


def css(c):
    accent = c["accent"]
    ice = c["ice"]
    return f"""
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:{W}px;height:{H}px;background:#07110F;}}
.page{{width:{W}px;height:{H}px;position:relative;overflow:hidden;color:#F3F7FC;
  font-family:"SimSun","Source Han Serif SC",serif;background:#07110F;}}
.bg{{position:absolute;inset:0;background-repeat:no-repeat;background-size:cover;}}
.scrim{{position:absolute;inset:0;}}
.frame{{position:absolute;inset:30px;border:1px solid rgba(206,232,238,.20);}}
.frame:before{{content:"";position:absolute;left:-1px;top:-1px;width:26px;height:26px;
  border-left:2px solid {accent};border-top:2px solid {accent};opacity:.85;}}
.frame:after{{content:"";position:absolute;right:-1px;bottom:-1px;width:26px;height:26px;
  border-right:2px solid {ice};border-bottom:2px solid {ice};opacity:.7;}}
.inner{{position:absolute;left:76px;right:76px;top:88px;}}
.kicker{{font-family:"Microsoft YaHei",sans-serif;font-size:10.2px;letter-spacing:5.2px;
  color:{ice};font-weight:400;}}
.rule{{width:34px;height:1.5px;background:{accent};margin-top:18px;}}
h1{{font-size:66px;line-height:1.26;font-weight:600;letter-spacing:5px;color:#FCFEFF;
  margin-top:88px;text-shadow:0 3px 30px rgba(3,10,9,.92),0 0 46px rgba(4,14,12,.6);}}
.vol{{font-size:40px;line-height:1.3;letter-spacing:8px;color:{accent};margin-top:14px;
  font-weight:600;text-shadow:0 2px 22px rgba(3,10,9,.9);}}
.sub{{font-size:24px;line-height:1.5;letter-spacing:5px;color:#EFF8F6;margin-top:26px;
  text-shadow:0 2px 18px rgba(3,10,9,.85);}}
.sub2{{font-family:"Microsoft YaHei",sans-serif;font-size:13.4px;letter-spacing:4.2px;
  color:rgba(226,240,238,.88);margin-top:12px;text-shadow:0 1px 12px rgba(3,10,9,.8);}}
.barwrap{{margin-top:50px;}}
.bar{{height:3px;width:100%;
  background:linear-gradient(90deg,{ice} 0%,#B9C9F0 48%,{accent} 100%);opacity:.92;}}
.ticks{{display:flex;justify-content:space-between;margin-top:10px;
  font-family:"Microsoft YaHei",sans-serif;font-size:8.8px;letter-spacing:1.1px;
  color:rgba(232,244,240,.88);text-shadow:0 1px 10px rgba(3,10,9,.9);}}
.tag{{font-size:16.4px;line-height:1.95;letter-spacing:2.2px;color:#F3FBF8;margin-top:44px;
  text-shadow:0 2px 16px rgba(3,10,9,.9);padding-left:16px;border-left:2px solid {accent};}}
.tag i{{font-style:normal;color:{accent};}}
.bottom{{position:absolute;left:76px;right:76px;bottom:80px;}}
.author{{font-size:15.6px;letter-spacing:3.6px;color:#FBFDFF;}}
.edition{{font-family:"Microsoft YaHei",sans-serif;font-size:10px;letter-spacing:2px;
  color:rgba(214,236,232,.60);margin-top:9px;}}
h2{{font-size:38px;line-height:1.44;letter-spacing:2.6px;font-weight:600;color:#FBFDFF;
  margin-top:18px;text-shadow:0 2px 22px rgba(4,12,20,.6);}}
.panel{{margin-top:22px;padding:24px 24px 20px;border:1px solid rgba(206,232,238,.16);
  background:linear-gradient(180deg, rgba(9,22,26,.66), rgba(5,13,18,.76));}}
.lead{{font-size:12.4px;line-height:1.98;letter-spacing:.4px;color:rgba(232,246,246,.92);}}
.lead em{{font-style:normal;color:{accent};}}
.toc{{margin-top:16px;list-style:none;}}
.toc li{{display:flex;gap:10px;align-items:baseline;padding:7px 0;
  border-top:1px solid rgba(206,232,238,.10);}}
.toc li b{{font-family:"Microsoft YaHei",sans-serif;font-size:10.6px;letter-spacing:2px;
  color:{ice};font-weight:500;white-space:nowrap;}}
.toc li span{{font-family:"Microsoft YaHei",sans-serif;font-size:9.6px;line-height:1.7;
  letter-spacing:.5px;color:rgba(226,240,244,.76);}}
.quote{{margin-top:24px;font-size:15.4px;line-height:1.95;letter-spacing:1.8px;
  color:#F4FAFB;border-left:2px solid {accent};padding-left:16px;}}
.quote small{{display:block;margin-top:7px;font-family:"Microsoft YaHei",sans-serif;
  font-size:9.4px;letter-spacing:1.7px;color:rgba(214,236,240,.55);}}
.who{{font-size:14.6px;letter-spacing:3.2px;color:#FBFDFF;line-height:1.8;}}
.who span{{font-family:"Microsoft YaHei",sans-serif;font-size:10px;letter-spacing:2px;
  color:rgba(214,236,240,.55);}}
"""


def front_html(m, c):
    ticks = "".join(f"<span>{t}</span>" for t in c["ticks"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css(c)}
.bg{{background-image:url("{data_uri(c['art'])}");background-position:{c['art_pos']};}}
.scrim{{background:
  linear-gradient(100deg, rgba(4,12,11,.94) 0%, rgba(4,12,11,.80) 38%, rgba(4,12,11,.42) 70%, rgba(4,12,11,.20) 100%),
  linear-gradient(180deg, rgba(4,12,11,.72) 0%, rgba(4,12,11,.14) 30%, rgba(4,12,11,.32) 62%, rgba(3,9,9,.92) 100%);}}
</style></head><body><div class="page">
  <div class="bg"></div><div class="scrim"></div><div class="frame"></div>
  <div class="inner">
    <div class="kicker">{c['kicker']}</div>
    <div class="rule"></div>
    <h1>{c['main'][0]}</h1>
    <div class="vol">{c['main'][1]}</div>
    <div class="sub">{c['sub']}</div>
    <div class="sub2">{c['sub2']}</div>
    <div class="barwrap"><div class="bar"></div><div class="ticks">{ticks}</div></div>
    <div class="tag">{c['tag']}</div>
  </div>
  <div class="bottom">
    <div class="author">{m['author']}</div>
    <div class="edition">{m['year']} 年 · 第一版　·　{c['foot']}　·　CC BY-NC-SA 4.0</div>
  </div>
</div></body></html>"""


def back_html(m, c):
    rows = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in c["back_sections"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css(c)}
.bg{{background-image:url("{data_uri(c['back_art'])}");background-position:{c['back_pos']};}}
.scrim{{background:
  radial-gradient(720px 520px at 78% 16%, rgba(6,16,30,.28), transparent 74%),
  linear-gradient(180deg, rgba(4,10,18,.86) 0%, rgba(4,10,18,.66) 34%, rgba(4,10,18,.82) 76%, rgba(3,7,12,.95) 100%);}}
</style></head><body><div class="page">
  <div class="bg"></div><div class="scrim"></div><div class="frame"></div>
  <div class="inner">
    <div class="kicker">ABOUT THE BOOK</div>
    <div class="rule"></div>
    <h2>{c['back_title']}</h2>
    <div class="panel">
      <div class="lead">{c['back_lead']}</div>
      <ul class="toc">{rows}</ul>
    </div>
    <div class="quote">{c['quote']}<small>{c['quote_src']}</small></div>
  </div>
  <div class="bottom">
    <div class="who">{m['author']}<br><span>{m['year']} 年 · 第一版　·　{c['foot']}</span></div>
  </div>
</div></body></html>"""


def art_html(c):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css(c)}
.bg{{background-image:url("{data_uri(c['art'])}");background-position:{c['art_pos']};}}
.scrim{{background:
  linear-gradient(100deg, rgba(4,12,11,.88) 0%, rgba(4,12,11,.64) 42%, rgba(4,12,11,.34) 72%, rgba(4,12,11,.24) 100%),
  linear-gradient(180deg, rgba(4,12,11,.72) 0%, rgba(4,12,11,.16) 32%, rgba(4,12,11,.34) 64%, rgba(3,9,9,.88) 100%);}}
</style></head><body><div class="page">
  <div class="bg"></div><div class="scrim"></div><div class="frame"></div>
</div></body></html>"""


def build(vol_dir, browser=None):
    vol_dir = Path(vol_dir)
    meta = json.load(open(vol_dir / "book.json", encoding="utf-8"))
    c = meta["cover"]
    out = vol_dir / "images"
    out.mkdir(parents=True, exist_ok=True)

    def shoot(b, name, html):
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=3)
        pg.set_content(html, wait_until="load")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(450)
        pg.screenshot(path=str(out / name), type="jpeg", quality=92)
        pg.close()
        print("saved", out / name, round((out / name).stat().st_size / 1e6, 2), "MB")

    if browser is not None:
        shoot(browser, "cover.jpg", front_html(meta, c))
        shoot(browser, "backcover.jpg", back_html(meta, c))
        shoot(browser, "cover-art.jpg", art_html(c))
        return

    with sync_playwright() as p:
        args = ["--font-render-hinting=none", "--force-color-profile=srgb"]
        b = None
        for kw in ({"channel": "chrome"}, {"channel": "msedge"}, {}):
            try:
                b = p.chromium.launch(headless=True, args=args, **kw)
                break
            except Exception:
                continue
        if b is None:
            raise SystemExit("没有可用的 Chrome 或 Edge")
        shoot(b, "cover.jpg", front_html(meta, c))
        shoot(b, "backcover.jpg", back_html(meta, c))
        shoot(b, "cover-art.jpg", art_html(c))
        b.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    a = ap.parse_args()
    build(ROOT / a.book)


if __name__ == "__main__":
    main()
