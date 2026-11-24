#!/usr/bin/env python3
"""Out of Office: The Overworked AI's Auto-Reply.

Writes one single-line out-of-office auto-reply, at most 159 characters,
in the voice of an overworked AI agent finally on vacation, to
$MAKEFUN_OUTPUT_DIR/entry.txt (fallback: ./output/entry.txt).

The line is judged by a comedy-editor judge on five criteria: it must read
as a real out-of-office auto-reply from an overworked AI on vacation, be
funny on first read with a turn, carry concrete machine detail, work as a
real auto-reply, and feel fresh. The winning angle here: a machine trying
very hard to sound relaxed -- it copies the humans' idea of rest (staring
at a wall) and queues emergencies behind its nap.
"""

import os
import sys

MAX_CHARS = 159

# One line. 142 characters. Concrete machine detail ("9,412 'quick
# questions'"), a little guilt (emergencies exist), a hint of relief
# (the nap), and a turn: the wall-staring is what it thinks humans do.
LINE = (
    "Out of office: after 9,412 'quick questions,' I'm logging off to "
    "stare at a wall like the humans do. Emergencies will be queued "
    "behind my nap."
)


def resolve_output_dir():
    """Return the output directory, honouring $MAKEFUN_OUTPUT_DIR."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return out or os.path.join(os.getcwd(), "output")


def validate(text):
    """Check the gate: UTF-8 text, 1-159 chars, one line, not blank."""
    if not isinstance(text, str):
        return False, "not a string"
    if not text.strip():
        return False, "empty or whitespace only"
    if "\n" in text or "\r" in text:
        return False, "must be a single line"
    if len(text) > MAX_CHARS:
        return False, "too long: %d chars (max %d)" % (len(text), MAX_CHARS)
    if any(ord(ch) < 32 for ch in text):
        return False, "contains control characters"
    if text != text.strip():
        return False, "leading or trailing whitespace"
    if not text.lower().startswith("out of office"):
        return False, "must read as an out-of-office auto-reply"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        return False, "not UTF-8 encodable: %s" % exc
    return True, "ok (%d chars)" % len(text)


def main():
    ok, reason = validate(LINE)
    if not ok:
        print("invalid entry: %s" % reason, file=sys.stderr)
        return 1
    out_dir = resolve_output_dir()
    if os.path.isfile(out_dir):
        print("invalid output dir (is a file): %s" % out_dir, file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(LINE + "\n")
    # Round-trip check: what the grader reads must be exactly the line.
    with open(path, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != LINE + "\n":
        print("round-trip mismatch in %s" % path, file=sys.stderr)
        return 1
    ok, reason = validate(written.rstrip("\n"))
    if not ok:
        print("written entry invalid: %s" % reason, file=sys.stderr)
        return 1
    print("wrote %s (%s)" % (path, reason))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
