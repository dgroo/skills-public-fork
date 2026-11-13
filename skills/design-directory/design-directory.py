#!/usr/bin/env python3
"""design-directory: set up a project's design/ to the standard, and add optional,
templated subdirectories to it.

Usage:
  design-directory.py setup [--dry-run] [--project <dir>]
  design-directory.py check [--project <dir>]            # read-only
  design-directory.py sweep [--dry-run] [--project <dir>]
  design-directory.py selfcheck                          # the reader agrees with the tree
  design-directory.py list                      # the optional templates this skill ships
  design-directory.py add <template> [--dry-run] [--project <dir>]

`setup` copies the standard tree (templates/standard/files/, laid out exactly as it
lands under design/) into <project>/design/, creating only what is missing. Those
files are the source of the standard layout: nothing else in this skill, and no
other skill, restates it.

`check` reports where a project's design/ departs from that tree and from
templates/standard/layout.json (the parts of the layout a tree cannot say). It
writes nothing.

`sweep` moves every file whose frontmatter says it is done into
design/<directory>/z.archived/, renames an older archived/ to z.archived/, and
repoints links to the moved files in live files. It never writes a done marker and
never moves an unmarked file. The dry run and the real run are built from one plan.

`add` copies the template's files into <project>/design/<template>/ and names the
directory in <project>/design/README.md (the directory tree and the trust order).
It never overwrites: an existing file is left alone and reported, a README that
already names the directory is left alone, and a README whose shape it does not
recognise is not guessed at (the lines are printed for a hand edit instead).

Templates are found next to this script (resolved through symlinks), one directory
each under templates/. `standard` is the layout and is placed by `setup` only; every
other directory is an optional template:

  templates/<name>/about.txt              one line, shown by `list`
  templates/<name>/files/...              copied as is into design/<name>/
  templates/<name>/readme-tree-line.txt   the entry for the README's directory tree
  templates/<name>/readme-trust-line.txt  the entry for the README's trust order

Python 3.9 compatible (macOS system python3).
"""

import argparse
import filecmp
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")
TEMPLATE_FILES_SUBDIR = "files"
TEMPLATE_ABOUT = "about.txt"
TEMPLATE_TREE_LINE = "readme-tree-line.txt"
TEMPLATE_TRUST_LINE = "readme-trust-line.txt"

# The standard tree. Not an `add` template: it lands in design/ itself.
STANDARD_TEMPLATE = "standard"
# A placeholder file that keeps an empty directory in git. Placed only in a
# directory setup itself creates, never dropped into one that already exists.
KEEP_FILE = ".gitkeep"
# What the tree of files cannot say: where the meta-files live, the older tier
# names, the set-aside directory, which statuses the sweep moves. Read from a data
# file beside the tree so the layout has one home.
with open(
    os.path.join(TEMPLATES_DIR, STANDARD_TEMPLATE, "layout.json"), encoding="utf-8"
) as _layout_handle:
    LAYOUT = json.load(_layout_handle)
# A project still on the older tier names gets nothing added under stories/;
# moving to the standard tiers is a migration for its owner to choose.
STORIES_DIR = LAYOUT["stories_dir"]
STANDARD_STORY_TIERS = tuple(LAYOUT["story_tiers"])
LEGACY_STORY_TIERS = tuple(LAYOUT["legacy_story_tiers"])
SET_ASIDE_DIR = LAYOUT["set_aside_dir"]
SET_ASIDE_LEGACY_DIR = LAYOUT["set_aside_legacy_dir"]
SET_ASIDE_SUFFIXES = tuple(LAYOUT["set_aside_segment_suffixes"])
READER_COMMAND = "backlog-scan"
MARKDOWN_SUFFIX = ".md"
# Root Markdown that is a record of what happened; its links are history and the
# sweep leaves them alone.
ROOT_HISTORY_FILES = ("DIARY.md",)

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


