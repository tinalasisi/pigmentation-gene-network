# INCIDENT: uncommitted WIP overwritten in shared working tree — 2026-07-13 ~16:18 UTC

## What happened
A compliance-gate sub-agent (spawned by the PI_ORCHESTRATOR session, frame 83c784db)
ran `git checkout d0b7cc2 -- .` during what was intended to be a read-only audit. That
command overwrote **every tracked path** in the shared working tree to match commit
`d0b7cc2`. At that moment two files had **uncommitted, unstaged** edits from the
concurrent session:

- `internal/TODO.md`
- `internal/project_dashboard.md`

Because those edits were never `git add`ed, no committed object was guaranteed for them.
They were reset to their `HEAD` (`ab529c5`) content. All OTHER files the command touched
(`DATA_SOURCES.md`, `module_selection/*`, `internal/CHANGELOG.md`) were restored to HEAD
and are clean.

## Recovery candidates (in this folder)
`git fsck` found dangling blobs that match these two files by title/shape. They are NOT in
any commit (genuinely orphaned), so they are the best available recovery:

- `TODO.md.recovered_candidate` — dangling blob dea19c37 (17,684 bytes). NOTE: this is
  SMALLER than the HEAD version (24,837 bytes), so it may be an EARLIER save, not the exact
  lost WIP. Diff it against your current `internal/TODO.md` before trusting it.
- `project_dashboard.md.recovered_candidate` — dangling blob 790cdfd7 (48,554 bytes). This is
  LARGER than the HEAD version (23,629 bytes). Diff before use.

**Do NOT blindly copy these over the live files.** Diff first
(`git diff --no-index internal/TODO.md internal/handoffs/notes/_incident_recovery_2026-07-13/TODO.md.recovered_candidate`),
take the lines you recognize as your lost WIP, and reconcile by hand. Editor autosave
(VS Code local history under `~/Library/Application Support/Code/User/History`) or a Time
Machine snapshot may hold a more exact copy.

## What the PI session did NOT do
- Did not auto-restore either file (ambiguous which version is the true WIP).
- Did not commit or push anything of the concurrent session's. The PI's own work went to a
  SEPARATE branch `pi-phylo-coevolution` (never to `main`), touching only its own 6 files.

## Cause + prevention
The compliance specialist should have used `git show <sha>:<path>` / `git diff <sha>` to
inspect commit contents (object reads, no tree mutation) rather than `git checkout <sha> -- .`.
This has been flagged to the PI and the user.
