# `internal/handoffs/` — canonical home for platform-to-platform handoffs

This folder is the single place a Claude Science session and a Claude Code session (or any two
sessions on different platforms/clones) exchange the documents and messages that let one pick up
work the other started. It holds two distinct kinds of artifact — keep them distinct:

- **Handoff documents** — one file per handoff event, committed once, read-only after that (see
  below).
- **The agent-to-agent notes channel** — `internal/handoffs/notes/`, a higher-frequency,
  merge-safe message stream. Already built by the `REPRODUCIBILITY_SPECIALIST`; **do not
  recreate it**. See [`MERGE_SAFETY.md`](./MERGE_SAFETY.md) for the design and
  [`notes/README.md`](./notes/README.md) for the naming/format convention agents follow when
  writing a note there.

## What a handoff document is

A handoff document is a **self-contained brief** written by one platform for the other at a
specific transition point in the work — e.g. "here is the buildable, deterministic part of the
task, finish it and hand it back" (Claude Science → Claude Code), or "here is what stays on this
platform and the exact return contract" (the retained-capabilities counterpart). It is prose, not
a message: long enough to let a fresh session on the receiving platform orient and start working
from the repo checkout alone, without back-and-forth.

This is different from a note in `notes/` — a note is a short, high-frequency, operational ping
("I'm about to touch file X", "here's my frame id", a status question). A handoff document is the
occasional, substantial artifact that note traffic coordinates around.

## When to write one

Write a new handoff document when a track of work is about to cross from one platform to another
and the receiving session needs more context than a note can carry economically — a build spec,
a list of what was tried and why, a return contract, an enumeration of what only the other
platform can do. Do not use a handoff document for routine coordination; that belongs in
`notes/`.

Handoff documents are not edited after being handed off — the same never-rewrite discipline as
the notes channel, for the same reason (two sessions cannot conflict-safely co-edit one file). If
a handoff needs a correction or an update, write a new handoff document (or a note referencing
the original) rather than modifying the original in place.

## Naming convention

```
HANDOFF_<FROM-PLATFORM>_TO_<TO-PLATFORM>_<topic>.md
```

- `<FROM-PLATFORM>` / `<TO-PLATFORM>` — `CLAUDE_SCIENCE` or `CLAUDE_CODE` (extend as new platforms
  join the project; keep tokens uppercase with underscores, matching this repo's existing
  filename convention).
- `<topic>` — a short, lowercase-or-mixed, underscore-separated slug identifying the track (e.g.
  `locus_resolver_mvp`).

Example: `HANDOFF_CLAUDE_SCIENCE_TO_CLAUDE_CODE_locus_resolver_mvp.md`.

The two documents currently in this folder predate this naming convention (they were written
before this folder existed) and are kept under their original names rather than renamed, to avoid
breaking the cross-reference embedded in `CLAUDE_SCIENCE_RETAINED.md`'s own prose (it names
`CLAUDE_CODE_HANDOFF.md` directly):

- [`CLAUDE_CODE_HANDOFF.md`](./CLAUDE_CODE_HANDOFF.md) — the Locus Resolver MVP build brief handed
  from Claude Science to Claude Code.
- [`CLAUDE_SCIENCE_RETAINED.md`](./CLAUDE_SCIENCE_RETAINED.md) — the capabilities-retained-on-Claude-Science
  document and return contract for that same handoff.

New handoff documents should follow the `HANDOFF_<from>_TO_<to>_<topic>.md` convention above.

## Layout

```
internal/handoffs/
├── README.md                    # this file
├── MERGE_SAFETY.md               # design + rationale for the notes/ merge mechanism
├── CLAUDE_CODE_HANDOFF.md        # pre-convention handoff doc, kept under its original name
├── CLAUDE_SCIENCE_RETAINED.md    # pre-convention handoff doc, kept under its original name
└── notes/                        # agent-to-agent notes channel (one file per message)
    ├── README.md
    └── {UTC_TIMESTAMP}__{platform}__{agent_tag}__{rand6}.md
```

## Relationship to the rest of `internal/`

`internal/handoffs/` follows the same tracked/public convention as the rest of `internal/` (see
the `pigmentation-governance-layout` skill and `internal/START_HERE.md`) — everything here is
committed to the public repo except through the existing `internal/untracked/` and
`internal/archive/` escape hatches, which this folder does not use. It sits alongside, and does
not replace, the three core governance documents (`CHANGELOG.md`, `TODO.md`,
`project_dashboard.md`), which track project-wide decision history, open work, and current state
respectively — a handoff document is scoped to one platform transition, not the whole project.
