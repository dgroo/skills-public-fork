---
author: both
priority: high
---

# Ask-and-answer loop in /sup, /next, /helping-hands, /pm, /ponder, /wrapup

_Authored by Claude Opus 5.5 with Derek · Last updated 2026-11-13 12:30._

## Executive summary

**What:** Maps grootPM's decided ask-and-answer loop onto this repo's skills: a shared thread rule, `· taken` decisions, a walk over everything waiting on Derek, answered threads first.  
**Where it stands:** Pondered 2026-11-13; five two-way calls taken, one blocked on the reader in remote-coding-setup; nothing built.  
**Needs you:**

- **Look** D1: one shared `pm/threads.md` holds the scribe and `· taken` rules; skills point at it.
- **Look** D2: the walk is built now on what `backlog-scan` already reports.
- **Look** D3: a transcribed answer is signed `derek`, with a one-line "said in the terminal" note.
- **Look** D4: `--all` appends replies to other repos' VF threads, but routes decisions there via `ask --project`.
- **Look** D5: `/sup` and `/next` wait for remote-coding-setup's `answered` field; no interim scanner here.
- **Do** CLAUDE.md recap: let `Decision:` fire for every taken two-way door (your file; § Asks of others).

## Decisions (yours first; the analysis is below)

All five are two-way doors inside a design you already said go to, so under the policy this story implements (grootPM D4) they are taken on the recommendation, each with a Look: say if not.

