# Module-selection analysis

Frozen-data replicable analysis of **which module (pigmentation vs sex-hormone)
selection tilts toward along each independent origin of primate hair
dichromatism**, plus an Opie-analog test of dichromatism's trait dynamics.

## Reproduce
```
# analysis + tables (R, needs phytools/ape/tidyverse)
quarto render module_selection_analysis.qmd     # or: Rscript -e 'knitr::purl(...)' then source
# figures (Python, needs pandas/matplotlib)
python figures.py
```
All inputs are frozen in `data/` (HPC commit 4c07317 + own ASR + Leakey phenotype).
No network access required.

## Outputs
- `fig_module_balance.png` — diverging bar, 11 origins, −1 (all hormone) .. +1 (all pigmentation)
- `fig_per_lineage_genes.png` — gene × origin dot-matrix, RELAX-confirmed genes ringed
- `module_balance_results.csv` — the metric per origin
- `opie_analog_results.csv` — Opie 2012 method applied to dichromatism

## Key results
- **Module balance spans the full range.** Origins tilt all the way to hormone
  (Eulemur, Alouatta, Colobus guereza) and all the way to pigmentation (Pithecia).
  Trachypithecus (origin_7) is richest: 8 pigmentation + 18 hormone genes.
- **RELAX confirms the powered origins:** Trachypithecus 12 genes both modules,
  Nomascus POMC only, Eulemur none.
- **Opie-analog:** dichromatism is a labile derived state — gained rarely, lost
  ~9x faster (ARD preferred, dAIC~20). Mirror-image of Opie et al.'s finding that
  mating systems evolve *into* monogamy as an absorbing state. Same method
  family (Mk ASR + directional rate asymmetry), opposite dynamic. We do NOT use
  their mating-system data (unavailable); we replicate the method on our trait.

## Method notes / caveats
- Module balance uses aBSREL tip-branch selection (all origins) with RELAX
  overlay for the 3 powered origins (>=2 tips). Single-tip origins are aBSREL-only.
- Rate/ASR (analysis 3) uses the **224-tip Leakey phenotype tree**, not the
  genome-sampled 117 set, to avoid ascertainment bias inflating the gain rate.
- Opie et al. 2012 = Commun Integr Biol 5(5):458-461, doi:10.4161/cib.20821.
