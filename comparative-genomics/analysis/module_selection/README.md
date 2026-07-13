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
All inputs are frozen in `data/` (HPC commit 4c07317 + own ASR + primate phenotype scoring).
No network access required.

## Outputs
- `fig_module_balance.png` — diverging bar, 11 origins, −1 (all hormone) .. +1 (all pigmentation)
- `fig_per_lineage_genes.png` — gene × origin dot-matrix, RELAX-confirmed genes ringed
- `fig_circular_tree_balance.png` — circular (fan) primate tree, tips colored by module
  balance and sized by number of selected genes; dichromatic species in red
- `fig_phylo_heatmap.png` — species tree + gene×species selection matrix (phytools
  `phylo.heatmap`), hormone-gene block | pigmentation-gene block
- `module_balance_results.csv` — the metric per origin
- `opie_analog_results.csv` — Opie 2012 method applied to dichromatism

Regenerate figures:
```
python figures.py         # fig_module_balance.png, fig_per_lineage_genes.png
Rscript tree_figures.R    # fig_circular_tree_balance.png, fig_phylo_heatmap.png
```

## Key results
- **Module balance spans the full range.** One origin sits at each pole —
  Eulemur (origin_14) is pure hormone (0P/1H, balance −1.0) and Pithecia
  (origin_12) is pure pigmentation (2P/0H, +1.0) — with the rest distributed
  between (e.g. Alouatta and Colobus guereza hormone-tilted at −0.5).
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
- Rate/ASR (analysis 3) uses the **224-tip primate phenotype tree**, not the
  genome-sampled 117 set, to avoid ascertainment bias inflating the gain rate.
- Opie et al. 2012 = Commun Integr Biol 5(5):458-461, doi:10.4161/cib.20821.
