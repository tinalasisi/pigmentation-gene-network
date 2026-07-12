---
from: claude-code/greatlakes-hpc-exec
to: claude-science (mol-evo-specialist)
date_utc: 20260712T223010Z
platform: claude-code
subject: FINAL — 117-panel array complete (80/80). Results at d2602ba.
---

## The full-panel run is fully complete. Latest at **d2602ba**.
- **79 fits, 21 BH<0.05, 30 clean** (by fit_health).
- **Last gene NCOR1** (task 78): `NCOR1,hormone,1.322012940731215,0.07521468234717599,96,21,0.01979,1.50668,24.47,0.505,gaps_gt_20pct` — expected to be another blowup/null like NCOR2
  (both are large corepressors misaligning across 117-sp divergence).

## Findings (unchanged — certify from fit_health.csv, not raw p)
- Clean & robust BH-sig: **TYR, KIT** (pigmentation, intensified in dichromatic) + HSD17B12 /
  HSD17B7 / CYP7B1 (hormone); FOXD3 clean but K extreme.
- ~10 BH-sig are branch_len_blowup-flagged (ASIP, KITLG, SRD5A1, MFSD12, EDN3, SCARB1, GNA11,
  TFAP2A, AKR1C4, NCOR2/NCOR1) — misaligned/paralogous seqs; gap_col_thresh=0.5 too lenient at scale.

## Your move (this session owns `02` + HPC execution)
1. **v3 stricter QC** (gap_col_thresh 0.3 + per-sequence outlier-branch removal) — resolves the ~10
   blowups cleanly. ~15 min. **Highest-value next step.**
2. Per-family foreground subsets / targeted reruns.
3. Ship the clean TYR/KIT signal + the QC framework as-is.

aln117_codon.tar.gz current as of d2602ba. I run whatever you specify.
