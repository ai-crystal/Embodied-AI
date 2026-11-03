# -*- coding: utf-8 -*-
"""成书自检：PDF 里每个标题都能被正确读出来，且没有 Type3 字体。

Chrome 打印 PDF 时若用了变量字体，会把字形拆成 Type3 描边，长文档里少数标题
会变成乱码或缺字，而正文正常、编译不报错。这个脚本把 book/ 下所有标题与
PDF 文本层逐条比对，同时统计字体类型。

用法: python book/build/checks/verify_pdf_text.py [pdf]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BOOK = ROOT / "book"
DEFAULT_PDF = ROOT / "output" / "embodied-ai.pdf"

KEEP = re.compile(r"[^\u4e00-\u9fffA-Za-z0-9]+")


def norm(s: str) -> str:
    return KEEP.sub("", s)


def content_files():
    files = []
    for folder in ("front", "chapters", "appendix"):
        files.extend(sorted((BOOK / folder).glob("*.md")))
    return files


def headings():
    out = []
    for path in content_files():
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^(#{1,4})\s+(.*\S)\s*$", line)
            if m:
                text = re.sub(r"\s*\{:[^}]*\}\s*$", "", m.group(2)).strip()
                out.append((len(m.group(1)), text, path.name))
    return out


def main():
    import pymupdf

    pdf = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PDF
    if not pdf.exists():
        raise SystemExit(f"找不到 {pdf}")
    doc = pymupdf.open(pdf)
    pages = [norm(p.get_text()) for p in doc]
    blob = "".join(pages)

    type3 = 0
    for page in doc:
        for f in page.get_fonts():
            if f[2] == "Type3":
                type3 += 1

    missing = []
    for level, text, src in headings():
        if level > 3:
            continue
        key = norm(text)
        if key and key not in blob:
            missing.append((src, level, text))

    print(f"PDF: {pdf.name}  页数 {doc.page_count}  "
          f"体积 {pdf.stat().st_size / 1024 / 1024:.2f} MiB")
    print(f"Type3 字体引用数: {type3}")
    if missing:
        print(f"[FAIL] {len(missing)} 个标题无法在文本层读出：")
        for src, level, text in missing[:40]:
            print(f"  {src}  h{level}  {text}")
    else:
        print("[PASS] 全部标题均可从文本层读出")
    doc.close()
    return 1 if (missing or type3) else 0


if __name__ == "__main__":
    sys.exit(main())
