---
author: user
priority: high
---

# design-setup — one skill that owns a project's design/ directory

> **Captured via `/pm` — not yet pondered.** Verbatim capture below; no exploration or design thinking has happened. Run `/ponder design-setup-skill` to develop it. Don't implement from this stub.

Related (found at triage): `groot-project-conformance-sweep.md` (drafts, 2026-06-20 — the same 'check the project against the standard' idea); [design-directory-lifecycle-in-skills](design-directory-lifecycle-in-skills.md) and [notes-tracker](notes-tracker.md) both change what this skill would absorb.

Asked 2026-11-11 06:27 (via design/ASKS.md):

high — Build a design-setup skill (Derek, 2026-11-10, from grootPM): one skill that owns a project's design/ directory, both checking that it is clean and set up to the standard and spawning its structured subdirectories (e.g. 'design-setup research' creates design/research/ with the Do Research file). It absorbs /groot-project's design-subtree phase (groot-project then calls it) and /cleanup-design conformance, so it is the one place that knows the layout, not a third. Templates are files in the skill's directory, not text embedded in SKILL.md; the first optional template is Empathy's design/research/Do Research.md (project-neutral, copy as is) plus the two lines it needs in design/README.md. Derek's reason for a separate skill: making this general enough for Empathy and Very Fine Company, where someone who is not Derek sets up a Pod's design directory without the rest of /groot-project. Decide in the story which copy of the layout stays the source: the skill's templates, groot-claude-coord design-corpus/DESIGN.md (what conformance reads today), or backlog-scan's standard/optional lists (its optional list is empty today). The name design-setup is free as a command and a skill. Story-sized: a refactor of a 1,078-line skill, not an add.
