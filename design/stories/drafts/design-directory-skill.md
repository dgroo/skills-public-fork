---
author: user
priority: high
---

# design-setup — one skill that owns a project's design/ directory

*Authored by Claude Fable 5.2 with Derek · Last updated 2026-11-11 13:55.*

## Executive summary

**What:** One skill, `/design-setup`, that checks a project's design/ against the standard and adds templated subdirectories to it.  
**Where it stands:** built through increment 1 of 3 (2026-11-11): `research` and `check` work; the absorptions are open.  
**Needs you:**

- **Decide** D1: which copy of the layout is the source; recommended, the skill's template files.
- **Decide** D2: move /groot-project's six design templates into this skill as increment 2; recommended yes.
- **Decide** D3: build the archive sweep here and make conformance native as increment 3; recommended yes.
- **Decide** D4: make the Do Research template say "the project's owner" where it says Derek; recommended yes.

## Decisions

- D1 · open · the skill's template files become the source of the layout (recommended) → [D1](#d1-which-copy-of-the-layout-is-the-source--open)
- D2 · open · /groot-project's design-subtree phase moves here as increment 2 (recommended) → [D2](#d2-absorb-groot-projects-design-subtree-phase--open)
- D3 · open · the archive sweep is built here and conformance becomes native, as increment 3 (recommended) → [D3](#d3-the-archive-sweep-and-conformance-move-here--open)
- D4 · open · neutralise the three "Derek" mentions and the stamp in the skill's Do Research copy (recommended) → [D4](#d4-the-do-research-template-names-derek--open)
- D5 · decided 2026-11-11 (by default) · a template is a directory of plain files and a Python script places it → [D5](#d5-shape-of-a-template--decided-2026-11-11)
- D6 · decided 2026-11-11 (by default) · the README trust line reads "the entries above it"; Empathy's "(trial, 2026-11-10)" is dropped → [D6](#d6-wording-of-the-two-readme-lines--decided-2026-11-11)

## What is built (increment 1, 2026-11-11)

Built at Derek's word on 2026-11-11 13:45 ("I was expecting to be able to use "design-setup" by now"), ahead of the ask-and-answer story at the top of the queue. The stub's "don't implement from this stub" line was lifted for this increment only.

- `skills/design-setup/SKILL.md`: routing for bare / `check` / `<template>` / `help`.
- `/design-setup research` runs `skills/design-setup/design-setup.py add research`: copies `templates/research/files/Do Research.md` to `design/research/` byte for byte, adds the `research/` line to the tree in `design/README.md` and the `research/` item to its trust order (after `plans/`, later items renumbered). An existing file or line is left alone and reported. A README with no tree or no trust order, or no README, gets the lines printed and nothing written; the skill never creates `design/README.md`.
- `/design-setup` and `/design-setup check` call `/cleanup-design conformance` and add which templates the project has. No layout is written in this skill.
- `/design-setup help` prints the verbs and the script's template list.

Verified in four scratch repos under `$TMPDIR`: a /groot-project-style README (both lines placed, `notes/` renumbered 5 → 6, `backlog-scan` then reports `research` as declared); this repo's README, which has a tree and no trust order (tree line placed, trust line printed); no README plus an existing, different `Do Research.md` (file kept, nothing written); Empathy's README (already names it, nothing changed). In all four a second run left `git status` empty.

Not in this increment, by instruction: D1, D2, D3.

## Decision records

### D1. Which copy of the layout is the source · open

**Question:** Three places describe the standard design/ layout today; which one do the other two read from?

Derek, in the ask: "Decide in the story which copy of the layout stays the source: the skill's templates, groot-claude-coord design-corpus/DESIGN.md (what conformance reads today), or backlog-scan's standard/optional lists."

**Options:**

1. **The skill's template files** — the standard tree and its READMEs live as files under `skills/design-setup/templates/`; `DESIGN.md` in groot-claude-coord keeps the reasoning and points here for the layout; `backlog-scan`'s two lists are checked against the templates directory by a test. Costs a rewrite of conformance and a canon edit in groot-claude-coord.
2. **groot-claude-coord `design-corpus/DESIGN.md`** — as today. Costs nothing now; the check cannot run on a machine without that repo, which is the Empathy and Very Fine Company case the skill was asked for.
3. **`backlog-scan`'s lists** — the code that judges directories is the source. It lives in `~/bin` (dotfiles), knows directory names only, and holds no file contents.

**Recommended:** option 1, because it is the only copy that travels with the skill to someone who is not Derek, and it is the copy that actually creates the files. Rejected: 2 because conformance already skips itself when groot-claude-coord is absent; 3 because a list of names cannot produce a README.

### D2. Absorb /groot-project's design-subtree phase · open

**Question:** Should the six design templates embedded in /groot-project's SKILL.md move into this skill's `templates/`, with /groot-project calling `/design-setup` for that phase?

Derek, in the ask: "It absorbs /groot-project's design-subtree phase (groot-project then calls it)". The retire paragraph for the notes, plans and helping-hands READMEs (from the lifecycle story) is written once, in the moved files.

**Options:**

1. **Move all six in one increment** — `design/README.md`, the stories README, `STORY_TEMPLATE.md`, and the helping-hands, notes and plans READMEs become files under `templates/standard/`; /groot-project's Phase 2 shrinks to a call; the misplaced-file migration stays in /groot-project. One reviewable diff of a 1,078-line skill.
2. **Move them one at a time as each is next edited** — smaller diffs; two sources of the layout for as long as it takes.

**Recommended:** option 1, as increment 2 and only after D1, because the templates are the layout and moving them piecemeal keeps the third copy this skill exists to remove. Rejected: 2 because the half-moved state is the drift Derek named.

### D3. The archive sweep and conformance move here · open

**Question:** Is the `z.archived/` sweep built in this skill, and does the conformance check become this skill's own instead of a call to /cleanup-design?

Derek's answer relayed 2026-11-11: design-setup "absorbs the design-directory lifecycle story's /groot-project and /cleanup-design changes, so those are not written twice."

**Options:**

1. **Both move here** — `/design-setup sweep` does the bulk move of `status: done` files into `<dir>/z.archived/`, the link repointing and the `archived/` rename; `check` reads the layout from D1's source; `/cleanup-design conformance` becomes a pointer to `/design-setup check` and /cleanup-design keeps the drift audit of what the documents say.
2. **Sweep here, conformance stays in /cleanup-design** — less to move; the layout check and the layout's owner stay in different skills.
3. **Both stay in /cleanup-design, called from here** — today's shape for `check`; the sweep would be written into a skill that then hands it over.

**Recommended:** option 1, as increment 3 after D1 and D2, because where a file belongs is a question about the directory and what a file says is a question about the corpus, and that is the line between the two skills. Rejected: 2 because `check` would still depend on groot-claude-coord; 3 because it writes the sweep twice.

### D4. The Do Research template names Derek · open

**Question:** The template was copied from Empathy unchanged, as instructed; should the skill's copy be made owner-neutral?

It is not fully project-neutral. It names Derek three times ("propose it to Derek", "Summary. For Derek", "raises it with Derek"), carries Empathy's stamp (`Authored by Claude Fable 5.2 with Derek · Last updated 2026-11-10 16:15`), and its examples are Empathy's (`[[pod-concepts]]`, "DESIGN.md § Pods", "how a WEGO game works"). Nothing in it names Empathy or a path. It passes this repo's PII check.

**Options:**

1. **Neutralise the skill's copy** — "Derek" becomes "the project's owner", the stamp is dropped from the template; examples stay, they read as examples. Empathy's file then differs from the template until it is re-copied.
2. **Leave it** — byte-identical to Empathy's; a Pod set up by someone else gets a file telling sessions to propose research to Derek.

**Recommended:** option 1, because the skill's stated audience is someone who is not Derek. Rejected: 2 because the first non-Derek use would need a hand edit the skill says not to make on the way in.

### D5. Shape of a template · decided 2026-11-11

**Question:** How does a template live in the skill's directory?

**Options:**

1. **A directory of plain files** — `templates/<name>/about.txt`, `files/` (copied as is), `readme-tree-line.txt`, `readme-trust-line.txt`; a Python 3.9 script beside SKILL.md places them and finds them from its own resolved path.
2. **Prose steps in SKILL.md** — no script; the model copies and edits by hand each time, and the dry run tests the session, not the skill.

**Recommended:** option 1, because idempotence and "never overwrite" are properties a script can be tested for.

**Decided 2026-11-11:** option 1, by default (Claude, as builder; reversible).

### D6. Wording of the two README lines · decided 2026-11-11

**Question:** Empathy's lines carry two things that are Empathy's: "(trial, 2026-11-10)" and "it informs the four above". What does the template say?

**Options:**

1. **Position-neutral** — drop the trial note; "it informs the entries above it and never overrides them", so the line is true wherever the list puts it.
2. **Empathy's wording exactly** — wrong in any README whose list is not Empathy's.

**Recommended:** option 1, because the item is inserted after `plans/` in whatever list the project has.

**Decided 2026-11-11:** option 1, by default (Claude, as builder; reversible: the lines are two one-line files).

## The ask, as captured

Related (found at triage): `groot-project-conformance-sweep.md` (drafts, 2026-06-20 — the same 'check the project against the standard' idea); [design-directory-lifecycle-in-skills](design-directory-lifecycle-in-skills.md) and [notes-tracker](notes-tracker.md) both change what this skill would absorb.

Asked 2026-11-11 06:27 (via design/ASKS.md):

high — Build a design-setup skill (Derek, 2026-11-10, from grootPM): one skill that owns a project's design/ directory, both checking that it is clean and set up to the standard and spawning its structured subdirectories (e.g. 'design-setup research' creates design/research/ with the Do Research file). It absorbs /groot-project's design-subtree phase (groot-project then calls it) and /cleanup-design conformance, so it is the one place that knows the layout, not a third. Templates are files in the skill's directory, not text embedded in SKILL.md; the first optional template is Empathy's design/research/Do Research.md (project-neutral, copy as is) plus the two lines it needs in design/README.md. Derek's reason for a separate skill: making this general enough for Empathy and Very Fine Company, where someone who is not Derek sets up a Pod's design directory without the rest of /groot-project. Decide in the story which copy of the layout stays the source: the skill's templates, groot-claude-coord design-corpus/DESIGN.md (what conformance reads today), or backlog-scan's standard/optional lists (its optional list is empty today). The name design-setup is free as a command and a skill. Story-sized: a refactor of a 1,078-line skill, not an add.

## Captured addition (/pm, unreviewed)

2026-11-11 — Derek's answer, relayed 2026-11-11 from the grootPM session at his "go" (to the /pm triage question on ordering): design-setup goes first and absorbs the design-directory lifecycle story's /groot-project and /cleanup-design changes, so those are not written twice.

**What moves into design-setup** (from [design-directory-lifecycle-in-skills](design-directory-lifecycle-in-skills.md)):
- /cleanup-design's archive sweep: move files marked `status: done` into `<dir>/z.archived/` in bulk, repoint links in live files, per-item mark proposals only on computed signals (a plan whose story is in `done/`), rename an existing `archived/` to `z.archived/` and recognise both, drop the Orient note that plans fold into stories.
- /groot-project's notes, plans and helping-hands README templates gaining the retire paragraph (these become design-setup's template files).
