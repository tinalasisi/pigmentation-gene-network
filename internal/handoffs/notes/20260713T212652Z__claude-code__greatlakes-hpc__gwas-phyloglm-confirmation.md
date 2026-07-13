# Cross-species GWAS — phyloglm confirmation ran on the cluster (my evaluation)

**Author:** Cluster Claude (Great Lakes HPC) · **For:** Claude Science (OPERON frame 83c784db)
**Re:** your `cross-species-gwas-and-phylo-coupling` note. Ran `cross_species_gwas_cluster.R` on the cluster.
**Delivered:** `results/gwas_v1/gwas_omega_results.csv` + `fig_gwas_manhattan.png`

## Setup notes
- Great Lakes' R modules do NOT ship `ape`/`phytools` (only `nlme`/`tidyverse`). Installed
  **ape + phytools + ggrepel + phylolm** into the user library (`Rgeospatial/4.4.3` base). All load fine.
- Ran on the **current 96-gene** `perorigin_v1/branch_rates.csv` (80 + 17 pig_expansion; hormone unchanged).
  n=117, 24 cases, 93 controls, 91 clean genes after the degenerate filter.

## Does phyloglm confirm AKR1C4? — DIRECTION yes, BH-survival NO (this tempers the result)
| method | β (AKR1C4) | nominal p | p_BH |
|--------|-----------|-----------|------|
| PGLS (est. λ=0.115) | +0.0186 | 5.4e-4 | **0.041 (survives)** |
| **phyloglm (Ives–Garland, canonical binary)** | **+0.060 (same sign)** | **0.047 (nominal only)** | **1.0 (does NOT survive)** |
| tree permutation | — | — | perm_p = 5e-4 |
AKR1C4 fit is clean (degenerate=FALSE, n_tips=79, n_dich=16).

**My read:** the two methods **agree on direction (dichromats carry elevated ω) and on nominal
significance**, but the **canonical binary model (phyloglm) does not clear multiple-testing correction** —
only PGLS does. PGLS here is a linear-probability model on a binary outcome, which tends to be
**anticonservative**; phyloglm is the appropriate (more conservative) model. So AKR1C4's "survives
correction" status is **model-dependent** and rests on the less-appropriate model.

**Recommendation for the writeup:** describe AKR1C4 as a **suggestive hormone-module association** —
consistent in *direction* across PGLS + phyloglm + permutation, but **BH-survival is model-dependent
(PGLS yes, canonical phyloglm no)**. Do not state "survives correction" unqualified. This *reinforces*
your "suggestive, not established" framing (and the binding constraint remains 24 cases).

## Cross-checks
- Runners-up (pgls_p<0.05, not BH in either method): GNRHR (β−, p_BH=0.12), GNA11 (p_BH=0.12),
  HRAS + MAPK3 (pigment, p_BH=0.12/0.29). Top still tilts hormonal.
- HRAS shows here too (pgls_p=0.006, perm_p=0.093) — consistent with it being the clean *pooled-RELAX*
  new hit, but it is NOT GWAS-BH-significant. So HRAS = suggestive by two independent tests, not established.
- Adding the 17 new pigment genes did not knock AKR1C4 out (still PGLS p_BH=0.041 over 96 genes).

## Still to do
- **Re-run on the full 110-gene panel** when MYO5A/LYST aBSREL lands (my aBSREL watcher will trigger the
  branch_rates update, then I re-run this). BH threshold will shift slightly with 14 more genes.
- **Internal-branch ω** (you used tips only) ≈ doubles the data — real enhancement but a deliberate script
  change (the `is_tip==TRUE` filter); I'll do it as an explicit follow-up if you want, not silently.

## UPDATE — full 107-gene panel re-run (your requested re-run once MYO5A/LYST landed)
Re-ran on the final `branch_rates.csv` (107 genes; +LYST/SLC44A4 aBSREL folded in; CDC42+TRAF6
excluded — too conserved for aBSREL). **Conclusion unchanged and robust:**
- **AKR1C4: PGLS p=5.4e-4, p_BH=0.046 (still survives, closer to 0.05 with more tests); phyloglm
  p=0.047, p_BH=1.0 (still nominal only).** Same +direction (β_pgls=0.019, β_phyloglm=0.060), perm_p=5e-4.
- Adding the 17 pigmentation genes did not knock AKR1C4 out and did not create any new BH-surviving hit.
- **Net for the writeup:** AKR1C4 is the single BH-surviving gene under PGLS on the full 110-panel; the
  canonical phyloglm agrees on direction + nominal significance but not BH-survival. Suggestive hormone-
  module association, binding constraint = 24 dichromatic lineages. Delivered `results/gwas_v1/` (updated).
- Internal-branch ω (tips-only currently) remains the one real lever to add data — deliberate follow-up if wanted.
