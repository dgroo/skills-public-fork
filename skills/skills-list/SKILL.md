---
name: skills-list
description: List installed skills by source, or one line each by job with `brief`. Use for "what skills and commands do I have".
argument-hint: "[all | groups | mine | gstack | installed | plugins | upstream | commands] [brief]"
allowed-tools: Bash
summary: "Lists installed skills grouped by source, as plain script output with no analysis."
group: tooling
---

# Skill List

Run the script and print its output **verbatim**. No analysis, no commentary, no summary. The script is the answer.

```bash
bash ~/code/claude/skills/scripts/skills-list.sh "$ARGUMENTS"
```

That's it. One bash call, print the output, stop.

## Help

When invoked as `/skills-list help`, print the following block verbatim:

```
skills-list — List installed Claude Code skills, grouped by source.

Usage: /skills-list [group]

Subcommands (passed to the underlying script verbatim):
  (none)            Same as `make list` from this repo.
  all               Everything, grouped.
  groups            Available group names.
  mine              Local-owned skills.
  gstack            gstack-family skills.
  installed         Directly-installed (~/.claude/skills/) only.
  plugins           Skills from installed plugins.
  upstream          Upstream-tracked (joewalnes/skills) skills.
  commands          The slash commands in ~/.claude/commands, one line each.
  <group> brief     One line each. `mine brief` is the skills index: every
                    skill in this repo and the commands, grouped by job, from
                    each skill's summary: line. Bare `brief` means `mine brief`.
  help              Show this message.

Implementation: shells out to scripts/skills-list.sh and prints output verbatim.
The brief lines come from scripts/skills-index.py, which also writes README § Skills.

See SKILL.md for full reference.
```