- **D1 · taken 2026-11-13** — the rules live once, in a new `skills/pm/threads.md` beside `exec-summary.md`; each of the six skills gets one pointer line. [record](#d1-where-the-thread-rules-live--taken-2026-11-13)
- **D2 · taken 2026-11-13** — `/helping-hands` walks every open thread now, from what the reader already emits; it does not wait for the `answered` state. [record](#d2-build-the-walk-before-the-reader-change--taken-2026-11-13)
- **D3 · taken 2026-11-13** — a transcribed answer is a `## derek · <time>` entry whose first line says where he said it and who wrote it down. [record](#d3-how-a-transcribed-answer-is-signed--taken-2026-11-13)
- **D4 · taken 2026-11-13** — `--all` appends reply entries to other projects' VF threads directly; anything that edits another project's story (a `Decided` line) goes as an `ask --project`. [record](#d4-what---all-may-write-in-other-projects--taken-2026-11-13)
- **D5 · taken 2026-11-13** — answered-first in `/sup` and `/next` waits for the reader; no scanner of our own. [record](#d5-answered-first-before-the-reader-has-it--taken-2026-11-13)

## Decision records

### D1. Where the thread rules live · taken 2026-11-13

**Question:** The scribe rule and the `· taken` grammar apply in six skills; where is the one copy?

**Options:**

1. **A shared `skills/pm/threads.md`**, the way `pm/exec-summary.md` holds the summary grammar for three skills; each skill gets one line pointing at it. Costs one file and six pointers.
2. **The rule restated in each skill.** No indirection, six copies that drift; the copy problem the exec-summary file was created to end.
3. **A fleet rule in `~/.claude/rules/`** (dot-claude). Loads by path, but path rules fire on touching `design/` files, while an answer given in chat arrives before any design file is touched; and it moves the rule out of this repo.

**Recommended:** option 1, because it has a precedent that has held (exec-summary.md, three callers, one grammar since 2026-10-23). Rejected: 2 because six copies drift; 3 because it fires on the wrong trigger.

**Taken 2026-11-13:** option 1. Look: say if not.

### D2. Build the walk before the reader change · taken 2026-11-13

**Question:** Should the `/helping-hands` walk wait for remote-coding-setup's thread work, or start on what `backlog-scan` reports today?

**Options:**

1. **Build now on today's reader.** `backlog-scan` already reports, per project, the threads that are Derek's turn: `for_you.waiting` (open VF Comments threads whose last entry is not his), `waiting.marks` (open `derek(<source>)` marks), `waiting.helping_hands`, and each story's `· open` headings via its Needs-you check. That is the whole "asked" side, which is what a walk presents. Costs nothing on the rcs side.
2. **Wait for the fleet-side story** (`remote-coding-setup` `ask-and-answer-loop-fleet-side.md`, an unpondered stub), which will group marks into threads with `state` and `kind`. Cleaner input; no date.

**Recommended:** option 1, because the walk only needs the asked side, which exists, and grootPM wanted it tried on the phone early. Rejected: 2 because it blocks the one increment that needs no one else.

**Taken 2026-11-13:** option 1. Look: say if not.

### D3. How a transcribed answer is signed · taken 2026-11-13

**Question:** When Derek answers in the terminal or on the phone, the session writes his words into the VF thread. Whose name goes on the entry?

**Options:**

1. **`## derek · <time>`, first line `*(said in the terminal; written down by cc-<project>/claude/<model>)*`**, then his words verbatim. The reader's `last_author` turns over to `derek`, so the thread leaves his waiting list, which is the loop working; the provenance line keeps it honest.
2. **Signed by the session** (`## cc-skills/claude/opus-5.5`) quoting him. Truthful about the writer, but the reader then still shows the thread as Derek's turn, and the loop never closes.
3. **A suffix after the time** (`· via cc-skills`). Breaks the VF grammar, which allows only `resolved` or `reopened` there.

**Recommended:** option 1, because the entry is his words and the reader keys on the author. Rejected: 2 because the thread stays on his list; 3 because it breaks the plugin's grammar.

**Taken 2026-11-13:** option 1. Look: say if not.

### D4. What `--all` may write in other projects · taken 2026-11-13

**Question:** A host-wide walk takes answers about other repos. Does it write into them?

**Options:**

1. **Replies yes, story edits no.** A VF thread reply is an append to a file only the thread uses, the write grootPM accepted for the board (its D2 amendment); the design-sync watcher commits it. A decision answered from the walk, which means appending a `Decided` line and flipping a heading in that project's story, goes as `ask --project <name>` with his words, and that project's session records it.
2. **Everything direct.** Fastest, but edits stories in working trees where a session may be live: the collision the worktree gate exists for.
3. **Nothing direct; every answer via `ask --project`.** Safest, but a reply then waits for that project's next session to copy it into the thread, so the asker sees no answer meanwhile.

**Recommended:** option 1, because it writes only the append-only form and leaves story content to the owner (the federation default). Rejected: 2 for live-tree collisions; 3 because it delays the cheap case for no gain.

**Taken 2026-11-13:** option 1. Look: say if not.

### D5. Answered-first before the reader has it · taken 2026-11-13

**Question:** `/sup` and `/next` should show answered threads above the ASKS queue. The reader does not emit `answered` yet. Do the skills scan for it themselves meanwhile?

**Options:**

1. **Wait; write the skill text against a named field** (`for_you.answered`: open threads whose last entry is Derek's), and ask remote-coding-setup for that field, an inverse of the `waiting` filter it already has. Costs a few lines there.
2. **An interim scanner in `/sup`.** Works today, but a second parser of the VF format beside the reader, which is the drift the reader exists to prevent.

**Recommended:** option 1, because the reader is the fleet's one parser and the field is small. Rejected: 2 because it forks the parser.

**Taken 2026-11-13:** option 1. Look: say if not.

## The frame

grootPM decided the loop on 2026-11-03 (`design/stories/ready/ask-and-answer-loop.md`, D1–D5; D6 bounded). This repo owns two of its increments: **2, surfacing and the scribe rule**, and **4, the walk**, plus D4's amendment that taken decisions are told to Derek in the session and listed by `/wrapup`. The design is settled; this story is the build plan for the skill side and the calls that the plan itself raises. Out of scope: the reader (`backlog-scan`, remote-coding-setup increment 1), the marks grammar (rcs increment 0), the dashboard (grootPM increment 3), the policy text in the contract (grootPM increment 5).

## What has changed since the ask (2026-11-07)

- **VF Comments threads exist** (fleet rule `~/.claude/rules/vf-comments.md`, plugin v0.3.0): a thread is a file under `design/vfcomments/` with `state:` and append-only `## author · time` entries. That is D2's "thread in place" in a concrete form, and the reader already parses it (`scan_comment_threads_waiting`).
- **`/ponder` no longer writes the count mark** at the Decisions heading; that sub-item of the ask is done.
- **The decision-record shape landed** (2026-11-11, `pm/exec-summary.md` § Decision records) with status words `open | decided`. `· taken` is the third; this story adds it there.
- **`boot-ritual.py` moved to dot-claude** (`~/.claude/hooks/`), so the SessionStart half of answered-first is not this repo's.

## Design

**`skills/pm/threads.md`** (D1), one page:

- *The scribe rule.* Whatever channel Derek answers on (the terminal, a `Next` token, `AskUserQuestion`, the phone over Remote Control), the session appends his words to the thread the answer belongs to (D3's signing), then acts, then records the outcome. Generalised from `/ponder` step 4.
- *Taking a two-way door.* A decision that is reversible in LLM time, inside work Derek said go to, and not on the one-way list (deletion or history rewrite; money or usage-billed APIs; privacy tier or anything leaving a repo; external-facing behaviour; a taste call he has flagged; a kind he has overridden before) is taken: the heading reads `· taken <date>`, the record ends `**Taken <date>:** option N. Look: say if not.`, and the same turn's recap names it in plain words. The list is grootPM D4's until the contract carries it (grootPM increment 5), then a pointer.
- *An override.* When Derek overrides a taken decision, append `**Decided <date>:** option M (Derek: "…") · overrode the taken option N`, and the next decision of that kind in that project is asked, not taken.

**`pm/exec-summary.md`**: add `taken <date>` to the heading status words and the `**Taken <date>:**` line to the record shape; a taken decision whose Look is unanswered gets a **Look** bullet in Needs you (the reader tolerates bullets beyond the `· open` count).

**`/ponder`**: step 1 already sorts one-way from two-way doors; step 4 writes two-way ones as taken and step 5's route lists them as Looks.

**`/helping-hands`** (D2, D4): a `walk` verb (`/helping-hands walk`, `walk --all`) over every thread that is Derek's turn, in grootPM D5's order: a Decide that a live `NEXT.md` thread names, then Decides, Dos, Looks; within a kind, oldest first by `git blame`. One thread at a time: a problem statement for someone with no context, the recommendation, then his answer written down by the scribe rule. The existing per-item flow (Orient, Validate, Extend, Present) runs unchanged for helping-hands files; Validate applies to every kind (an ask already answered elsewhere is closed, not presented).

**`/sup`, `/next`** (D5): render `for_you.answered` above the ASKS queue as "Derek answered N things since …", each a thread to act on; ranked by `next/backlog-ranking.md` as rule 0a, under the baton. Absent field: the line is omitted, no error.

**`/wrapup`**: Phase 3 lists the session's taken decisions (from the stories it edited, `· taken <today>`) in the verdict, one plain line each.

**`/pm`**: triage and the pass follow the scribe rule when an answer arrives through them; one pointer line.

**Blast radius.** One shared file serves six skills: a wrong rule there is wrong everywhere, which is also how it gets fixed everywhere; worth it, as with exec-summary.md. `--all` couples the walk to every project's reader output: one project's malformed thread file must skip that thread with a named warning, not end the walk.

## First-increment candidates (each waits for a go)

1. **The rules page**: `pm/threads.md`, the `taken` status in `exec-summary.md`, `/ponder` writing taken decisions, `/wrapup` listing them, pointer lines in `/pm`. Text only; no dependency. ≈ one session.
2. **The walk**: `/helping-hands walk` and `walk --all` on today's reader output. Then try it once from the phone over Remote Control, as grootPM asks.
3. **Answered-first** in `/sup` and `/next`, once remote-coding-setup ships `for_you.answered`.

## Asks of others

- **remote-coding-setup** (the reader): `for_you.answered` — open VF threads whose last entry is by `derek`, the inverse of the existing `waiting` filter; and later the grouped mark threads its fleet-side story plans. Its queue already holds the fleet-side story; this names the one field this repo needs first.
- **Derek** (global CLAUDE.md, recap footer): `Decision:` fires today for "a real fork taken before a long chunk of work". grootPM D4 wants every taken two-way door named in the turn's recap. Proposed wording: "`Decision:` — also fires for any two-way door the session took on the recommendation, one plain line each (`went with X; say if not`)." Your file, so not edited here.

## Non-goals

- The reader's parsing, the marks grammar, the dashboard and the policy text: other repos' increments.
- Backfilling old decision records with `taken`: none, as with the record shape.
- A notification push: the walk over Remote Control is the phone path.

## The ask, verbatim (2026-11-07 12:11, via `design/ASKS.md`)

high, from grootPM (2026-11-07): the ask-and-answer loop is decided; see grootPM design/stories/ready/ask-and-answer-loop.md, increments 2 and 4, and D4's amendment. /sup and /next rank answered threads above the ASKS queue; the scribe rule from /ponder step 4 (record Derek's answer inline, whatever channel it came on) generalises to /sup, /next, /helping-hands and /pm; /ponder stops writing the count mark at the Decisions heading and writes `· taken <date>` for two-way doors; /helping-hands extends its walk from helping-hands files to every open thread in the project, with --all; /wrapup lists the session's taken decisions and the turn recap names them in plain words. Thread state comes from the backlog-scan change asked of remote-coding-setup.
