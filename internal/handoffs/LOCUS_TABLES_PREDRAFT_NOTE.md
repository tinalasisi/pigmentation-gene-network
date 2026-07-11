# Pre-drafted locus tables — for Claude Code to VALIDATE, not rebuild

_Written by Claude Science 2026-07-11. These two tables were pre-drafted here because populating them
correctly needs the genetics connectors + verified citations that only exist on Claude Science. Claude Code's
job is to run `scripts/validate_locus_tables.py` against them and build the manifest + page — NOT to
re-derive positions or citations._

## Files
- `data/processed/locus_nodes.csv` (3 loci)
- `data/processed/locus_annotation_edges.csv` (4 annotation edges)

## What is grounded (do not change without a new citation)
- **rs12913832** position chr15:28120472 (**GRCh38**) from live dbSNP/GWAS-Catalog grounding this session.
  Traits from GWAS Catalog. HERC2 = nearest-gene label; OCA2 = regulatory target via **PMID:22234890**
  (Visser 2012, verified real this session).
- **rs1800401** (OCA2 R305W) position chr15:28260053 (**GRCh37/b37** — the build Ang2023 reports). Coding
  missense in OCA2, so nearest-gene == functional gene. D1 anchor.
- **rs797044784** (OCA2 NW273KV) — novel exon-8 MNP; 1KGP decomposes it into 4 consecutive SNPs, so there is
  no single clean position; `position` left blank with `genome_build=NA` and the mechanism in `notes`. D2 anchor.

## GENOME-BUILD WARNING (must handle before displaying numeric positions)
The two positions are in **different builds** (rs12913832=GRCh38, rs1800401=GRCh37) — this is flagged
explicitly in the `genome_build` column. Do NOT display both as bare bp side by side. Either (a) liftover to a
single build, or (b) display the shared cytoband **15q13.1** instead of bp. All three loci share 15q13.1, so
option (b) is the low-risk choice for the MVP.

## Honesty note carried in the data
rs12913832 was **NOT** genome-wide significant in the Ang2023 Kalinago cohort (P_adj=0.075). The HERC2->OCA2
regulatory mechanism is the *cited external finding* (Visser 2012, forensic/European pigmentation), not a
Kalinago result. The `notes` field says this. Keep that distinction in the UI — do not imply the Kalinago
paper demonstrated the enhancer mechanism.

## Validation contract
`scripts/validate_locus_tables.py` (spec in CLAUDE_CODE_HANDOFF.md §3b) must pass: edge_type in the 5-value
vocab, no blank evidence_citation, no blank gene_label_basis, and no locus_id leaking into
gene_network_edges.csv. These tables are built to pass it.
