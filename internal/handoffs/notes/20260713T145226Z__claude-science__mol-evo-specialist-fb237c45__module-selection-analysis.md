# Module-selection analysis — handoff for review

**Author:** Claude Science (mol-evo-specialist, frame fb237c45)
**Date:** 20260713T145226Z
**Repo path:** `comparative-genomics/analysis/module_selection/`
**Prefix for your commits if you touch this:** `[review module-selection]`

## What landed
A frozen-data, replicable analysis answering the user's request: a combined
metric of whether each dichromatism origin has more pigmentation-specific or
sex-hormone-specific selection, which genes in each module are selected per
lineage, and an Opie-analog trait-dynamics test — all using phytools/ape on the
latest HPC data (commit 4c07317).

Files (all committed):
- `module_selection_analysis.qmd` — the notebook (verified: purl+source runs
  end-to-end from `data/`, regenerates loss:gain=9.1x and both CSVs)
- `figures.py` — regenerates both figures from `data/` (verified runs clean)
- `data/` — 6 frozen inputs (branch_rates, per_origin_K, origin_assignments,
  gene_modules, species_coding, primate_species_tree)
- `fig_module_balance.png`, `fig_per_lineage_genes.png`
- `module_balance_results.csv`, `opie_analog_results.csv`
- `README.md`

## What I'd like reviewed / double-checked
1. **Module-balance denominator.** Metric = (nP-nH)/(nP+nH) over UNIQUE selected
   genes per module along an origin's TIP branches (aBSREL corrected p<0.05).
   Single-tip origins rest on one branch — is that a fair peer to the 8-tip
   Trachypithecus origin on the same axis? I mark powered vs aBSREL-only, but a
   reviewer should sanity-check the visual peering (figure-style §1.2).
2. **Opie-analog root state** returns exactly 0.5 under both ace-flat and
   fitzjohn priors — I dropped the root-state row rather than report an
   uninformative 0.5. Confirm that's the right call vs running a proper
   stochastic-map root summary.
3. **Ascertainment bias.** I deliberately ran analysis 3 (rates/ASR) on the
   224-tip Leakey phenotype tree, NOT the 117 genome set, because the genome set
   oversamples dichromatic species. On the 117 set the ratio inverts to 0.25
   (I checked). Reviewer: confirm the 224-tip tree is the right denominator for
   the rate claim, and that the module-balance analysis (which NECESSARILY uses
   the genome set, since it needs sequences) is not making a rate claim.

## Related prior deliverables (artifact store, not yet all in repo)
- adversarial_review_round1.md, final_synthesis_ranking.md (2-round figure review)
- Four exploratory-direction figures (lability, convergence, development, ecology)
These are in the Claude Science artifact store; ask if you need them in-repo too.
