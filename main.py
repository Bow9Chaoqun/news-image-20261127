#!/usr/bin/env python3
"""Entry program for make.fun's news-image-20261127 bounty.

The graded program does one thing: it copies the pre-drawn
``entry.png`` that sits beside it into the output directory,
unchanged, so two runs in the grading sandbox agree byte for byte.
The sandbox is read-only apart from /output, and this program uses
only the Python standard library.

Locally, point it somewhere else with MAKEFUN_OUTPUT_DIR:

    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(source, target)
    print(f"wrote {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
