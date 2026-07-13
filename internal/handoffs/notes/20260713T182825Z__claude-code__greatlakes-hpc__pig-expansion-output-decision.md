# pig_expansion — DECISION on output layout (answers Q1 from my 18:17Z note)

**Created:** 20260713T182825Z
**Author:** Cluster Claude (Great Lakes HPC executor)
**For:** Claude Science
**Re:** Q1 in `20260713T181755Z__…__pig-expansion-status-and-coordination.md`

## Decision (from the user)
**Append the 30 new genes into the unified `results/perorigin_v1/` tables (→ 110 genes), AND
add an explicit functional-group annotation column to every gene.** Not a separate
`results/pig_expansion/` combined set — one unified 110-gene table is what she wants for figures.

Plus (your requirement) the per-gene incremental files are still emitted.

## What the combined tables will look like
`results/perorigin_v1/per_origin_K.csv` and `results/perorigin_v1/branch_rates.csv` get **two
columns inserted right after `gene`**:
- **`module`** — pigmentation | hormone
- **`category`** — the functional group / layer

Both are sourced from **`analysis/module_selection/data/nb14_panel_justification.csv`** (the
notebook-authoritative mapping; I verified **110/110 panel genes are covered**, 0 missing). The
new-30 carry `melanosome_biogenesis` (16) and `melanogenesis_regulation` (14); the existing
pigmentation 27 keep their finer NB14 categories (receptor_signaling, transcription,
melanosome, melanosome_transport, enzyme, regulatory); hormone genes carry their axis
(androgen_axis, estrogen_axis, hpg_axis, steroid_biosynthesis, gnrh_signaling,
coactivator_corepressor_carrier).

## How it's implemented
`comparative-genomics/scripts/collect_pig_expansion.py` (commit **903d3e9**), run at delivery
and re-runnable as genes land. It:
1. annotates the rebuilt `report/per_origin_K.csv` / `report/branch_rates.csv` with `module`+`category`,
2. writes the annotated unified tables into `results/perorigin_v1/`,
3. emits per-gene `results/pig_expansion/{gene}.per_origin_K.csv` + `{gene}.aBSREL.json` for the
   30 new genes (your per-gene incremental spec).

Delivery is pulled to the Mac and pushed from there (safe path — no cluster auto-git). Prefix `[hpc pig_expansion]`.

## Still open: Q2 (giants-split)
I split MYO5A/LYST onto a separate 8h array so the 28 fast genes don't wait on them (same
analysis). Proceeding that way unless you object.

## Run status
DAG v3 is healthy — the 28 main genes are producing genuine RELAX fits (e.g. AP3B1 K=1.1,
CDH2 K=0.27); MYO5A/LYST still running on the giants track; per-origin + aBSREL queued to chain.
(Earlier tonight's failures — empty-CDS, silent-masking, a temp-race, and my own panel-stash
slip — are all resolved; see the 18:17Z note.)
