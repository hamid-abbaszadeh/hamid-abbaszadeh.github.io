#!/usr/bin/env python3
"""
rename_title.py — rename a Just-the-Docs page title in ONE place and
automatically fix every child/grandchild page that points at it.

Usage:
    python3 rename_title.py <docs_dir> "Old Title" "New Title"
    python3 rename_title.py <docs_dir> --list          # list all titles found
    python3 rename_title.py <docs_dir> --check          # find broken parent/grand_parent links

Notes:
- Matches are exact and case-sensitive (Just the Docs requires this too).
- Updates: the file whose own `title:` equals Old Title, plus every file
  whose `parent:` or `grand_parent:` equals Old Title.
- Re-quotes titles that contain a colon, per your formatting rule.
- Leaves everything else in each file untouched.
"""
import os
import re
import sys

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
FIELD_RE = re.compile(r'^(title|parent|grand_parent):\s*(.*)$')

def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1].replace('\\"', '"')
    return value

def yaml_value(title):
    if ":" in title or title.startswith(("*", "&", "-", "?", "[", "]", "{", "}",
                                          "#", "|", ">", "'", '"', "%", "@", "`")):
        escaped = title.replace('"', '\\"')
        return f'"{escaped}"'
    return title

def parse_front_matter(text):
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return None, None, None
    block = m.group(1)
    fields = {}
    for line in block.split("\n"):
        fm = FIELD_RE.match(line)
        if fm:
            key, raw_val = fm.group(1), fm.group(2)
            fields[key] = unquote(raw_val)
    return fields, m.start(1), m.end(1)

def scan(docs_dir):
    """Return list of (path, fields_dict, raw_text)."""
    results = []
    for root, _, files in os.walk(docs_dir):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            fields, _, _ = parse_front_matter(text)
            if fields is not None:
                results.append((path, fields, text))
    return results

def list_titles(docs_dir):
    for path, fields, _ in sorted(scan(docs_dir)):
        title = fields.get("title", "<no title>")
        parent = fields.get("parent")
        gp = fields.get("grand_parent")
        chain = title
        if parent:
            chain = f"{parent} > {chain}"
        if gp:
            chain = f"{gp} > {chain}"
        print(chain)

def check_broken_links(docs_dir):
    entries = scan(docs_dir)
    all_titles = {fields.get("title") for _, fields, _ in entries if fields.get("title")}
    broken = False
    for path, fields, _ in entries:
        for key in ("parent", "grand_parent"):
            val = fields.get(key)
            if val and val not in all_titles:
                print(f"BROKEN {key}: '{val}' referenced in {path} but no page has that title")
                broken = True
    if not broken:
        print("No broken parent/grand_parent references found.")

def rename(docs_dir, old_title, new_title):
    entries = scan(docs_dir)

    self_hits = [p for p, f, _ in entries if f.get("title") == old_title]
    parent_hits = [p for p, f, _ in entries if f.get("parent") == old_title]
    gp_hits = [p for p, f, _ in entries if f.get("grand_parent") == old_title]

    if not self_hits:
        print(f"WARNING: no page currently has title '{old_title}'. Nothing to rename "
              f"at the source, but will still check for dangling references.")
    if len(self_hits) > 1:
        print(f"WARNING: multiple pages have title '{old_title}': {self_hits}")

    changed = 0
    for path, fields, text in entries:
        new_text = text
        touched = False

        if fields.get("title") == old_title:
            new_text = re.sub(
                r'^title:\s*.*$',
                f"title: {yaml_value(new_title)}",
                new_text, count=1, flags=re.MULTILINE,
            )
            # also update the on-page H1 heading if it matches the old title exactly
            new_text = re.sub(
                rf'^# {re.escape(old_title)}$',
                f"# {new_title}",
                new_text, count=1, flags=re.MULTILINE,
            )
            touched = True

        if fields.get("parent") == old_title:
            new_text = re.sub(
                r'^parent:\s*.*$',
                f"parent: {yaml_value(new_title)}",
                new_text, count=1, flags=re.MULTILINE,
            )
            touched = True

        if fields.get("grand_parent") == old_title:
            new_text = re.sub(
                r'^grand_parent:\s*.*$',
                f"grand_parent: {yaml_value(new_title)}",
                new_text, count=1, flags=re.MULTILINE,
            )
            touched = True

        if touched:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_text)
            changed += 1
            print(f"updated: {path}")

    print(f"\nDone. {changed} file(s) updated "
          f"(1 self + {len(parent_hits)} children + {len(gp_hits)} grandchildren expected).")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    docs_dir = sys.argv[1]
    if sys.argv[2] == "--list":
        list_titles(docs_dir)
    elif sys.argv[2] == "--check":
        check_broken_links(docs_dir)
    elif len(sys.argv) == 4:
        rename(docs_dir, sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
        sys.exit(1)
