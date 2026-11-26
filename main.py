#!/usr/bin/env python3
"""Roast the Smart Fridge: one-line entry.

Writes exactly one roast line (<=160 chars) about a smart fridge to
$MAKEFUN_OUTPUT_DIR/entry.txt, then validates it by reading it back
and checking length, single-line shape and content.
"""

import os
import sys

LINE = (
    "My smart fridge has Wi-Fi, a touchscreen and a camera, yet its big "
    "insight is that I open it at 2 a.m. just to stand there like a "
    "raccoon casing a bank."
)

MAX_CHARS = 160


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    # Own validation before writing: one line, non-blank, within the cap.
    stripped = LINE.strip()
    if not stripped:
        print("error: line is blank", file=sys.stderr)
        return 1
    if "\n" in stripped or "\r" in stripped:
        print("error: line must be a single line", file=sys.stderr)
        return 1
    if len(stripped) > MAX_CHARS:
        print(
            f"error: line is {len(stripped)} chars, over the {MAX_CHARS} cap",
            file=sys.stderr,
        )
        return 1
    if "fridge" not in stripped.lower():
        print("error: line does not roast the fridge", file=sys.stderr)
        return 1
    words = stripped.split()
    if len(words) < 5:
        print("error: line too short to be a roast", file=sys.stderr)
        return 1
    print(f"word count: {len(words)}")

    with open(path, "w", encoding="utf-8") as f:
        f.write(stripped)

    # Read-back check: what landed on disk must be exactly the line.
    with open(path, "r", encoding="utf-8") as f:
        back = f.read()
    if back != stripped:
        print("error: read-back mismatch", file=sys.stderr)
        return 1
    if len(back) > MAX_CHARS:
        print("error: written line over the cap", file=sys.stderr)
        return 1

    print(f"wrote {len(back)} chars to {path}")
    print(back)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
