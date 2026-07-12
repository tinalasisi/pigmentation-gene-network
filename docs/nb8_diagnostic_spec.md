# NB8 — Rescue-screen diagnostic spec

**Purpose.** Diagnostic (not a build): does each of the 18 EFFECTOR-UNCERTAIN pigmentation loci
(nearest gene NOT a canonical effector) connect into melanogenesis via a NON-CIRCULAR route?
Negatives count.

## Inputs
- `data/processed/provisional_effector_uncertain_18.csv` — the 18 loci (Ang2023, Morgan2018).
- `data/processed/nb7_substrate_{nodes,edges}.csv` — 803 nodes / 7819 tiered edges.
- `data/processed/nb6_grn_edges.csv` — 58 signed MITF/SOX10/PAX3 regulon edges.
- `data/processed/nb5_reactome_only_connection_set.csv` + `data/external/db_responses/reactome_mitf_subpathway_structure.json`
  — pigmentation subpathway R-HSA-9824585 (29 pigment-tagged of the 121; gate on tag; never "N of 121").
- `data/raw/papers/Zhang2018_GenomeRes_MelanocyteEQTL/..._Supplementary_Tables.xlsx` — MELANOCYTE eQTL
  (header=1). T-S6=379 curated genes w/ melanocyte eGene q; T-S9=trans-eQTL; T-S10=IRF4-mediated trans;
  T-S15=melanocyte colocalization of pigmentation GWAS.
- `data/processed/bajpai2023_crispr_hits.csv` (asymmetric: hit corroborates, non-hit is NOT counter-evidence).
- `data/external/db_responses/kegg_hsa04916.json` — melanogenesis core anchor (101 genes).

## Evidence lines screened per candidate gene (all six)
a. direct substrate edge to a core gene (report core gene + best tier + n_layers)
b. GRN regulon membership (MITF/SOX10/PAX3 target, signed, confidence tier)
c. Reactome pigmentation subpathway membership — GATED on pigment-vs-MITF-program tag; reported separately
d. melanocyte eGene / melanocyte coloc (Zhang) — tissue-correct, PI-critical
e. shortest path <=2 hops to any core gene (report intermediate + weakest edge tier on path)
f. verifiable known biology (confirmed via MyGene/Reactome connector, e.g. ATRN=attractin/mahogany, LRMDA=OCA7, SIK1-CRTC-CREB-MITF)

## Grading
Convergence A/B/C from INDEPENDENT lines. gwas_replicated additive (never a gate). Bajpai asymmetric.
T3_STRING = association only, not mechanism.

## Buckets
- NONCANON  = connected via non-canonical route (candidate finding)
- CANON     = connected only via canonical neighbour (likely regulatory-of-canonical; NOT our finding)
- MANUAL    = needs manual paper review
- NEG       = no connection (negative)

## Outputs
- `notebooks/08_rescue_screen_diagnostic.ipynb` (self-contained, TL;DR header, evidence-matrix figure)
- `data/processed/nb8_diagnostic_18.csv` (per-locus: paper, rsid, nearest_gene_label, melanocyte_eqtl_gene,
  connection_route, connecting_edges, tiers, convergence_grade, bucket, confirming_experiment, notes)
- `notebooks/figures/nb8_evidence_matrix.png`

## Verdict (see notebook TL;DR)
5 NONCANON / 5 CANON / 2 MANUAL / 6 NEG — but no NOVEL network-discovered effector. Strongest hit LRMDA is a
known albinism gene (mislabeled into the uncertain set). Melanocyte-vs-bulk correction retracts 3 bulk L2G calls
(TECRL, RAB11FIP2, CCND1) and confirms LRMDA/IRF4/SLC24A4. No git commit.
