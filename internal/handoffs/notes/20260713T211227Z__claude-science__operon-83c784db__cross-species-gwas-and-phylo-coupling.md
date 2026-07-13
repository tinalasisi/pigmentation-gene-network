# Cross-species GWAS + module-coupling tests on perorigin_v1 (OPERON, frame 83c784db)

**Date:** 20260713T211227Z
**Author:** claude-science / OPERON specialist / frame 83c784db
**Scope of this session's work:** phylogenetic comparative-genomics on the *existing* HPC output
(`results/perorigin_v1/`). No new HyPhy runs. All analysis is local (phytools/ape/nlme), seconds of
CPU. Everything below derives numbers by executed code from `branch_rates.csv` per the project
verification convention.

---

## What I did (4 analyses, all new)

### 1. fitPagel coupling test RE-RUN on the 96-gene data
The frozen `coevolution_test.qmd` ran fitPagel on the 78-gene panel. Re-ran on current
`perorigin_v1/branch_rates.csv` (96 genes; +17 pigmentation from pig_expansion, hormone unchanged).
Phenotype coding + trees are UNCHANGED (`dichromatism_coding.csv` 238 sp, same md5;
`species_coding.csv` 117).
- **Result HOLDS and strengthens:** independent model still AIC-preferred for both modules.
  Pigment dAIC +3.69→+5.92, p 0.37→0.72; hormone +5.71→+6.95, p 0.68→0.90.
- **DATA GOTCHA (important for anyone re-running):** the 17 new pigment genes carry `set = "?"`
  but `module = "pigmentation"`. The frozen qmd filters on `set`, so a naive re-run SILENTLY DROPS
  them. Use the `module` column (or fix `set`). File: `fitpagel_rerun_96gene.csv`.

### 2. Module-vs-module evolutionary concordance (the user's "are the two modules' *evolution*
related?" question — distinct from fitPagel's module-vs-trait)
Per-branch fraction of each module's tested genes under aBSREL selection; does pigment track hormone
across branches?
- Raw Spearman 0.50 is **inflated by per-branch power** (each module's selected-count ~0.6 with
  total genes tested).
- Survives power control AND two phylo controls: tree-structured permutation **p=0.0015**; PGLS
  Brownian pigment **β=0.42 SE 0.10 p=1e-4**; Moran's I on resid=0.044 p=0.005 (correction
  warranted). Modest but real "concordant lineage-level selective tempo."
- Files: `module_concordance_hardened.csv`, `fig_nb16_module_concordance.png`.
- **NOTE:** user judged this "didn't seem interesting" → it is NOT the NB16 content (see below), but
  the result stands and is saved.

### 3. Dichromat vs monochromat contrast, per module (phylo-corrected)
- **Module level (amount of selection): NULL** after proper phylo control. Pigment phylANOVA p=0.87,
  PGLS with ESTIMATED λ (λ=0.31) β=−0.01 p=0.43. Hormone p=0.88/0.92.
  **METHODS LESSON:** a fixed-Brownian PGLS (λ=1) manufactured a spurious dich effect (p=0.018);
  estimating λ or using phylANOVA killed it. Always estimate λ / cross-check.
- **Per gene:** 50 genes testable (≥3 tip selection events), tree-structured permutation + BH →
  **zero survive** (min p_BH=0.96). File: `per_gene_dich_contrast.csv`.

### 4. Cross-species GWAS (this is NB16 — `notebooks/16_cross_species_gwas.ipynb`)
Reframes the project question as GWAS: case/control = dichromatic/mono; per-gene "genotype" =
per-lineage log1p(ω) (winsorized at 99pct — raw max was ~6e15 blowup); **stratification control =
phylogenetic covariance with Pagel's λ estimated per gene** (the kinship-matrix analog). PGLS per
gene + degenerate-fit filter + BH + tree-structured permutation confirmation.
- **One gene survives correction: AKR1C4** (hormone module, steroid/androgen reductase). β=+0.019
  (dichromats carry elevated ω), PGLS p_BH=0.041, permutation p=5e-4. First single-gene hit to
  survive multiple testing in ANY dichromatism contrast in the project.
- Runners-up (raw p<0.05, not BH): GNRHR, GNA11 (both hormone), HRAS/MAPK3 (pigment). Top tilts
  hormonal but only AKR1C4 clears.
- **Treat as SUGGESTIVE, not established:** 1 hit / 80 genes / 24 cases. The binding constraint is
  the number of dichromatic lineages, not method.
- Files: `gwas_omega_pgls_clean.csv`, `gwas_omega_pgls.csv`, `fig_nb16_gwas_manhattan.png`.

---

## What I need from the cluster (see paste-message below / `cross_species_gwas_cluster.R`)

The association layer runs locally in seconds — **do NOT re-run HyPhy for this.** Two things the
cluster can add that the sandbox cannot:
1. **Canonical phyloglm.** `phylolm::phyloglm` (Ives–Garland phylogenetic logistic regression) is the
   textbook binary-outcome model. It will NOT load in the Claude Science sandbox (the R kernel
   refuses to `dyn.load` a compiled `.so` from any writable path; `r-phylolm` is not on conda). On
   the cluster's managed R library it installs and loads fine. The script runs BOTH PGLS and
   phyloglm and joins them — if they agree on AKR1C4, that's the confirmation for the writeup.
2. **Expanded / internal-branch data.** The script's `--branch_rates` flag defaults to perorigin_v1,
   so it auto-picks-up the 110-gene panel once MYO5A/LYST land. Internal-branch ω (I used tips only)
   ~doubles the data.

Script: `comparative-genomics/analysis/coevolution_test/cross_species_gwas_cluster.R`
(self-contained, flag-driven, writes `gwas_omega_results.csv` + `fig_gwas_manhattan.png`).

---

## Coordination / safety
- I touched ONLY files under `comparative-genomics/analysis/coevolution_test/` and
  `notebooks/16_cross_species_gwas.ipynb`. I did NOT touch CHANGELOG/TODO/project_dashboard,
  `dichromatism_synthesis/`, `interactive/`, or `scripts/` — those are other sessions' WIP.
- No restricted data (darcy/bajpai/hirisplex) referenced.
- The prior "NB16 = module concordance" notebook was retired from the tree (its content is superseded
  by the GWAS as NB16 per user decision); the concordance CSV+figure remain committed as analysis
  outputs.