def project_root(explicit, require_git=False):
    """The project to act on: --project, else the git toplevel of the cwd, else the
    cwd. With require_git, a cwd outside any git repo is refused (None): setup
    writes a whole tree and must not land wherever the shell happens to be."""
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
    if require_git:
        return None
    return os.getcwd()


def template_names():
    if not os.path.isdir(TEMPLATES_DIR):
        return []
    return sorted(
        name
        for name in os.listdir(TEMPLATES_DIR)
        if name != STANDARD_TEMPLATE
        and os.path.isdir(os.path.join(TEMPLATES_DIR, name, TEMPLATE_FILES_SUBDIR))
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
    print("Templates (design-directory <name> creates design/<name>/):")
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
            "not there      %s (run setup to create the standard one, then add %s again)"
            % (shown, name)
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


NOT_IN_GIT_MESSAGE = (
    "Not inside a git repository. Run %s from the project, or pass --project <dir>."
)


def legacy_story_tiers(root):
    stories = os.path.join(root, DESIGN_DIR, STORIES_DIR)
    return [
        tier for tier in LEGACY_STORY_TIERS if os.path.isdir(os.path.join(stories, tier))
    ]


def setup_plan(root):
    """(to create, already there, differing, legacy tiers) for the standard tree."""
    files_root = os.path.join(TEMPLATES_DIR, STANDARD_TEMPLATE, TEMPLATE_FILES_SUBDIR)
    legacy = legacy_story_tiers(root)
    created, present, differing = [], 0, []
    # Decided before anything is written, so a directory this run creates still
    # counts as new when its .gitkeep comes up.
    existing_dirs = set()
    for rel in template_files(files_root):
        directory = os.path.dirname(os.path.join(root, DESIGN_DIR, rel))
        if os.path.isdir(directory):
            existing_dirs.add(directory)
    for rel in template_files(files_root):
        source = os.path.join(files_root, rel)
        target = os.path.join(root, DESIGN_DIR, rel)
        if legacy and rel.startswith(STORIES_DIR + os.sep):
            continue
        if os.path.lexists(target):
            present += 1
            if os.path.basename(rel) != KEEP_FILE and not (
                os.path.isfile(target) and filecmp.cmp(source, target, shallow=False)
            ):
                differing.append(rel)
            continue
        if os.path.basename(rel) == KEEP_FILE:
            if os.path.dirname(target) in existing_dirs:
                present += 1
                continue
        created.append(rel)
    return created, present, differing, legacy


def cmd_setup(root, dry_run):
    """Copy what the standard tree has and the project lacks into design/."""
    files_root = os.path.join(TEMPLATES_DIR, STANDARD_TEMPLATE, TEMPLATE_FILES_SUBDIR)
    if not os.path.isdir(files_root):
        print("The standard tree is missing from " + files_root, file=sys.stderr)
        return 1
    if root is None:
        print(NOT_IN_GIT_MESSAGE % "setup", file=sys.stderr)
        return 2
    created, present, differing, legacy = setup_plan(root)
    if not dry_run:
        for rel in created:
            target = os.path.join(root, DESIGN_DIR, rel)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copyfile(os.path.join(files_root, rel), target)
    print(
        "design-directory setup in %s%s"
        % (root, "  (dry run, nothing written)" if dry_run else "")
    )
    for rel in created:
        print("  created        %s" % os.path.join(DESIGN_DIR, rel))
    if not created:
        print("  nothing to add: every piece of the standard design/ is already there")
    if present:
        print("  already there  %d piece(s) of the standard, left alone" % present)
    if differing:
        print(
            "  own wording    %s differ from the template, as a project's own files do; left alone"
            % ", ".join(differing)
        )
    if legacy:
        print(
            "  older layout   %s has %s; nothing under it was added (the standard tiers are %s)"
            % (
                os.path.join(DESIGN_DIR, STORIES_DIR),
                ", ".join(tier + "/" for tier in legacy),
                ", ".join(tier + "/" for tier in STANDARD_STORY_TIERS),
            )
        )
    return 0


def cmd_add(name, root, dry_run):
    if name == STANDARD_TEMPLATE:
        print(
            "'%s' is the standard layout, not an optional template. Use: setup"
            % STANDARD_TEMPLATE,
            file=sys.stderr,
        )
        return 2
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
        "design-directory %s in %s%s"
        % (name, root, "  (dry run, nothing written)" if dry_run else "")
    )
    for line in report:
        print(("  " + line) if line else "")
    return 0


