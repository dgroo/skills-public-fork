---
name: cleanup-design
description: Audit a project's design docs for stale content and drift from recent decisions. Use after decisions land.
when_to_use: 'Use for "clean up design", "what is stale", "should anything move to done", "audit the design docs", "any drift between recent decisions and docs", "post-decision sweep". For the layout of design/ itself ("does this match our standard layout", "conform this project"), and for moving finished files to z.archived/, use /design-directory.'
summary: "Audits what a project's design docs say for stale content and drift; design-directory owns the layout."
group: design
---

# cleanup-design

Audits and refreshes a project's design corpus — `stories/`, `helping-hands/`, `notes/`, and canonical design docs (`DESIGN.md` or similar). Catches drift that accumulates when decisions are made in one place but the docs elsewhere haven't been updated yet.

## What this is, and what it is not

This skill audits what the documents **say**: a decision made in one place that the docs elsewhere have not caught up with, a dead reference, a story whose summary went stale. Run it with bare `/cleanup-design`.

Where files **belong** is `/design-directory`'s: the standard layout, the check against it, and the sweep that moves finished files into `z.archived/`. `/cleanup-design conformance` is kept as a way in to that check (see [Conformance](#conformance)).

## When to use vs. skip

Use for: "clean up design", "audit design docs", "what's stale", "should anything move to done", "any drift since [date]", "post-decision sweep".

Skip if: the project has no `design/` or equivalent corpus, or the user wants a single targeted edit (use Edit directly).

## Phases

### 1. Orient

Discover the project's design layout. Typical:

