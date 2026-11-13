# Design

Design artifacts for this project. The structure separates **living/authoritative** docs from **snapshots and notes** so future sessions know which to trust.

## What's here

```
design/
├── README.md # this file
├── DESIGN.md # ← canonical, living. Source of truth for project design.
├── stories/ # ← living. Feature specs, trust-tiered.
├── plans/ # ← living. Dated implementation plans.
├── helping-hands/ # ← living. Open asks for actions only the user can take.
└── notes/ # ← informal, may be stale. Snapshots, vision braindumps, external reference.
```

## Trust hierarchy

When in doubt, trust this order:

1. **`DESIGN.md`** — canonical project design. If something here disagrees with anything else in this directory, this wins.
2. **`stories/ready/`** — feature specs at implementation-ready quality. Apply drift + authorship checks (see `stories/README.md`) before treating as a spec.
3. **`stories/drafts/`** — explicitly partial stories. Reference only; do not implement from.
4. **`plans/`** — implementation plans, dated. Trust the latest dated plan for any given concern.
5. **`notes/`** — exploratory thinking and external reference. **Do not assume any note is current.**

Authorship of any individual story lives in its frontmatter, not its directory.

## Helping-hands

`helping-hands/` is a parallel track: tasks needing the user's hands, eyes, account credentials, or physical access. Surfaced just-in-time when a story or plan cites one. See `helping-hands/README.md`.
