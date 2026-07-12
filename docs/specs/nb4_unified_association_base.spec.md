# nb4_unified_association_base.csv — spec / provenance

## Purpose

Joins the 105 curated genotype→phenotype-discordance loci (the 105 legacy rows of
`discordance_loci_effector_classified.csv`, `paper != "Kim2024"`, NB3-upstream) against the frozen
NHGRI-EBI GWAS Catalog pigmentation pull by rsID, **keeping both
provenance rows** rather than collapsing a locus reported by both sources into one, and attaches a
gene-level GWAS-replication convergence annotation. This is one layer of the convergence-graded
rescue screen: it establishes whether an independent GWAS signal exists (by exact rsID, and
separately by gene symbol) for loci the original papers could not mechanistically explain.

Produced by `notebooks/04_unified_association_base.ipynb`.

## Inputs (all frozen, offline, committed in-repo)

| File | Rows | Role |
|---|---|---|
| `data/processed/discordance_loci_effector_classified.csv` (105 legacy rows, `paper != "Kim2024"`) | 105 | Curated discordance loci with per-locus effector-status classification (`effector_uncertain`, `canonical_effector_variant_gap`, `effector_ambiguous_near`, `regulatory_of_canonical_neighbour`, `not_a_locus`). Upstream (NB3); not re-derived here. |
| `data/external/gwas_catalog/pigmentation_gwas_catalog.csv` | 1,072 | Deduplicated lead GWAS Catalog associations, one row per rsID, GRCh38 (`pos_hg38`). Access-UTC 2026-07-12T14:46:57Z (see `docs/specs/gwas_catalog.spec.md`). |
| `data/external/gwas_catalog/gwas_pigmentation_associations.csv` | 723 | Granular associations (`efo_id, trait, gene, snp_id, pvalue`); used ONLY for the gene-level replication count. No committed `.meta.json` — a documented reproducibility gap (regeneration via `scripts/pull_gwas_associations.py`, exact original CLI args not recorded in-repo). |

**Kim et al. 2024 (PMID 38849341)** was checked for inclusion and found to have **no extracted
data file anywhere in this repository** — it is cited only in internal planning documents
(`internal/START_HERE.md`, `internal/PROJECT_EVOLUTION.md`, `internal/CHANGELOG.md`), where
`internal/CHANGELOG.md` records that a standalone population atlas built from this source was
deliberately preempted (the source already publishes its own atlas). **Not folded into the
unified base** — this gap is recorded, not fabricated.

## Method

1. **Build tagging (105 curated loci).** `coord_build` free text classified into a controlled
   `coord_build_tag`: `GRCh37` / `GRCh38` (explicit build token present), `ambiguous` (a
   chromosome is named but no build token anywhere — 2 rows: Crawford2017 `chr16`, Salvo2023
   `chr15`), `no_build` (neither — 23 rows: covariates, legacy cDNA/codon numbering, unenumerated
   variant sets, etc.). Result: **74 GRCh37 / 23 no_build / 6 GRCh38 / 2 ambiguous.** GWAS Catalog
   rows are uniformly tagged `GRCh38` (as served by the download endpoint).
2. **rsID extraction and join.** Every `rs\d+` token is extracted from both the curated `rsid` and
   `locus_id` free-text columns (a locus's primary or credible-set-member rsIDs are sometimes only
   named in `locus_id`). 93/105 curated rows have >=1 extractable rsID (12 do not — covariates, a
   variant with no dbSNP entry at publication, unenumerated polygenic sets). Both the deduplicated
   (1,072) and granular (723) catalog rsID sets are checked; a curated row gets `also_in_*` flags,
   and each matching catalog row independently gets `also_in_curated_105` /
   `also_in_curated_52_unexplained` flags on its own row.
3. **Unified base assembly — both provenance rows kept, nothing collapsed.** The output is the
   concatenation of the 105 curated rows and all 1,072 catalog rows (**1,177 total**), not a merge
   that drops one side. Cross-reference flags on each row point at the other source; no row is
   deleted or deduplicated across sources.
4. **Gene-level GWAS-replication convergence (additive annotation, granular file ONLY).** Group
   the 723-row granular file by `gene`, count associations (`gwas_n_assoc`), flag
   `gwas_replicated = (gwas_n_assoc >= 2)`. **83 of 318 genes** clear this threshold. Gene labels
   in the curated set and catalog are free text (parenthetical annotations, positional qualifiers,
   multi-gene lists); a small symbol-extraction helper (`extract_gene_symbols`) strips these before
   matching — a naive exact-uppercase match only recovers 63/105 curated rows, the cleaned matcher
   recovers 87/105. **This annotation is never used to filter or gate a candidate** — see
   Non-negotiables below.

## Non-negotiables

- **Both provenance rows are always kept.** A locus reported in both the curated set and the GWAS
  Catalog appears twice in the unified base (once per `source_type`), cross-referenced, never
  collapsed into a single merged row.
- **`gwas_n_assoc` / `gwas_replicated` is an ADDITIVE convergence annotation, never a filter or
  gate.** Computed only from the granular 723-row file (never the deduplicated 1,072, which cannot
  support a per-gene count). A `>=2`-association gate is explicitly backwards for this project's
  thesis: it would systematically favor canonical, heavily-GWAS'd nearest-genes (OCA2, HERC2,
  MC1R, IRF4) and discard exactly the off-canonical, singleton, or novel loci the rescue screen
  exists to surface. `gwas_replicated=False` is not evidence against a locus.
- **No fabricated gene-gene relationships.** This notebook adds no gene-gene edges; it is a
  locus/association-level join with a gene-level count annotation.
- **Kim 2024 is a documented gap, not a fabricated row.**

## Headline numbers

| Metric | Value |
|---|---|
| Unified base rows | **1,177** (105 curated + 1,072 GWAS Catalog) |
| Curated loci (upstream) | 105 |
| Author-unexplained loci (rescue-candidate population) | **52** |
| coord_build tags (105 curated) | GRCh37 74 / no_build 23 / GRCh38 6 / ambiguous 2 |
| 52-set loci with an rsID hit in the 1,072-row dedup catalog | **27** |
| Genes with >=1 granular association (723-row file) | 318 |
| Genes with `gwas_replicated=True` (>=2 assoc.) | **83** |
| 52-set loci whose gene clears `gwas_replicated` (symbol-matched) | **40** |
| 105-set loci whose gene clears `gwas_replicated` (symbol-matched) | 87 |

## Files

- `data/processed/nb4_unified_association_base.csv` — the 1,177-row long-format output.
- `notebooks/04_unified_association_base.ipynb` — this build, self-contained, offline-reproducible.
- `docs/specs/nb4_unified_association_base.spec.md` — this document.

## Upstream / sibling specs

- `docs/specs/discordance_loci_effector_classified.spec.md` — the 105-locus curated input and the
  per-locus effector-status classification that defines the rescue target.
- `docs/specs/gwas_catalog.spec.md` — the deduplicated 1,072-row GWAS Catalog pull.
