# Spec — NB9 orphan reconciliation (`nb9_orphan_reconciliation.csv`)

**Status:** DERIVED, produced by `notebooks/09_bajpai_reconciliation.ipynb`.
**Produced:** 2026-07-12. **Rows:** 142 (one per Bajpai CRISPR orphan). **US spelling** enforced.

## What this file is

The per-orphan reconciliation result behind the project's primary finding: the 142 Bajpai 2023
CRISPR-validated melanin genes that were "orphans" (in no curated pigmentation network), scored for how they
connect to the canonical melanogenesis core under a **symmetric** STRING pull.

## The finding it supports

142 of 169 Bajpai CRISPR hits (KO reduces melanin) were orphans **only because the original STRING pull was
seeded on the curated gene sets alone** (464-gene union). A STRING edge is returned only if *both* endpoints
are in the query set, so an orphan-to-curated edge was structurally unobservable. Re-querying STRING on the
**full 714-gene union of all layers** (symmetric seed; `string_union_symmetric_pull_v12.json`, STRING v12.0,
score>=700, 709 mapped, 5,446 edges) reconciles **93/142** orphans to the core within <=4 hops, up from a
structural **0** under the curated-only seed. This is the third "the choice changes the answer" result
(source, tissue, and now **seeding**).

## Core melanogenesis set (the reconciliation target, 23 genes)

TYR, TYRP1, DCT, MLANA, PMEL, OCA2, HERC2, MC1R, KIT, KITLG, MITF, SLC45A2, SLC24A5, EDNRB, EDN3, POMC, ASIP,
SOX10, PAX3, MLPH, RAB27A, MYO5A, GPR143.

## Columns

| column | type | meaning |
|---|---|---|
| `gene` | str | Orphan gene symbol (Bajpai hit, `n_sets==0` in `nb5_gene_set_membership.csv`). |
| `casTLE` | float | Bajpai `Combined_casTLE_Effect`. Uniform sign: KO reduces melanin (positive effector). Causal anchor. |
| `in_symmetric_graph` | bool | Gene is a node in the symmetric STRING graph. |
| `dist_to_core` | float | BFS shortest-path distance (STRING hops) to the nearest core gene; NaN if unreachable. |
| `nearest_core_gene` | str | The core gene at that distance. |
| `path_intermediates` | str | ` | `-separated intermediate genes on the shortest path (`(direct)` if adjacent). |
| `path_full` | str | Full `A -> ... -> core` shortest path (STRING preferred names). |
| `weakest_edge_score` | float | Minimum STRING score on the path (in [0.7,1.0]); the path is only as strong as its weakest link. |
| `in_GRN` | bool | Gene is a MITF/SOX10/PAX3 regulon target (`nb6_grn_edges.csv`). |
| `reactome_pig_tagged` | bool | Gene is in the curated Reactome pigmentation union. |
| `direct_core_adjacency` | bool | `dist_to_core == 1` (direct STRING edge to a core gene). |
| `hub_mediated_path` | bool | Path routes through a promiscuous STRING hub (BRCA1, GRB2, ACTB, ...); reachability inflated, flagged. |
| `n_convergence_lines` | int | Count of independent supporting lines (<=4-hop path, direct edge, GRN, Reactome-pig). |
| `convergence_grade` | str | A (>=3 lines), B (2), C (1); empty for knowledge-gap. |
| `bucket` | str | `reconciled` (dist<=4) or `knowledge-gap` (no <=4-hop core path even under symmetric pull). |
| `confirming_experiment` | str | Proposed test to promote the STRING association to mechanism (co-IP/BioID + epistasis double-KO). |
| `citation` | str | Bajpai CRISPR causal anchor (all rows) + STRING v12 (reconciled rows). Citation-completeness gate: 142/142. |

## Result summary (reproduced in-notebook)

- **Reconciled (symmetric seed, <=4 hops): 93** — vs **0** under the curated-only seed (headline: 0 -> 93).
- **Distance distribution (reconciled):** 1 hop: 1 · 2 hops: 38 · 3 hops: 35 · 4 hops: 19.
- **Convergence grade:** C (STRING path only): 92 · B: 1 (SLC24A4, direct MC1R edge) · A: 0.
- **Knowledge-gap residue: 49** — CRISPR-validated melanin genes with no <=4-hop path to core even under the
  symmetric pull (3 unmapped by STRING: AC002398.9, BLOC1S5-TXNDC5, C10ORF11).

## Guard rails (baked into the interpretation)

- STRING edges are **association** — undirected, unsigned. A path is a **hypothesis** (association-tier);
  sign/direction are NOT coerced onto it.
- The **CRISPR hit is the causal anchor**; STRING supplies candidate wiring, tested by `confirming_experiment`.
- Reconciliation is **thin**: 92/93 rest on a single line (STRING); GRN and Reactome corroborate 0; 22/93
  paths are hub-mediated. Reported honestly, not hidden.

## Inputs (frozen, in-repo; sha256 verified in the notebook)

- `data/external/db_responses/string_union_symmetric_pull_v12.json` (symmetric seed)
- `data/external/db_responses/string_network_pulls_v12.json` (curated-only seed, counterfactual)
- `data/external/db_responses/reactome_pigmentation_curated_union.json`
- `data/processed/bajpai2023_crispr_hits.csv`, `nb5_gene_set_membership.csv`, `nb6_grn_edges.csv`