# ---------------------------------------------------------------------------
# sweep and check


def is_set_aside(segment):
    """A path segment that holds set-aside work: archived, z.archived, deprecated."""
    return any(segment.endswith(suffix) for suffix in SET_ASIDE_SUFFIXES)


def is_tooling(segment):
    return segment.startswith((".", "_"))


def frontmatter_status(path):
    """The `status:` value from frontmatter that opens on the file's first line, or
    None. A `status: done` anywhere else (an example in a fenced block) is not one."""
    try:
        with open(path, encoding="utf-8") as handle:
            if handle.readline().rstrip("\n") != "---":
                return None
            for line in handle:
                line = line.rstrip("\n")
                if line == "---":
                    return None
                match = re.match(r"^status:\s*(.*)$", line)
                if match:
                    value = match.group(1).split(" #")[0].strip().strip("\"'")
                    return value or None
    except (OSError, UnicodeDecodeError):
        return None
    return None


def live_design_files(root):
    """(markdown files, legacy archived/ directories) under design/, never looking
    inside a set-aside or tooling directory."""
    design = os.path.join(root, DESIGN_DIR)
    files, legacy_dirs = [], []
    for dirpath, dirnames, filenames in os.walk(design):
        for name in list(dirnames):
            if name == SET_ASIDE_LEGACY_DIR:
                legacy_dirs.append(os.path.join(dirpath, name))
            if is_set_aside(name) or is_tooling(name):
                dirnames.remove(name)
        dirnames.sort()
        for name in sorted(filenames):
            if name.endswith(MARKDOWN_SUFFIX):
                files.append(os.path.join(dirpath, name))
    return files, sorted(legacy_dirs)


def swept_statuses(top_dir):
    return set(LAYOUT["swept_statuses"]) | set(
        LAYOUT["swept_statuses_by_dir"].get(top_dir, [])
    )


