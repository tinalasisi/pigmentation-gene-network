# Project dashboard — pigmentation gene-network build

**Status: TENTATIVE (first version created 2026-07-12T01:41Z).** Snapshot / control surface for the project. This
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

## Where the project is now (as of 2026-07-12T01:41Z)

- **Execution route settled and PI-approved:** the convergence-graded rescue screen, built as notebooks
  **NB4–NB8** (unified association base → compare candidate networks → harmonized multi-layer substrate →
  resolution + convergence-graded rescue screen → optional population conditionality). Six decisions behind
  it are in `CHANGELOG.md` 2026-07-12T00:29Z; phase tracking is in `TODO.md`.
- **Foundation (NB1–NB3) is stable and committed.** The Raghunath network reconstruction (NB1), its
  gene-resolution + OmniPath validation (NB2), and the curated discordance-case assembly (NB3) are the
  confident base the rescue screen builds on. **NB2 reproducibility was restored and committed** (`95f1969`,
  see `CHANGELOG.md` 2026-07-12T01:16Z) — a fresh clone can now re-run NB2 offline.
- **NB4–NB5 are in progress in a concurrent session.** Their outputs (`nb5_*.csv`,
  `discordance_loci_author_explained.csv`, the `darcy2023_S*.csv` extracts) are **on disk but not yet
  committed** — see the inventory. Their counts are deliberately not pinned here until the notebooks and
  outputs are committed and stable.
- **Dashboard status: tentative.** This is the first version; the phase-status detail lives in `TODO.md`,
  which is the authority. As NB4–NB8 outputs are committed, promote them from the "in-flight" inventory
  group to the Key-metrics table.

## Key metrics — committed foundation ONLY

Load-bearing counts for the **stable, committed** NB1–NB3 outputs. Each row cites the pinned file and
reconciles against it mechanically (`pigmentation-plan-sync` → `check_plan_sync()`). In-flight NB4/NB5
numbers are **intentionally excluded** — pinning a volatile number is what caused previous plans to drift.

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
- NB4–NB8 notebook files do **not exist yet**; the concurrent session is producing their outputs first.

**Committed processed foundation (`data/processed/`, tracked)** — pinned above where load-bearing:
- `raghunath_nodes_typed.csv`, `raghunath_edges_typed_signed.csv` — NB1 raw typed/signed network.
- `node_resolution.csv` (+ `.meta.json`), `complex_members.csv`, `chem_resolution_evidence.csv` — NB2 resolution intermediates.
- `gene_network_nodes.csv`, `gene_network_edges.csv` — NB2 resolved gene network.
- `gene_graph_nodes.csv`, `gene_graph_edges_projection.csv`, `gene_graph_edges_topology.csv` — NB2 graph layers.
- `nb2_omnipath_validation.csv`, `nb2_backbone_cited.csv`, `nb2_projection_cited.csv` — NB2 validation + citation tables.
- `discordance_loci.csv`, `discordance_case_classification.csv` — NB3 curated cases.
- `bajpai2023_crispr_hits.csv`, `baxter2018_650_pigmentation_genes.csv`, `hirisplexs2018_markers.csv` — extractor outputs (01a–01c).

**In-flight, UNCOMMITTED (`data/processed/`, on disk in a concurrent NB4/NB5 session — do not pin counts, do not commit from here):**
- `discordance_loci_author_explained.csv` — NB4 author-explanation-status extension of the discordance loci.
- `darcy2023_S1_disease_genes.csv`, `darcy2023_S2_sysgo_annotation.csv`, `darcy2023_S4_string_edges.csv`, `darcy2023_S5_string_nodes.csv`, `darcy2023_S6_massspec_expression.csv` — NB5 D'Arcy 2023 supplement extracts.
- `nb5_gene_set_membership.csv`, `nb5_raghunath_string_edge_coverage.csv`, `nb5_string_drift_darcy_vs_ourpull.csv`, `nb5_darcy_only_phenotype_overlay.csv` — NB5 candidate-network comparison outputs.

**Frozen DB responses (`data/external/db_responses/`, tracked)** — NB2 offline inputs (restored in `95f1969`):
- `uniprot_annotation_direct.json` (+ `.meta.json`), `hgnc_gene_groups.json`, `pomc_cleavage_refs.json`, `omnipath_internal.json` (+ `omnipath.meta.json`), `kegg_hsa04916.json`.

**Figures (`notebooks/figures/`, tracked):** `step2_annotation_types.png`, `step4_gene_layer_edges.png`, `step5_network_overview.png`, `step5_centrality.png`, `step6_validation_verdict.png` — NB2 figures, now generated by NB2 cells 8/15/20/22/27 (generating code restored 2026-07-12T01:44Z; regenerated PNGs pending commit).

**Internal governance (`internal/`):** `START_HERE.md`, `CHANGELOG.md`, `TODO.md`, `PROJECT_EVOLUTION.md`, `TRACEABILITY_coverage_and_resolution_logic.md` (tracked); this `project_dashboard.md` (tentative, being committed); `archive/`, `untracked/` (gitignored); `handoffs/` (agent coordination).

**Raw inputs (`data/raw/`, `data/case_records/`):** source papers/supplements and the 13 `EXTRACT_*.csv` case records — see `DATA_SOURCES.md` for provenance and licensing per source.

## How to keep this current (the anti-drift contract)

This document reconciles against the files and the living documents, **never against memory**. Do the
following in the SAME turn as the change, then re-save this file as a new version of its single artifact:

1. **A committed foundation CSV changes** → run `check_plan_sync(repo_root=...)` from the
   `pigmentation-plan-sync` skill; fix every `DRIFT`/`missing_file`; copy new numbers from
   `compute_canonical_facts()`, never retype them.
2. **An NB4–NB8 output is committed and stabilizes** → move it from the "in-flight" inventory group to the
   Key-metrics table (if load-bearing) or the committed inventory, and add its stem so the orphan scan stays
   clean.
3. **Scope/route changes** → update the "Where the project is now" prose to match the latest `CHANGELOG.md`
   entry; do not restate phase status here (that is `TODO.md`'s job) — point to it.
4. **Never** duplicate the changelog's history or the TODO's open-work list here. A second copy is a second
   source of truth, and the two silently diverge.
5. **Stamp every "now" with a full UTC datetime** (`YYYY-MM-DDTHH:MMZ`), never a bare date — the project
   convention (`START_HERE.md`), because work spans many hours across days. When you refresh the "Where the
   project is now" section, update its `as of` timestamp in the heading to the current datetime.

_Single backing artifact; update in place via `save_artifacts(version_of=...)`. Do not create `*_v2` /
`*_final` copies._
