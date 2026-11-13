# Plans

Dated implementation plans. One file per plan: `YYYY-MM-DD-<slug>.md`.

A plan is a concrete blueprint for a piece of work: scope, steps, decision points, fallbacks. Distinct from stories (which are _what and why_) and notes (which are exploratory).

The most recent dated plan for any given concern is the one to trust.

## When a plan is done

A plan is done when the story it implements is in `../stories/done/`. The session that moves the story marks the plan where it sits: `status: done`, `done: <date>` and `superseded_by: <the done story>` in the frontmatter, and one line under the H1, `> **Done <date> (<who>):** <what shipped and where the record is>`.

A marked plan stays here until a cleanup sweep moves it into `z.archived/`, which is read only when asked. Nothing unmarked is ever moved.
