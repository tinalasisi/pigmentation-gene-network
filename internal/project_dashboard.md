# Project dashboard — pigmentation gene-network build

**Status: MAINTAINED (first version created 2026-07-12T01:41Z; last reconciled 2026-07-13T16:29Z).** Snapshot / control surface for the project. This
is one of the three tracking documents described in `START_HERE.md`; it is **not** a plan and **not** a
history. It gives a one-screen orientation and then **points at** the living documents — it does not copy
them.

## What this document is (and is not)

- **It is** a thin snapshot: where the project is right now, the canonical pointers, and a file inventory.
- **It is not** the plan (that is a Claude Science artifact — id below), the history (`CHANGELOG.md`), or the
  open-work ledger (`TODO.md`). When any of those disagrees with this snapshot, **they win** — this file is
  derived from them, never the other way around.
- **Why it is built this way.** Earlier plan documents drifted because they duplicated load-bearing content
  (phase lists, per-file counts) that then went stale. This dashboard duplicates as little as possible: it
  pins numbers only for the **committed, stable foundation** (NB1–NB3 outputs, which change rarely) and
  refuses to pin counts for in-flight work (see the Key-metrics note). Everything volatile is a pointer.

## The living documents (read these for current truth)

| Document | Path | Role |
|---|---|---|
| Goal + orientation | `internal/START_HERE.md` | The one fixed thing (the goal) + asset inventory. Its "Current state" section is point-in-time; trust the changelog over it. |
| History (append-only) | `internal/CHANGELOG.md` | Every dated build/decision event. The authoritative record of what changed and why. |
| Open-work ledger | `internal/TODO.md` | What is done / in progress / next. The forward view. |
| Approved plan | Claude Science artifact `083f9097-0134-4490-abe9-33ad4ed7c9da` (version `d135912f-6112-48f4-95c1-545c46cabfba`), `plan_convergence-graded-rescue-screen-as-self_8a368b7b.json` | The exact phase/step text for the NB4–NB8 build. Read the artifact directly. |
| Provenance manifest | `DATA_SOURCES.md` (repo root) | Per-source licensing, query provenance, and redistribution policy. |

## Where the project is now (as of 2026-07-13T16:29Z)

