# Helping hands

Tasks that need Derek's hands, eyes, account credentials, paid subscription, or physical access.

## Format

- One markdown file per item, date-prefixed: `YYYY-MM-DD-<slug>.md`
- YAML frontmatter: `status` (open/in-progress/done/dropped), `created`, `priority`, `estimated_time`
- Body structure, **in this exact order** — TL;DR and the concrete steps must be readable without scrolling past the title. Background context lives below the fold.
  1. `# <Friendly title>` — phrased as a request, not a directive.
  2. `**TL;DR:** <one sentence>` — the _why_, not the _what_. Like a code comment: explain the non-obvious reason this needs doing, and briefly why it needs the user's hands rather than something the LLM could close. The _what_ is enumerated in `## Do this`, just below — don't duplicate it here.
  3. `## Do this` — numbered concrete steps, paste-ready, one action per step. Second from top, never buried.
  4. `## Tell me when you're done` — what the user reports back (or what the LLM will detect) to unblock the next step.
  5. `---` separator.
  6. `## Background (optional reading)` containing:
     - `### Why this matters`
     - `### What I already did to make this easier`
     - `### Related`

  Snags, gotchas, future-state notes, and other detail are additional `###` sub-sections inside Background.

- The "what I already did" section is non-decorative — if it would be empty, the entry should not have been created. Do that work first instead.

## Surfacing in chat

Filed entries surface as a one-liner only: `Filed: <title> — see design/helping-hands/`. Not a paragraph. Not a recap. The artifact is the source of truth.

## Just-in-time, not session-start

When picking up work, check whether any open helping-hands item is referenced as a blocker by the current task, its parent story, or its plan. If so, name the specific blocker before pressing on. Do not auto-scan the directory at session start.
