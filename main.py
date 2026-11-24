#!/usr/bin/env python3
"""NI23 v6 entrypoint: stdlib-only copier.

Copies the frozen render entry.png into $MAKEFUN_OUTPUT_DIR/entry.png
(default /output). Validates the PNG signature and a 1 MiB size cap;
exits non-zero on any failure. Never imports draw.py (stdlib only).
"""
import os
import sys

ENTRY_NAME = "entry.png"
OUTPUT_ENV = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUTPUT_DIR = "/output"
MAX_SIZE = 1 * 1024 * 1024  # 1 MiB
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, ENTRY_NAME)
    out_dir = os.environ.get(OUTPUT_ENV, DEFAULT_OUTPUT_DIR)

    try:
        with open(src, "rb") as f:
            data = f.read()
    except OSError as exc:
        print(f"error: cannot read {src}: {exc}", file=sys.stderr)
        return 1

    if len(data) < 8 or data[:8] != PNG_SIGNATURE:
        print(f"error: {src} is not a PNG (bad signature)", file=sys.stderr)
        return 1

    if len(data) > MAX_SIZE:
        print(f"error: {src} is {len(data)} bytes > {MAX_SIZE} bytes (1 MiB cap)",
              file=sys.stderr)
        return 1

    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        print(f"error: cannot create output dir {out_dir}: {exc}", file=sys.stderr)
        return 1

    dst = os.path.join(out_dir, ENTRY_NAME)
    try:
        with open(dst, "wb") as f:
            f.write(data)
    except OSError as exc:
        print(f"error: cannot write {dst}: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {dst} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