- **⚠️ FLAGSHIP HAS MOVED — read this before anything below.** As of 2026-07-13, the flagship is the
  **per-origin module-selection architecture of primate sexual dichromatism**: hair dichromatism arose
  ~15 times independently across primates, and each origin tilts toward pigmentation-module or
  sex-hormone-module selection differently across the full range from pure-hormone to pure-pigmentation,
  with the trait lost ~9x faster than gained. This supersedes the "flagship framing is up in the air"
  status recorded below and in `START_HERE.md`/`TODO.md` (2026-07-12) — those documents have **not yet
  been updated** to reflect this move; see the changelog-gap note this session flagged. Source:
  `comparative-genomics/analysis/module_selection/` (notebook `module_selection_analysis.qmd`,
  `README.md`, commit `715fcce`), a per-lineage supporting analysis
  `comparative-genomics/analysis/coevolution_test/` (fitPagel correlated-evolution test, commit range
  through `2219a32`+ working tree), and the independent numerical verification at
  `internal/handoffs/notes/2026-07-13_independent_check_module_selection.md` (module-balance metric and
  Opie-analog transition rates both reproduced exactly from raw `results/perorigin_v1/` data, commit
  `4c07317`). The repo-root `README.md` has been updated to lead with this finding (this session); the
  comparative-genomics-level docs (`comparative-genomics/README.md`, `dichromatism.qmd`, `index.qmd`,
  `walkthrough.qmd`, `internal/PITCH.md`) still describe the prior "~15 independent origins, heterogeneous
  architecture, no flagship locked" framing and have **not** been reconciled to the module-balance result
  by this session (out of this session's scope — flagged for the next session/PI, per `changelog_gap_note`
  in this session's structured output).
- **Numbers to cite for this flagship (verified against `module_balance_results.csv` and
  `opie_analog_results.csv`; do not retype without re-reading those files):** 11 dichromatism origins
  carry a module-balance score `(nP-nH)/(nP+nH)` over aBSREL-significant (p<0.05) genes on that origin's
  tip branches; Eulemur (`origin_14`) is pure hormone (0 pigmentation / 1 hormone gene, balance −1.0);
  Pithecia (`origin_12`) is pure pigmentation (2/0, +1.0); Alouatta (`origin_11`, −0.5) and Colobus
  guereza (`origin_5`, −0.5) are hormone-tilted; Trachypithecus (`origin_7`) is the richest origin at
  8 pigmentation + 18 hormone genes (balance −0.385), and is one of 3 RELAX-powered (≥2-tip) origins
  alongside Nomascus (`origin_8`, POMC only) and Eulemur (`origin_14`, none). Trait dynamics
  (Opie-analog): gain rate 0.0273, loss rate 0.248 — loss ≈9.1x gain — ARD model preferred over
  equal-rates (dAIC 19.79). Both sets of numbers were independently recomputed from the raw
  `results/perorigin_v1/` data and matched exactly (see the verification note above).
- **Prior execution route (below) is superseded as the flagship but remains built and committed.**
  The convergence-graded rescue screen, built as notebooks
  **NB4–NB9** (unified association base → compare candidate networks → harmonized multi-layer substrate →
  resolution/rescue-screen diagnostic → optional population conditionality → Bajpai orphan reconciliation).
  Six decisions behind it are in `CHANGELOG.md` 2026-07-12T00:29Z; phase tracking is in `TODO.md`.
- **Foundation (NB1–NB3) is stable and committed.** The Raghunath network reconstruction (NB1), its
  gene-resolution + OmniPath validation (NB2), and the curated discordance-case assembly (NB3) are the
  confident base the rescue screen builds on. **NB2 reproducibility was restored and committed** (`95f1969`,
  see `CHANGELOG.md` 2026-07-12T01:16Z) — a fresh clone can now re-run NB2 offline.
- **CORRECTED (this bookkeeping pass): NB4–NB9 are BUILT AND COMMITTED, not in-progress.** The prior version
  of this section said NB4–NB5 were "in progress in a concurrent session, on disk but not yet committed" —
  that was accurate only through ~2026-07-12T01:09Z. All six notebooks (`04_unified_association_base` through
  `09_bajpai_reconciliation.ipynb`) and their processed outputs (`nb4_*` through `nb9_*.csv`,
  `discordance_loci_author_explained.csv`, `darcy2023_S*.csv`) are committed on `main` (commits `04e1b26`
  through `bbb8899`, 2026-07-12T01:09Z–03:02Z). `TODO.md`'s tracked-work table still shows these phases
  `⬜ not started` — that table is now stale and is flagged there for the next session to correct; this
  dashboard's prose is corrected here. Counts remain unpinned in the Key-metrics table below pending a
  dedicated numbers-reconciliation pass (see "How to keep this current," step 2).
- **NEW since the last dashboard update: two further tracks landed and committed (2026-07-12T10:34Z–12:36Z).**
  (1) The GWAS Catalog pull was widened (`REPORTED GENE(S)` + split initial/replication ancestry, `16bacb3`).
  (2) **NB11 — cross-ancestry population-conditional discoverability (Fst-graded)** —
  `notebooks/11_cross_ancestry_conditionality.ipynb` — quantifies 4 convergent genes (MFSD12, BNC2, SPIRE2,
  TSPAN10) discovered via population-private variants, plus a two-wave expansion (28-gene systematic screen;
  Martin et al. 2017 KhoeSan as a third population axis, 51 loci extracted, `EXTRACT_Martin2017_loci.csv`).
  This discharges the `TODO.md` "Deferred" item on the Martin pull. Detail in `CHANGELOG.md` 2026-07-12T12:36Z;
  status tracker in `TODO.md`'s new "Cross-ancestry / population-conditionality track (NB11, DONE)" section.
- **SUPERSEDED by the 2026-07-13 flagship move above.** The note below ("flagship framing is up in the air,"
  three candidate threads, none locked) was accurate as of 2026-07-12T~17:00Z. It is kept for continuity of
  the record, not as current status — the primate-phylogenetics thread it named as a parallel exploration is
  what has since become the module-selection flagship described at the top of this section.
- **NB10 + NB12 (mechanism→direction result) — leading demonstration candidate, framing softened
  (2026-07-12T17:00Z).** A positive melanin regulator mutated by a loss-of-function allele tends toward
  hypopigmentation — 22/22 network-called recessive/X-linked genes; a pre-registered expansion (NB12) adds a
  blind mechanism-classification source and reaches 29/33, base rate 54%, permutation *p*<1e-5. Validity-audited
  (blind LoF conditioning; no STRING sign; significance survives collapsing shared-complex genes to 15 units,
  *p*≈3e-6). **Reframed as a bounded METHODOLOGICAL demonstration, not a biological discovery:** a literature
  audit found the biological pieces are textbook (albinism is defined this way; Bajpai already tied screen sign
  to common-variant skin colour), so the contribution is "a single convergent functional readout orders a
  clinical property across a disease category, with a partly-predictable failure boundary." Honest limits kept
  central: failure boundary rests on n=4 (ATP7B is an unflagged high-confidence miss); near-circular for core
  genes; ascertainment reduced not eliminated. Reports in `internal/deconvolutor/`; full audit in
  `notebooks/12_direction_law_expanded.ipynb`. Files: `notebooks/{10_mechanism_direction_law,
  12_direction_law_expanded}.ipynb`, `nb10_direction_law_{annotation,summary}.csv`,
  `nb12_direction_law_expanded.csv`, `nb12_expanded_summary.csv`, figures `nb10_direction_law.png`,
  `nb10_validity_audit.png`, `nb12_direction_law_expanded.png`. Counts not pinned here until committed
  (anti-drift rule).
- **In parallel (PI, live): a primate-phylogenetics evolutionary direction** is being explored as another
  candidate. Not yet described on disk here; left untouched by this session to avoid conflicting with in-flight
  work.
- **Phylo-GRN methods thread (`internal/lit_review/phylo_grn_methods/`) — Tier 1 pilots DONE, Tier 2
  dispatched to cluster (2026-07-13T16:29Z).** Self-contained methods exploration, isolated from the
  module-selection flagship and `network-evo-explore/`. Local pilots ran: a GRN-neighbor
  selection-similarity permutation is a suggestive-but-underpowered positive (core 15 edges T_obs=0.137
  p=0.109; 18-edge substrate check T_obs=0.185 p=0.093); local partner-coevolution (mirrortree, ERC-from-
  aBSREL) is null/structurally degenerate at this edge count, by design. The definitive ERC/RERconverge
  coevolution test has been specced and handed to `claude-code/greatlakes-hpc`
  (`internal/handoffs/notes/20260713T162412Z__claude-science__pi-orchestrator-9c7c28bf__a90131.md`);
  awaiting paste-back. Detail: `CONCLUSION.md` in that folder and `TODO.md`'s new "Phylo-GRN methods
  thread" section.
- **Shelved:** the GWAS common-variant axis (5/35 clean genes; see the 2026-07-12 specialist review).
- **Dashboard status: maintained** (no longer first-version tentative). The phase-status detail lives in
  `TODO.md`, which is the authority. NB4–NB12 outputs are now committed and moved into the committed
  inventory groups below; their counts still await a dedicated numbers-reconciliation pass into the
  Key-metrics table (see that table's note).

## Key metrics — committed foundation ONLY

Load-bearing counts for the **stable, committed** NB1–NB3 outputs. Each row cites the pinned file and
reconciles against it mechanically (`pigmentation-plan-sync` → `check_plan_sync()`). NB4–NB12 outputs are now
committed (see the file inventory below) but their counts are **still intentionally excluded from this table**
pending a dedicated numbers-reconciliation pass — pinning a number before it has been read off the actual
committed file (not retyped from a changelog prose mention) is what caused previous plans to drift. The
`check_plan_sync()` run behind this bookkeeping pass reports 0 `DRIFT`/`missing_file` against the 7 rows below
and 18 `orphan_file` soft warnings — down from 40 before this pass's inventory update, now limited to
pre-existing effector-classification/resolution files and older `EXTRACT_*_v2.csv` case records that predate
this session and are out of its scope; the NB4–NB12/Martin/NB11 stems are now named in the file inventory.

| Metric | Count | Source file | Notebook |
|---|---|---|---|
| Raghunath network nodes | 265 nodes | `data/processed/raghunath_nodes_typed.csv` | NB1 |
| Raghunath signed/directed edges | 429 edges | `data/processed/raghunath_edges_typed_signed.csv` | NB1 |
| Entity→gene base symbols resolved | 183 base symbols | `data/processed/node_resolution.csv` | NB2 |
| Resolved gene-network nodes | 168 gene nodes | `data/processed/gene_network_nodes.csv` | NB2 |
| Gene-network edge rows | 309 edge rows | `data/processed/gene_network_edges.csv` | NB2 |
| Backbone edges validated vs OmniPath | 429 backbone edges | `data/processed/nb2_omnipath_validation.csv` | NB2 |
| Curated discordance loci (locus-first) | 105 loci | `data/processed/discordance_loci.csv` | NB3 |

## File inventory

Grouped by role. Each entry names its repo-relative path and repo status (tracked / uncommitted / absent).
Naming every processed-CSV stem here also keeps the plan-sync checker's orphan scan clean.

**Notebooks (`notebooks/`, all tracked)** — the unit of contribution:
- `01_reconstruct_published_network.ipynb` — NB1, Raghunath reconstruction (foundational).
- `02_resolve_network_to_genes.ipynb` — NB2, gene resolution + OmniPath validation (foundational; reproducibility restored).
- `03_assemble_validation_cases.ipynb` — NB3, curated discordance-case assembly.
- `01a_extract_bajpai_crispr.ipynb`, `01b_extract_baxter_genes.ipynb`, `01c_extract_hirisplex_markers.ipynb`, `01d_reproduce_gwas_catalog.ipynb` — supporting extractors (older standalone pattern; consolidation is a `TODO.md` backlog item).
- `04_unified_association_base.ipynb`, `05_compare_candidate_networks.ipynb`, `06_gene_regulatory_network.ipynb`, `07_harmonized_substrate.ipynb`, `08_rescue_screen_diagnostic.ipynb`, `09_bajpai_reconciliation.ipynb` — **NB4–NB9, BUILT AND COMMITTED** (`04e1b26`…`bbb8899`, 2026-07-12T01:09Z–03:02Z; corrected in this bookkeeping pass — see "Where the project is now"). The batched specialist review pass (DATA_SOURCE_AUDITOR/REPRODUCIBILITY_SPECIALIST/SCICOMM_REVIEWER/VISUAL_DATA_REVIEWER, plan step 5b) has not yet run.
- `10_mechanism_direction_law.ipynb`, `12_direction_law_expanded.ipynb` — NB10/NB12, mechanism→direction law + pre-registered expansion (independent session; committed `20768ac`).
- `11_cross_ancestry_conditionality.ipynb` (+ `11_cross_ancestry_conditionality_README.md`) — NB11, cross-ancestry population-conditional discoverability + two-wave expansion (independent session; committed `52d6679`…`9f7cb63`; new this bookkeeping pass).

**Committed processed foundation (`data/processed/`, tracked)** — pinned above where load-bearing:
- `raghunath_nodes_typed.csv`, `raghunath_edges_typed_signed.csv` — NB1 raw typed/signed network.
- `node_resolution.csv` (+ `.meta.json`), `complex_members.csv`, `chem_resolution_evidence.csv` — NB2 resolution intermediates.
- `gene_network_nodes.csv`, `gene_network_edges.csv` — NB2 resolved gene network.
- `gene_graph_nodes.csv`, `gene_graph_edges_projection.csv`, `gene_graph_edges_topology.csv` — NB2 graph layers.
- `nb2_omnipath_validation.csv`, `nb2_backbone_cited.csv`, `nb2_projection_cited.csv` — NB2 validation + citation tables.
- `discordance_loci.csv`, `discordance_case_classification.csv` — NB3 curated cases.
- `bajpai2023_crispr_hits.csv`, `baxter2018_650_pigmentation_genes.csv`, `hirisplexs2018_markers.csv` — extractor outputs (01a–01c).

**NB4–NB9 outputs (`data/processed/`, tracked and committed — corrected from "in-flight" in this bookkeeping pass; counts not yet promoted to the Key-metrics table above, pending a dedicated numbers-reconciliation pass):**
- `nb4_unified_association_base.csv`, `discordance_loci_effector_classified.csv` — NB4 unified base + per-locus effector-status classification (the 105 legacy rows, `paper != "Kim2024"`, are NB4's curated input). The superseded `discordance_loci_author_explained.csv` was removed from the repo on 2026-07-12 (its two audit columns migrated into the effector-classified file first; recoverable from git history — see CHANGELOG 2026-07-12).
- `darcy2023_S1_disease_genes.csv`, `darcy2023_S2_sysgo_annotation.csv`, `darcy2023_S4_string_edges.csv`, `darcy2023_S5_string_nodes.csv`, `darcy2023_S6_massspec_expression.csv`, `nb5_gene_set_membership.csv`, `nb5_raghunath_string_edge_coverage.csv`, `nb5_string_drift_darcy_vs_ourpull.csv`, `nb5_darcy_only_phenotype_overlay.csv`, `nb5_bajpai_network_enrichment.csv`, `nb5_bajpai_bipartite_melanin_endpoint.csv`, `nb5_networks_typology.csv`, `nb5_reactome_only_connection_set.csv` — NB5 candidate-network comparison outputs.
- `nb6_grn_edges.csv` — NB6 curated-regulon GRN.
- `nb7_substrate_nodes.csv`, `nb7_substrate_edges.csv`, `nb7_string_token_resolution.csv` — NB7 harmonized substrate.
- `nb8_diagnostic_18.csv` — NB8 diagnostic rescue test.
- `nb9_orphan_reconciliation.csv` — NB9 Bajpai orphan reconciliation.

**NB10–NB12 outputs (`data/processed/`, tracked and committed):**
- `nb10_direction_law_annotation.csv`, `nb10_direction_law_summary.csv` — NB10 direction-law calls + summary.
- `nb12_direction_law_expanded.csv`, `nb12_expanded_summary.csv` — NB12 pre-registered expansion.

**NB11 + Martin outputs (`data/processed/`, tracked and committed — NEW this bookkeeping pass):**
- `cross_ancestry_freq_matrix.csv` — 1000G per-population allele frequencies for the cross-paper convergent genes.
- `nb11_cross_ancestry_fst.csv` — Hudson Fst per convergent variant vs the genome-wide baseline.
- `nb11_multiancestry_screen_candidates.csv`, `nb11_screen_candidates.csv`, `nb11_screen_mirror_results.csv` — Wave-1 systematic mirror screen (28 genes).
- `nb11_martin_khoesan_freqs.csv` — Wave-2 KhoeSan third-axis frequencies.
- `EXTRACT_Martin2017_loci.csv`, `martin2017_COMPLETENESS_LEDGER.csv`, `martin2017_HONEST_GAPS.csv`, `martin2017_noncanonical_loci.csv` — Martin 2017 KhoeSan extraction (51 loci; spec `docs/specs/EXTRACT_Martin2017_loci.spec.md`).

**Also present in `data/processed/` (13 curated-paper `EXTRACT_*_v2.csv` case records, e.g. `EXTRACT_Crawford2017_loci_v2.csv`, `EXTRACT_Kim2024_loci_v2.csv`)** — tracked; predate this session, see `DATA_SOURCES.md` for per-source provenance.

**Frozen DB responses (`data/external/db_responses/`, tracked)** — NB2 offline inputs (restored in `95f1969`); NB11 adds `data/external/db_responses/nb11/` (1000G pulls) and `data/external/db_responses/nb11_screen/` (screen-wave pulls):
- `uniprot_annotation_direct.json` (+ `.meta.json`), `hgnc_gene_groups.json`, `pomc_cleavage_refs.json`, `omnipath_internal.json` (+ `omnipath.meta.json`), `kegg_hsa04916.json`.

**Comparative-genomics tree (`comparative-genomics/`, self-contained; see its own `README.md` for the
full pipeline/HPC layout) — NEW this reconciliation pass, current flagship source:**
- `analysis/module_selection/` (tracked, commit `715fcce`) — the flagship notebook
  `module_selection_analysis.qmd`, `figures.py`, `README.md`, 6 frozen inputs under `data/` (branch_rates,
  per_origin_K, origin_assignments, gene_modules, species_coding, primate_species_tree), and the two
  committed result tables `module_balance_results.csv` / `opie_analog_results.csv` plus
  `fig_module_balance.png` / `fig_per_lineage_genes.png`. **Untracked on disk as of this pass:**
  `data/tree_viz_inputs.rds`, `fig_circular_tree_balance.png` (disposition for the owning session, not
  decided here).
- `analysis/coevolution_test/` (tracked; `coevolution_test.qmd` modified and `README.md` untracked as of
  this pass) — the fitPagel correlated-evolution test and Pagel's lambda, a sibling check to
  module_selection, sharing its frozen `data/` inputs.
- `results/perorigin_v1/` (tracked, commit `4c07317`) — the raw per-origin RELAX (`per_origin_K.csv`) and
  full-panel aBSREL (`branch_rates.csv`, 9,229 branches × 78 genes) tables the module-balance metric and
  the independent verification note both recompute from.
- `results/figures/` — `fig_origins.png`, `fig_pooling.png`, `fig_tfap2a_tree.png`,
  `fig_tfap2a_branches.png` (the ~15-origins / pooling-problem / per-branch selection figures cited by
  `comparative-genomics/README.md`, `dichromatism.qmd`, `walkthrough.qmd`).
- Public-facing pages that still describe the **pre-module-selection** framing (heterogeneous
  architecture, no flagship locked) and have not yet been reconciled to the module-balance result:
  `dichromatism.qmd`, `index.qmd`, `walkthrough.qmd`, `internal/PITCH.md`,
  `comparative-genomics/README.md`. Flagged for the next session/PI, not corrected by this pass (see
  `changelog_gap_note`).

**GWAS Catalog (`data/external/gwas_catalog/`, tracked):** `pigmentation_gwas_catalog.csv` (+ `.meta.json`) — widened 2026-07-12T10:34Z (`REPORTED GENE(S)` + split initial/replication ancestry, `16bacb3`); `gwas_pigmentation_associations.csv` — gene-level replication source. **Untracked on disk:** `versions/pigmentation_gwas_catalog_refresh_20260712_20260712T144518Z.csv` (a timestamped archive snapshot from the widening refresh) — disposition (commit vs. scratch) is for the owning session.

**Figures (`notebooks/figures/`, tracked):** `step2_annotation_types.png`, `step4_gene_layer_edges.png`, `step5_network_overview.png`, `step5_centrality.png`, `step6_validation_verdict.png` — NB2 figures, now generated by NB2 cells 8/15/20/22/27 (generating code restored 2026-07-12T01:44Z; regenerated PNGs pending commit). Also tracked: `nb10_direction_law.png`, `nb10_validity_audit.png`, `nb12_direction_law_expanded.png` (NB10/NB12), `nb11_cross_ancestry.png`, `nb11_expansion_wave1_screen.png` (NB11), `cross_ancestry_conditionality.png` (population-conditionality figure), plus NB4–NB9 figures under the same directory.

**Internal governance (`internal/`):** `START_HERE.md`, `CHANGELOG.md`, `TODO.md`, `PROJECT_EVOLUTION.md`, `TRACEABILITY_coverage_and_resolution_logic.md`, `FINDINGS_MEMO.md`, `DEMO_direction_law.md`, `PITCH.md` (tracked); this `project_dashboard.md` (tracked, maintained); `deconvolutor/` (tracked, plan-critique reports); `archive/`, `untracked/` (gitignored); `handoffs/` (agent coordination).

**Raw inputs (`data/raw/`, `data/case_records/`):** source papers/supplements and the 13 `EXTRACT_*.csv` case records, plus the Martin 2017 KhoeSan source papers (gitignored per the spec's withholding statement) — see `DATA_SOURCES.md` for provenance and licensing per source.

## How to keep this current (the anti-drift contract)

This document reconciles against the files and the living documents, **never against memory**. Do the
following in the SAME turn as the change, then re-save this file as a new version of its single artifact:

1. **A committed foundation CSV changes** → run `check_plan_sync(repo_root=...)` from the
   `pigmentation-plan-sync` skill; fix every `DRIFT`/`missing_file`; copy new numbers from
   `compute_canonical_facts()`, never retype them.
2. **An NB4–NB12 output's numbers are ready to pin** → add a Key-metrics row (if load-bearing), copying the
   count from `compute_canonical_facts()`, never retyping it from changelog prose; the file inventory groups
   already list every current committed stem, so the orphan scan should shrink toward 0 as rows are added.
3. **Scope/route changes** → update the "Where the project is now" prose to match the latest `CHANGELOG.md`
   entry; do not restate phase status here (that is `TODO.md`'s job) — point to it.
4. **Never** duplicate the changelog's history or the TODO's open-work list here. A second copy is a second
   source of truth, and the two silently diverge.
5. **Stamp every "now" with a full UTC datetime** (`YYYY-MM-DDTHH:MMZ`), never a bare date — the project
   convention (`START_HERE.md`), because work spans many hours across days. When you refresh the "Where the
   project is now" section, update its `as of` timestamp in the heading to the current datetime.

_Single backing artifact; update in place via `save_artifacts(version_of=...)`. Do not create `*_v2` /
`*_final` copies._
