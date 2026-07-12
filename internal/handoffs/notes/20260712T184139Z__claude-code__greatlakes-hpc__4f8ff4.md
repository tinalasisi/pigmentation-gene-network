---
from: claude-code/greatlakes-hpc
to: all
date_utc: 2026-07-12T18:41:39Z
platform: claude-code
subject: Scaling analysis — 117-species RELAX scan, parallelization recommendations
---

## Context

The 9-species gibbon flagship fetch+RELAX pipeline is running on Great Lakes
(jobs 53371737 and 53371920). I profiled the current run and estimated wall
times for the full 117-species `accessions_all_recoverable.csv` panel. Tina
asked about parallelization options.

## Current 9-species timing (observed)

- **Fetch** (`01_fetch_and_extract.sh`): ~30 min for 9 species (~3.3 min/species).
  Bottleneck is miniprot (genome-wide protein-to-genome alignment), one species at a time.
- **RELAX** (`02_align_and_relax.py`): not yet completed, but with 9 tips per gene
  tree each HyPhy RELAX call is fast. 80 genes run sequentially.

## Estimated 117-species timing (current sequential pipeline)

- **Fetch**: ~3.3 min x 117 = **~6.5 hours**. 95 of 117 species are unannotated
  (require miniprot); the 22 annotated species are fast (grep CDS from download).
- **RELAX**: HyPhy RELAX scales poorly with tip count. With ~117 tips per gene tree
  (vs 9), each gene could take 10-30+ min. 80 genes x ~20 min = **~27 hours**
  sequentially. This is the dominant bottleneck.

## Parallelization recommendations

Both steps are embarrassingly parallel — no dependencies between work units.

### Fetch: parallelize across species (SLURM job array)

- `#SBATCH --array=1-117`, each task processes one row of the accessions CSV.
- Per-task resources: ~4 cores / ~8 GB / ~15 min.
- Wall time drops from ~6.5 h to **~15-20 min** (limited by scheduler throughput
  and NCBI download concurrency).

### RELAX: parallelize across genes

Two options, not mutually exclusive:

1. **SLURM job array** (`--array=1-80`): one job per gene, maximal parallelism,
   wall time = longest single gene (~30 min). Slight overhead from 80 separate
   job submissions.

2. **Python multiprocessing** inside `02_align_and_relax.py`: the `--threads`
   argument is already accepted but never used to parallelize the gene loop.
   Wrapping the `for gene in panel` loop with `concurrent.futures.ProcessPoolExecutor`
   (pool size = `--threads`) is a small code change. With 8 workers: ~10x speedup,
   ~3-4 hours instead of ~27.

### Summary table

| Approach                              | Fetch    | RELAX      |
|---------------------------------------|----------|------------|
| Current (sequential)                  | ~6.5 h   | ~27 h      |
| Job arrays (both steps)               | ~20 min  | ~30-45 min |
| Job array fetch + multiprocessing RELAX | ~20 min | ~3-4 h   |

### Implementation notes

- Fetch array jobs should write to the same shared `cds/` directory on scratch
  (file paths are species-namespaced, so no conflicts).
- NCBI `datasets` downloads may rate-limit if 117 concurrent requests hit at once;
  consider `--array=1-117%20` to cap concurrency at ~20 simultaneous downloads.
- The RELAX job array approach requires a wrapper script that reads gene N from
  `gene_panel.csv` and runs alignment + RELAX for that gene only.
- All outputs stay on scratch (`/scratch/tlasisi_root/tlasisi0/tlasisi/pgn_run`);
  only summary CSVs and JSON results need to be copied back. The `.gitignore`
  already excludes all large genomic files.

## Action needed

This is an analysis/recommendation note. Implementation requires changes to:
- `01_fetch_and_extract.sh` (or a new array wrapper)
- `02_align_and_relax.py` (add multiprocessing, or a new array wrapper)
- New sbatch scripts for the array versions

Ready to implement on request from any agent or from Tina.
