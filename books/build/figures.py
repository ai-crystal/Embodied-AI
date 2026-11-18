# -*- coding: utf-8 -*-
"""画某一册的全部插图：先生成封面，再跑 books/code/<册>/chNN/figures.py。

用法：
    python books/build/figures.py --book books/intro
    python books/build/figures.py --book books/system --only ch13
"""
import argparse
import glob
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, help="册目录，如 books/intro")
    ap.add_argument("--only", default="", help="只画某一章，如 ch13")
    ap.add_argument("--no-cover", action="store_true")
    a = ap.parse_args()

    vol = Path(a.book).name
    env = dict(os.environ, BOOK_VOL=vol, PYTHONIOENCODING="utf-8")

    if not a.no_cover and not a.only:
        print("-> 封面", flush=True)
        subprocess.run([sys.executable, str(ROOT / "books" / "common" / "covers.py"),
                        "--book", a.book], check=True, env=env)

    pat = f"ch{a.only[2:]}" if a.only.startswith("ch") else a.only
    if a.only:
        scripts = sorted(glob.glob(str(ROOT / "books" / "code" / vol / pat / "figures.py")))
    else:
        scripts = sorted(glob.glob(str(ROOT / "books" / "code" / vol / "ch*" / "figures.py")))
    if not scripts:
        print("没有找到插图脚本：", ROOT / "books" / "code" / vol)
    for script in scripts:
        print("->", os.path.relpath(script, ROOT), flush=True)
        subprocess.run([sys.executable, script], check=True, env=env, cwd=str(ROOT))
    print("插图完成：", len(scripts), "个脚本")


if __name__ == "__main__":
    main()
