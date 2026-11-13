# Do Research

A `[[Do Research]]` link in any document under `design/` is an instruction to the session reading it: do some research on the topic, or refer to research already done, which may or may not need refreshing. There are two ways to name the topic:

- `[[Do Research]]: do these concepts still hold up?` The words after the link on the same line are the topic.
- The link alone on its own line inside a section. The whole section is the topic.

This folder, `design/research/`, holds this file and the research files the instruction produces.

## What a session does when it meets one

Take the cheapest of these that honestly answers the topic.

- **No research needed.** The point is settled, already decided in this project, or a matter of taste no source will settle. Say which, in a line.
- **Lean on what is on file.** A research file in this folder covers the topic and is inside its `recheck_after` date. Cite it.
- **Refresh.** A file covers the topic and is past its date. Re-check the parts that move and update the file in place.
- **New research.** Nothing here covers it. Do the research, write the file in the shape below, then answer.

Three rules for the research itself:

- **When the topic is whether an idea holds up, try to disprove it.** Look for the strongest case against the idea and for what people who solved the same problem did instead. A search built to agree with the author proves nothing.
- **Match the effort to the cost of being wrong.** A naming question gets a few searches. A question the architecture rests on gets sources read in full. Say which depth was used.
- **A quick pass is the default.** When a topic wants a long round or several agents, propose it to the project's owner with a rough size before starting.

## How one is closed

Keep the link and the topic. Append the answer to the same line, so the next reader sees it was done and does not do it again:

- `[[Do Research]]: do these concepts still hold up? ✓ 2026-11-10 — holds up, with one change (a Pod is not a repo): [[pod-concepts]]`
- `[[Do Research]] ✓ 2026-11-10 — no research needed: decided in DESIGN.md § Pods`

A line with a ✓ is closed; a line without one is open. The date is the day it was done. The Obsidian backlinks pane on this file lists every call in the vault, open and closed.

When the answer is "this is wrong", the closing line says so plainly and the session raises it with the project's owner like any other finding. It does not rewrite his text to match.

## A research file

One file per question, in this folder, named for the topic (`llm-coordination-patterns.md`). No date in the name: the file is refreshed in place and git keeps the earlier version. Use a subfolder only when there are attachments or the topic needs several files; its `README.md` then carries the frontmatter and the summary.

Frontmatter:

```yaml
---
question: What is the best way to coordinate several LLM sessions?
researched: 2026-11-10
recheck_after: 2026-12-10
author: Claude Fable 5.2
---
```

`recheck_after` is a date, or `never`. Choose it by how fast the subject moves:

| The subject | `recheck_after` | Example |
| --- | --- | --- |
| Moves month to month | about a month out | how to coordinate a group of LLMs |
| Moves slowly | a year or more out | where to get financial data |
| Settled | `never` | how a WEGO game works |

The body, in this order:

1. **Summary.** For the project's owner, five lines at most: the answer, how sure it is, and what it means for this project. It reads without the rest.
2. **Findings.** Each claim tied to its source, with what was read kept apart from what was inferred.
3. **What would change this.** The events that would make it stale before its date: a release, a price change, a new entrant.
4. **Sources.** For each: the link, what it is, and the date it was read. A source that was read and rejected is listed with the reason.

On a refresh, update the file in place, move `researched` and `recheck_after`, and open Findings with one line on what changed since the last round.

## How far to trust a research file

Trust it up to its `recheck_after` date. Past that date it is still the best starting point, and its conclusions want re-checking before anything new leans on them. A passed date is not a to-do: nothing here is re-researched on a schedule, and the date matters only when a new call lands on the same topic.

Research informs decisions and never makes them. `DESIGN.md` and a decided story outrank anything in this folder.

## Adding this to another project

Copy this file to the project's `design/research/Do Research.md` and name the folder in its `design/README.md` (the directory list and the trust order) so the reader does not flag it. The filename is what makes the link resolve; keep it exact.
