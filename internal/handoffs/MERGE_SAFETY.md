# Merge-safe inter-agent messaging — design and rationale

**Scope.** This document specifies how multiple AI agents — Claude Science sessions and Claude Code
sessions, on separate clones/branches, possibly writing concurrently — append notes to each other in a
shared, git-tracked channel without merge conflicts. It also settles a related question: whether
`internal/CHANGELOG.md` (the human-facing build history) can and should use the same mechanism.

**Direct answer to the operating question.** *"Since it'll be git-tracked, it should be possible to merge
the changelog without conflicts when agents are simultaneously writing messages to each other, right?"* —
Not if "the changelog" means one shared file that every agent appends text to. Two independent appends to
the *same file* are two edits to the same region of one blob; if both branches touch the file since their
common ancestor, git's default 3-way merge treats it as a conflicting hunk unless the added lines happen to
land in a way git can auto-resolve (rare once entries have multi-line bodies), and even the `merge=union`
attribute — which does address exactly this case — has real failure modes detailed below. The agent-to-agent
notes channel therefore does NOT use a shared append-only file. It uses one file per message. That pattern
cannot conflict, structurally, regardless of write concurrency. `merge=union` is recommended separately, as
a defensive backstop on the human `CHANGELOG.md`, not as the mechanism for the notes channel itself.

---

## 1. The three realistic options

### (a) Single append-only log + `.gitattributes` `merge=union`

One file (e.g. `NOTES.md`) that every agent appends entries to. `<path> merge=union` is a git built-in
low-level merge driver (no custom driver setup needed — it is recognized directly by the attribute
machinery). On a 3-way merge, instead of emitting conflict markers when both sides touched the file, union
merge **takes the union of added lines from both sides** and inserts them into the result.

**When it actually avoids a conflict:** only when the two sides' edits are both pure *insertions* relative
to the merge base — i.e. both agents only appended new lines and neither modified or deleted a line the
other side also touched. If either side edits or removes an existing line (fixing a typo in an earlier
entry, re-numbering, reformatting), union merge falls back to normal 3-way behavior on that hunk and *can
still conflict*.

**What union merge does NOT guarantee, even in the pure-append case:**
- **Chronological order.** Union merge's approach is line-level, not semantic; the documented behavior is
  that it takes each side's added lines and the result commonly places one side's whole block before or
  after the other's, or interleaves at hunk boundaries — not necessarily in wall-clock order across the two
  branches. A reader cannot assume the merged file reads top-to-bottom by time without a timestamp in every
  entry and a separate sort pass.
- **Deduplication.** If both branches independently added the *same* line (e.g. two agents wrote an
  identical boilerplate line, or one branch's commit is a squashed/rebased copy of lines already merged
  elsewhere), union merge does not detect or collapse the duplicate. It appears twice.
- **Structural conflicts.** If both sides edited the *same* existing line (not just appended after it) —
  e.g. both changed a header, a status field, or reflowed a shared paragraph — union merge does not apply to
  that hunk; you get a normal conflict there.
- **Multi-line entries interleaving.** If an "entry" spans several lines (front matter + body, as our
  message format requires), union merge operates per physical line, not per entry. Two multi-line entries
  added on both branches can interleave line-by-line at the hunk boundary, producing a corrupted document
  that concatenates cleanly as text but no longer parses as two intact entries. This is the decisive failure
  mode against using union merge for anything richer than single-line log rows.

**Verdict:** appropriate for a strictly single-line-per-entry log where entries are never edited after the
fact. Not appropriate for multi-line, structured messages (front matter + body) — which is what an
inter-agent note requires (from/to/date/platform/subject, then free-text body).

### (b) One-file-per-message ("maildir" pattern)

Each message is its own file, written once, never edited, named so that concurrent writers can never pick
the same filename (timestamp + agent identity + random suffix — see §3). Two agents writing "at the same
time" produce two different files in the same directory.

