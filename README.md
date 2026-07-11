# Pigmentation gene network

**Goal.** Build a way to know how much to trust a claimed link between a genetic variant and a phenotype, by
making independent lines of evidence converge — statistical association, mechanistic pathway knowledge, and
experimental validation each capture part of the truth, and where they agree we can be confident the link is
real. Applied to human pigmentation as a model system, the aim is a resource that grades reported pigmentation
associations by how well independent evidence converges on each, and names the next step that would confirm it.

Pigmentation is the model system because it is highly heritable, has near-zero environmental variance, has a
well-characterized molecular mechanism, and shows the same prediction/portability failures — the same allele
causal in one population and silent in another — in a visible, checkable form.

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
