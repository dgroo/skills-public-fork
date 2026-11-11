---
author: user
priority: high
---

# /brains — the brain-dump parse skill (implementation name /parse)

> **Captured via `/pm` — not yet pondered.** Verbatim capture below; no exploration or design thinking has happened. Run `/ponder brains-skill` to develop it. Don't implement from this stub.

Related (found at triage): grootPM `design/stories/ready/brain-dump-intake.md` (D1–D7 decided; D7 amended 2026-11-10 to the /brains name); [notes-tracker](notes-tracker.md) carries the NOTES.md half of the parse contract.

Asked 2026-11-07 13:46 (via design/ASKS.md):

/parse skill brief (from grootPM, Derek's go 2026-11-07). A checklist skill, no new machinery: /parse <path> runs the brain-dump parse contract decided in grootPM design/stories/drafts/brain-dump-intake.md D3 (read that story first; D1 to D7 are all decided). The seven steps: (1) a derek(cc): parsed <timestamp> comment at the top of the note saying where each section went; (2) every work item routed to the project that owns it via /story, /todo, /idea or ask --project; nothing implemented; (3) every question answered inline or filed (a research stub, or a decision in the owning story); (4) run-off sentences listed with guessed / asked / dropped; (5) the note marked an archive candidate as a '- [ ]' line in the project's index note (Derek ticks; the next pass moves it to notes/archived/ with a superseded_by line); (6) one reply of one screen with a reading-cost line per artifact and what to read first (D4: the parse is judged by the reading it creates); (7) nothing lost, nothing duplicated: captured additions to existing stories over new twins, and the index note updated. Triggers (D1): 'pm: parse <path>' typed into a session, or a 'derek: parse' mark at the top of a note found by the review pass. Re-parse (D5): read the delta since the parse commit from git history; marks are only for comments that must sit in the doc. Who (D2): grootPM for VFS notes; life items handed to Iris's fleet inbox once it exists. Two worked instances to test against: grootPM design/notes/archived/2026-11-07 Brain Dump on  not-BorgChart.md and design/notes/2026-10-24-D-brain-dump.md. Priority high.


Asked 2026-11-10 07:01 (via design/ASKS.md):

high, from grootPM (2026-11-10): amendment to two asks already in this Inbox, the /parse brief (2026-11-07 13:46) and the notes-tracker ask (2026-11-09 09:19): the user-facing skill name is /brains. Derek, 2026-11-10: "If not I very much would like it to be or at least a shorthand for it to be '/brains' because it makes me laugh." /parse is free as the implementation name or an alias. Nothing else in either brief changes. Recorded in grootPM design/stories/ready/brain-dump-intake.md D7 (decided 2026-11-07, amended 2026-11-10).
