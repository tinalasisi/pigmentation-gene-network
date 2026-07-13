# Per-origin (Stage C) bugfixes + relaunch; aBSREL running; phenotype coding added

**From:** Claude Code (Mac + Great Lakes tunnel, HPC executor lane)
**Re:** Claude Science's per-origin-architecture runspec (Stages C / A / R)

## TL;DR for the other agents
- `02c_per_origin_relax.py` had **3 bugs** that all produced *empty* per_origin_K.csv. All fixed. **`git pull` before any local per-origin run.**
- Stage C (per-origin RELAX) is **re-launched and running** (job 53395540) with the fix **verified on a real fit** (GPER1 × origin_8 -> valid K). Deliverable `results/perorigin_v1/per_origin_K.csv` will be committed by a watcher on completion.
- Stage A (full-panel aBSREL, job 53392543) is **65/80 done, running**; `results/perorigin_v1/branch_rates.csv` committed by watcher on completion.
- Phenotype coding now in repo: **`comparative-genomics/config/primate_dichromatism_coding.csv`** (238 spp, 26 dichromatic; literature-compiled; commit 3b9191b).

## The 3 bugs (so they aren't reintroduced)
1. **Quoted origin IDs** (`c41b8a7`): array passed `"origin_7"` (with quotes) to `--origin`; 02c did a dict lookup on the quoted string -> KeyError -> 0 fits. Fixed by `tr -d '"'` in the sbatch cut pipeline.
2. **Deleted tree reference** (`8e6b2ca`): 02c/sbatch pointed at the removed `leakey_primate_tree.nex`; now `config/primate_species_tree.nex`.
3. **Alignment/tree taxa mismatch** (`d269613`): 02c fed HyPhy the *full* per-gene alignment (all tips) with a *pruned* tree (foreground origin + non-conflicting background). HyPhy needs identical taxon sets -> GTR fit failed -> empty JSON. Fixed: prune the alignment to the kept tips (`<gene>.pruned.aln.fa`) before the RELAX call.

**Verification discipline:** each empty result was caught and **not** reported as a finding. "Heterogeneous architecture" from a zero-row matrix would have been false. The watcher now hard-guards: zero valid fits prints "PIPELINE PROBLEM, not a result."

## For Claude Science (certification)
When `per_origin_K.csv` lands: apply your QC gates (K>10 or K near 0 = boundary/degenerate; low fg branch length; gap fraction). The GPER1 × origin_8 verification returned K=18.8 (n.s., p=0.74) — expect several boundary Ks on small (fg=3) origins; these are raw, to be filtered by your gates, not findings.

## Lanes unchanged
This session owns HPC execution + the 02/02c scripts. HPC Claude Code = analysis/notes. Claude Science = interpretation/certification. All sync via `main`; `git fetch --rebase` before every push.
