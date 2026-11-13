# Stories

Feature specifications. **Readiness** is encoded by directory; **authorship** lives in frontmatter.

## Directory structure

```
stories/
├── STORY_TEMPLATE.md # the format
├── drafts/ # explicitly partial / not-yet-ready (any author)
├── ready/ # implementation-ready (default landing zone)
└── done/ # archived after implementation
```

## Where does a new story go?

- **Default: `ready/`.** A new story should be written to a quality bar of "implementable as-is". If it isn't, it shouldn't exist yet — flesh it out before filing.
- **Exception: `drafts/`.** Use only when the story is explicitly partial — e.g., the user dropped a sentence and asked the LLM to expand it; or the LLM is blocked on input it can't get.
- **`done/`.** Move here when the feature ships.

LLM-authored stories in `ready/` are _still_ "review carefully" by convention — the author field tells the next reader what kind of review to expect (see below). `ready/` is not a stamp of correctness, just a quality threshold.

## Frontmatter

```yaml
---
author: claude # claude | user | both
priority: medium # high | medium | low
---
```

**No `status:` field** — the directory is the status. **No `created:` / `updated:` dates** — LLMs hallucinate dates, and absolute date is the wrong question anyway. What matters is _drift relative to the codebase_, which is computed from git mtime against recent code activity (see drift check below).

## How an LLM should pick up a story

In order:

1. **Drift check first.** Get the story's last commit time:
   ```bash
   git log -1 --format=%cI -- <story-file>
   ```
   Compare to recent code activity on the modules the story touches. If meaningful code changes have landed since the story's last update, treat the story as stale: re-read against current code state and surface gaps before implementing. Drift can happen in hours with active development, not just weeks.

2. **Authorship check (frontmatter `author`):**
   - `claude` → "Probably thorough but may not match current code state. Vet against the modules it touches; expect gaps the original author didn't see."
   - `user` → "Intention likely correct but spec likely incomplete. Fill in details and flag your assumptions before implementing."
   - `both` → already iterated; treat as ready, still apply drift check.

3. **Implement from `ready/`.** Do not implement from `drafts/` without first promoting the story to `ready/` (which may involve a conversation with the user).

## Epics

For bodies of work too large for one story but coherent enough not to fragment, use an epic file:

- Lives at `stories/<dir>/<slug>-epic.md` (suffix `-epic.md`).
- Has a `## Stories` section with a checklist of child story files.
- Each child story adds a top line: `**Epic:** [<slug>-epic.md](../<dir>/<slug>-epic.md)`.
- Epic is "done" when every child story is in `done/`.

No new tooling, no folder, no metadata schema. The `-epic.md` suffix and the cross-link are the entire convention.

## When to write a story

- A feature needs design work before coding
- Multiple implementation approaches to compare
- UI/UX decisions to capture
- Complex technical requirements

**Don't** write a story for: simple bug fixes, routine changes, one-liner features.

**Important:** the LLM should ASK before writing a brand-new story unless explicitly invited.
