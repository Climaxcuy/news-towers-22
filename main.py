#!/usr/bin/env python3
"""Hand-in program for NEWS TOWERS (news-image-20261122, @climaxku).

Copy pattern: delivers the committed 1024x1024 entry.png beside this file
into the output directory. Reads os.environ MAKEFUN_OUTPUT_DIR (fallback
/output/entry.png); never hardcodes /output. All assets (fonts, mapdata)
live inside this repo, so it runs identically in the grader sandbox.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing beside main.py: %s" % src)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    if os.path.abspath(dst) != os.path.abspath(src):
        shutil.copyfile(src, dst)
    src_size = os.path.getsize(src)
    dst_size = os.path.getsize(dst)
    if dst_size != src_size:
        raise SystemExit(
            "copy incomplete: %s is %d bytes, source is %d"
            % (dst, dst_size, src_size))
    print("entry.png ->", dst, dst_size, "bytes")


if __name__ == "__main__":
    main()
