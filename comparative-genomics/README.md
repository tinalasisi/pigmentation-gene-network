# The genetic architecture of primate sexual dichromatism

**The finding.** In birds, sexual dichromatism is nearly a single-gene switch — *MC1R*
(Nadeau et al. 2007). In primates it is not. Hair dichromatism has **arisen ~15 times
independently** across the primate radiation, is **polygenic in every origin** (and *MC1R* is
not the hit), and shows **no single shared genetic signature across those origins** — the
architecture is origin-specific. The trait is also evolutionarily labile (lost ~9× more readily
than it is gained), consistent with dichromatism being reachable by several different
**pigmentation × sex-hormone** genetic routes rather than one canonical switch.

This reframes an earlier analysis that had pooled all dichromatic species into one foreground
and asked "does selection intensify in dichromatic lineages." That design presupposed a shared,
convergent architecture — the very thing at issue. Our own ancestral-state reconstruction (run
from raw trait scores + tree topology, not inherited) shows the 24 genomically-sampled
dichromatic species collapse to only **14 independent origins**, of which **11 are single tips**
and 3 are multi-tip radiations (*Trachypithecus* ×8, *Nomascus* ×3, *Eulemur* ×2). Pooling gave
one clade a third of the foreground weight. The correct unit of analysis is the **origin**, and
the architecture question is answered per origin.

**What the pipeline does.** **miniprot** (homology-based CDS extraction) → **MAFFT** (codon-aware
alignment) → three selection layers, each matched to what the origin structure can support:

1. **Per-origin RELAX** (`02c`) — for the 3 multi-tip origins: do they intensify the *same*
   genes (convergence) or *different* genes (heterogeneous architecture)?
2. **Per-branch aBSREL** (`02b`) — recovers all 11 single-tip origins as individual branches;
   a per-branch dN/dS + episodic-selection test that needs no ≥2-tip foreground.
3. **RERconverge** (`04`) — relative-rate convergence across all origins at once.

See `results/figures/` (origins tree, pooling breakdown, per-branch TFAP2A) and the run-spec in
`../internal/handoffs/notes/` for the full cluster protocol.

Run on the University of Michigan **Great Lakes** cluster (SLURM + Lmod). This directory is
self-contained and independent of the rest of the repo.

## Figures

![Independent origins](results/figures/fig_origins.png)

*Hair dichromatism arose ~15 times independently on the 235-tip primate tree; 14 origins are
captured genomically (Presbytis hosei has no genome). Stars = gains, × = reversals. The
Trachypithecus block is one gain sampled 8× — the pooling problem, visualized.*

![Per-branch TFAP2A](results/figures/fig_tfap2a_branches.png)

*On TFAP2A, episodic selection is scattered across the tree — 4 of 21 dichromatic tips and 8 of
67 monochromatic tips — not concentrated on dichromatic lineages. Being dichromatic does not
predict selection on this gene.*

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

1. **miniprot** (`01`) — align a human+macaque reference proteome onto each target assembly → per-gene CDS.
2. **MAFFT / codon alignment + QC** (`02`) — codon-aware alignment, per-sequence outlier removal,
   gap-column trimming; produces the alignments + tagged trees all downstream stages reuse.
3. **HyPhy RELAX, pooled** (`02`) — baseline: relaxation/intensification on the pooled dichromatic
   vs. monochromatic partition (`config/species_states.csv`). Reproduces the earlier result.
4. **HyPhy RELAX, per-origin** (`02c`) — the primary test: one RELAX per gene *per independent
   origin* (`config/origin_assignments.csv`), tagging one origin's tips as `{Test}` and dropping
   the other origins' dichromatic tips so each reference stays purely monochromatic. Powered for
   the 3 multi-tip origins.
5. **HyPhy aBSREL, per-branch** (`02b`) — per-branch baseline ω + episodic-selection test on every
   branch; recovers the 11 single-tip origins that per-origin RELAX cannot fit.
6. **RERconverge** (`04`) — relative-rate convergence across origins.

Small summary tables (`report/SUMMARY.md`, `branch_rates.csv`, `per_origin_K.csv`,
`rer_results.csv`) are the paste-back deliverables; large intermediates (alignments, JSONs) stay
on scratch and are never committed.
