# Cluster runspec — pigmentation-module expansion (43 genes)

**Created:** 20260713T163427Z
**Author:** module-selection session (fb237c45)
**Why:** The selection panel was built asymmetrically — hormone module = whole endocrine
pathway (53 genes), pigmentation module = canonical melanogenesis core only (27 genes).
This biases every per-module comparison (a random lineage sits at balance −0.33, not 0).
Fix: expand the pigmentation module to comparable breadth using genes that are pigmentation
genes **in our own network layers** (OMIM pigmentation phenotype / Baxter2018 / Raghunath
melanogenesis mechanism / melanosome proteome / functional screen). Justification for every
gene is in `notebooks/14_hormone_pigment_interface.ipynb` and
`comparative-genomics/analysis/module_selection/data/nb14_panel_justification.csv`.

## Genes to run (43)
Config: `comparative-genomics/config/gene_panel_expansion_pigmentation.csv`

**Group A — melanosome biogenesis & transport (21):** AP3B1, AP3D1, BLOC1S3, BLOC1S5, BLOC1S6, CTNS, GPR143, HPS1, HPS3, HPS4, HPS5, HPS6, LYST, MLPH, MYO5A, RAB27A, RAB5C, SLC17A5, SLC1A2, SLC29A3, SLC44A4

**Group B — melanogenesis regulation (22):** BCL2, CDC42, CDH2, CTNNB1, EDN1, EGFR, EP300, FASLG, HGF, HRAS, MAP2K1, MAP2K2, MAPK3, PAK1, PPP3CA, RAC1, RACK1, RAF1, SPTLC2, SRC, TP53, TRAF6

## What to run (same pipeline as the existing panel)
For each gene: miniprot extraction → mafft codon alignment → HYPHY
1. **aBSREL** full-panel branch scan (append rows to `results/.../branch_rates.csv`)
2. **RELAX** per-origin on the 3 powered origins (7=Trachypithecus, 8=Nomascus, 14=Eulemur)
   (append rows to `results/.../per_origin_K.csv`)
Reuse the staged 117-set alignments/tree. Same QC gates as before (stop-codon cleanup,
non-triplet handling — the EDN3 lesson).

## CRITICAL: incremental / per-gene output (user requirement)
Run as a SLURM **array with one output file per gene**, e.g.
`results/pig_expansion/{gene}.aBSREL.json` and `{gene}.per_origin_K.csv`, so results can be
pulled as each gene lands — **do not** wait on the slowest gene (MYO5A, ~1850aa) or write a
single monolithic output at the end. A small collector script should append finished per-gene
files into branch_rates.csv / per_origin_K.csv on each poll, so the local session can rebuild
figures from partial results.

Suggested array: `--array=1-43`, one gene per task, `cpus=16`. Order the array so the fast
small genes (BLOC1S3/5/6, RAB5C, SLC*) run first and MYO5A/LYST (large) last.

## Time estimate
Wall ≈ slowest gene as a parallel array: MYO5A aBSREL ~1–1.5h; RELAX ~40min; most genes minutes.
With per-gene outputs the useful results (melanosome core) land within ~30–45 min.

## Prefix on commits
`[hpc pig_expansion]`
