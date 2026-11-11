#!/usr/bin/env python3
"""design-setup: add an optional, templated subdirectory to a project's design/.

Usage:
  design-setup.py list                      # the templates this skill ships
  design-setup.py add <template> [--dry-run] [--project <dir>]

`add` copies the template's files into <project>/design/<template>/ and names the
directory in <project>/design/README.md (the directory tree and the trust order).
It never overwrites: an existing file is left alone and reported, a README that
already names the directory is left alone, and a README whose shape it does not
recognise is not guessed at (the lines are printed for a hand edit instead).

Templates are found next to this script (resolved through symlinks), one directory
each under templates/:

  templates/<name>/about.txt              one line, shown by `list`
  templates/<name>/files/...              copied as is into design/<name>/
  templates/<name>/readme-tree-line.txt   the entry for the README's directory tree
  templates/<name>/readme-trust-line.txt  the entry for the README's trust order

Python 3.9 compatible (macOS system python3).
"""

import argparse
import filecmp
import os
import re
import shutil
import subprocess
import sys

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")
TEMPLATE_FILES_SUBDIR = "files"
TEMPLATE_ABOUT = "about.txt"
TEMPLATE_TREE_LINE = "readme-tree-line.txt"
TEMPLATE_TRUST_LINE = "readme-trust-line.txt"

DESIGN_DIR = "design"
DESIGN_README = "README.md"

TREE_BRANCH = "├── "
TREE_LAST_BRANCH = "└── "
TREE_ENTRY = re.compile(r"^(├── |└── )(\S+)")
TRUST_ITEM = re.compile(r"^(\d+)\. (.*)$")
TRUST_ITEM_DIR = re.compile(r"^\d+\. \*\*`([^`]+)`\*\*")
# The entry a new directory goes in front of in the tree, and the trust items it
# goes after (first one found wins) or, failing that, in front of.
TREE_INSERT_BEFORE = "notes/"
TRUST_INSERT_AFTER = ("plans/", "stories/drafts/", "stories/")
TRUST_INSERT_BEFORE = "notes/"


def project_root(explicit):
    if explicit:
        return os.path.abspath(explicit)
    try:
        top = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if top:
            return top
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return os.getcwd()


def template_names():
    if not os.path.isdir(TEMPLATES_DIR):
        return []
    return sorted(
        name
        for name in os.listdir(TEMPLATES_DIR)
        if os.path.isdir(os.path.join(TEMPLATES_DIR, name, TEMPLATE_FILES_SUBDIR))
    )


def read_one_line(path):
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as handle:
        return handle.read().strip() or None


def cmd_list():
    names = template_names()
    if not names:
        print("No templates found under " + TEMPLATES_DIR)
        return 1
    print("Templates (design-setup <name> creates design/<name>/):")
    for name in names:
        about = read_one_line(os.path.join(TEMPLATES_DIR, name, TEMPLATE_ABOUT)) or ""
        print("  %-12s %s" % (name, about))
        files_root = os.path.join(TEMPLATES_DIR, name, TEMPLATE_FILES_SUBDIR)
        for rel in template_files(files_root):
            print("  %-12s   · %s" % ("", rel))
    return 0


def template_files(files_root):
    found = []
    for dirpath, _dirnames, filenames in os.walk(files_root):
        for filename in filenames:
            found.append(os.path.relpath(os.path.join(dirpath, filename), files_root))
    return sorted(found)


def copy_files(name, root, dry_run, report):
    files_root = os.path.join(TEMPLATES_DIR, name, TEMPLATE_FILES_SUBDIR)
    target_root = os.path.join(root, DESIGN_DIR, name)
    for rel in template_files(files_root):
        source = os.path.join(files_root, rel)
        target = os.path.join(target_root, rel)
        shown = os.path.join(DESIGN_DIR, name, rel)
        if os.path.lexists(target):
            same = os.path.isfile(target) and filecmp.cmp(source, target, shallow=False)
            report.append(
                "already there  %s (%s, left alone)"
                % (
                    shown,
                    "same as the template" if same else "differs from the template",
                )
            )
            continue
        if not dry_run:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copyfile(source, target)
        report.append("created        %s" % shown)


def fence_ranges(lines):
    """(start, end) line-index pairs of the bodies of ``` fenced blocks."""
    ranges, start = [], None
    for index, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            if start is None:
                start = index + 1
            else:
                ranges.append((start, index))
                start = None
    return ranges


def add_tree_line(lines, name, tree_line):
    """Insert the directory's entry into the README's tree. Returns a status word."""
    wanted = name + "/"
    for start, end in fence_ranges(lines):
        entries = [(i, TREE_ENTRY.match(lines[i])) for i in range(start, end)]
        entries = [(i, m) for i, m in entries if m]
        if not entries:
            continue
        if any(m.group(2) == wanted for _i, m in entries):
            return "present"
        before = [i for i, m in entries if m.group(2) == TREE_INSERT_BEFORE]
        if before:
            lines.insert(before[0], TREE_BRANCH + tree_line)
        else:
            last_index = entries[-1][0]
            if lines[last_index].startswith(TREE_LAST_BRANCH):
                lines[last_index] = (
                    TREE_BRANCH + lines[last_index][len(TREE_LAST_BRANCH) :]
                )
            # Skip any nested lines that belong to the last entry.
            insert_at = last_index + 1
            while insert_at < end and lines[insert_at].startswith((" ", "│")):
                insert_at += 1
            lines.insert(insert_at, TREE_LAST_BRANCH + tree_line)
        return "added"
    return "no-anchor"