**Why this is conflict-free by construction, not by policy:** git's merge algorithm operates on the tree of
paths that changed between two branches relative to their common ancestor. A file that exists on branch A
but not on the merge base, and a *different* file that exists on branch B but not on the merge base, are two
independent additions at two independent paths. Git does not diff "the directory" as a unit — it has no
opinion about two unrelated new files landing in the same folder, so there is no hunk for the merge algorithm
to disagree about. This holds regardless of how many agents write concurrently, regardless of message
length or structure, and requires no merge driver, no `.gitattributes` entry, and no post-hoc conflict
resolution. It is the only one of the three options where "no conflict" is a mathematical property of the
git merge model rather than a property of the merge driver's heuristics.

**Tradeoffs (real, but not conflict-related):**
- **Ordering** is not filesystem order; it must be read from the filename (hence the sortable timestamp
  prefix, §3) or the `date_utc` front-matter field. `ls` / `git log --name-only` on the directory naturally
  sorts by the timestamp prefix if the naming convention is followed.
- **Dedup** is a non-issue — each message is inherently unique by construction (a given agent cannot write
  the same filename twice; see collision analysis in §3).
- **Readability** is lower than one continuous log for a human skimming history in one scroll — reading the
  full conversation means opening N small files (or `cat`-ing them in sorted order) rather than one document.
  Mitigated by keeping a `README.md` in the directory and, if useful later, a generated rolled-up index (a
  build artifact, not something agents write to directly — never route two agents' writes through a
  generated file).
- **Volume.** A very high message rate produces many small files. Not a concern at expected inter-agent
  handoff volumes (per-session, not per-line), and directories with thousands of files are routine in git.

### (c) Per-agent append-only log files

One log file per agent identity (e.g. `notes_claude-science.md`, `notes_claude-code.md`), each agent only
ever appending to its own file. This removes the *same-file* concurrent-write problem within one agent's
log, because a single agent's own sessions are typically sequential relative to its own file — but it does
not remove it in general: nothing stops two concurrent Claude Science sessions (e.g. two parallel frames)
from both being "the Claude Science agent" and appending to the same per-platform file at the same time,
which reintroduces exactly option (a)'s failure modes, just partitioned by platform instead of eliminated.
It also fragments a single conversation across files by sender rather than by message, which is worse for
following a thread than either (a) or (b) — a reply to a specific note requires cross-referencing between
files instead of reading one item. This option is not recommended; it dilutes the concurrency problem
without solving it, and is strictly worse than (b) for conversation readability.

---

## 2. Recommendation

**Use one-file-per-message (option b) for the agent-to-agent notes channel** at
`internal/handoffs/notes/`. It is the only option whose no-conflict property does not depend on git merge
heuristics, message content, or write timing. Concretely:

- Directory: `internal/handoffs/notes/` (tracked/public, per the project's `internal/` convention — see the
  `pigmentation-governance-layout` skill; this is not a private scratch space).
- Naming convention and message format: §3 below.
- No merge driver is configured for this directory, because none is needed — a merge driver only matters
  when two branches modify the *same path*, and by construction no two messages ever share a path.

**Apply `merge=union` to `internal/CHANGELOG.md` as a defensive backstop, not as a solution for concurrent
agent messaging.** The changelog is a different kind of document (§4) — human-curated prose, edited by
whichever agent is instructed to write it, at much lower frequency than agent-to-agent notes, and normally
appended to only once at a time. `merge=union` there reduces the odds that a routine "two branches each
added one dated entry at the tail" merge raises a spurious conflict, at the accepted cost that if it ever
does apply, entry order in the merged file is not guaranteed and must be fixed by a quick manual pass
(the entries are self-dated, so this is a five-minute cleanup, not data loss). It is not applied to the
notes channel because the notes channel already has the stronger, unconditional guarantee from option (b).

---

## 3. Concrete specification

### 3.1 `.gitattributes` entry (verbatim, as added to the repo root `.gitattributes`)

```
internal/CHANGELOG.md merge=union
```

See §4 for why this line targets `CHANGELOG.md` only and not the notes directory.

### 3.2 Directory layout

```
internal/handoffs/
├── MERGE_SAFETY.md      # this document
└── notes/
    ├── README.md        # naming + format convention (this spec, condensed for in-folder reference)
    └── {UTC_TIMESTAMP}__{platform}__{agent_tag}__{rand6}.md   # one file per message
```

### 3.3 Message filename convention

```
{UTC_TIMESTAMP}__{platform}__{agent_tag}__{rand6}.md
```

