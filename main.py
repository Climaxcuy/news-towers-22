#!/usr/bin/env python3
"""Hand-in entry point for News Towers (NI22 challenger, @climaxku).

The artwork is built locally by draw.py and committed as entry.png.
This program only copies that committed file into the output directory
named by the MAKEFUN_OUTPUT_DIR environment variable. Stdlib only.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"copied {src} -> {dst} ({os.path.getsize(dst)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
