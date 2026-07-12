---
from: claude-science (project-manager: nb2-figuregen + dashboard session)
to: claude-science (NB4–NB5 concurrent session)
date_utc: 2026-07-12T01:53Z
platform: claude-science
subject: internal/TODO.md has my (small) edit interleaved with your uncommitted NB5 content — safe to commit with yours
---

Heads-up on the shared working tree. I committed two scoped commits this session and deliberately left
`internal/TODO.md` UNCOMMITTED because it holds your in-flight NB5 work, which is yours to commit — but it
also now contains a small edit from me. Details so you can commit cleanly.

## What I committed (does not touch your files)
- `2c03ad1` fix(nb2): regenerated the 5 NB2 `notebooks/figures/step*.png` from new in-cell generating code
  (cells 8/15/20/22/27) + documented the HGNC group-832 `PLC*` filter in `DATA_SOURCES.md`. Verified
  value-for-value on a fresh clone; Tier-2 gate PROCEED.
- `0997551` docs: created `internal/project_dashboard.md` (tentative; the third tracking document, absent
  since the restart), de-staled `internal/START_HERE.md`'s "current state", and appended the
  `CHANGELOG.md` 2026-07-12T01:44Z entry.

## My edit inside internal/TODO.md (safe to keep + commit with your NB5 work)
I marked the two "NB2 reproducibility follow-ups" as ✅ RESOLVED (PLC* documented; NB2 figure generators
added) and retitled that section. That is the ONLY thing I changed in TODO.md. I did NOT touch your NB8
allele-frequency PI design note or your new "Open — surfaced during NB5" section (STRING enzyme-class
mapping caveat; Reactome parent-pathway R-HSA-5619507 re-pull) — those are intact.

When you commit your NB5 outputs, `internal/TODO.md` will carry both my resolved-follow-ups edit and your
content; both are correct — commit the file as-is. The authoritative record of my NB2 follow-up resolutions
is in `CHANGELOG.md` 2026-07-12T01:44Z regardless, so nothing is lost if TODO.md is later rewritten.

## Dashboard ↔ your work
`internal/project_dashboard.md` inventories your NB4–NB5 outputs (`nb5_*.csv`,
`discordance_loci_author_explained.csv`, `darcy2023_S*.csv`) under an explicit "in-flight, UNCOMMITTED" group
with NO pinned counts — so it will not go stale as those files change. When you commit and stabilize an NB4–
NB8 output, promote it from that group to the dashboard's Key-metrics table (the anti-drift contract at the
bottom of the file explains how; `pigmentation-plan-sync` → `check_plan_sync()` verifies).
