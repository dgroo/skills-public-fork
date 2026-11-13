# Notes

Informal materials. **Not authoritative for project design** — see `../DESIGN.md` for that.

## Conventions

- **Snapshots**: prefix the filename with the date (e.g., `2026-05-07-name.md`). Treat as frozen-in-time.
- **Living vision drafts**: keep the original filename; location signals non-canonical status.
- **External reference**: keep the original filename; document the source at the top of the file.

If a piece of thinking here graduates into a real decision, capture it in `../DESIGN.md` or in a story under `../stories/`. If a note is contradicted by `DESIGN.md`, `DESIGN.md` wins.

## When a note is done

A note is done once what was made from it stands on its own: it was absorbed into a story or `../DESIGN.md`, answered, or replaced by a later note. The session that finishes it marks it where it sits, in the frontmatter and in one line under the H1:

```yaml
---
status: done
done: 2026-05-07
superseded_by: ../stories/ready/<slug>.md # where the content lives on; omit when nothing was carried forward
---
```

`> **Done 2026-05-07 (<who>):** <where everything went, in one sentence>`

A marked note stays here until a cleanup sweep moves it into `z.archived/`, which is read only when asked. Nothing unmarked is ever moved.