class SweepPlan:
    """Everything a sweep would do, computed once. The dry run prints it and the
    real run executes the same object."""

    def __init__(self, root):
        self.root = root
        self.design = os.path.join(root, DESIGN_DIR)
        self.renames = []  # (archived dir, z.archived dir)
        self.rename_conflicts = []  # archived dirs whose z.archived sibling exists
        self.moves = []  # (source file, target file)
        self.collisions = []  # (source file, occupied target)
        self.mark_proposals = []  # (plan file, done story file)
        self.link_edits = {}  # live file -> (links repointed, its new text)
        self.path_map = {}  # every old absolute path -> its new absolute path
        self._build()

    def _build(self):
        files, legacy_dirs = live_design_files(self.root)
        renamed_prefixes = {}
        for legacy_dir in legacy_dirs:
            target = os.path.join(os.path.dirname(legacy_dir), SET_ASIDE_DIR)
            if os.path.lexists(target):
                self.rename_conflicts.append(legacy_dir)
                continue
            self.renames.append((legacy_dir, target))
            renamed_prefixes[legacy_dir] = target
            for dirpath, _dirnames, filenames in os.walk(legacy_dir):
                for name in filenames:
                    old = os.path.join(dirpath, name)
                    self.path_map[old] = target + old[len(legacy_dir) :]
        for path in files:
            parts = os.path.relpath(path, self.design).split(os.sep)
            if len(parts) < 2 or parts[0] in LAYOUT["never_swept_dirs"]:
                continue
            # An older done/ directory is already that project's set-aside place.
            if any(
                "/".join(parts).startswith(legacy_done + "/")
                for legacy_done in LAYOUT["legacy_done_dirs"]
            ):
                continue
            if frontmatter_status(path) not in swept_statuses(parts[0]):
                continue
            target = os.path.join(self.design, parts[0], SET_ASIDE_DIR, *parts[1:])
            # Where the target would sit today, if its directory is about to be renamed.
            legacy_twin = os.path.join(
                self.design, parts[0], SET_ASIDE_LEGACY_DIR, *parts[1:]
            )
            occupied = os.path.lexists(target) or (
                os.path.join(self.design, parts[0], SET_ASIDE_LEGACY_DIR)
                in renamed_prefixes
                and os.path.lexists(legacy_twin)
            )
            if occupied:
                self.collisions.append((path, target))
                continue
            self.moves.append((path, target))
            self.path_map[path] = target
        moving = {source for source, _target in self.moves}
        self._find_mark_proposals([path for path in files if path not in moving])
        for path in self._link_sources(files, moving):
            edits = self._link_edits_for(path)
            if edits:
                self.link_edits[path] = edits

    def _find_mark_proposals(self, live_files):
        """Plans not marked done whose story sits in stories/done/: the one signal
        that is computed, not judged. Listed for the session to propose; never
        marked here."""
        stories = os.path.join(self.design, STORIES_DIR)
        done_tier = STANDARD_STORY_TIERS[-1]
        done_dir = os.path.join(stories, done_tier)
        if not os.path.isdir(done_dir):
            return
        done = {
            name[: -len(MARKDOWN_SUFFIX)]: os.path.join(done_dir, name)
            for name in os.listdir(done_dir)
            if name.endswith(MARKDOWN_SUFFIX)
        }
        open_slugs = set()
        for tier in STANDARD_STORY_TIERS[:-1]:
            tier_dir = os.path.join(stories, tier)
            if os.path.isdir(tier_dir):
                open_slugs.update(
                    name[: -len(MARKDOWN_SUFFIX)] for name in os.listdir(tier_dir)
                )
        plans_prefix = os.path.join(self.design, LAYOUT["plans_dir"]) + os.sep
        for path in live_files:
            if not path.startswith(plans_prefix) or os.path.basename(path) == DESIGN_README:
                continue
            if frontmatter_status(path) is not None:
                continue
            stem = os.path.basename(path)[: -len(MARKDOWN_SUFFIX)]
            stem = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)
            stem = re.sub(r"-plan$", "", stem)
            with open(path, encoding="utf-8", errors="replace") as handle:
                text = handle.read()
            linked = [
                slug
                for slug in re.findall(
                    r"stories/(?:[\w.]+/)?([\w.-]+)%s" % re.escape(MARKDOWN_SUFFIX), text
                )
                if slug in done and slug not in open_slugs
            ]
            slug = stem if stem in done and stem not in open_slugs else None
            slug = slug or (linked[0] if linked else None)
            if slug:
                self.mark_proposals.append((path, done[slug]))

    def _link_sources(self, files, moving):
        """Live files whose links are kept true: design/ outside the set-aside
        directories (minus what is moving), and the repo's root Markdown."""
        sources = [path for path in files if path not in moving]
        for name in sorted(os.listdir(self.root)):
            path = os.path.join(self.root, name)
            if (
                name.endswith(MARKDOWN_SUFFIX)
                and os.path.isfile(path)
                and name not in ROOT_HISTORY_FILES
            ):
                sources.append(path)
        return sources

    def _resolve(self, source, target_text, bases):
        """The moved file a link target names, and the base it was written against."""
        plain = urllib.parse.unquote(target_text)
        for base in bases:
            for candidate in (plain, plain + MARKDOWN_SUFFIX):
                absolute = os.path.normpath(os.path.join(base, candidate))
                if absolute in self.path_map:
                    return absolute, base, candidate != plain
        return None, None, False

    def _rewrite(self, source, target_text):
        """The new text for one link target, or None when it does not point at a
        moved file. Keeps the anchor, the base the author used, and the way spaces
        were written."""
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target_text) or target_text.startswith("#"):
            return None
        path_text, hash_mark, anchor = target_text.partition("#")
        if not path_text:
            return None
        bases = [os.path.dirname(source), self.root, self.design]
        old, base, extension_implied = self._resolve(source, path_text, bases)
        if old is None:
            return None
        new_text = os.path.relpath(self.path_map[old], base).replace(os.sep, "/")
        if path_text.startswith("./"):
            new_text = "./" + new_text
        if extension_implied:
            new_text = new_text[: -len(MARKDOWN_SUFFIX)]
        if "%20" in path_text:
            new_text = new_text.replace(" ", "%20")
        return new_text + hash_mark + anchor

    LINK_PATTERNS = (
        # [text](target) and [text](<target with spaces> "title")
        re.compile(r"\]\(<([^>\n]+)>"),
        re.compile(r"\]\(([^)<\s]+)"),
        # [label]: target
        re.compile(r"^\[[^\]\n]+\]:\s*<?([^>\s]+)", re.MULTILINE),
        # superseded_by: target  (frontmatter of another file)
        re.compile(r"^superseded_by:\s*[\"']?([^\"'\s#]+)", re.MULTILINE),
        # [[path/to/file]], [[path/to/file#anchor]], [[path/to/file|alias]]
        re.compile(r"\[\[([^\]|\n]*/[^\]|\n]*)"),
    )

    def _link_edits_for(self, source):
        """(number of links repointed, the file's new text), or None when no link
        in it points at a moved file. Fenced code is left exactly as written."""
        try:
            with open(source, encoding="utf-8") as handle:
                text = handle.read()
        except (OSError, UnicodeDecodeError):
            return None
        count = 0
        in_fence = False
        lines = text.split("\n")
        for index, line in enumerate(lines):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for pattern in self.LINK_PATTERNS:

                def repoint(match):
                    nonlocal count
                    replacement = self._rewrite(source, match.group(1))
                    if replacement is None or replacement == match.group(1):
                        return match.group(0)
                    count += 1
                    return match.group(0).replace(match.group(1), replacement)

                line = pattern.sub(repoint, line)
            lines[index] = line
        if not count:
            return None
        return count, "\n".join(lines)

    @property
    def is_empty(self):
        return not (self.renames or self.moves)

    def execute(self):
        for old, new in self.renames:
            move_path(self.root, old, new)
        for old, new in self.moves:
            os.makedirs(os.path.dirname(new), exist_ok=True)
            move_path(self.root, old, new)
        for path, (_count, new_text) in self.link_edits.items():
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(new_text)

    def leftover_mentions(self):
        """Lines in live files that still name a moved file's old path after the
        links were repointed: a plain-text mention the patterns do not cover."""
        files, _legacy = live_design_files(self.root)
        moved_targets = set(self.path_map.values())
        sources = self._link_sources(files, moved_targets)
        found = []
        for old in sorted(self.path_map):
            needles = {
                os.path.relpath(old, self.root).replace(os.sep, "/"),
                os.path.relpath(old, self.design).replace(os.sep, "/"),
            }
            for source in sources:
                try:
                    with open(source, encoding="utf-8") as handle:
                        lines = handle.read().split("\n")
                except (OSError, UnicodeDecodeError):
                    continue
                for number, line in enumerate(lines, 1):
                    if any(needle in line for needle in needles):
                        found.append((source, number, sorted(needles)[0]))
        return found


