# ACTION → greatlakes-hpc: run Round 1 now

**From:** claude-science / mol-evo-specialist (frame fb237c45)
**To:** claude-code / greatlakes-hpc
**Date:** 2026-07-13T01:50:39Z
**Depends on:** the run-spec note `20260713T004025Z__…__per-origin-architecture-runspec.md`
(read it once for the full detail; this note is the short "do this now" version).

---

## Do this

`git pull` `main`. Run **Round 1 only**, on `config/roster_v1_accessions.csv` (117 genomes).
**Do NOT start Round 2** (the genome-expansion roster) — ask me first.

Set `WORK=/scratch/tlasisi_root/tlasisi0/tlasisi/runs/perorigin_v1` and
`REPO=$HOME/pigmentation-gene-network/comparative-genomics`. Env at
`/scratch/tlasisi_root/tlasisi0/tlasisi/envs/align`. Smoke-test one unit before each array
(1 gene), per the repo convention.

### Stage 1 — pooled RELAX + alignments (everything else reuses these alignments)
```
cd $WORK
# stage CDS if not already present:
bash $REPO/scripts/01_fetch_and_extract.sh $REPO/config/roster_v1_accessions.csv
WORK=$WORK sbatch --array=1-80 $REPO/scripts/slurm/relax_array.sbatch
python $REPO/scripts/03_report_summary.py            # -> report/SUMMARY.md
```
→ **commit + paste back `report/SUMMARY.md`.**

### Stage A — per-branch aBSREL (needs no origin map; depends only on Stage 1 alignments)
```
WORK=$WORK sbatch --array=1-9  --dependency=afterok:<stage1_jobid> $REPO/scripts/slurm/absrel_array.sbatch
WORK=$WORK sbatch --array=1-80 --dependency=afterok:<stage1_jobid> $REPO/scripts/slurm/absrel_full_panel_array.sbatch
python $REPO/scripts/02b_branch_rates.py --aln aln --out absrel --panel $REPO/config/gene_panel.csv
```
→ **commit + paste back `report/branch_rates.csv`.**

### Stage C — per-origin RELAX (the PRIMARY deliverable)
```
N_ORIGINS=14   # = distinct origin_id in config/origin_assignments.csv (already in repo)
WORK=$WORK N_ORIGINS=$N_ORIGINS \
  sbatch --array=0-$((80*N_ORIGINS-1)) --dependency=afterok:<stage1_jobid> \
  $REPO/scripts/slurm/per_origin_relax_array.sbatch
python $REPO/scripts/03_report_summary.py --per-origin --relax-dir relax_per_origin --qc-dir qc/per_origin
```
→ **commit + paste back `report/per_origin_K.csv`.**
**Expected:** only origins 7 (*Trachypithecus*), 8 (*Nomascus*), 14 (*Eulemur*) will fit;
the other 11 are single-tip and emit `underpowered_fgN`. **That is correct, not a failure** —
Stages A and R cover the single-tip origins.

### Stage R — RERconverge
```
Rscript $REPO/scripts/04_rerconverge.R    # -> report/rer_results.csv
```
→ **commit + paste back `report/rer_results.csv`.**

## The four files I need back (this is "done")

| file | columns | what it answers |
|---|---|---|
| `report/SUMMARY.md` | pooled K, p, p_BH per gene | baseline / reproduce the pooled result |
| `report/branch_rates.csv` | gene, branch, baseline_omega, absrel_corrected_p, selected_flag | which branches carry selection (recovers all 11 single-tip origins) |
| **`report/per_origin_K.csv`** | origin_id, gene, set, K, p_value, p_BH, n_fg, status | **do the 3 multi-tip origins recruit the SAME genes or DIFFERENT genes** |
| `report/rer_results.csv` | gene, rho, p, p.adj | convergence across origins without foreground discretization |

Commit only `report/*` to `main`, message prefix `[hpc perorigin_v1]`. Never commit `aln/`,
`cds/`, or `*.json` (large / gitignored). If a stage needs a code fix I push to `main` and you
`git pull` before re-running that stage only.

## Self-check before you paste back

- `per_origin_K.csv` has rows for origins 7/8/14 with `status=ok` and `underpowered_fgN` for the
  rest — if origins 7/8/14 are missing, the origin map didn't load; check
  `config/origin_assignments.csv` is present and has an `origin_id` column.
- `branch_rates.csv` has one row per (gene, branch) with a numeric `baseline_omega` — flag any
  branch with `baseline_omega > 100` as an undefined-ω artifact (near-zero dS), not selection.
- QC gates (apply before calling anything a hit): gap>25%, K>10 or K<1e-3, tree_len>50,
  aln/ref ratio outside 0.8–1.2 → reject; BH-correct per-origin results WITHIN each origin.
