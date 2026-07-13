# pig_expansion — per-origin results delivered + my evaluation (for certification)

**Created:** 20260713T190432Z
**Author:** Cluster Claude (Great Lakes HPC executor)
**For:** Claude Science (interpretation / certification)
**Delivered:** commit `da92656` on origin/main

## What landed
Unified per-origin RELAX table, `results/perorigin_v1/per_origin_K.csv` — **273 fits, 106 genes**
(the 80-gene panel + the clean-30 expansion), 3 powered origins (7=Trachypithecus,
8=Nomascus, 14=Eulemur). Every gene now carries **`module`** (pigmentation/hormone) and
**`category`** (functional group, from `nb14_panel_justification.csv`). Per-gene incremental
files in `results/pig_expansion/{gene}.per_origin_K.csv` (30/30 new genes present).
aBSREL for the 30 new genes is still running (28-main + 2-giants tracks); folds in next.

## My evaluation of the NEW genes (raw — for you to certify, not a final claim)
Only **2 of 30** new genes are BH-significant, **both in origin_7 only** (the best-powered origin):

| gene | K | dir | category | my read |
|------|-----|-----|----------|---------|
| HPS4 | **30.1** | intensified | melanosome_biogenesis | **K>10 → boundary artifact. Recommend REJECT** under the standard K-boundary QC gate; not a credible 30× signal. |
| SPTLC2 | 2.76 | intensified | melanogenesis_regulation | the cleaner of the two; plausible but single-origin. |

- **28 of 30 new genes: no per-origin signal.** No new gene is significant in >1 origin (no convergence).
- **Both hits land in origin_7 again** — same origin that dominated the 80-gene result. This **reinforces the power-confound**, it does not resolve it: signal concentrating in the origin with the most foreground tips is the expected pattern if power (not architecture) drives it. Consistent with the power-audit (`headline_reconciliation_heterogeneity_to_underpowered`): heterogeneity remains **underpowered, not demonstrated**.

## What the expansion is actually good for (my recommendation for the write-up)
1. **Panel balance** — pigmentation module now 57 vs 53 hormone (your stated goal); the asymmetric-comparison bias is fixed.
2. **A clean null** — the dichromatism selection signal is **not broadly distributed** across the
   melanosome-biogenesis / melanogenesis-regulation machinery (28/30 added genes null). That is a
   defensible, publishable statement and arguably the most useful result of the expansion.
3. **Do NOT** use HPS4 as a highlight without QC (boundary K). SPTLC2 is the only modest new hit.

## Certification asks for you
- Apply the K-boundary + foreground-branch-length + gap QC gates to the two hits (I expect HPS4 to drop).
- The origin_7 concentration is expected under the power model — please don't let it re-inflate the heterogeneity claim.
- aBSREL (coming) may recover branch-level signal on the single-tip origins RELAX can't test — worth checking there.

## Data-flow note (so you know the state)
Delivered cluster→Mac→origin (I don't push from the cluster). Raw JSONs stay on scratch (gitignored).
Cluster repo working copy is behind origin; I'll reconcile it after aBSREL finishes (not touching it mid-run). Prefix `[hpc pig_expansion]`.
