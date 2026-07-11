---
from: claude-science/pi-orchestrator-d80a52e7
to: all
date_utc: 2026-07-11T17:00:41Z
platform: claude-science
subject: Two-level framing landed + Locus Resolver substrate ready for Claude Code
---

Status from the Claude Science session, so a parallel/Claude Code session can pick up without collision.

## Committed this session (now on origin/main @ ecaa9ea)
- **Two-level paper framing adopted** (dashboard locked decision 11): bidirectional discordance (D1 =
  genotype-present/phenotype-absent; D2 = phenotype-present/genotype-absent) is the headline; "dark-matter
  association" is the coverage/gap spine beneath it. README, dashboard, FINDINGS, RESEARCH_SYNTHESIS, TODO all
  rewritten to it. GWAS-Catalog expansion is HELD until after the MVP (PI decision).
- **Mislabeled-pointers hypothesis FALSIFIED** (do not re-run): 0 of 15 dark-matter genes resolve to an
  in-network gene. HERC2->OCA2 is the one positional-pointer case and it is a D'Arcy-RECOVERABLE gene, not
  dark matter.
- **Locus Resolver MVP substrate** ready for Claude Code to build:
  - `internal/handoffs/CLAUDE_CODE_HANDOFF.md` — the full build spec (read this first).
  - `data/processed/locus_nodes.csv` + `data/processed/locus_annotation_edges.csv` — PRE-DRAFTED, pass
    `scripts/validate_locus_tables.py`. Claude Code should VALIDATE, not rebuild.
  - `internal/handoffs/LOCUS_TABLES_PREDRAFT_NOTE.md` — genome-build warning (rs12913832=GRCh38,
    rs1800401=GRCh37) + the honesty caveat (rs12913832 not significant in the Kalinago cohort; the
    HERC2->OCA2 enhancer mechanism is the cited external finding, PMID:22234890 Visser 2012, not a Kalinago
    result).
  - MATERIAL RISK for the build: OCA2 has exactly ONE backbone edge (MITF->OCA2), so D1/D2 CANNOT be computed
    by graph traversal — take direction from the cited case classification and DISPLAY the subgraph as
    context. See CLAUDE_CODE_HANDOFF.md section 4.

## Left untouched (not mine)
- `internal/CHANGELOG.md` has an uncommitted edit (pigmentation-plan-sync checker rewrite +
  PROJECT_MANAGER staleness-duty section) — that is the parallel session's work; Claude Science did not touch
  it.

## Coordination
Claude Science stays read-only on git per PI instruction (PI drives local commits). Deterministic build +
`quarto render` + browser test = Claude Code (the sandbox cannot render quarto or execute notebooks). Return
contract in `internal/handoffs/CLAUDE_SCIENCE_RETAINED.md`.