def add_trust_line(lines, name, trust_line):
    """Insert the directory's item into the README's numbered trust order and
    renumber what follows. Returns a status word."""
    wanted = name + "/"
    items = []  # (line index, directory named in bold-code, or None)
    for index, line in enumerate(lines):
        if TRUST_ITEM.match(line):
            named = TRUST_ITEM_DIR.match(line)
            items.append((index, named.group(1) if named else None))
    if any(directory == wanted for _i, directory in items):
        return "present"
    insert_at = None
    for anchor in TRUST_INSERT_AFTER:
        hits = [i for i, directory in items if directory == anchor]
        if hits:
            insert_at = hits[-1] + 1
            break
    if insert_at is None:
        hits = [i for i, directory in items if directory == TRUST_INSERT_BEFORE]
        if hits:
            insert_at = hits[0]
    if insert_at is None:
        return "no-anchor"
    lines.insert(insert_at, "0. " + trust_line)
    # Renumber the contiguous list the new item landed in.
    first = insert_at
    while first > 0 and TRUST_ITEM.match(lines[first - 1]):
        first -= 1
    number = int(TRUST_ITEM.match(lines[first]).group(1))
    index = first
    while index < len(lines) and TRUST_ITEM.match(lines[index]):
        lines[index] = "%d. %s" % (number, TRUST_ITEM.match(lines[index]).group(2))
        number += 1
        index += 1
    return "added"


def update_readme(name, root, dry_run, report):
    tree_line = read_one_line(os.path.join(TEMPLATES_DIR, name, TEMPLATE_TREE_LINE))
    trust_line = read_one_line(os.path.join(TEMPLATES_DIR, name, TEMPLATE_TRUST_LINE))
    if not tree_line and not trust_line:
        return
    shown = os.path.join(DESIGN_DIR, DESIGN_README)
    readme_path = os.path.join(root, DESIGN_DIR, DESIGN_README)
    by_hand = []
    if not os.path.isfile(readme_path):
        report.append(
            "not there      %s (not created: this skill does not write the layout)"
            % shown
        )
        by_hand = [
            ("directory tree", TREE_BRANCH + tree_line if tree_line else None),
            ("trust order", "N. " + trust_line if trust_line else None),
        ]
    else:
        with open(readme_path, encoding="utf-8") as handle:
            original = handle.read()
        lines = original.split("\n")
        if tree_line:
            status = add_tree_line(lines, name, tree_line)
            if status == "added":
                report.append(
                    "added          %s: the %s/ line in the directory tree"
                    % (shown, name)
                )
            elif status == "present":
                report.append(
                    "already there  %s: %s/ in the directory tree" % (shown, name)
                )
            else:
                report.append(
                    "no tree found  %s: no directory tree to add %s/ to" % (shown, name)
                )
                by_hand.append(("directory tree", TREE_BRANCH + tree_line))
        if trust_line:
            status = add_trust_line(lines, name, trust_line)
            if status == "added":
                report.append(
                    "added          %s: the %s/ item in the trust order (later items renumbered)"
                    % (shown, name)
                )
            elif status == "present":
                report.append(
                    "already there  %s: %s/ in the trust order" % (shown, name)
                )
            else:
                report.append(
                    "no list found  %s: no trust order to add %s/ to" % (shown, name)
                )
                by_hand.append(("trust order", "N. " + trust_line))
        updated = "\n".join(lines)
        if updated != original and not dry_run:
            with open(readme_path, "w", encoding="utf-8") as handle:
                handle.write(updated)
    by_hand = [(where, line) for where, line in by_hand if line]
    if by_hand:
        report.append("")
        report.append("Add by hand to %s so the directory is named there:" % shown)
        for where, line in by_hand:
            report.append("  (%s)  %s" % (where, line))


def cmd_add(name, root, dry_run):
    if name not in template_names():
        print(
            "No template named '%s'. Templates: %s"
            % (name, ", ".join(template_names()) or "none"),
            file=sys.stderr,
        )
        return 2
    report = []
    if not os.path.isdir(os.path.join(root, DESIGN_DIR)):
        report.append(
            "note           %s has no design/ yet; creating design/%s/ only"
            % (root, name)
        )
    copy_files(name, root, dry_run, report)
    update_readme(name, root, dry_run, report)
    print(
        "design-setup %s in %s%s"
        % (name, root, "  (dry run, nothing written)" if dry_run else "")
    )
    for line in report:
        print(("  " + line) if line else "")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Add a templated subdirectory to a project's design/."
    )
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("list", help="list the templates")
    add = sub.add_parser("add", help="create design/<template>/ from a template")
    add.add_argument("template")
    add.add_argument(
        "--dry-run", action="store_true", help="report what would change, write nothing"
    )
    add.add_argument(
        "--project", help="project root (default: the git toplevel of the cwd)"
    )
    args = parser.parse_args()
    if args.command == "list":
        return cmd_list()
    if args.command == "add":
        return cmd_add(args.template, project_root(args.project), args.dry_run)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
