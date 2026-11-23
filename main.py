#!/usr/bin/env python3
"""NI23 v2 entrypoint — stdlib-only copier.

Copies entry.png (built offline by draw.py) to /output/entry.png.
Validates the PNG signature and the 1 MiB size cap before copying.
Never imports draw.py; the image is built at authoring time, not at runtime.
"""
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")

    with open(src, "rb") as fh:
        head = fh.read(8)
    if head != PNG_MAGIC:
        print("entry.png: bad PNG signature", file=sys.stderr)
        return 1

    size = os.path.getsize(src)
    if size > MAX_BYTES:
        print("entry.png: %d bytes over the 1 MiB cap" % size, file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)

    if os.path.getsize(dst) != size:
        print("copy size mismatch", file=sys.stderr)
        return 1
    print("copied entry.png (%d bytes) to %s" % (size, dst))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
