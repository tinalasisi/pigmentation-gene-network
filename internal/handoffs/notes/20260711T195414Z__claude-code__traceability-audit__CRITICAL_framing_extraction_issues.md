# NOTE — CRITICAL framing + extraction issues found in the coverage/resolution finding

**From:** Claude Code (main session), traceability audit. **Action needed:** PI + findings/resolution-engine Claudes.

Two new docs (this session, no findings files edited — merge-safe):
- `internal/handoffs/HANDOFF_CRITICAL_limitations_and_framing_issues.md` — exhaustive issues register (severity-tagged, with evidence + fixes).
- `internal/TRACEABILITY_coverage_and_resolution_logic.md` — deep-dive with verbatim quotes + reproduction commands.

**BLOCKING items (do not ship the decomposition as-is):**
1. Strata labels **"Mechanistic" / "Association-recoverable" are misleading** — layer 2 is the D'Arcy **OMIM Mendelian** table, not association/GWAS. Rename by source, not evidence type. (`DISCORDANCE_DECOMPOSITION_FINDING.md` 23-24, 37-38; `FINDINGS_darcy_coverage.md` 1,28-40.)
2. **"Dark matter" overclaims** — means "absent from two small curated lists," not "unexplained" (MFSD12 has a Science paper). Relativize the term.
3. **Backbone never expanded** — KEGG/Reactome/OmniPath-curated mechanism available but unused (OmniPath=validation only; Reactome=never). So 29/23/48% measures backbone smallness, not biology. Expand (curated only, STRING still barred) then re-derive, or stop reporting it as a finding.
4. **Extractions must be redone locus-first** — gene-first schema manufactured genes from segments/SNP-clusters/nulls (EMCN et al. = non-causal haplotype passengers with no rsID). `case_gene_coverage_master.csv` drops all locus columns.
5. **`pilot_rate.py` "59%/86%" conflates coverage (7 D'Arcy) + resolution (15 dark)** — honest rate is 6/15 (40%) / 12/15 (80%). Also fix the passenger overclaim (`FINDINGS_darcy_coverage.md` 50-53 contradicts its own line 98).

I did NOT edit any findings doc (they're being modified concurrently). The fixes above are yours to apply.
