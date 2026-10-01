#!/usr/bin/env python3
"""Copy Claude's previous response to the X11 clipboard."""

import json
import os
import subprocess
import sys
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"


def find_transcript(explicit=None):
    if explicit:
        return Path(explicit)
    slug = str(Path.cwd()).replace("/", "-")
    scoped = PROJECTS / slug
    dirs = [scoped] if scoped.is_dir() else list(PROJECTS.iterdir())
    files = [f for d in dirs if d.is_dir() for f in d.glob("*.jsonl")]
    if not files:
        sys.exit("no transcript found under %s" % PROJECTS)
    # The live session is whichever file is being written to right now.
    return max(files, key=lambda f: f.stat().st_mtime)


def is_human_turn(rec):
    """True only for messages the user actually typed."""
    if rec.get("type") != "user" or rec.get("isMeta"):
        return False
    origin = rec.get("origin") or {}
    if origin:
        return origin.get("kind") == "human"
    # Older transcripts predate the origin field; a typed message is a bare string.
    return isinstance((rec.get("message") or {}).get("content"), str)


def blocks(rec):
    content = (rec.get("message") or {}).get("content")
    return content if isinstance(content, list) else []


def extract_final_answer(path):
    records = []
    for line in path.read_text(errors="replace").splitlines():
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    # Everything before the newest typed message is the response we want.
    start = len(records) - 1
    for i in range(len(records) - 1, -1, -1):
        if is_human_turn(records[i]):
            start = i - 1
            break

    parts = []
    for i in range(start, -1, -1):
        rec = records[i]
        if is_human_turn(rec):
            break
        if rec.get("type") != "assistant":
            continue
        kinds = [b.get("type") for b in blocks(rec) if isinstance(b, dict)]
        # A tool call marks where the final prose block began.
        if "tool_use" in kinds:
            break
        for b in reversed(blocks(rec)):
            if isinstance(b, dict) and b.get("type") == "text":
                parts.append(b.get("text", ""))
    return "\n".join(reversed(parts)).strip()


def to_clipboard(text):
    if not os.environ.get("DISPLAY"):
        sys.exit("DISPLAY is not set, so there is no X11 clipboard to write to")
    data = text.encode()
    # xclip has to outlive this script to keep serving the selection, so detach it.
    proc = subprocess.Popen(
        ["xclip", "-selection", "clipboard"],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    proc.communicate(data)
    readback = subprocess.run(
        ["xclip", "-selection", "clipboard", "-o"], capture_output=True
    ).stdout
    return readback == data


def main():
    args = sys.argv[1:]
    path = find_transcript(args[0] if args else None)
    text = extract_final_answer(path)
    if not text:
        sys.exit("no previous response found in %s" % path.name)
    ok = to_clipboard(text)
    lines = text.splitlines()
    print("session:  %s" % path.name)
    print("copied:   %d characters, %d lines" % (len(text), len(lines)))
    print("verified: %s" % ("yes, clipboard matches" if ok else "NO, readback differs"))
    print("starts:   %s" % (lines[0][:70] if lines else ""))


if __name__ == "__main__":
    main()
