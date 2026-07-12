# comparative-genomics

Comparative molecular-evolution pipeline for pigmentation genes across primates:
**miniprot** (homology-based CDS extraction) → **MAFFT** (codon-aware alignment) →
**HyPhy RELAX** (relaxation/intensification of selection), with the gibbon clade as the priority.

Run on the University of Michigan **Great Lakes** cluster (SLURM + Lmod). This directory is
self-contained and independent of the rest of the repo.

## What is and isn't committed

Genome assemblies are **large and re-downloadable from public accessions**, so we commit the
*recipe*, not the data:

| Committed (the replication key) | Git-ignored (regenerate locally) |
| --- | --- |
| `config/accessions.tsv` — the exact assemblies used | assemblies / FASTA / GFF (`data/`, `*.fa`, `*.gff*`) |
| `config/branch-partition.tsv` — test vs. reference labels | alignments (`alignments/`) |
| `config/genes.txt` — target gene set | large per-gene RELAX JSONs (`*.raw.json`) |
| `scripts/` — SLURM job scripts | BAM-scale intermediates (`*.bam`) |
| `envs/environment.yml` — exact tool versions | |
| `results/` — small summary tables | |

Anyone with `config/accessions.tsv` can re-fetch the identical genomes and reproduce the run.

## Storage layout on Great Lakes

- **This dir (code/config/env spec):** `~/pigmentation-gene-network/comparative-genomics/` (home, backed up)
- **Assemblies + large intermediates:** `/scratch/tlasisi_root/tlasisi0/tlasisi/` (GPFS, no snapshots, **not backed up**, 60-day purge)
- **Final outputs to keep:** `~/tlasisi/pigmentation-gene-network/` (Turbo)

## Reproduce

```bash
# 1. Clone (SSH — no token needed)
git clone git@github.com:tinalasisi/pigmentation-gene-network.git
cd pigmentation-gene-network/comparative-genomics

# 2. Environment: prefer Lmod modules; fall back to a conda env ON SCRATCH (never bare -n → Turbo)
module load Bioinformatics
module spider miniprot mafft hyphy        # check what's modularized
module load mamba
mamba create -p /scratch/tlasisi_root/tlasisi0/tlasisi/envs/align \
  -c conda-forge -c bioconda ncbi-datasets-cli miniprot mafft hyphy
mamba env export -p /scratch/tlasisi_root/tlasisi0/tlasisi/envs/align > envs/environment.yml

# 3. Fetch assemblies from the committed accession list onto scratch
#    (datasets download genome accession <acc> ... for each row of config/accessions.tsv)

# 4. Run the pipeline (see scripts/). Gibbons first.
```

## Job submission convention

**Smoke test before every large array.** Run ONE unit first (1 assembly for miniprot, 1 gene for
RELAX) as a short job, read real usage with `seff <jobid>` (peak mem, CPU %, elapsed), then size the
full array's `--mem` / `--time` / `--cpus-per-task` from that + ~25% headroom. Catches env/module
errors for the cost of one job and prevents oversized requests.

- Partition: `--partition=standard` (449 nodes → arrays fan out fast; these tools are CPU-bound, low-mem).
  `largemem` only if a single task truly OOMs above ~180 GiB (won't happen here).
- Account: `--account=tlasisi0`.
- Parallelize with **job arrays**: one task per assembly (miniprot), one task per gene (RELAX).
- Never run heavy compute on the login node.

## Pipeline stages

1. **miniprot** — align a human+macaque reference proteome onto each target assembly → per-gene CDS.
2. **MAFFT** — codon-aware multiple alignment per gene.
3. **HyPhy RELAX** — test relaxation/intensification of selection on the dichromatic (test) vs.
   monochromatic (reference) branch partition defined in `config/branch-partition.tsv`.

Results (RELAX K, p-values per gene) land in `results/` as small summary tables; large intermediates
stay on scratch.
