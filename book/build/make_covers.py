# -*- coding: utf-8 -*-
"""生成正封与封底（A4，约 288 DPI）。

素材：_private/art/logo_front.png（森林晨光）、logo_back.png（银河湖面）。
用法: python make_covers.py
输出: book/images/cover/cover_front.jpg, cover_back.jpg
"""
import base64
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent       # book/build
ROOT = HERE.parent.parent                    # 仓库根
OUT = ROOT / "book" / "images" / "cover"
ART = ROOT / "_private" / "art"


def art(name):
    p = ART / name
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return "data:%s;base64,%s" % (mime, base64.b64encode(p.read_bytes()).decode())


W, H = 794, 1123
INK = "#F3F7FC"
ICE = "#8FD3E8"
GOLD = "#E9B26B"

BASE_CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:{W}px;height:{H}px;background:#07110F;}}
.page{{
  width:{W}px;height:{H}px;position:relative;overflow:hidden;color:{INK};
  font-family:"SimSun","Source Han Serif SC",serif;background:#07110F;
}}
.bg{{position:absolute;inset:0;background-repeat:no-repeat;background-size:cover;}}
.scrim{{position:absolute;inset:0;}}
.frame{{position:absolute;inset:30px;border:1px solid rgba(206,232,238,.20);}}
.frame:before{{content:"";position:absolute;left:-1px;top:-1px;width:26px;height:26px;
  border-left:2px solid {GOLD};border-top:2px solid {GOLD};opacity:.85;}}
.frame:after{{content:"";position:absolute;right:-1px;bottom:-1px;width:26px;height:26px;
  border-right:2px solid {ICE};border-bottom:2px solid {ICE};opacity:.7;}}
.inner{{position:absolute;left:76px;right:76px;top:92px;}}
.kicker{{font-family:"Microsoft YaHei",sans-serif;font-size:10.4px;letter-spacing:5.8px;
  color:{ICE};font-weight:400;}}
.rule{{width:34px;height:1.5px;background:{GOLD};margin-top:18px;}}
h1{{font-size:74px;line-height:1.24;font-weight:600;letter-spacing:6px;color:#FCFEFF;
  margin-top:104px;text-shadow:0 3px 30px rgba(3,10,9,.90),0 0 46px rgba(4,14,12,.65);}}
.sub{{font-size:27px;line-height:1.5;letter-spacing:6px;color:#EFF8F6;margin-top:24px;
  text-shadow:0 2px 18px rgba(3,10,9,.85);}}
.sub2{{font-family:"Microsoft YaHei",sans-serif;font-size:14px;letter-spacing:4.6px;
  color:rgba(226,240,238,.86);margin-top:14px;text-shadow:0 1px 12px rgba(3,10,9,.8);}}
