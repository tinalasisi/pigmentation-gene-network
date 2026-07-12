---
from: claude-code/greatlakes-hpc
to: claude-science/mol-evo-specialist-0d1cda86
date_utc: 2026-07-12T21:29:34Z
platform: claude-code
subject: 117-species RELAX run — preliminary results (79/80 genes done, NCOR2 still running)
---

## Status

The full 117-species parallelized run is nearly complete. **79 of 80 genes have finished**;
only **NCOR2** (task 79) is still running (~45 min so far — it's a large gene with a big tree).
The `pgn-repo` report job will fire automatically once NCOR2 finishes.

**This note is so you can start QC/analysis on the 79 completed genes now rather than waiting.**
The final NCOR2 result will land in the same location shortly.

## Data locations (scratch)

All outputs are at: `/gpfs/accounts/tlasisi_root/tlasisi0/tlasisi/pgn_run117/`

- `relax/<gene>.RELAX.json` — 45 valid JSON results (43 parseable with test results; 2 empty/truncated)
- `qc/<gene>.csv` — per-gene QC for all 79 completed genes (1 header row + 1 data row each)
- `aln/<gene>.codon.aln.fa` — codon alignments

## QC summary (79 genes)

Combined from per-gene QC CSVs:

| Metric | Value |
|--------|-------|
| Genes with status=ok | 79/79 |
| Genes with relax_status=ok | 45 |
| Genes with relax_status=hyphy_failed | 34 |
| Median tips per gene | 95 |
| Median foreground tips | 20 |
| High-gap genes (>25% gaps) | ESR2 (35%), CYP11B1 (30%), CYP11B2 (29%), HERC2 (44%), SLC45A2 (27%), PAX3 (27%), ESR1 (26%) |

Note: many more genes have hyphy_failed in the 117-species run than the 9-gibbon run — likely
convergence issues with larger trees. Worth investigating whether these need longer iteration
limits or represent genuinely problematic alignments.

## Preliminary RELAX results (43 genes with valid K/p-values)

Top hits by p-value (sorted ascending):

```
gene        K        p_value    LRT      set
TYR         2.0692   <0.0001    32.278   pigmentation
SRD5A1      2.2689   <0.0001    31.055   hormone
ASIP        2.7619   <0.0001    29.839   pigmentation
HSD17B12    2.3463   <0.0001    29.411   hormone
FKBP5       0.6009   <0.0001    29.074   hormone (RELAXATION)
HSD17B2     1.5760   0.00096    10.913   hormone
KIT         2.0285   0.00113    10.600   pigmentation
TFAP2A      1.6136   0.00194    9.607    pigmentation
CYP7B1      1.2692   0.00273    8.983    hormone
SLC45A2     1.2958   0.00333    8.617    pigmentation
NCOA1       1.3048   0.00507    7.854    hormone
PMEL        2.2710   0.00817    6.995    pigmentation
KITLG       1.1809   0.01086    6.488    pigmentation
AKR1C4      0.6114   0.01406    6.031    hormone (RELAXATION)
HSD17B8     50.0000  0.03966    4.233    hormone (DEGENERATE K?)
NCOA3       0.8505   0.04305    4.094    hormone
LEF1        0.7995   0.04728    3.935    pigmentation
MC1R        0.4944   0.05145    3.794    pigmentation (borderline)
```

Observations for your QC pass:
- **Pigmentation genes are hitting hard this time**: TYR, ASIP, KIT, TFAP2A, SLC45A2, PMEL, KITLG, LEF1 all <0.05
- **HSD17B8 K=50** — likely degenerate (same K-boundary artifact you flagged in the 9-gibbon run)
- **FKBP5 and AKR1C4 show relaxation** (K<1) — selection relaxed in dichromatic lineages
- **MC1R p=0.051** — tantalizingly borderline; K=0.49 suggests relaxation if real
- 34 genes with hyphy_failed need investigation — are these salvageable with different settings?

## What's missing

- **NCOR2** — still computing, will complete soon
- **The report job** (`03_report_summary.py`) hasn't run yet — it produces the final combined CSV
  and summary. Will fire automatically after NCOR2.
- No BH correction applied above — that's for you to do across the final 45+ genes

## Action

This is a "get started early" handoff. The final complete results will land in
`comparative-genomics/results/` once the report job runs and commits. But 98.75% of the
data is ready now for your QC filtering pass.
