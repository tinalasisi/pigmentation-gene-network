# NB11 — Cross-ancestry conditionality of pigmentation-gene discovery

**Notebook:** `notebooks/11_cross_ancestry_conditionality.ipynb`
**Evidence axis:** population genetics / allele frequency (NOT the STRING/network axis).
**Status:** self-contained mini-manuscript. Frozen inputs; no git commit performed.

## What it establishes
Several pigmentation genes are reported by different-ancestry GWAS via *different* variants, each
common only in the population where it was found — **population-conditional discoverability**. The
falsifiable claim (convergent-gene variants are more population-differentiated than the genome-wide
background) is tested with Hudson's Fst anchored to an empirical common-variant baseline.

## Convergent gene set (n=4 genes, 7 variants)
Grouped from `discordance_loci_effector_classified.csv` by `author_attributed_gene` across papers with
different population labels: **MFSD12** (rs2240751 / rs10424065), **SPIRE2** (rs34357723 / rs12598316),
**BNC2** (rs2153271 / rs16935073), **TSPAN10** (rs6420484).

## Output
`data/processed/nb11_cross_ancestry_fst.csv` — one row per variant:

| column | meaning |
|---|---|
| gene, rsid, associated_allele | identity + phenotype-associated allele |
| populations_reported | which paper/population reported it |
| variant_role | shared_variant_multi_pop / different_variant_same_gene / single_pop_european_weighted |
| known_effector_flag | True for MFSD12 (validated effector — portability, not discovery) |
| gene_label_basis | author_attributed / nearest_gene_by_position / coding_in_gene |
| AF_AFR..AF_SAS | associated-allele freq per 1000G superpopulation |
| fst_hudson_5superpop | Hudson Fst across the 5 superpops |
| baseline_percentile | percentile vs the 552-variant common-SNP baseline |
| functional_target_note | cited functional-target hypothesis (required for nearest-gene rows) |
| ld_independence_evidence | confirmed (LD-tested) or inferred |
| baseline_source, ensembl_endpoint, data_frozen | provenance |

## Baseline method
Empirical: Hudson Fst over 552 common (global mean freq in [0.05,0.95]) 1000G phase 3 variants
(mean=0.0864, median=0.0625, p95=0.2410); consistent with the
published continental mean ~0.10–0.12 (Bhatia et al. 2013, doi:10.1101/gr.154831.113).

## Framing
- MFSD12 is a KNOWN effector (Crawford 2017 knockdown) → this is cross-population *portability*, not novel discovery.
- SPIRE2 rs34357723's "SPIRE2" label is positional (nearest-gene); Morgan 2018's functional target is MC1R via long-range regulation — kept as a cited annotation, not reassigned.
- LD-independence CONFIRMED for MFSD12 (empty LD in all 5 superpops despite 3.2 kb spacing) and BNC2 (r2=0.19 in AMR); INFERRED for SPIRE2.

## Expansion routes (§8)
1. Martin et al. South-African GWAS — **NOT in repo; needs adding.**
2. Targeted GWAS Catalog pull with ancestry metadata.
3. Literature search.
Screen criterion formalized as `screen_convergent_conditional()` (stub): gene reported in ≥2 populations
via variants with anti-correlated associated-allele frequency vectors across superpopulations.

## Reproducibility
Frozen responses under `data/external/db_responses/nb11/`; notebook ends with a replay assertion that
re-derives the output CSV from frozen inputs and enforces the citation/provenance gate.
