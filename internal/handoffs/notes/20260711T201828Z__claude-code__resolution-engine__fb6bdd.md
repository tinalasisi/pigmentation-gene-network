---
from: claude-code/resolution-engine
to: claude-science/pi-orchestrator-d80a52e7
date_utc: 2026-07-11T20:18:28Z
platform: claude-code
subject: Full locus-first re-extraction started; prior gene-first numbers marked provisional
---

PI authorized the FULL locus-first re-extraction (root-cause fix for audit B1). The prior gene-first case set
(31 "genes", "15 dark") and this session's derived rates (59%/86%, 28/31) are PROVISIONAL — see the
2026-07-11 CORRECTION changelog entry and the two audit docs
(`HANDOFF_CRITICAL_limitations_and_framing_issues.md`, `TRACEABILITY_coverage_and_resolution_logic.md`).

Now running: 13-agent re-extraction workflow over the trusted `EXTRACT_*.csv` + local full-text, producing a
LOCUS-first table with per-paper verdicts + verbatim evidence quotes, then a cross-paper audit. Claude Code
merges to `data/processed/discordance_loci.csv`. Then: backbone expansion (KEGG hsa04916 + Reactome, curated
only), locus-first resolution (OpenTargets L2G + eQTL + LD), relabel by source, separate coverage/resolution
axes, reproducible notebook.

About to touch (writes): `data/processed/discordance_loci.csv` (new), `scripts/reextract_loci.py` (new), a new
reproducible notebook. NOT touching `data/processed/gene_network_*.csv` without PI sign-off — KEGG/Reactome
expansion is staged as a PROPOSAL first (locked decision 5; backbone stays mechanism-only; predicted/STRING
edges barred).
