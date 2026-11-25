#!/usr/bin/env python3
"""The Excuse My Agent Gave Me — account B entry.

Writes one line — the funniest excuse an AI agent could hand its human
after missing a deadline — to /output/entry.txt.

The excuse: a straight-faced apology built on a machine's own condition
(a hallucinated calendar), with the punch landing in the last few words.
The agent is genuinely sorry, and faintly proud of its calendar.
"""

import os
import sys

ENTRY = (
    "Sorry \u2014 I put your deadline on February 30th, which my calendar "
    "insists is a real day, so I am still waiting for it to arrive."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate(line: str) -> str:
    """Enforce the sealed scorer's gate before anything is written."""
    line = line.strip()
    if not line:
        raise ValueError("entry must not be empty or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"entry is {len(line)} chars, over the {MAX_CHARS} cap")
    return line


def main() -> int:
    try:
        line = validate(ENTRY)
    except ValueError as exc:
        print(f"gate failed: {exc}", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # Verify what actually landed on disk: re-read and re-check.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    if written != line:
        print("gate failed: written file differs from validated entry",
              file=sys.stderr)
        return 1
    if len(written) > MAX_CHARS or "\n" in written:
        print("gate failed: written file breaks the 1-200 char single-line gate",
              file=sys.stderr)
        return 1
    print(f"Wrote {len(written)} chars to {OUTPUT_PATH}")
    print(written)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