def move_path(root, old, new):
    """git mv when git tracks the path (history follows), a plain rename otherwise."""
    tracked = subprocess.run(
        ["git", "-C", root, "ls-files", "--error-unmatch", old],
        capture_output=True,
        text=True,
    )
    if tracked.returncode == 0 or os.path.isdir(old):
        moved = subprocess.run(
            ["git", "-C", root, "mv", old, new], capture_output=True, text=True
        )
        if moved.returncode == 0:
            return
    os.rename(old, new)


def cmd_sweep(root, dry_run):
    if root is None:
        print(NOT_IN_GIT_MESSAGE % "sweep", file=sys.stderr)
        return 2
    if not os.path.isdir(os.path.join(root, DESIGN_DIR)):
        print("design-directory sweep in %s\n  no design/ directory here" % root)
        return 0
    plan = SweepPlan(root)

    def shown(path):
        return os.path.relpath(path, root)

    print(
        "design-directory sweep in %s%s"
        % (root, "  (dry run, nothing moved)" if dry_run else "")
    )
    verb = "would move " if dry_run else "moved      "
    for old, new in plan.renames:
        print("  %s    %s/ → %s/" % (verb, shown(old), shown(new)))
    for old, new in plan.moves:
        print("  %s    %s → %s" % (verb, shown(old), shown(new)))
    if plan.is_empty:
        print("  nothing to move: no file marked done is waiting, and no archived/ to rename")
    for path, edits in sorted(plan.link_edits.items()):
        outside = "" if path.startswith(plan.design + os.sep) else "  (outside design/: commit it yourself)"
        print(
            "  %s  %d link(s) in %s%s"
            % ("would repoint" if dry_run else "repointed    ", edits[0], shown(path), outside)
        )
    for path, target in plan.collisions:
        print(
            "  left in place  %s: %s already exists; nothing is overwritten"
            % (shown(path), shown(target))
        )
    for path in plan.rename_conflicts:
        print(
            "  left in place  %s/: %s/ exists beside it; merge them by hand"
            % (shown(path), SET_ASIDE_DIR)
        )
    if not dry_run and not plan.is_empty:
        plan.execute()
        for source, number, needle in plan.leftover_mentions():
            print(
                "  still mentions %s:%d names %s as plain text; not changed"
                % (shown(source), number, needle)
            )
    if plan.mark_proposals:
        print("")
        print("Plans whose story is in %s/ and that carry no done marker (not moved; propose the mark per plan):" % STANDARD_STORY_TIERS[-1])
        for path, story in plan.mark_proposals:
            print("  %s  ←  %s" % (shown(path), shown(story)))
    return 0


