---
# Spec — `data/processed/nb7_substrate_nodes.csv` + `data/processed/nb7_substrate_edges.csv`

**Produced by:** `notebooks/07_harmonized_substrate.ipynb`
**Source data:** already-frozen/processed outputs of NB1/NB2/NB5/NB6 — no live network calls at run time.

## What this is

The harmonized multi-layer substrate for the pigmentation rescue-screen flagship — one node table and
one edge table merging six independent evidence layers, each tagged so a downstream notebook (NB8) can
identify exactly which layer supports any given node or edge:

1. **Raghunath et al. 2015** mechanistic melanogenesis network (T0, directed+signed) — DOI:10.1186/s13104-015-1128-6,
   *BMC Res Notes* 8:170.
2. **KEGG hsa04916 + Reactome curated union** (node-membership only; neither pull is an edge list).
3. **GRN TF→target regulons** from NB6 (T1, directed+signed transcriptional).
4. **OmniPath literature validation** from NB2 (T2b, edges only added for `confirmed`/`sign_conflict`
   verdicts already resolved to gene symbols).
5. **Our fresh STRING v12.0 pull** (T3, association, unsigned/undirected) — enzyme-class-token artifact
   resolved before attribution (see below).
6. **D'Arcy et al. 2023** Table S4 STRING PPI (T3, association) — DOI:10.3390/bioengineering10010013,
   PMC9854651, CC BY 4.0.

D'Arcy's OMIM disease-gene table (Table S1), mass-spec proteome (Table S6), and the Bajpai et al. 2023
CRISPR screen hit flags (from `nb5_gene_set_membership.csv`) are folded in as **node-level annotations
only** — by design they never create or delete an edge.

## Row counts