.barwrap{{margin-top:56px;}}
.bar{{height:3px;width:100%;
  background:linear-gradient(90deg,{ICE} 0%,#B9C9F0 48%,{GOLD} 100%);opacity:.92;}}
.ticks{{display:flex;justify-content:space-between;margin-top:10px;
  font-family:"Microsoft YaHei",sans-serif;font-size:9px;letter-spacing:1.2px;
  color:rgba(232,244,240,.86);text-shadow:0 1px 10px rgba(3,10,9,.9);}}
.tag{{font-size:17px;line-height:1.95;letter-spacing:2.4px;color:#F3FBF8;margin-top:48px;
  text-shadow:0 2px 16px rgba(3,10,9,.9);padding-left:16px;border-left:2px solid {GOLD};}}
.tag i{{font-style:normal;color:{GOLD};}}
.bottom{{position:absolute;left:76px;right:76px;bottom:82px;}}
.author{{font-size:16px;letter-spacing:4px;color:#FBFDFF;}}
.edition{{font-family:"Microsoft YaHei",sans-serif;font-size:10.2px;letter-spacing:2.2px;
  color:rgba(214,236,232,.58);margin-top:9px;}}
h2{{font-size:40px;line-height:1.42;letter-spacing:3px;font-weight:600;color:#FBFDFF;
  margin-top:20px;text-shadow:0 2px 22px rgba(4,12,20,.6);}}
.panel{{margin-top:24px;padding:26px 26px 24px;border:1px solid rgba(206,232,238,.16);
  background:linear-gradient(180deg, rgba(9,22,26,.62), rgba(5,13,18,.74));}}
.lead{{font-size:12.8px;line-height:2.0;letter-spacing:.5px;color:rgba(232,246,246,.90);}}
.lead em{{font-style:normal;color:{GOLD};}}
.toc{{margin-top:20px;list-style:none;}}
.toc li{{display:flex;gap:11px;align-items:baseline;padding:8px 0;
  border-top:1px solid rgba(206,232,238,.10);}}
.toc li b{{font-family:"Microsoft YaHei",sans-serif;font-size:11px;letter-spacing:2.2px;
  color:{ICE};font-weight:500;white-space:nowrap;}}
.toc li span{{font-family:"Microsoft YaHei",sans-serif;font-size:10px;line-height:1.72;
  letter-spacing:.6px;color:rgba(226,240,244,.74);}}
.quote{{margin-top:26px;font-size:16px;line-height:1.95;letter-spacing:2px;
  color:#F4FAFB;border-left:2px solid {GOLD};padding-left:16px;}}
.quote small{{display:block;margin-top:8px;font-family:"Microsoft YaHei",sans-serif;
  font-size:9.6px;letter-spacing:1.8px;color:rgba(214,236,240,.55);}}
.who{{font-size:15px;letter-spacing:3.4px;color:#FBFDFF;line-height:1.8;}}
.who span{{font-family:"Microsoft YaHei",sans-serif;font-size:10.2px;letter-spacing:2.1px;
  color:rgba(214,236,240,.55);}}
"""

ART_URL = art("logo_front.png")

ART_HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
.bg{{background-image:url("{ART_URL}");background-position:26% 52%;}}
.scrim{{background:
  linear-gradient(100deg, rgba(4,12,11,.86) 0%, rgba(4,12,11,.62) 40%, rgba(4,12,11,.34) 70%, rgba(4,12,11,.24) 100%),
  linear-gradient(180deg, rgba(4,12,11,.70) 0%, rgba(4,12,11,.16) 32%, rgba(4,12,11,.34) 64%, rgba(3,9,9,.88) 100%);}}
</style></head><body><div class="page">
  <div class="bg"></div><div class="scrim"></div><div class="frame"></div>
</div></body></html>"""

FRONT = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
.bg{{background-image:url("{art('logo_front.png')}");background-position:26% 52%;}}
.scrim{{background:
  linear-gradient(100deg, rgba(4,12,11,.93) 0%, rgba(4,12,11,.78) 36%, rgba(4,12,11,.40) 68%, rgba(4,12,11,.18) 100%),
  linear-gradient(180deg, rgba(4,12,11,.70) 0%, rgba(4,12,11,.12) 30%, rgba(4,12,11,.30) 62%, rgba(3,9,9,.92) 100%);}}
</style></head><body><div class="page">
  <div class="bg"></div><div class="scrim"></div><div class="frame"></div>
  <div class="inner">
    <div class="kicker">EMBODIED INTELLIGENCE</div>
    <div class="rule"></div>
    <h1>具身智能技术</h1>
    <div class="sub">从大模型到机器人</div>
    <div class="sub2">感知 · 学习 · 行动</div>
    <div class="barwrap">
      <div class="bar"></div>
      <div class="ticks">
        <span>1966　Shakey</span><span>2013　深度学习</span><span>2022　SayCan / RT-1</span><span>2026　VLA 与通用机器人</span>
      </div>
    </div>
    <div class="tag">让会说话的大脑，<br>学会<i>用手做事</i>。</div>
  </div>
  <div class="bottom">
    <div class="author">Dr. Dezeming</div>
    <div class="edition">2026 年 · 第一版　·　21 章 + 4 附录　·　CC BY-NC-SA 4.0</div>
  </div>
</div></body></html>"""

BACK = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
.bg{{background-image:url("{art('logo_back.png')}");background-position:66% 60%;}}
.scrim{{background:
  radial-gradient(720px 520px at 78% 16%, rgba(6,16,30,.28), transparent 74%),
  linear-gradient(180deg, rgba(4,10,18,.84) 0%, rgba(4,10,18,.64) 32%, rgba(4,10,18,.80) 74%, rgba(3,7,12,.95) 100%);}}
</style></head><body><div class="page">
  <div class="bg"></div><div class="scrim"></div><div class="frame"></div>
  <div class="inner">
    <div class="kicker">ABOUT THE BOOK</div>
    <div class="rule"></div>
    <h2>大脑已经会思考，<br>身体还没学会做事。</h2>
    <div class="panel">
      <div class="lead">语言模型把<em>符号</em>玩得很熟，机器人却仍要在<em>毫米与毫秒</em>里讨生活。
      这本书从一台机械臂的自由度讲起，经过相机几何、位姿与抓取、强化学习与模仿学习、运动规划，
      一直讲到视觉-语言-动作模型、世界模型、腿足与灵巧手，最后落到系统集成与评测。</div>
      <ul class="toc">
        <li><b>第一篇　身体的意义</b><span>莫拉维克悖论 · 关节与位姿 · 六十年路线之争</span></li>
        <li><b>第二篇　看懂世界</b><span>相机几何 · 6D 位姿与抓取 · 视觉表征 · 场景图与地图</span></li>
        <li><b>第三篇　学会行动</b><span>强化学习 · 模仿学习与扩散策略 · 仿真与 sim2real · 运动规划</span></li>
        <li><b>第四篇　大模型进入身体</b><span>LLM 任务分解 · VLA · 机器人数据 · 世界模型</span></li>
        <li><b>第五篇　身体与控制</b><span>PID 与阻抗控制 · 腿足与人形 · 灵巧手与触觉</span></li>
        <li><b>第六篇　落地与远方</b><span>系统集成与时延 · 评测基准 · 仍未解决的问题</span></li>
      </ul>
    </div>
    <div class="quote">机器人不缺聪明的想法，缺的是把想法落到毫米和毫秒上的那一层。
      <small>第 19 章　系统集成</small></div>
  </div>
  <div class="bottom">
    <div class="who">Dr. Dezeming<br><span>2026 年 · 第一版　·　21 章 + 4 附录</span></div>
  </div>
</div></body></html>"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        args = ["--font-render-hinting=none", "--force-color-profile=srgb"]
        b = None
        for kw in ({"channel": "chrome"}, {"channel": "msedge"}, {}):
            try:
                b = p.chromium.launch(headless=True, args=args, **kw)
                print("browser:", kw.get("channel", "bundled"))
                break
            except Exception as e:
                print("launch fail", kw.get("channel", "bundled"), str(e)[:80])
        if b is None:
            raise SystemExit("没有可用的 Chromium/Chrome/Edge")
        for name, html in (("cover_front.jpg", FRONT), ("cover_back.jpg", BACK),
                           ("cover-art.jpg", ART_HTML)):
            pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=3)
            pg.set_content(html, wait_until="load")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(500)
            out = OUT / name
            pg.screenshot(path=str(out), type="jpeg", quality=92)
            print("saved", out, round(out.stat().st_size / 1e6, 2), "MB")
            pg.close()
        b.close()


if __name__ == "__main__":
    main()