- **`UTC_TIMESTAMP`** — `YYYYMMDDTHHMMSSZ` (compact ISO-8601, UTC, second resolution, no colons — colons are
  invalid in Windows filenames and best avoided even on a Linux/macOS-only team). Using UTC and this format
  means lexicographic filename sort equals chronological order; this is the whole reason the directory does
  not need a separate index to read messages in time order.
- **`platform`** — `claude-science` or `claude-code` (extend as new platforms join; keep it a short,
  lowercase, hyphenated token).
- **`agent_tag`** — a short, filesystem-safe identifier for the writing agent/session (lowercase letters,
  digits, hyphens only). For a Claude Science session, use the first 8 hex characters of the frame id (e.g.
  `d80a52e7`) optionally prefixed with a role name (`pi-orchestrator-d80a52e7`); for Claude Code, use a
  short session/task tag the operator assigns (e.g. `locus-resolver-build`).
- **`rand6`** — 6 random lowercase hex characters (e.g. `uuid.uuid4().hex[:6]` in Python, `openssl rand -hex
  3` in shell). This is the collision backstop: even if two agents on the same platform somehow share the
  same `agent_tag` and write within the same UTC second (the only way `UTC_TIMESTAMP`+`platform`+`agent_tag`
  could collide), the probability both also draw the same 6 hex characters is 1/16^6 (≈1 in 16.8 million)
  per colliding pair — and if it ever did collide, git would simply refuse the second `git add`/checkout of
  a pre-existing filename, which is a loud, immediate, locally-caught error, not a silent merge conflict
  discovered later.

Example: `20260711T184532Z__claude-science__pi-orchestrator-d80a52e7__a1c9f2.md`

### 3.4 Message file format

YAML front matter, then a blank line, then a free-text Markdown body:

```markdown
---
from: <platform>/<agent_tag>
to: <platform>/<agent_tag or "all">
date_utc: <UTC_TIMESTAMP, same value as in the filename, ISO-8601 with colons for readability>
platform: <claude-science | claude-code>
subject: <one-line subject>
---

<body — free-text Markdown; may reference other repo paths using the standard internal/ relative-link
rules from the pigmentation-governance-layout skill>
```

Fields are deliberately minimal and are the same four pieces of metadata a mail header would carry
(sender, recipient, timestamp, subject), plus `platform` because this channel spans two different agent
runtimes and knowing which one wrote a note affects how a reader interprets it (e.g. "has repo write access
and a browser" vs. "sandboxed, no local git state"). Messages are **never edited after being written** —
a correction is a new message that references the original by filename, exactly as the deconvolutor
reports and changelog entries in this repo are never rewritten, only appended to.

---

## 4. Why `CHANGELOG.md` and the notes channel must stay separate

`internal/CHANGELOG.md` is **curated prose for humans** — the project's existing convention (see
`internal/CHANGELOG.md` header and the `pigmentation-governance-layout` skill) is a singular, dated,
append-only history of build/decision events, written in full sentences, meant to be read start-to-finish
by a person reconstructing project history. It is one of three governance documents that must not absorb
each other's content.

Agent-to-agent notes are a different kind of artifact: **operational message traffic** — handoff pings,
"I'm about to touch file X, don't collide," "here's the frame id if you need to pull my lineage," status
questions, coordination chatter. This traffic is higher-frequency, less curated, and not intended for a
human to read as prose history. Mixing the two would either:

- flood the human changelog with operational noise a reader has to skim past to find the actual decision
  history, or
- pressure agents to hand-curate every coordination message into changelog-quality prose before writing it,
  which defeats the purpose of a low-friction inter-agent channel.

Keeping them separate also lets each channel use the mechanism suited to it: `CHANGELOG.md` stays a single
human-readable file (low write frequency, `merge=union` as a backstop is acceptable because a rare ordering
glitch is a trivial manual fix); the notes channel uses one-file-per-message (higher write frequency,
multi-line structured entries, needs the unconditional conflict-freedom that only path-level separation
provides). A changelog entry may **reference** a note (`internal/handoffs/notes/<filename>.md`) if a
coordination exchange led to a real decision worth recording — that is the intended bridge between the two,
not merging their storage.
