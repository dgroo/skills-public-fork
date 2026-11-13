---
author: user
priority: high
---

# Design-directory lifecycle: z.archived sweep, done markers, retire paragraphs

> **Captured via `/pm` — not yet pondered.** Verbatim capture below; no exploration or design thinking has happened. Run `/ponder design-directory-lifecycle-in-skills` to develop it. Don't implement from this stub.

Related (found at triage): grootPM `design/stories/ready/design-directory-lifecycle.md` (D3, D4, D7). Touches the same /cleanup-design and /groot-project surfaces as [design-directory](../done/design-directory-skill.md) and [notes-tracker](notes-tracker.md); sequence with them. Also `groot-project-conformance-sweep.md`.

Asked 2026-11-07 12:11 (via design/ASKS.md):

high, from grootPM (2026-11-07): the design-directory lifecycle is decided; see grootPM design/stories/ready/design-directory-lifecycle.md, D3, D4, D7. /cleanup-design: the archive bucket becomes the sweep (move files marked status: done into <dir>/z.archived/ in bulk, repoint links in live files, per-item mark proposals only on computed signals such as a plan whose story is in done/; when sweeping a project with an existing archived/ rename it to z.archived/; recognise both; drop the Orient note that plans fold into stories). /wrapup Phase 3 asks 'notes absorbed, plans whose story shipped this session?' and writes the marker (status: done, done: <date>, superseded_by: <path>, one-line Done banner under the H1). /pm's accuracy review covers notes as well as stories. /groot-project's notes, plans and helping-hands README templates gain the retire paragraph.

## Captured addition (/pm, unreviewed)

2026-11-11 — Derek's answer, relayed 2026-11-11 from the grootPM session at his "go" (to the /pm triage question on ordering): design-setup goes first and absorbs the design-directory lifecycle story's /groot-project and /cleanup-design changes, so those are not written twice.

**Moves to [design-directory](../done/design-directory-skill.md):** the /cleanup-design archive sweep (z.archived bulk move, link repointing, computed-signal mark proposals, archived/ → z.archived/ rename, dropping the Orient note) and the /groot-project README templates' retire paragraph.

**Built 2026-11-13** in `/design-directory` (`sweep`, and the retire paragraphs in its notes, plans and helping-hands README templates); see [design-directory](../done/design-directory-skill.md), increments 2 and 3.

**Stays here:** /wrapup Phase 3 asking "notes absorbed, plans whose story shipped this session?" and writing the done marker (`status: done`, `done: <date>`, `superseded_by: <path>`, one-line Done banner under the H1); /pm's accuracy review covering notes as well as stories. Sequenced after design-setup, which owns the layout the marker feeds.
