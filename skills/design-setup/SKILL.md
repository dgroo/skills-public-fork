---
name: design-setup
description: Check a project's design/ against the standard, or add a templated subdirectory to it. Use for "design-setup research".
summary: "Checks a project's design/ against the standard and adds templated subdirectories (research/ with the Do Research file)."
group: design
argument-hint: "[check | research | help]"
---

# design-setup — a project's design/ directory

Two jobs: say whether a project's `design/` is set up to the standard, and add the optional subdirectories a project asks for, each from a template file that ships in this skill's directory. It works in any project and needs nothing else from `/groot-project`.

The layout itself is not written here. The check reads it where `/cleanup-design conformance` reads it, and a template adds one directory and the lines that name it; neither restates the standard tree.

## Routing

| Invocation | What it does |
| --- | --- |
| `/design-setup` or `/design-setup check` | Report whether `design/` meets the standard (see [Check](#check)) |
| `/design-setup <template>` (today: `research`) | Create `design/<template>/` from the template (see [Add a template](#add-a-template)) |
| `/design-setup help` | Print usage and the templates available (see [Help](#help)) |

Anything else: say it is not a subcommand or a template, and print the help.

## Check

Invoke the `cleanup-design` skill with the argument `conformance` and relay its findings. That mode owns the comparison, the safe-versus-deliberate classification and the approval rules; add nothing to them and apply no fix it would not.

Then add one line of this skill's own: which templates the project already has (a `design/<template>/` directory exists) and which it could add, from `list` below.

When `cleanup-design` is not installed, or it reports that it has no canon to compare against (it reads `~/code/groot-claude-coord/design/design-corpus/DESIGN.md`, which a machine outside Derek's fleet will not have), say exactly that and stop. Do not improvise a standard from memory or from another project.

## Add a template

Run the script that sits beside this file, from anywhere inside the project (it finds the git root; pass `--project <dir>` otherwise). `<skill-dir>` is this skill's base directory, `~/.claude/skills/design-setup` when installed:

```bash
python3 <skill-dir>/design-setup.py add <template>
```

Print its report as is. It is safe to run without asking and safe to run twice:

- Each template file is copied to `design/<template>/` byte for byte. A file already there is left alone, and the report says whether it matches the template.
- `design/README.md` gets the directory's line in its tree and its item in the trust order, with later items renumbered. A line already there is left alone.
- When the README has no tree or no trust order, or does not exist, the script prints the lines and changes nothing. Offer to place them by hand where they fit that README; do not create a `design/README.md`, which would be a second copy of the layout.

`--dry-run` reports without writing. The script does not commit; leave that to the project's own habits (a design-synced repo commits `design/` by itself).

Do not edit a template's content on the way in, including to adapt it to the project. If a project needs different wording, that is an edit to its own copy afterwards, by whoever owns it.

## Templates

One directory per template under `templates/` in this skill's directory; `python3 <skill-dir>/design-setup.py list` prints them with their files. A template is `about.txt` (one line), `files/` (copied as is), and `readme-tree-line.txt` and `readme-trust-line.txt` (the two README entries). Adding a template is adding that directory; no change to this file is needed beyond the argument hint.

- **research** — `design/research/Do Research.md`: a `[[Do Research]]` link in any design doc tells the session reading it to look the topic up, and the answers are filed in that folder with a recheck date.

## Help

When invoked as `/design-setup help`, print the following block, then the output of `python3 <skill-dir>/design-setup.py list`:

```
design-setup — Check a project's design/ against the standard, or add a templated subdirectory to it.

Usage: /design-setup [check | <template> | help]

Verbs:
  (none), check     Report whether design/ meets the standard, via
                    /cleanup-design conformance, plus which templates are in use.
  <template>        Create design/<template>/ from the template and name it in
                    design/README.md. Never overwrites; safe to run twice.
  help              Show this message and the templates available.

See SKILL.md for full reference.
```

## Related

- `/cleanup-design` — owns the conformance check this skill calls, and the drift audit of the documents inside `design/`.
- `/groot-project` — bootstraps a whole project, including the standard `design/` subtree. This skill adds to a `design/` that exists; it does not create the standard one.