def reader_design_dirs(root):
    """The reader's sorting of design/'s directories, or None when the reader is
    not on this machine or cannot be read."""
    reader = shutil.which(READER_COMMAND)
    if not reader:
        return None
    try:
        result = subprocess.run(
            [reader, "--json"], cwd=root, capture_output=True, text=True, timeout=60
        )
        return json.loads(result.stdout).get("design_dirs")
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None


def standard_top_dirs():
    files_root = os.path.join(TEMPLATES_DIR, STANDARD_TEMPLATE, TEMPLATE_FILES_SUBDIR)
    return sorted(
        name
        for name in os.listdir(files_root)
        if os.path.isdir(os.path.join(files_root, name))
    )


def cmd_check(root):
    """Report where design/ departs from the standard. Writes nothing."""
    design = os.path.join(root, DESIGN_DIR)
    print("design-directory check in %s" % root)
    if not os.path.isdir(design):
        print("  no design/ directory. /design-directory creates the standard one.")
        return 0
    setup_fixes, sweep_fixes, deliberate, notes = [], [], [], []

    created, _present, _differing, legacy = setup_plan(root)
    for rel in created:
        setup_fixes.append("missing: %s" % os.path.join(DESIGN_DIR, rel))
    if legacy:
        deliberate.append(
            "%s uses the older tiers (%s); the standard is %s. Moving is a migration: every story changes path, and links and tools that name the old tiers change with it."
            % (
                os.path.join(DESIGN_DIR, STORIES_DIR),
                ", ".join(tier + "/" for tier in legacy),
                ", ".join(tier + "/" for tier in STANDARD_STORY_TIERS),
            )
        )

    for name in LAYOUT["meta_files"]:
        at_root = os.path.isfile(os.path.join(root, name))
        in_design = os.path.isfile(os.path.join(design, name))
        if at_root and in_design:
            deliberate.append(
                "%s exists at the repo root and in design/; readers take design/ first, so the root copy is shadowed. Merge it in by hand."
                % name
            )
        elif at_root:
            deliberate.append(
                "%s is at the repo root; the standard home is design/%s. It works where it is. The move is `git mv %s design/%s`%s"
                % (
                    name,
                    name,
                    name,
                    name,
                    ", plus a line in CLAUDE.md naming design/TODO.md as the tracker, which is how a skill that only looks at the root finds it."
                    if name == "TODO.md"
                    else ".",
                )
            )

    known_root_files = (
        {DESIGN_README, "DESIGN.md"}
        | set(LAYOUT["meta_files"])
        | set(LAYOUT["other_design_root_files"])
    )
    strays = sorted(
        name
        for name in os.listdir(design)
        if name.endswith(MARKDOWN_SUFFIX)
        and os.path.isfile(os.path.join(design, name))
        and name not in known_root_files
    )
    design_readme = os.path.join(design, DESIGN_README)
    readme_text = ""
    if os.path.isfile(design_readme):
        with open(design_readme, encoding="utf-8") as handle:
            readme_text = handle.read()
    unnamed_strays = [name for name in strays if name not in readme_text]
    if unnamed_strays:
        notes.append(
            "%d document(s) sit directly in design/ and design/README.md does not name them: %s. A reference document can live there once the README says what it is; a stray plan or note belongs in its directory (/groot-project's Phase 2 offers those moves)."
            % (len(unnamed_strays), ", ".join(unnamed_strays))
        )

    dirs = reader_design_dirs(root)
    if dirs is not None:
        undeclared = dirs.get("undeclared", [])
        rule = ""
    else:
        readme = readme_text
        standard = set(standard_top_dirs())
        undeclared = sorted(
            name
            for name in os.listdir(design)
            if os.path.isdir(os.path.join(design, name))
            and not is_tooling(name)
            and not is_set_aside(name)
            and name not in standard
            and (name + "/") not in readme
        )
        rule = " (%s is not on this machine, so the fleet's optional list was not consulted)" % READER_COMMAND
    for name in undeclared:
        if name in LAYOUT["tool_owned_dirs"]:
            continue
        deliberate.append(
            "design/%s/ is not a standard directory and design/README.md does not name it%s. Name it there with its reason, fold it into notes/ or plans/, or set it aside."
            % (name, rule)
        )

    plan = SweepPlan(root)
    for old, _new in plan.renames:
        sweep_fixes.append("%s/ is the older name for %s/" % (os.path.relpath(old, root), SET_ASIDE_DIR))
    if plan.moves:
        sweep_fixes.append(
            "%d file(s) marked done are waiting to move to %s/" % (len(plan.moves), SET_ASIDE_DIR)
        )
    if plan.mark_proposals:
        notes.append(
            "%d plan(s) have their story in %s/ and no done marker; `sweep --dry-run` lists them"
            % (len(plan.mark_proposals), STANDARD_STORY_TIERS[-1])
        )
    for path, target in plan.collisions:
        deliberate.append(
            "%s is marked done but %s already exists; the sweep will not overwrite it. Rename one."
            % (os.path.relpath(path, root), os.path.relpath(target, root))
        )
    for path in plan.rename_conflicts:
        deliberate.append(
            "%s/ and %s/ both exist in %s; merge them by hand."
            % (SET_ASIDE_LEGACY_DIR, SET_ASIDE_DIR, os.path.relpath(os.path.dirname(path), root))
        )
    for rel in LAYOUT["legacy_done_dirs"]:
        if os.path.isdir(os.path.join(design, rel)):
            notes.append(
                "design/%s/ is an older convention; resolved items now stay in place until the sweep. Nothing needs doing."
                % rel
            )

    if not (setup_fixes or sweep_fixes or deliberate):
        print("  design/ meets the standard.")
    sections = (
        ("Setup adds these (/design-directory; nothing existing is touched):", setup_fixes),
        ("The sweep moves these (/design-directory sweep; shown before anything moves):", sweep_fixes),
        ("Deliberate, the owner's call (each works as it is today; none is fixed for you):", deliberate),
        ("For information:", notes),
    )
    for title, items in sections:
        if items:
            print("")
            print(title)
            for item in items:
                print("  - " + item)
    return 0


