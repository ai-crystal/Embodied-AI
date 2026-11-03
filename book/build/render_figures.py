# -*- coding: utf-8 -*-
"""按章生成全部插图：先封面，再 book/code/chNN/figures.py。"""
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOOK = os.path.join(ROOT, "book")


def main():
    scripts = [os.path.join(BOOK, "build", "make_covers.py")]
    scripts += sorted(glob.glob(os.path.join(BOOK, "code", "ch*", "figures.py")))
    for script in scripts:
        print("->", os.path.relpath(script, ROOT), flush=True)
        subprocess.run([sys.executable, script], check=True)
    print("插图完成")


if __name__ == "__main__":
    main()
