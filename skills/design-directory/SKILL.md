---
name: design-directory
description: Set up, check or clean up a project's design/ directory, or add a templated subdirectory such as research/.
summary: "Sets up a project's design/ to the standard, checks it, adds templated subdirectories, and opens cleanup-design."
group: design
argument-hint: "[check | cleanup | research | help]"
---

# design-directory — a project's design/ directory

The one place to go for a project's `design/` directory: set it up to the standard, say whether it meets it, add the optional subdirectories a project asks for, and reach the cleanup audit without remembering its name. It works in any project and needs nothing else from `/groot-project`.

The standard layout is the files under `templates/standard/files/` in this skill's directory, laid out exactly as they land under `design/`. That tree is the one copy: this file does not restate it, and `/groot-project` creates its `design/` by calling this skill's script. To change the standard, change those files.

## Routing

| Invocation | What it does |
| --- | --- |
| `/design-directory` | Set up: add what the standard has and the project lacks (see [Setup](#setup)) |
| `/design-directory check` | Report whether `design/` meets the standard; read-only (see [Check](#check)) |
| `/design-directory cleanup [args]` | Run `/cleanup-design` (see [Cleanup](#cleanup)) |
| `/design-directory <template>` (today: `research`) | Create `design/<template>/` from the template (see [Add a template](#add-a-template)) |
| `/design-directory help` | Print usage and the templates available (see [Help](#help)) |

Anything else: say it is not a verb or a template, and print the help.

## Setup

Run the script that sits beside this file, from anywhere inside the project (it finds the git root; pass `--project <dir>` otherwise, and it refuses to guess outside a git repository):

```bash
python3 ${CLAUDE_SKILL_DIR}/design-directory.py setup
```

Print its report as is. It is safe to run without asking and safe to run twice: it creates only the standard files and directories that are missing, never overwrites or edits one that exists, and commits nothing. A project whose `stories/` still uses the older tier names gets nothing added under `stories/`; the report says so.

Then, in one or two lines: which optional templates the project could add (from `list`), and that `/design-directory check` reports what is off about a `design/` that already exists, which setup does not judge.

`design/DESIGN.md` arrives as a skeleton with `<placeholders>`. When setup has just created it and the project's name and one-line purpose are plain from its README or CLAUDE.md, fill those two in; leave the other sections for the project's owner. Every other standard file is used as it lands.

## Check

Invoke the `cleanup-design` skill with the argument `conformance` and relay its findings. That mode owns the comparison, the safe-versus-deliberate classification and the approval rules; add nothing to them and apply no fix it would not.

Then add one line of this skill's own: which templates the project already has (a `design/<template>/` directory exists) and which it could add, from `list` below.

When `cleanup-design` is not installed, or it reports that it has no canon to compare against (it reads `~/code/groot-claude-coord/design/design-corpus/DESIGN.md`, which a machine outside Derek's fleet will not have), say exactly that and stop. Do not improvise a standard from memory or from another project.

## Cleanup

Invoke the `cleanup-design` skill, passing along whatever followed `cleanup` (nothing, or one of its own arguments), and follow it. This verb is a door, kept here so the audit can be found under the directory's name; the audit, its phases and its approval rules are that skill's and are not restated here.

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

Usage: /design-directory [check | cleanup | <template> | help]

Verbs:
  (none)            Set up: create whatever the standard design/ has and the
                    project lacks. Never overwrites; safe to run twice.
  check             Report whether design/ meets the standard, read-only, via
                    /cleanup-design conformance, plus which templates are in use.
  cleanup [args]    Run /cleanup-design: the audit for stale docs and drift.
  <template>        Create design/<template>/ from the template and name it in
                    design/README.md. Never overwrites; safe to run twice.
  help              Show this message and the templates available.

See SKILL.md for full reference.
```

## Related

- `/cleanup-design` — owns the conformance check this skill calls, and the drift audit of the documents inside `design/` that `cleanup` opens.
- `/groot-project` — bootstraps a whole project. Its `design/` phase runs this skill's `setup`, so the two cannot drift.
