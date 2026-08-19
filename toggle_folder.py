#!/usr/bin/env python3
"""
toggle_folder.py — temporarily hide or fully disable a folder of pages
by adding/removing Just-the-Docs front matter flags, recursively.

Usage:
    python3 toggle_folder.py <folder> --hide      # nav_exclude: true  (page still builds, just off the sidebar)
    python3 toggle_folder.py <folder> --unhide     # remove nav_exclude
    python3 toggle_folder.py <folder> --disable    # published: false  (page excluded from the build entirely)
    python3 toggle_folder.py <folder> --enable     # remove published: false
    python3 toggle_folder.py <folder> --status     # show current state of every page under folder

Examples:
    python3 toggle_folder.py docs/cplusplus26 --disable
    python3 toggle_folder.py docs/cplusplus26 --enable
"""
import os
import re
import sys

FRONT_MATTER_RE = re.compile(r"^(---\n)(.*?)(\n---\n)", re.DOTALL)

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def md_files(folder):
    for root, _, files in os.walk(folder):
        for fn in files:
            if fn.endswith(".md"):
                yield os.path.join(root, fn)

def set_field(text, key, value):
    """Add or update `key: value` inside the front matter block. value=None removes the key."""
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return text, False
    open_tag, block, close_tag = m.group(1), m.group(2), m.group(3)
    lines = block.split("\n")
    key_re = re.compile(rf'^{re.escape(key)}:\s*.*$')

    found = False
    new_lines = []
    for line in lines:
        if key_re.match(line):
            found = True
            if value is not None:
                new_lines.append(f"{key}: {value}")
            # if value is None, drop the line (removes the key)
        else:
            new_lines.append(line)

    changed = False
    if value is not None and not found:
        new_lines.append(f"{key}: {value}")
        changed = True
    elif value is not None and found:
        changed = True
    elif value is None and found:
        changed = True

    new_block = "\n".join(new_lines)
    new_text = text[:m.start()] + open_tag + new_block + close_tag + text[m.end():]
    return new_text, changed

def apply(folder, key, value, label):
    count = 0
    for path in md_files(folder):
        text = load(path)
        new_text, changed = set_field(text, key, value)
        if changed:
            save(path, new_text)
            count += 1
            print(f"{label}: {path}")
    print(f"\nDone. {count} file(s) updated under {folder}.")

def status(folder):
    for path in sorted(md_files(folder)):
        text = load(path)
        m = FRONT_MATTER_RE.match(text)
        block = m.group(2) if m else ""
        nav_excluded = bool(re.search(r'^nav_exclude:\s*true', block, re.MULTILINE))
        unpublished = bool(re.search(r'^published:\s*false', block, re.MULTILINE))
        flags = []
        if nav_excluded:
            flags.append("HIDDEN (nav_exclude)")
        if unpublished:
            flags.append("DISABLED (unpublished)")
        state = ", ".join(flags) if flags else "active"
        print(f"{state:32s} {path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    folder, flag = sys.argv[1], sys.argv[2]
    if not os.path.isdir(folder):
        print(f"Not a directory: {folder}")
        sys.exit(1)

    if flag == "--hide":
        apply(folder, "nav_exclude", "true", "hidden from nav")
    elif flag == "--unhide":
        apply(folder, "nav_exclude", None, "restored to nav")
    elif flag == "--disable":
        apply(folder, "published", "false", "disabled (excluded from build)")
    elif flag == "--enable":
        apply(folder, "published", None, "enabled (included in build)")
    elif flag == "--status":
        status(folder)
    else:
        print(__doc__)
        sys.exit(1)
