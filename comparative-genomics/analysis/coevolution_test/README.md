# coevolution_test — correlated evolution of module selection & dichromatism

Frozen, replicable R notebook (`coevolution_test.qmd`) for the one Opie-analog
test not covered by the sibling `../module_selection/` notebook: the
**correlated-evolution** test (`phytools::fitPagel`, ML analog of Opie's
BayesTraits *Discrete* dependent-vs-independent test), plus Pagel's lambda for
the dichromatism trait.

## Result (summary)
- Pagel's lambda = 0.65 (LR p < 1e-6): dichromatism has strong phylogenetic signal.
- ARD transition rates: loss 9.1x gain (dAIC 19.79 vs equal-rates) — labile trait,
  lost more readily than gained. (Cross-check of the module_selection result.)
- **fitPagel: independent model AIC-preferred for BOTH modules** (pigmentation
  dAIC 3.7, LR p=0.37; hormone dAIC 5.7, LR p=0.68). No detectable lineage-level
  coupling between which module is under selection and dichromatism state. This
  reinforces the non-significant set-level contrast (p=0.87). Power-limited (21
  dichromatic tips), so this is "no detectable coupling," not "coupling excluded."

## Run
```
quarto render coevolution_test.qmd     # or run chunks in R
```
Needs R with `ape`, `phytools`, `tidyverse`. No network — reads only `./data/`.
Ends with a replay-equality assertion (`REPLAY OK`) proving the frozen values
reproduce.

## Frozen inputs (`data/`)
All copied verbatim from repo-tracked sources; see the provenance table in the
notebook. `branch_rates.csv` = `results/perorigin_v1/` (commit 4c07317);
`species_coding.csv`, `gene_modules.csv`, `primate_species_tree.nex` = copies of
`../module_selection/data/`; `leakey_pruned_tree.nex` +
`leakey_dichromatism_coding.csv` = the 235-tip Leakey phenotype tree and a
2-column extract (species_binom, hair_dichromatism_any) of
`Leakey2025/data/primate_prelim_complete.csv`.

## Relationship to other work
- `../module_selection/` — per-lineage module-balance metric + Opie
  ancestral-state/transition-rate analysis (concurrent session; numbers
  independently verified, see `internal/handoffs/notes/2026-07-13_independent_check_module_selection.md`).
- This notebook does not duplicate that; it adds the fitPagel test and lambda.
