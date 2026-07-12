# Spec — `data/processed/nb6_grn_edges.csv`

**Produced by:** `notebooks/06_gene_regulatory_network.ipynb`
**Source data:** `data/external/db_responses/omnipath_internal.json` (frozen 2026-07-09, re-used from NB2) +
`data/external/db_responses/omnipath_dorothea_level_mitf_sox10_pax3.json` (frozen 2026-07-12, this notebook).

## What this is

The gene-regulatory-network (GRN) layer: directed, signed TF→target transcriptional regulation edges for
the three melanocyte master regulators present in the frozen data (MITF, SOX10, PAX3). This is the
**primary and only edge-bearing layer** for NB6 — curated DoRothEA/CollecTRI regulons, not ChIP-seq binding
peaks (excluded as a category error).

## Row count

58 edges total: MITF 34, PAX3 19 (18 DoRothEA/CollecTRI-curated + 1 hand-added literature edge, `PAX3->RET`,
cited to two live-verified PMIDs: 11032856 and 12668617), SOX10 5.

## Columns

| Column | Type | Description |
|---|---|---|
| `source_TF` | str | Transcription factor (`MITF`, `SOX10`, or `PAX3`). |
| `target` | str | Target gene symbol. |
| `sign` | str | `activation` / `repression` / `ambiguous` (conflicting stimulation+inhibition evidence, OmniPath consensus fields could not resolve) / `unsigned`. |
| `confidence_tier` | str | DoRothEA A–E benchmark tier where available (`A` highest); `CollecTRI(ungraded)` for CollecTRI-only literature-mined edges with no DoRothEA benchmark level; `literature-added(low-confidence)` for the one hand-added PAX3→RET edge. |
| `citation` | str | `PMID:<comma-separated PMIDs>` when the aggregator record exposes one, else an explicit statement that the row is an OmniPath-curated aggregator record with no PMID field. Every row is non-blank (citation-completeness gate asserted in the notebook). The hand-added `PAX3->RET` row carries two live-verified PMIDs (`PMID:11032856;PMID:12668617` — Lang et al. 2000, J Clin Invest 106:963-971 and Lang & Epstein 2003, Hum Mol Genet 12:937-945), confirmed via PubMed/JCI/HMG before being written to this table. |
| `edge_provenance` | str | Free-text description of where the edge came from (regulon-resource frozen pull, or the hand-added literature edge). |
| `omnipath_sources` | str | `;`-joined list of every OmniPath `sources` tag backing the edge (e.g. `CollecTRI;DoRothEA;TRRUST`). |
| `n_pmids` | int | Count of distinct PMIDs found in the merged `references` field across all underlying OmniPath rows for this (TF, target) pair. |
| `mixed_sign_evidence` | bool | True when the underlying OmniPath row's raw `is_stimulation` AND `is_inhibition` are both True (mixed cross-source evidence), even where `consensus_*` resolved a majority sign. |
| `note` | str | Free-text caveat; non-empty for every PAX3 edge (lower-confidence, literature/database-curated, no melanocyte ChIP-seq support as of this pull). |

## Known exclusion (by design, not omission)

`PAX3 -> LEF1` (SIGNOR-only, not DoRothEA/CollecTRI-backed) exists in `omnipath_internal.json` but is
excluded from this table — the adjudicated scope for NB6 is DoRothEA/CollecTRI regulons only. It is
reported in the notebook (Step 3) for transparency but never written to this CSV.

## Reproducibility

Both frozen inputs are committed under `data/external/db_responses/`. The notebook's Step 2 carries a
visible, re-runnable query cell (`REQUERY_DOROTHEA_LEVEL`) documenting the exact OmniPath REST call that
regenerates `omnipath_dorothea_level_mitf_sox10_pax3.json`; the notebook itself runs offline from the
committed JSON.
