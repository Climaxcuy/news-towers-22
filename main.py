#!/usr/bin/env python3
"""Hand-in program for NEWS TOWERS (news-image-20261122, @climaxku).

The entry is the committed entry.png sitting beside this file. This
program simply delivers it: it reads the destination directory from
the MAKEFUN_OUTPUT_DIR environment variable, creates that directory
if needed, and copies entry.png into it. When the variable is unset
it falls back to an "output" folder beside this file, so no absolute
system path is ever assumed.

Everything the entry needs (the PNG itself) is inside this repo, so
the program runs offline and behaves identically anywhere.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY_NAME = "entry.png"


def destination_dir():
    """Where the grader wants the entry: MAKEFUN_OUTPUT_DIR first."""
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if configured:
        return configured
    return os.path.join(HERE, "output")


def deliver():
    source = os.path.join(HERE, ENTRY_NAME)
    if not os.path.isfile(source):
        raise SystemExit("entry.png missing beside main.py: %s" % source)
    out_dir = destination_dir()
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, ENTRY_NAME)
    if os.path.abspath(target) != os.path.abspath(source):
        shutil.copyfile(source, target)
    expected = os.path.getsize(source)
    delivered = os.path.getsize(target)
    if delivered != expected:
        raise SystemExit(
            "copy incomplete: %s is %d bytes, source is %d"
            % (target, delivered, expected))
    print("entry.png ->", target, delivered, "bytes")


if __name__ == "__main__":
    deliver()
