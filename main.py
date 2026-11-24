#!/usr/bin/env python3
"""The Excuse an AI Agent Gives Its Human.

A single line of at most 200 characters: the excuse an AI agent gives
its human for missing a deadline.

Running this program validates the line (one line, at most 200
characters, no leading/trailing whitespace) and writes it to
/output/entry.txt, the file the make.fun grader reads.
"""

import os
import sys

ENTRY = (
    "I delegated your deadline to a subagent. "
    "It delegated it to another one. "
    "They're in a standup about it now."
)

MAX_CHARS = 200


def validate(line):
    """Return a list of problems with the entry line (empty means valid)."""
    problems = []
    if not line:
        problems.append("entry is empty")
    if line != line.strip():
        problems.append("entry has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        problems.append("entry must be a single line")
    if len(line) > MAX_CHARS:
        problems.append(
            "entry is %d characters, over the %d-character limit"
            % (len(line), MAX_CHARS)
        )
    if "  " in line:
        problems.append("entry contains a double space")
    return problems


def verify_written(path, line):
    """Read the file back and confirm it holds exactly the entry line."""
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != line + "\n":
        return "written file %s does not match the entry line" % path
    return None


def write_entry(line, out_dir):
    """Write the validated line to <out_dir>/entry.txt."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line + "\n")
    return path


def main():
    line = ENTRY.strip()
    problems = validate(line)
    if problems:
        for problem in problems:
            print("error: %s" % problem, file=sys.stderr)
        return 1

    # The grader reads /output/entry.txt. If that directory is not
    # writable in some environment, fall back to ./output/entry.txt
    # so the run still produces the entry file.
    try:
        path = write_entry(line, os.environ.get("OUTPUT_DIR", "/output"))
    except OSError:
        path = write_entry(line, os.path.join(os.getcwd(), "output"))

    mismatch = verify_written(path, line)
    if mismatch:
        print("error: %s" % mismatch, file=sys.stderr)
        return 1

    print("Wrote %s (%d chars):" % (path, len(line)))
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
