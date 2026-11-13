# Todo

<!-- Format: [status] P<priority> (category) Title -->
<!-- Status: [ ] open, [~] in progress, [x] done, [-] won't fix -->
<!-- Priority: P0 critical, P1 high, P2 medium, P3 low -->
<!-- Category: bug, feature, chore, docs -->

## Open

- [ ] **P3** (docs) Write the upstream-merge recipe under "Upstream provenance" in `CLAUDE.md` — 2026-10-01
  The first merge in three months (2026-10-01, `b3911fc`) was done by hand: rename any local skill whose name upstream now uses (ours, not theirs — `go-team` calls upstream's `consolidate` by path), `git merge upstream/main`, resolve `README.md` / `TODO.md` / `DIARY.md` to the fork, keep upstream's `CLAUDE.md` additions but drop its commit-policy hunk (`/consolidate` before push), `make install` and read it for `COLLISION` lines. Source: meta-feedback 2026-10-01.
- [x] **P3** (chore) Decide: stay a fork of joewalnes/skills, or restructure as a wrapper/overlay — 2026-06-09 · **decided 2026-10-01: stay a fork and merge** (Derek; merge `b3911fc` cost five conflicts, four of them repo docs). Unblocks the `upstream-*` → `fork-*` rename and the status-skill consolidation.
  Derek recalls an rcs-session conversation proposing converting this repo from a fork of Joe's into something that *wraps* it (pull upstream skills without fork history). The outcome was never recorded — searched all design docs, diaries, TODO/REVISIT surfaces, and CC transcripts (2026-06-09); no trace outside the session that re-raised it. Needs a fresh decision: fork (status quo: `upstream-check.sh`/`check-upstream-edits.sh` + `make upstream-*` targets manage drift) vs wrapper (e.g. upstream as a plugin-marketplace install or git submodule/subtree, personal skills as pure overlay — cf. the "third-party skills via plugin marketplace" precedent in rcs auto-memory). Blocks beginners-mind R17 (renaming `upstream-*` scripts to `fork-*` is wasted churn if the restructure happens).
  After a `/clear`, `sibling-sessions.py` reports the *predecessor* transcript as a hot parallel sibling: the clear writes an `away_summary` to the old jsonl, so it shows up as "active Ns ago" with a topic hint that matches the current arc (because it *is* the current arc). This led `/sup` to recommend "switch windows rather than restart here" when there was no real parallel session. Fix idea: suppress a sibling whose latest `away_summary` timestamp ≈ the current session's start time (the `/clear` fingerprint), or whose jsonl stopped being written right as the current one began. Confirmed live on Serenity26 in the Changer theme-prototype worktree.

## Done

- [x] **P3** (chore) Descriptions over 120 characters: move trigger phrases to `when_to_use:` so the `/` picker shows what each skill does — 2026-11-11 · **done 2026-11-13**: 31 own skills now have a one-sentence `description:` of 120 characters or fewer and their trigger phrases in `when_to_use:` (go-ahead: the grootPM session's reading of Derek's "check if 2 is still an issue, if so I'd say fix them").
  The picker shows about two terminal lines of `description:` and nothing of `when_to_use:` (probed 2026-11-11 on Claude Code 2.1.322; `/pm` was fixed this way). Most own skills still open with mechanics or triggers. Mechanical once the short description is written; the index `summary:` is a good first draft of each.
- [x] **P2** (bug) Ten skills have frontmatter that is not valid YAML; seven show no description in the model's skill listing — 2026-11-11 · **fixed 2026-11-13**: the failing `description:` and `argument-hint:` values are quoted in all ten (Derek, relayed by the grootPM session: "check if 2 is still an issue, if so I'd say fix them"). The six upstream-tracked ones are a commit of their own, one line each, offered upstream.
  Found while checking the index edits with a strict parser (`ruby -ryaml`); present before them. An unquoted `: ` inside `description:`, or an unquoted `[…] […]` `argument-hint:`. Own: `relay-setup` (argument-hint; listed with no description), `md-add`, `meta-feedback`, `groot-project` (these three still list a description). Upstream-tracked, so not editable here: `go-team`, `consolidate`, `retro`, `delegate-security-audit`, `delegate-bulk`, `scorecard` (all listed with no description) — report to Joe or carry in the fork decision. Fix for the own four is quoting the value; a strict-YAML check could join `make readme-check`.
- [x] **P1** (feature) Skills index in README § Skills + `/skills-list brief`, generated from a `summary:` field — 2026-11-10
  **Decided 2026-11-11 (Derek, relayed from grootPM):** each skill carries a one-line `summary:` and a `group:` field (its job) in its own frontmatter; README § Skills and `/skills-list … brief` are generated from them, not hand-written. Derek: "I tend to prefer colocating knowledge of the thing with the thing"; "part of updating (and creating, obviously) a skill is to make sure that line is always correct." Scope: (1) `summary:` + `group:` on every own skill; (2) a generator that rewrites README § Skills (groups in a fixed order listed in the generator; the five `~/.claude/commands` rows; one pointer line for gstack/plugins); (3) a `make readme-check` / pre-commit check that fails when a skill lacks `summary:` or `group:`, or the README section is out of date; (4) `/skill-add` writes both fields on creation, and CLAUDE.md § When adding a new skill plus the skill-editing guidance say to re-check `summary:` on every edit; (5) `brief` as a modifier on any `/skills-list` group. Acceptance: `/skills-list mine brief`.
  **Open sub-call:** 21 of the 55 skills are upstream-tracked (Joe's), and the upstream-edit hook blocks adding frontmatter to them. Default: their `summary:`/`group:` live in one sidecar file (`scripts/upstream-summaries.toml`) until the fork question (`design/stories/drafts/fork-or-follow-upstream.md`) is settled; the check covers both sources.
  Resolved 2026-11-11: `summary:` + `group:` on the 35 own skills, the 21 upstream-tracked skills and the five commands in `scripts/skills-index-sidecar.toml`; `scripts/skills-index.py` generates README § Skills (`make readme-index`) and the brief listing; `make readme-check` runs in the pre-commit hook for commits touching `skills/`, `README.md` or the index scripts; `/skill-add` and `/cmd-add` write the line. Commands are a group on the listing (`/skills-list commands`, and the last block of `/skills-list mine brief`), not a new `/commands` command. Sidecar named for what it now holds, not `upstream-summaries.toml`.

- [x] **P3** (chore) iterm-setup missing from README skills table — 2026-05-17
  Resolved: Added the iterm-setup row in alphabetical position. Also fixed a parallel drift in MAINTAINERS.md — 7 Derek-authored skills (cleanup-design, helping-hands, idea, integrate-comments, skill-add, subagent, sup) had been added since the last manifest sync. Single commit.

- [x] **P2** (bug) iterm-setup reads/writes `~/.zshrc` only — misses `~/.shrc` — 2026-05-16
  Resolved: Added `shell_config_files()` discovery and `primary_shell_config_file()` write-target helpers; refactored `aliases_targeting_cwd` to read combined text from all discovered files; renamed `add_alias_to_zshrc` → `add_alias_to_shell_config` with conflict-check across both files. Detection regex handles guarded source patterns (`[ -f ~/.shrc ] && source ~/.shrc`, `if [...]; then source X; fi`) and ignores commented-out lines. 16 new pytest cases in `test_shell_config.py`. Belt-and-suspenders: added a "Shell config layout" section to `~/.claude/CLAUDE.md` so LLM-driven tools route correctly without needing the same discovery code.

- [x] **P3** (chore) Standardize frontmatter fields across skills — 2026-03-31
  Resolved: Added `argument-hint` to all skills that accept arguments (bug-bash, project-setup, readme, scorecard, tool-web). Removed redundant `user_invocable: true` from tool-web. Documented frontmatter convention in CLAUDE.md: `name` and `description` required, `argument-hint` when args accepted, `allowed-tools` optional and enforced.


- [x] **P2** (bug) plugin.json has wrong repository URL — 2026-03-31
  Resolved: Changed `"repository"` from `joe/skills` to `joewalnes/skills` in `.claude-plugin/plugin.json`

- [x] **P2** (bug) Broken placeholder link in tool-web skill — 2026-03-31
  Resolved: Removed the "Onesies Integration" section entirely — it was project-specific boilerplate with a placeholder URL, not appropriate for a shared skill

- [x] **P3** (chore) Add .gitignore — 2026-03-31
  Resolved: Added `.gitignore` with standard exclusions (OS files, editor swap files, env files, logs)

- [x] **P1** (chore) Deduplicate /bug and /todo skills — 2026-03-31
  Resolved: Replaced 118-line copy-paste in `bug/SKILL.md` with thin wrapper delegating to `/todo`

- [x] **P1** (docs) README missing 6 of 8 skills — 2026-03-31
  Resolved: Added all 8 skills to README table in alphabetical order
