#!/usr/bin/env python3
"""Deliver the committed entry.png to MAKEFUN_OUTPUT_DIR."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(os.path.join(HERE, "entry.png"), dest)
    print(f"entry.png delivered: {dest} {os.path.getsize(dest)} bytes")

if __name__ == "__main__":
    main()
