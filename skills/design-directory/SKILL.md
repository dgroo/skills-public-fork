---
name: design-directory
description: Set up, check or clean up a project's design/ directory, or add a templated subdirectory such as research/.
summary: "Sets up a project's design/ to the standard, checks it, sweeps done files to z.archived/, and opens cleanup-design."
group: design
argument-hint: "[check | cleanup | sweep | research | help]"
---

# design-directory — a project's design/ directory

The one place to go for a project's `design/` directory: set it up to the standard, say whether it meets it, add the optional subdirectories a project asks for, and reach the cleanup audit without remembering its name. It works in any project and needs nothing else from `/groot-project`.

The standard layout is the files under `templates/standard/files/` in this skill's directory, laid out exactly as they land under `design/`. What a tree cannot say (where the meta-files live, the older tier names, the set-aside directory) is `templates/standard/layout.json` beside it. Those two are the one copy: this file does not restate them, `/groot-project` creates its `design/` by calling this skill's script, and `/cleanup-design conformance` runs this skill's check. To change the standard, change those files.

## Routing

| Invocation | What it does |
| --- | --- |
| `/design-directory` | Set up: add what the standard has and the project lacks, then say what is off (see [Setup](#setup)) |
| `/design-directory check` | Report where `design/` departs from the standard; read-only (see [Check](#check)) |
| `/design-directory cleanup [args]` | The sweep, then the `/cleanup-design` audit (see [Cleanup](#cleanup)) |
| `/design-directory sweep` | Move files marked done into `z.archived/` (see [Sweep](#sweep)) |
| `/design-directory <template>` (today: `research`) | Create `design/<template>/` from the template (see [Add a template](#add-a-template)) |
| `/design-directory help` | Print usage and the templates available (see [Help](#help)) |

Anything else: say it is not a verb or a template, and print the help.

## Setup

Run the script that sits beside this file, from anywhere inside the project (it finds the git root; pass `--project <dir>` otherwise, and it refuses to guess outside a git repository):

```bash
python3 ${CLAUDE_SKILL_DIR}/design-directory.py setup
```

Print its report as is. It is safe to run without asking and safe to run twice: it creates only the standard files and directories that are missing, never overwrites or edits one that exists, and commits nothing. A project whose `stories/` still uses the older tier names gets nothing added under `stories/`; the report says so.

Then run the [Check](#check) script and print its report too, so one command says both what was added and what is off. Close with one line on which optional templates the project could add (from `list`).

`design/DESIGN.md` arrives as a skeleton with `<placeholders>`. When setup has just created it and the project's name and one-line purpose are plain from its README or CLAUDE.md, fill those two in; leave the other sections for the project's owner. Every other standard file is used as it lands.

## Check

```bash
python3 ${CLAUDE_SKILL_DIR}/design-directory.py check
```

Print its report as is. It writes nothing and needs nothing outside this skill; where `backlog-scan` is on the machine it asks it which directories are undeclared, and says so when it had to use the weaker rule instead.

The report sorts what it finds into three kinds, and the difference is the point:

- **Setup adds these** — missing standard pieces. Bare `/design-directory` creates them; nothing existing is touched.
- **The sweep moves these** — files already marked done, an `archived/` to rename. See [Sweep](#sweep).
- **Deliberate** — a meta-file at the repo root, the older story tiers, a directory `design/README.md` does not name. Each works as it is. Report them, say why it works today, and let the owner choose; never apply one as part of a check, and never bundle one into a setup or a sweep. A project deliberately on an older layout that works is not a bug.

Before moving a root `TODO.md` into `design/` on the owner's say-so: `git mv` it, and add or update a line in the project's `CLAUDE.md` naming `design/TODO.md` as the tracker. The upstream `/todo` and `/bug-bash` skills look only at the root, `docs/` and that pointer.

Do not improvise a standard from memory or from another project; the script's report is the check.

## Cleanup

Two steps, in this order:

1. The [Sweep](#sweep), which is mechanical: it moves what is already marked done.
2. Invoke the `cleanup-design` skill, passing along whatever followed `cleanup`, and follow it. That is the audit of what the documents say (stale references, decisions the docs have not caught up with); its phases and approval rules are that skill's and are not restated here.

When the sweep has nothing to move, say so in one line and go straight to the audit.

## Sweep

A file in `design/` ends its life in two steps: the session that finishes it marks it done where it sits (`status: done` in its frontmatter and a one-line banner; the notes, plans and helping-hands READMEs say how), and a sweep later moves marked files into `design/<directory>/z.archived/`. The mark is the judgment; the move is bookkeeping.

```bash
python3 ${CLAUDE_SKILL_DIR}/design-directory.py sweep --dry-run
```

Print the list. If it would move or rename anything, ask once whether to go ahead with all of it (the judgment was made when each file was marked, so one answer covers the list), and stop until answered. On yes, run the same command without `--dry-run` and print its report; both runs are built from one plan, so what was shown is what moves.

What the script does and does not do:

- Moves every Markdown file under a `design/` subdirectory whose frontmatter has `status: done` (in `helping-hands/`, also `dropped`), keeping its path below that directory: `notes/queue/x.md` goes to `notes/z.archived/queue/x.md`. It uses `git mv` for tracked files and commits nothing.
- Never touches `stories/` (a story's directory is its state), a file with no marker, or anything already inside `archived/`, `z.archived/`, `deprecated/` or an older `helping-hands/done/`.
- Renames an existing `archived/` to `z.archived/`. Where both exist it reports and leaves them.
- Never overwrites: a name already taken in `z.archived/` is reported and the file stays.
- Repoints links to the moved files in live `design/` files and in the repo's root Markdown other than the diary (Markdown links, reference definitions, `superseded_by:` values, path-style wiki links; fenced code is left alone). An edit outside `design/` is flagged, because a design-sync watcher will not commit it. Lines that still name an old path as plain text are listed for a look, not changed.
- Never writes a done marker.

**Plans whose story shipped.** The script ends by listing plans that carry no marker while their story sits in `stories/done/`. That is the one mark that can be computed. Offer it per plan, not in bulk; on a yes, write the marker the plans README describes (`status: done`, `done: <today>`, `superseded_by:` the done story, and the `> **Done <date> (<who>):** …` banner under the H1). The plan then moves on the next sweep. Do not propose marks for notes here: whether a note is done is a judgment for the session that absorbed it, or for `/pm`'s review.

## Add a template

Run the script that sits beside this file, from anywhere inside the project (it finds the git root; pass `--project <dir>` otherwise):

```bash
python3 ${CLAUDE_SKILL_DIR}/design-directory.py add <template>
```

Print its report as is. It is safe to run without asking and safe to run twice:

- Each template file is copied to `design/<template>/` byte for byte. A file already there is left alone, and the report says whether it matches the template.
- `design/README.md` gets the directory's line in its tree and its item in the trust order, with later items renumbered. A line already there is left alone.
- When the README has no tree or no trust order, the script prints the lines and changes nothing; offer to place them by hand where they fit that README. When there is no `design/README.md` at all, run [Setup](#setup) first and then the template again; do not write a README by hand.

`--dry-run` reports without writing. The script does not commit; leave that to the project's own habits (a design-synced repo commits `design/` by itself).

Do not edit an optional template's content on the way in, including to adapt it to the project. If a project needs different wording, that is an edit to its own copy afterwards, by whoever owns it.

## Templates

One directory per optional template under `templates/` in this skill's directory (`templates/standard/` is the layout itself and is placed only by setup); `python3 ${CLAUDE_SKILL_DIR}/design-directory.py list` prints them with their files. A template is `about.txt` (one line), `files/` (copied as is), and `readme-tree-line.txt` and `readme-trust-line.txt` (the two README entries). Adding a template is adding that directory; no change to this file is needed beyond the argument hint.

- **research** — `design/research/Do Research.md`: a `[[Do Research]]` link in any design doc tells the session reading it to look the topic up, and the answers are filed in that folder with a recheck date.

## Help

When invoked as `/design-directory help`, print the following block, then the output of `python3 ${CLAUDE_SKILL_DIR}/design-directory.py list`:

```
design-directory — Set up, check or clean up a project's design/ directory, or add a templated subdirectory to it.

Usage: /design-directory [check | cleanup | sweep | <template> | help]

Verbs:
  (none)            Set up: create whatever the standard design/ has and the
                    project lacks, then report what is off. Never overwrites.
  check             Report where design/ departs from the standard. Read-only.
  cleanup [args]    The sweep, then /cleanup-design: the audit for stale docs
                    and drift.
  sweep             Move files marked done into <dir>/z.archived/ and repoint
                    links to them. Shows the list and asks once before moving.
  <template>        Create design/<template>/ from the template and name it in
                    design/README.md. Never overwrites; safe to run twice.
  help              Show this message and the templates available.

See SKILL.md for full reference.
```

## Related

- `/cleanup-design` — the audit of what the documents inside `design/` say, which `cleanup` opens after the sweep. Where a file belongs is this skill's question; what a file says is that one's.
- `/groot-project` — bootstraps a whole project. Its `design/` phase runs this skill's `setup`, so the two cannot drift.