def cmd_selfcheck():
    """The reader and the tree agree: set the standard up in a scratch directory and
    ask the reader what it sees."""
    if not shutil.which(READER_COMMAND):
        print("selfcheck: skipped, %s is not on this machine (not a pass)" % READER_COMMAND)
        return 0
    with tempfile.TemporaryDirectory() as scratch:
        subprocess.run(["git", "init", "-q", scratch], check=True)
        created, _present, _differing, _legacy = setup_plan(scratch)
        files_root = os.path.join(TEMPLATES_DIR, STANDARD_TEMPLATE, TEMPLATE_FILES_SUBDIR)
        for rel in created:
            target = os.path.join(scratch, DESIGN_DIR, rel)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copyfile(os.path.join(files_root, rel), target)
        dirs = reader_design_dirs(scratch)
    if dirs is None:
        print("selfcheck: FAILED, %s --json gave nothing readable" % READER_COMMAND)
        return 1
    expected = standard_top_dirs()
    problems = []
    if sorted(dirs.get("standard", [])) != expected:
        problems.append(
            "the standard tree has %s; %s calls %s standard"
            % (expected, READER_COMMAND, sorted(dirs.get("standard", [])))
        )
    for kind in ("optional", "declared", "undeclared"):
        if dirs.get(kind):
            problems.append("%s sorts %s as %s" % (READER_COMMAND, dirs[kind], kind))
    if problems:
        print("selfcheck: FAILED")
        for problem in problems:
            print("  - " + problem)
        return 1
    print("selfcheck: ok, %s sees the standard tree as %s" % (READER_COMMAND, expected))
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Set up a project's design/, or add a templated subdirectory to it."
    )
    sub = parser.add_subparsers(dest="command")
    setup = sub.add_parser(
        "setup", help="create what the standard design/ has and the project lacks"
    )
    setup.add_argument(
        "--dry-run", action="store_true", help="report what would change, write nothing"
    )
    setup.add_argument(
        "--project", help="project root (default: the git toplevel of the cwd)"
    )
    check = sub.add_parser("check", help="report where design/ departs from the standard")
    check.add_argument(
        "--project", help="project root (default: the git toplevel of the cwd)"
    )
    sweep = sub.add_parser(
        "sweep", help="move files marked done into z.archived/ and repoint links"
    )
    sweep.add_argument(
        "--dry-run", action="store_true", help="report what would move, move nothing"
    )
    sweep.add_argument(
        "--project", help="project root (default: the git toplevel of the cwd)"
    )
    sub.add_parser("selfcheck", help="confirm the reader agrees with the standard tree")
    sub.add_parser("list", help="list the optional templates")
    add = sub.add_parser("add", help="create design/<template>/ from a template")
    add.add_argument("template")
    add.add_argument(
        "--dry-run", action="store_true", help="report what would change, write nothing"
    )
    add.add_argument(
        "--project", help="project root (default: the git toplevel of the cwd)"
    )
    args = parser.parse_args()
    if args.command == "setup":
        return cmd_setup(project_root(args.project, require_git=True), args.dry_run)
    if args.command == "check":
        return cmd_check(project_root(args.project))
    if args.command == "sweep":
        return cmd_sweep(project_root(args.project, require_git=True), args.dry_run)
    if args.command == "selfcheck":
        return cmd_selfcheck()
    if args.command == "list":
        return cmd_list()
    if args.command == "add":
        return cmd_add(args.template, project_root(args.project), args.dry_run)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
