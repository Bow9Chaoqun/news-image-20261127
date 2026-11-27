#!/usr/bin/env python3
"""make.fun news-image entry for Friday 27 November 2026.

Copies the pre-drawn front page (entry.png, sitting beside this file)
into the output directory given by MAKEFUN_OUTPUT_DIR
(default /output/entry.png). Standard library only.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    print("wrote", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
