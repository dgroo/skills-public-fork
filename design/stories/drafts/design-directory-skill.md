---
author: user
priority: high
---

# design-directory — one skill that owns a project's design/ directory

*Authored by Claude Fable 5.2 with Derek · Last updated 2026-11-13 10:20.*

## Executive summary

**What:** One skill, `/design-directory` (first built as `/design-setup`), that sets up, checks and cleans up a project's design/ and adds templated subdirectories to it.  
**Where it stands:** built through increment 2 of 3 (2026-11-13): setup, `research`, `check` and `cleanup` work; increment 3 (the sweep and a native check) is being built on Derek's go.  
**Needs you:** nothing.

## Decisions

- D1 · decided 2026-11-13 · the skill's template files are the source of the layout → [D1](#d1-which-copy-of-the-layout-is-the-source--decided-2026-11-13)
- D2 · decided 2026-11-13 · all six /groot-project design templates move here in one increment → [D2](#d2-absorb-groot-projects-design-subtree-phase--decided-2026-11-13)
- D3 · decided 2026-11-13 · the archive sweep is built here and conformance becomes this skill's own → [D3](#d3-the-archive-sweep-and-conformance-move-here--decided-2026-11-13)
- D4 · decided 2026-11-13 · the skill's Do Research copy says "the project's owner" and drops the stamp → [D4](#d4-the-do-research-template-names-derek--decided-2026-11-13)
- D5 · decided 2026-11-11 (by default) · a template is a directory of plain files and a Python script places it → [D5](#d5-shape-of-a-template--decided-2026-11-11)
- D6 · decided 2026-11-11 (by default) · the README trust line reads "the entries above it"; Empathy's "(trial, 2026-11-10)" is dropped → [D6](#d6-wording-of-the-two-readme-lines--decided-2026-11-11)
- D7 · decided 2026-11-13 · the skill is renamed `design-directory`, with no alias; bare does setup, `cleanup` opens /cleanup-design → [D7](#d7-the-name-and-the-verbs--decided-2026-11-13)
- D8 · decided 2026-11-13 (by default) · once the sweep exists, `cleanup` runs the sweep and then the /cleanup-design audit → [D8](#d8-what-cleanup-runs-once-the-sweep-exists--decided-2026-11-13)
- D9 · decided 2026-11-13 (by default) · the helping-hands README and the story template also name "the project's owner", not Derek → [D9](#d9-the-other-templates-that-name-derek--decided-2026-11-13)

## Increment 2 (2026-11-13): the standard tree lives here

- The six design templates and the `DESIGN.md` skeleton that were embedded in /groot-project's SKILL.md are files under `skills/design-directory/templates/standard/files/`, laid out as they land in `design/` (`ea9b193`). They are the embedded blocks unescaped; the one repair is the stories README's frontmatter fence, mangled in the embedded copy and correct in deployed projects. /groot-project's SKILL.md went from 1,089 lines to 811.
- `design-directory.py setup` creates what is missing and nothing else. It never overwrites; a `.gitkeep` goes only into a directory it creates; a project whose `stories/` has the older tier names gets nothing added under `stories/`; outside a git repository it refuses unless given `--project`. `standard` is not accepted as an optional template.
- Bare `/design-directory` runs setup. /groot-project Phase 2 runs the same script and keeps its misplaced-file migration.
- The notes, plans and helping-hands READMEs each gained the retire paragraph from the lifecycle story (`a0c460b`): mark done where it sits, a sweep moves marked files to `z.archived/` later, nothing unmarked moves.
- D4 applied to Do Research, and D9 to two more templates (`aea45c2`).

Verified by the script in scratch repos: an empty repo (ten pieces created, then `research` placed both README lines, `backlog-scan` reports four standard directories, `research` declared, nothing uncategorized); a copy of plumage's `design/` (nothing added); two older-layout repos; a non-git directory (refused, nothing written). A second run changed nothing in each. In a fresh Haiku session, bare `/design-directory` in an empty repo created the tree and filled the DESIGN.md title and one-liner from the README. Not run: /groot-project itself, whose other phases create a GitHub repo and write `~/.shrc`; its Phase 2 path to the script was checked to resolve from both the plugin link and the old per-skill link.

Still owed from D1, with increment 3: the edit to groot-claude-coord `design-corpus/DESIGN.md` pointing at these files, and the test that `backlog-scan`'s standard list matches them. Both wait until the check no longer reads that document.

## The rename (2026-11-13)

`skills/design-setup/` became `skills/design-directory/` (`b2b4315`), the script `design-directory.py`. `/design-directory cleanup [args]` invokes /cleanup-design and passes the arguments on. Bare `/design-directory` is still `check` until increment 2 gives it standard templates to set up from (by default, Claude as builder: a setup verb with nothing to set up would only report). Verified in a fresh Haiku session on Rocinante26 in a scratch repo: the picker lists it as `/vfs:design-directory (design-directory)`; typing bare `/design-directory help`, `research` and `cleanup help` each ran; a second `research` run by the script left `git status` empty. The names below this section that say `design-setup` are the record of increment 1 as it was built.

## What is built (increment 1, 2026-11-11)

Built at Derek's word on 2026-11-11 13:45 ("I was expecting to be able to use "design-setup" by now"), ahead of the ask-and-answer story at the top of the queue. The stub's "don't implement from this stub" line was lifted for this increment only.

- `skills/design-setup/SKILL.md`: routing for bare / `check` / `<template>` / `help`.
- `/design-setup research` runs `skills/design-setup/design-setup.py add research`: copies `templates/research/files/Do Research.md` to `design/research/` byte for byte, adds the `research/` line to the tree in `design/README.md` and the `research/` item to its trust order (after `plans/`, later items renumbered). An existing file or line is left alone and reported. A README with no tree or no trust order, or no README, gets the lines printed and nothing written; the skill never creates `design/README.md`.
- `/design-setup` and `/design-setup check` call `/cleanup-design conformance` and add which templates the project has. No layout is written in this skill.
- `/design-setup help` prints the verbs and the script's template list.

Verified in four scratch repos under `$TMPDIR`: a /groot-project-style README (both lines placed, `notes/` renumbered 5 → 6, `backlog-scan` then reports `research` as declared); this repo's README, which has a tree and no trust order (tree line placed, trust line printed); no README plus an existing, different `Do Research.md` (file kept, nothing written); Empathy's README (already names it, nothing changed). In all four a second run left `git status` empty.

Not in this increment, by instruction: D1, D2, D3.

## Decision records

### D1. Which copy of the layout is the source · decided 2026-11-13

**Question:** Three places describe the standard design/ layout today; which one do the other two read from?

Derek, in the ask: "Decide in the story which copy of the layout stays the source: the skill's templates, groot-claude-coord design-corpus/DESIGN.md (what conformance reads today), or backlog-scan's standard/optional lists."

**Options:**

1. **The skill's template files** — the standard tree and its READMEs live as files under `skills/design-setup/templates/`; `DESIGN.md` in groot-claude-coord keeps the reasoning and points here for the layout; `backlog-scan`'s two lists are checked against the templates directory by a test. Costs a rewrite of conformance and a canon edit in groot-claude-coord.
2. **groot-claude-coord `design-corpus/DESIGN.md`** — as today. Costs nothing now; the check cannot run on a machine without that repo, which is the Empathy and Very Fine Company case the skill was asked for.
3. **`backlog-scan`'s lists** — the code that judges directories is the source. It lives in `~/bin` (dotfiles), knows directory names only, and holds no file contents.

**Recommended:** option 1, because it is the only copy that travels with the skill to someone who is not Derek, and it is the copy that actually creates the files. Rejected: 2 because conformance already skips itself when groot-claude-coord is absent; 3 because a list of names cannot produce a README.

**Decided 2026-11-13:** option 1. Derek: "go on all four, with one note:  I am thinking it might be easier for me if we had a "/design-directory" skill instead of "/design-setup" that by default does setup, but also allows for "/design-directory cleanup" (calls cleanup-design, which I can never remember or find in the long list of design named skills), and "/design-directory research" which would create our research directory, etc."

### D2. Absorb /groot-project's design-subtree phase · decided 2026-11-13

**Question:** Should the six design templates embedded in /groot-project's SKILL.md move into this skill's `templates/`, with /groot-project calling `/design-setup` for that phase?

Derek, in the ask: "It absorbs /groot-project's design-subtree phase (groot-project then calls it)". The retire paragraph for the notes, plans and helping-hands READMEs (from the lifecycle story) is written once, in the moved files.

**Options:**

1. **Move all six in one increment** — `design/README.md`, the stories README, `STORY_TEMPLATE.md`, and the helping-hands, notes and plans READMEs become files under `templates/standard/`; /groot-project's Phase 2 shrinks to a call; the misplaced-file migration stays in /groot-project. One reviewable diff of a 1,078-line skill.
2. **Move them one at a time as each is next edited** — smaller diffs; two sources of the layout for as long as it takes.

**Recommended:** option 1, as increment 2 and only after D1, because the templates are the layout and moving them piecemeal keeps the third copy this skill exists to remove. Rejected: 2 because the half-moved state is the drift Derek named.

**Decided 2026-11-13:** option 1. Derek: "go on all four".

### D3. The archive sweep and conformance move here · decided 2026-11-13

**Question:** Is the `z.archived/` sweep built in this skill, and does the conformance check become this skill's own instead of a call to /cleanup-design?

Derek's answer relayed 2026-11-11: design-setup "absorbs the design-directory lifecycle story's /groot-project and /cleanup-design changes, so those are not written twice."

**Options:**

1. **Both move here** — `/design-setup sweep` does the bulk move of `status: done` files into `<dir>/z.archived/`, the link repointing and the `archived/` rename; `check` reads the layout from D1's source; `/cleanup-design conformance` becomes a pointer to `/design-setup check` and /cleanup-design keeps the drift audit of what the documents say.
2. **Sweep here, conformance stays in /cleanup-design** — less to move; the layout check and the layout's owner stay in different skills.
3. **Both stay in /cleanup-design, called from here** — today's shape for `check`; the sweep would be written into a skill that then hands it over.

**Recommended:** option 1, as increment 3 after D1 and D2, because where a file belongs is a question about the directory and what a file says is a question about the corpus, and that is the line between the two skills. Rejected: 2 because `check` would still depend on groot-claude-coord; 3 because it writes the sweep twice.

**Decided 2026-11-13:** option 1. Derek: "go on all four". What `cleanup` then runs is D8.

### D4. The Do Research template names Derek · decided 2026-11-13

**Question:** The template was copied from Empathy unchanged, as instructed; should the skill's copy be made owner-neutral?

It is not fully project-neutral. It names Derek three times ("propose it to Derek", "Summary. For Derek", "raises it with Derek"), carries Empathy's stamp (`Authored by Claude Fable 5.2 with Derek · Last updated 2026-11-10 16:15`), and its examples are Empathy's (`[[pod-concepts]]`, "DESIGN.md § Pods", "how a WEGO game works"). Nothing in it names Empathy or a path. It passes this repo's PII check.

**Options:**

1. **Neutralise the skill's copy** — "Derek" becomes "the project's owner", the stamp is dropped from the template; examples stay, they read as examples. Empathy's file then differs from the template until it is re-copied.
2. **Leave it** — byte-identical to Empathy's; a Pod set up by someone else gets a file telling sessions to propose research to Derek.

**Recommended:** option 1, because the skill's stated audience is someone who is not Derek. Rejected: 2 because the first non-Derek use would need a hand edit the skill says not to make on the way in.

**Decided 2026-11-13:** option 1. Derek: "go on all four".

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

### D7. The name and the verbs · decided 2026-11-13

**Question:** What is the skill called, and what do its bare form and `cleanup` do?

Derek, 2026-11-13 09:59: "go on all four, with one note:  I am thinking it might be easier for me if we had a "/design-directory" skill instead of "/design-setup" that by default does setup, but also allows for "/design-directory cleanup" (calls cleanup-design, which I can never remember or find in the long list of design named skills), and "/design-directory research" which would create our research directory, etc."

**Options:**

1. **Rename to `design-directory`, no alias** — bare sets up (adds what the standard has and the project lacks, never overwriting, and says what is off); `check` stays the read-only form; `cleanup` opens /cleanup-design; `research` and later templates are verbs of the same shape.
2. **Keep `design-setup` and add `design-directory` beside it** — a second design-named entry in the list, which is the complaint.

**Recommended:** option 1, because his reason is finding it in "the long list of design named skills".

**Decided 2026-11-13:** option 1. The name is Derek's; the reading of the verbs (a rename and not a second skill, bare as setup, `cleanup` as a door and not a copy, "etc." as further templates) is the grootPM session's, relayed with his words.

### D8. What `cleanup` runs once the sweep exists · decided 2026-11-13

**Question:** After D3 moves the archive sweep here, does `/design-directory cleanup` run the sweep as well as the /cleanup-design audit?

**Options:**

1. **Sweep, then audit** — `cleanup` first moves what is already marked done into `z.archived/` (computed, shown before it moves), then opens the /cleanup-design audit of what the documents say; `sweep` alone stays available.
2. **Audit only** — `cleanup` is exactly /cleanup-design; the sweep is a separate verb to remember.

**Recommended:** option 1, because Derek reaches for one word, "cleanup", and the sweep is the mechanical half of it. Rejected: 2 because it puts back a second thing to remember.

**Decided 2026-11-13:** option 1, by default (Claude, as builder; reversible: one routing line).

### D9. The other templates that name Derek · decided 2026-11-13

**Question:** D4 covered Do Research; the helping-hands README ("Tasks that need Derek's hands") and the story template (the `with Derek` stamp, `(Derek: "…")` in the decision comment) name him too. Same treatment?

**Options:**

1. **Neutralise them** — "the project owner's hands", `with <owner>`, `(<owner>: "…")`. Derek's own new projects get the placeholder, which a session fills with his name. The `derek(<source>)` mark syntax stays: tools match on it.
2. **Leave them** — a Pod set up by someone else gets files naming Derek.

**Recommended:** option 1, for D4's reason: the skill's audience includes someone who is not Derek.

**Decided 2026-11-13:** option 1, by default (Claude, as builder; reversible: three lines in two files, `aea45c2`).

## The ask, as captured

Related (found at triage): `groot-project-conformance-sweep.md` (drafts, 2026-06-20 — the same 'check the project against the standard' idea); [design-directory-lifecycle-in-skills](design-directory-lifecycle-in-skills.md) and [notes-tracker](notes-tracker.md) both change what this skill would absorb.

Asked 2026-11-11 06:27 (via design/ASKS.md):

high — Build a design-setup skill (Derek, 2026-11-10, from grootPM): one skill that owns a project's design/ directory, both checking that it is clean and set up to the standard and spawning its structured subdirectories (e.g. 'design-setup research' creates design/research/ with the Do Research file). It absorbs /groot-project's design-subtree phase (groot-project then calls it) and /cleanup-design conformance, so it is the one place that knows the layout, not a third. Templates are files in the skill's directory, not text embedded in SKILL.md; the first optional template is Empathy's design/research/Do Research.md (project-neutral, copy as is) plus the two lines it needs in design/README.md. Derek's reason for a separate skill: making this general enough for Empathy and Very Fine Company, where someone who is not Derek sets up a Pod's design directory without the rest of /groot-project. Decide in the story which copy of the layout stays the source: the skill's templates, groot-claude-coord design-corpus/DESIGN.md (what conformance reads today), or backlog-scan's standard/optional lists (its optional list is empty today). The name design-setup is free as a command and a skill. Story-sized: a refactor of a 1,078-line skill, not an add.

## Captured addition (/pm, unreviewed)

2026-11-11 — Derek's answer, relayed 2026-11-11 from the grootPM session at his "go" (to the /pm triage question on ordering): design-setup goes first and absorbs the design-directory lifecycle story's /groot-project and /cleanup-design changes, so those are not written twice.

**What moves into design-setup** (from [design-directory-lifecycle-in-skills](design-directory-lifecycle-in-skills.md)):
- /cleanup-design's archive sweep: move files marked `status: done` into `<dir>/z.archived/` in bulk, repoint links in live files, per-item mark proposals only on computed signals (a plan whose story is in `done/`), rename an existing `archived/` to `z.archived/` and recognise both, drop the Orient note that plans fold into stories.
- /groot-project's notes, plans and helping-hands README templates gaining the retire paragraph (these become design-setup's template files).
