# Dark-matter ledger — per-gene resolution class (15 genes)

_Built by Claude Science 2026-07-11 from the committed Track A locus-resolution work
(`locus_resolution_table.csv`, artifact b6ba3948). Reconciles to project_dashboard.md §3's four-class
decomposition (6/3/2/4). Every row carries a citation. Descriptive, not causal._

## What this is
The 15 "dark-matter" case genes — cited by a case paper as carrying discordance signal, yet absent from BOTH
the 168-gene mechanistic network AND the D'Arcy OMIM-backed disease-gene compendium — each classified by
**gene-attribution status** under the nearest-gene-vs-causal discipline (a GWAS locus's nearest-gene label is
positional, not causal; a functional target is attached only with its own citation).

## The four classes (locked; project_dashboard.md §3, locked decision 11)
| class | n | meaning |
|---|---|---|
| genuinely_novel | 4 | Best-supported causal gene is the labelled gene itself (self); it is a correctly-labelled pigmentation gene simply missing from the network. |
| redirects_to_other_gene | 2 | A dominant eQTL/co-mapping redirect points to a DIFFERENT gene, but that target is also absent from the 168-gene network (or ineligible, e.g. a non-coding RNA). |
| signal_no_eQTL_redirect | 3 | A genuine pigmentation GWAS signal exists, but no dominant trait-relevant eQTL redirect to a different gene was found; the nearest-gene label stands unresolved. |
| LD_passenger_or_no_signal | 6 | No pigmentation GWAS signal at this locus; flagged by a case paper as a linkage/IBD passenger or coincidental co-location, not an independent association. |

**Key result (consistent with the FALSIFIED mislabeled-pointers hypothesis):** `target_in_168_network` is
False for all 15 — ZERO dark-matter genes resolve to an in-network gene. The one positional-pointer-to-network
case, HERC2→OCA2, is a D'Arcy-*recoverable* gene, not dark matter, and is documented in the locus tables, not
here.

## Columns
- `gene` — the case-paper gene symbol.
- `dark_matter_class` — one of the four locked classes above.
- `track_a_resolution_class` — the finer Track A class this maps from (5-value).
- `rsid`, `nearest_gene_label`, `likely_functional_target`, `target_in_168_network` — the resolution result.
- `pigmentation_traits`, `eqtl_target_gene`, `eqtl_dataset_pvalue` — the GWAS/eQTL evidence queried.
- `case_papers` — which of the 13 case papers cite the gene.
- `evidence_citation`, `notes` — the per-gene citation and rationale.

## Provenance
Source: Track A locus resolution (GWAS Catalog + eQTL Catalogue via the human-genetics connector),
artifact b6ba3948-057c-4d8a-98c4-ef5189e845d7. Class mapping and reconciliation to the dashboard's four-class
table documented in the build cell. No numbers recomputed from memory.

## Known enumeration note
This ledger's 15 genes use the RESEARCH_SYNTHESIS enumeration (includes LTO1, excludes ORAOV1/canonical LTO1)
— the same list as the dashboard §3 four-class table. A one-gene symbol-resolution edge case vs. the §3
dark-matter list (ORAOV1↔LTO1) is documented in project_dashboard.md and not silently reconciled here.