- **Nodes:** 803 genes (union of genes appearing in any edge/association-bearing layer: Raghunath, KEGG,
  Reactome, GRN, our-STRING post-token-resolution, D'Arcy-STRING).
- **Edges:** 7,819 unordered gene-pairs. Per tier: T0 Raghunath = 293, T1 GRN regulon = 39,
  T2b OmniPath validation = 1, T3 STRING association = 7,486. (A pair takes the *best*, i.e.
  lowest-numbered, tier across every layer that supports it — e.g. 18 of GRN's 57 unique pairs are also
  in Raghunath and are promoted to T0, leaving 39 GRN-only pairs at T1.)

## STRING enzyme-class-token artifact (resolved before attribution)

Six Raghunath nodes are enzyme-class placeholders (`PLA2`, `MMPs`, `Trypsin`, `Phosphodiesterase`, `PKC`,
`PLC`), each carrying an HGNC gene-group accession. Querying these literal token strings against STRING
causes its fuzzy symbol-matcher to resolve most of them to an unrelated single gene. Checked against the
frozen HGNC gene-group membership (`hgnc_gene_groups.json`):

| Token | STRING fuzzy match | Genuine HGNC group member? |
|---|---|---|
| PLA2 | (unmapped by STRING) | n/a |
| MMPs | BSG | No — spurious |
| Trypsin | PRSS1 | **Yes** — genuine |
| Phosphodiesterase | SMPDL3A | No — spurious |
| PKC | PRRT2 | No — spurious |
| PLC | HSPG2 | No — spurious |

Rule applied: attribute a STRING edge to the fuzzy match only when it is a genuine HGNC group member
(kept: `TRYPSIN`→`PRSS1`); otherwise drop the edge rather than mis-attribute it. **7 STRING edges were
dropped** for touching BSG/HSPG2/PRRT2/SMPDL3A as spurious fuzzy matches; **3,830 STRING edges were kept**
(union_all pull). All 6 class-token placeholder nodes remain in the node table
(`is_raghunath_enzyme_class_token=True`) as a record of the Raghunath T0 backbone's own topology, but
carry zero STRING-attributed edges beyond the genuine Trypsin case.

## Node-pair convergence

| n independent layers | n node-pairs |
|---|---|
| 1 | 6,799 |
| 2 | 882 |
| 3 | 114 |
| 4 | 17 |
| 5 | 7 |

1,020 pairs (13.0%) have convergence from >=2 independent layers; 138 pairs (1.8%) from >=3.

## Columns — nodes (`nb7_substrate_nodes.csv`)

| Column | Description |
|---|---|
| `gene` | Gene symbol. |
| `supporting_layers` | `\|`-joined list of edge-bearing layers containing this gene. |
| `n_edge_bearing_layers` | Count of the above. |
| `is_raghunath_enzyme_class_token` | True for the 6 Raghunath enzyme-class placeholder nodes. |
| `omim_disease_flag`, `omim_disease_names`, `omim_phenotype_class` | D'Arcy Table S1 OMIM annotation (node-only). |
| `massspec_detected_flag`, `massspec_a375_lfq`, `massspec_fm55_lfq` | D'Arcy Table S6 mass-spec annotation (node-only). |
| `bajpai_hit_flag`, `bajpai_castle_effect`, `bajpai_q_value`, `bajpai_direction`, `bajpai_orphan_hit` | Bajpai et al. 2023 CRISPR screen annotation (node-only). |
| `citation`, `citation_source` | `;`-joined resolvable citations from every supporting layer. |

## Columns — edges (`nb7_substrate_edges.csv`)

| Column | Description |
|---|---|
| `gene_a`, `gene_b` | Unordered gene-pair. |
| `source`, `target` | Directed orientation, populated **only** when a directed+signed layer (Raghunath or GRN) agrees on direction; else blank. |
| `merged_sign` | `+`/`-`/`unsigned`/`conflict` — derived **only** from directed+signed layers; never coerced from association layers (STRING) or the validation layer (OmniPath). |
| `sign_conflict`, `direction_conflict` | True when two directed+signed layers disagree. |
| `supporting_layers` | `\|`-joined list of layers asserting this pair. |
| `n_supporting_layers` | Node-pair convergence count. |
| `layer_evidence_type` | `;`-joined `layer:evidence_type` tags (e.g. `Raghunath:mechanistic_signed_directed`). |
| `tier` | Best tier across supporting layers: `T0_Raghunath` > `T1_GRN_regulon` > `T2b_OmniPath_validation` > `T3_STRING_association`. |
| `citation` | `;`-joined resolvable citations from every supporting layer. |

## Known exclusions / scope decisions (by design, not omission)

- **KEGG and Reactome contribute node membership only.** Both frozen pulls are gene lists (a KEGG
  pathway gene-link endpoint and a Reactome participants endpoint), not edge lists. Asserting
  all-pairs-within-pathway edges from a gene list would fabricate gene-gene relationships not supported
  by the source data — forbidden by this project's hard rules.
- **D'Arcy-OMIM, D'Arcy-mass-spec, and Bajpai never create nodes or edges.** They annotate genes already
  present via an edge-bearing layer. D'Arcy's mass-spec table in particular is an undifferentiated
  melanoma-cell-line whole-proteome background (4,232 genes, no pigmentation-pathway curation of its own)
  — including it as a node-creating layer would flood the substrate and destroy the meaning of
  "convergence."
- **9 direction conflicts + 1 sign conflict** among directed+signed layers are flagged, not silently
  resolved (mostly biologically plausible reciprocal/feedback loops, e.g. MITF/PAX3, NFKB1/TP53).

## Citation-completeness gate

Release-blocking check: every node and edge must carry >=1 resolvable citation. **PASSED** —
8,622 nodes+edges checked (803 nodes + 7,819 edges), 0 uncited.

## Reproducibility

Offline and deterministic — every input is already frozen/committed in-repo; no live network calls are
made in this notebook. Re-running `notebooks/07_harmonized_substrate.ipynb` end-to-end reproduces these
two CSVs and `data/processed/nb7_string_token_resolution.csv` exactly.
