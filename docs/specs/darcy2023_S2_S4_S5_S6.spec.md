# darcy2023_{S2,S4,S5,S6}_*.csv — spec / provenance

## Source

- **Publication**: D'Arcy, C.E. & Kiel, C. (2023). *Network Analysis and Protein-Protein
  Interaction Prediction of Skin Pigmentation Genes*. Bioengineering, 10(1), 13.
- **DOI**: 10.3390/bioengineering10010013
- **PMC**: PMC9854651
- **License**: CC BY 4.0
- **Retrieval route**: Europe PMC `supplementaryFiles` endpoint (as for Table S1; see
  `darcy2023_S1.spec.md`). Raw files committed at `data/raw/darcy2023/Table S{2,4,5,6} Bioengineering
  FINAL.xlsx`.

These four tables decompose D'Arcy 2023 into layers distinct from the S1 OMIM disease-gene table
(`darcy2023_S1_disease_genes.csv`) — none of S2/S4/S5/S6 is itself a "D'Arcy STRING pull" that should be
conflated with S1; each has its own evidentiary character (annotation, PPI-association, or orthogonal
mass-spec expression).

## Table S2 -> `darcy2023_S2_sysgo_annotation.csv`

- **Content**: SysGO biological-process (Process 1-3) + STRING-cluster + subcellular main-location
  annotation for the same 243 S1 disease genes, plus A375/FM55 mass-spec presence/expression columns.
  Annotation only — contributes no genes beyond the 243 already in S1.
- **Sheet / header**: `Sheet1`, `header=3` (rows 0-2 are title/subtitle/spacer). `Sheet2` of the same
  workbook duplicates a STRING-edge-like table and is superseded by the dedicated S4 edge extraction below
  (not separately extracted, to avoid a duplicate, less-complete edge table).
- **Columns**: `gene`, `gene_id_sysgo`, `associations_to_disease`, `cluster_string_no_expansion`,
  `process_1`, `process_2`, `process_3`, `main_location`, `in_a375`, `expr_a375_lfq`, `in_fm55`,
  `expr_fm55_lfq`, `citation`, `citation_source`.

## Table S4 -> `darcy2023_S4_string_edges.csv`

- **Content**: STRING protein-protein interaction edges of the *expanded* network (243 S1 genes expanded
  by STRING to 451/452 nodes). 4,668 edges, `combined_score > 0.7` per the paper's own methods text.
  **Undirected, unsigned association** — not a mechanistic, directed, signed network. Treat as a distinct
  evidentiary layer from Raghunath's signed backbone, never merged into it silently.
- **Sheet / header**: `Sheet1`, `header=2` (row 0 = title, row 1 = spacer).
- **Columns**: `node1`, `node2`, `combined_score`, `citation`, `citation_source`.
- **Extraction fidelity check**: 4,668 rows extracted, matching the paper's reported edge count exactly.

## Table S5 -> `darcy2023_S5_string_nodes.csv`

- **Content**: node annotation for the expanded 451/452-node STRING network — SysGO process/location,
  a `disease_gene_flag` (gene symbol repeated when disease-associated) + `disease_gene_class` (the OMIM
  phenotype class, same controlled vocabulary as S1), and A375/FM55 mass-spec presence.
- **Sheet / header**: `Sheet1`, `header=2`.
- **Columns**: `gene_string`, `gene_sysgo`, `process_1`, `process_2`, `process_3`, `main_location`,
  `disease_gene_flag`, `disease_gene_class`, `in_a375`, `expr_a375_lfq`, `in_fm55`, `expr_fm55_lfq`,
  `citation`, `citation_source`.
- **Known source discrepancy (documented, not silently fixed)**: one gene symbol present as an S4 edge
  endpoint (`HLA-DQA1`) has no corresponding S5 annotation row; one STRING-ID (`IKBKB`) appears twice in S5
  as an exact duplicate row. Both are preserved verbatim from the source rather than corrected, and flagged
  here.

## Table S6 -> `darcy2023_S6_massspec_expression.csv`

- **Content**: label-free-quantification (LFQ) protein expression measured by mass spectrometry in A375
  (unpigmented) and FM55 (pigmented) melanoma cell lines — an experimental layer orthogonal to any of the
  curated gene lists, giving expression evidence rather than a gene-set membership claim.
- **Sheet / header**: two sheets (`Sheet1` = A375, `Sheet2` = FM55), both `header=3`.
- **Extraction**: outer-merged on gene symbol across both sheets (4,232 genes with LFQ in A375 and/or
  FM55; 33 A375-only, 30 FM55-only — genes detected in one cell line's proteome but not the other's).
- **Columns**: `gene`, `a375_lfq_average`, `a375_log_lfq`, `fm55_lfq`, `fm55_log_lfq`, `citation`,
  `citation_source`.

## Role in the project

All four tables are consumed by `notebooks/05_compare_candidate_networks.ipynb` as characterization layers
of the D'Arcy source, distinct from the S1 disease-gene set used for the primary node-level comparison
against Raghunath/KEGG/Reactome. Per-file `.meta.json` sidecars in `data/processed/` record extraction
method, row/gene counts, and frozen timestamp for each.
