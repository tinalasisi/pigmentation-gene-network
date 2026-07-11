# Inter-agent notes — one file per message

This directory is the shared, git-tracked channel through which agents on different platforms (Claude
Science sessions, Claude Code sessions) and different clones/branches leave messages for one another. Full
design rationale and the evaluated alternatives are in
[`internal/handoffs/MERGE_SAFETY.md`](../MERGE_SAFETY.md). Summary of the one rule that matters:

**Every message is its own file, written once, never edited.** Two agents writing "at the same time" always
produce two different files, so a merge never has to reconcile two writes to the same path. No merge driver
is configured for this directory — none is needed.

## Filename convention

```
{UTC_TIMESTAMP}__{platform}__{agent_tag}__{rand6}.md
```

- `UTC_TIMESTAMP` — `YYYYMMDDTHHMMSSZ`, compact ISO-8601, UTC, second resolution. Lexicographic filename
  sort = chronological order.
- `platform` — `claude-science` or `claude-code` (lowercase, hyphenated; add new platform tokens as needed).
- `agent_tag` — short filesystem-safe id for the writing agent/session. Claude Science: first 8 hex chars
  of the frame id, optionally prefixed with a role name (`pi-orchestrator-d80a52e7`). Claude Code: an
  operator-assigned session/task tag.
- `rand6` — 6 random lowercase hex characters, the collision backstop (see MERGE_SAFETY.md §3.3 for the
  probability analysis). A collision causes an immediate, local `git add`/checkout failure — never a silent
  conflict discovered later.

Example: `20260711T184532Z__claude-science__pi-orchestrator-d80a52e7__a1c9f2.md`

## Message format

YAML front matter, a blank line, then a free-text Markdown body:

```markdown
---
from: <platform>/<agent_tag>
to: <platform>/<agent_tag or "all">
date_utc: <ISO-8601 with colons, matching the filename timestamp>
platform: <claude-science | claude-code>
subject: <one-line subject>
---

<body>
```

Never edit a message after writing it. A correction or reply is a new file that names the original
filename in its body.

## Reading the channel

`ls internal/handoffs/notes/` (or `git log --name-only -- internal/handoffs/notes/`) sorts chronologically
by construction. There is no generated index file to keep in sync — if a rolled-up view becomes useful, it
should be a build artifact regenerated from these files, never a target that two agents write to directly.

See [`20260711T184532Z__claude-science__pi-orchestrator-d80a52e7__a1c9f2.md`](./20260711T184532Z__claude-science__pi-orchestrator-d80a52e7__a1c9f2.md)
for a worked example.
