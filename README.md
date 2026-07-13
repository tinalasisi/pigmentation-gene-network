# The architecture of pigmentation genetics

**One question, two scales.** Is the link from genotype to pigmentation phenotype the simple
one-gene-one-trait picture, or is its architecture conditional on context? This project answers it
from two directions and finds the same thing: the map is not simple, and context decides.

- **Macroevolutionary arm — the discovery.** Sexual dichromatism is nearly a single-gene switch
  in birds (*MC1R*). Across primates it is not: it **arose ~15 times independently** and is built
  by **different pigmentation × sex-hormone gene combinations in different lineages** — a
  heterogeneous, origin-specific architecture. This is the first clade-wide, multi-gene selection
  test of the genomic basis of primate sexual dichromatism. Pipeline, figures, and cluster
  protocol are in [`comparative-genomics/`](comparative-genomics/).
- **Human arm — the method.** To know how much to trust a claimed variant→phenotype link, make
  independent lines of evidence converge — statistical association, mechanistic pathway knowledge,
  and experimental validation. Applied to human pigmentation, this grades reported associations,
  shows the same allele can be causal in one population and silent in another (context = ancestry),
  and shows an effect's *direction* is predictable from mechanism.

Pigmentation is the model system because it is highly heritable, has near-zero environmental
variance, has a well-characterized molecular mechanism, and shows these context effects in a
visible, checkable form — from a single human variant read across ancestries to a whole trait
reassembled across a primate radiation.

## Where to start

This project is mid-reorientation, and the **authoritative, current account** of the goal, the materials, the
open decisions, and where everything lives is:

> **[`internal/START_HERE.md`](internal/START_HERE.md)** — read this first.

Only the goal is fixed; the execution is being (re)designed. Earlier working material is under
`internal/archive/` (not committed) and is not part of the current project.

## Repository orientation (materials, not a prescribed order)

- `data/processed/gene_network_{nodes,edges}.csv`, `raghunath_*` — the Raghunath signed directed melanogenesis
  network (built by `notebooks/01`, `02`).
- `data/case_records/EXTRACT_*.csv`, `data/raw/papers/*` — curated papers and their extracts.
- `data/processed/discordance_loci.csv` — one processed, locus-first view of the curated discordance papers.
- `scripts/` — data-pull and harmonization tools (`gwas_catalog.py`, `harmonize.py`, …).
- `internal/` — governance, audits, and coordination; `DATA_SOURCES.md` — provenance manifest.

License: MIT (see `LICENSE`).
