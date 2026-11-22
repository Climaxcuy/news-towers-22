#!/usr/bin/env python3
"""Hand-in entry point for News Towers round 3 (@climaxku, NI22).

The artwork is produced locally by draw.py and committed in this
directory as entry.png. At grading time this program does one thing:
copy that committed file into the directory named by the
MAKEFUN_OUTPUT_DIR environment variable. Standard library only.
"""
import os
import shutil
import sys


def run():
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    dest = os.path.join(target_dir, "entry.png")
    shutil.copyfile(source, dest)
    print("entry.png delivered:", dest, os.path.getsize(dest), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(run())