- **Stories** at `design/stories/` with sub-categories: `drafts/`, `ready/`, `done/` (newer convention) or `llm_generated/`, `user_updated/`, `z.done/` (older).
- **Helping-hands** at `design/helping-hands/` (its README usually carries the project's conventions for status/closing).
- **Notes** at `design/notes/`, **plans** at `design/plans/`.
- **Set-aside directories**: any `z.archived/`, `archived/` or `deprecated/` inside those. Finished files live there; note that they exist and do not open them.
- **Canonical docs**: `design/DESIGN.md`, `design/README.md`, `design/NEXT.md` if present.
- **Project README** + **CLAUDE.md** for conventions.

If the project uses a different layout (`docs/architecture/`, `docs/specs/`, etc.), adapt accordingly. If unclear, ask via `AskUserQuestion` rather than guess.

**Layout glance.** Run `python3 ${CLAUDE_SKILL_DIR}/../design-directory/design-directory.py check` (read-only) and, if it reports anything, relay its report as one finding with the pointer "`/design-directory` handles these". Do not act on layout findings in this audit, and do not diff the layout by hand.

### 2. Scan

Run focused checks per artifact category.

**Stories** (`ready/` + `drafts/`):

- Read frontmatter (`status`, `priority`, `author`).
- Check cross-references in the body: do `../stories/...`, `../../notes/...`, `../helping-hands/...` paths resolve to live files?
- Check whether referenced files have moved to `deprecated/`.
- For acceptance criteria: surface only obvious satisfactions (a checkbox names a file/function that grep-able-exists in the codebase). Don't be aggressive.
- For Open Questions: check whether recently-closed helping-hands or recent commits answer them.
- Executive summary: `backlog-scan --json` carries each story's `summary_status`; `missing` or `stale` on a `drafts/` or `ready/` story is a finding (its `summary_issues` say why). An unpondered stub (a bold marker line ending `— not yet pondered.**`, however its first half is worded) is exempt: it has no block until it is pondered.

**Helping-hands**:

- Read frontmatter (`status`).
- If `status: done` and a Decision section exists, fine.
- If `status: open` but a Decision section or "resolved" mention exists elsewhere, flag.
- Closed items stay in place until `/design-directory sweep` moves them; do not move them here.

**Notes**:

- Dead-link check: find `notes/<foo>` paths in any live artifact that no longer resolve, including ones whose target now sits in a set-aside directory (the sweep repoints links when it moves a file; one it missed is a finding).
- A live note that a later document has plainly absorbed or answered, with no done marker: a `mark-done` finding, on strong signal only. The marker is described in the project's `notes/README.md`.

**Canonical design docs** (DESIGN.md or equivalent):

- Section-level dead-link check (path references that no longer resolve).
- **Drift detection** — the strong one: for each helping-hand marked `status: done` in the last N days (default N=14), grep the canonical doc for references to the _pre-decision_ state. Surface mismatches.
- Open Questions section: cross-reference against recent helping-hands marked done.

**Resume pointers** (`NEXT.md` or similar):

- "Next concrete action" — does it still reference content that's been updated?

### 3. Triage

Group findings into buckets with suggested dispositions:

- **`update-section`** — prose update needed in a specific file/section
- **`move-to-done`** — story whose acceptance criteria appear satisfied (only on strong signal)
- **`mark-resolved`** — helping-hand has decision elsewhere but status still open
- **`update-reference`** — cross-reference path is stale (file moved/deprecated)
- **`mark-done`** — a note or plan that is finished but carries no done marker. Propose the marker (`status: done`, `done:`, `superseded_by:`, the banner line); never move the file. Files already marked are not findings here: `/design-directory sweep` moves them
- **`refresh-summary`** — the story's `## Executive summary` block is missing or stale; the pass in `${CLAUDE_SKILL_DIR}/../pm/exec-summary.md` § The pass rewrites it
- **`leave`** — flagged but no action; mention only if explicitly listed

### 4. Present

Show the staged list grouped by bucket. For each item: file path, line number (if applicable), short description, suggested action.

- **0 findings** → report "design corpus is clean."
- **1–5 findings** → present each individually with a proposed change preview; `AskUserQuestion` per item or bulk-approve.
- **6+ findings** → present grouped by bucket; `AskUserQuestion` for bucket-level approval first, then walk per-item only for buckets the user opts to review.

### 5. Execute

On approval:

- Edit prose changes.
- Run the Executive-summary pass (`${CLAUDE_SKILL_DIR}/../pm/exec-summary.md` § The pass: a fresh Sonnet reader per story, spawned together; read back; `backlog-scan` confirms `ok`) on each approved `refresh-summary` story and on any live story another bucket edited — last, so the block is each story's final write.
- Move files (with `git mv` if in a git repo; otherwise Write+verify+delete).
- Update frontmatter (status changes, done markers).
- Strip dead references or update to new paths.

Never auto-act on items the user hasn't approved.

## Discovery heuristic — drift detection (the strong one)

The most useful finding type is _drift_: a recently-made decision whose spec hasn't caught up. To detect:

1. Find helping-hands with `status: done` and recent `resolved:` date (or recent mtime if no `resolved:` field).
2. Find the artifacts those helping-hands `Related:` link to (or are reciprocally linked from). Also include the canonical design doc (sections it touches) and any active story (likely in `ready/`).
3. Check those artifacts: do they still describe the pre-decision state?
4. Surface mismatches with the specific helping-hand cited as the evidence.

This is what catches "we made decision X in a helping-hand but DESIGN.md still says ~X."

## Conformance

`/cleanup-design conformance` runs the layout check that `/design-directory check` runs, and nothing else:

```bash
python3 ${CLAUDE_SKILL_DIR}/../design-directory/design-directory.py check
```

Print its report as is and stop. The standard it checks against is that skill's template files, which work on any machine. Its report separates what setup would add and what the sweep would move from the **deliberate** class (a meta-file at the repo root, the older story tiers, an undeclared directory): each of those works as it is, so report it, say why it works today, and let the owner choose. Do not manufacture conformance churn, and do not apply a deliberate change as part of an audit.

## Common mistakes

- **Aggressive auto-archive.** Moving a story to `done/` because acceptance criteria _look_ met. Always confirm with the user.
- **Treating drafts as drift candidates.** `drafts/` are inherently unsettled; don't propose archiving or moving them without strong signal.
- **Over-scanning a clean corpus.** Re-running on a clean corpus should report "clean" quickly, not produce noise.
- **Conflating recency with importance.** A 90-day-old story may still be live; don't propose archiving by date alone.
- **Reading set-aside files.** Anything under `z.archived/`, `archived/` or `deprecated/` is finished work kept for reference. Surface that such files exist but do not load their contents without being asked.
- **Moving files to tidy up.** This audit proposes edits and markers. Moving finished files is `/design-directory sweep`, and it moves only what is already marked.

## Quick reference

| Bucket           | Action                           | Strict approval?       |
| ---------------- | -------------------------------- | ---------------------- |
| update-section   | Edit prose                       | yes (per item)         |
| move-to-done     | Move story                       | yes (per item)         |
| mark-resolved    | Update status + decision section | yes (per item or bulk) |
| update-reference | Edit stale path                  | bulk-approve ok        |
| refresh-summary  | Rewrite the block via the pass   | bulk-approve ok        |
| mark-done        | Write the done marker; no move   | yes (per item)         |
| leave            | nothing                          | n/a                    |

## Help

When invoked as `/cleanup-design help`, print the following block verbatim:

```
cleanup-design — Audit and refresh a project's design corpus for drift.

Usage: /cleanup-design [conformance]

  (default)     Drift audit: walks stories/, helping-hands/, notes/, plans/ and
                the canonical design docs, and catches drift between recently
                made decisions and the docs that should reflect them.
  conformance   Runs /design-directory's layout check and prints its report.
                The layout, and moving finished files to z.archived/, belong
                to /design-directory.

Drift-audit phases (run in sequence):
  Orient            Discover project's design layout.
  Scan              Per-artifact checks: stories, helping-hands, notes,
                    canonical docs, resume pointers. Drift detection is
                    the strongest finding type.
  Triage            Group by bucket: update-section, move-to-done,
                    mark-resolved, update-reference, refresh-summary
                    (a missing or stale Executive summary), mark-done, leave.
  Present           Show staged list; per-item or bulk approval.
  Execute           Edit / mv / update frontmatter on approval only.

Layout conventions (auto-detected):
  design/stories/{drafts,ready,done}/           Newer (groot-project)
  design/stories/{llm_generated,user_updated,z.done}/  Older
  design/helping-hands/, design/notes/, design/DESIGN.md

For drafting walkthroughs from a user perspective, see /walkthrough.

See SKILL.md for full reference.
```

## Related

- `design-directory` — owns the layout of `design/`: setup, the check against the standard, and the sweep to `z.archived/`. `/design-directory cleanup` runs its sweep and then this audit.
- `walkthrough` — sister skill for narrative production + iteration toward design integration; this one is for design-corpus maintenance.
