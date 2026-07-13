# Real ↔ toy field mapping — INTERNAL ONLY

> **Do not share this file with the consultant.** It exists so we can drop the production data onto
> whatever gets prototyped against the toy dataset. The toy is a faithful structural mirror, so
> "swap in real data" = produce the same JSON shapes from our real tables using this dictionary.

## Concept mapping

| Toy concept | Real concept | Real source |
|---|---|---|
| entity / "suspect" (codename) | a node in the harmonized substrate | `data/processed/nb7_substrate_nodes.csv` (`gene`) |
| evidence channel / source | an evidence *layer* | node/edge `supporting_layers` (Raghunath, GRN, OmniPath, STRING×2, KEGG, Reactome) |
| `n_channels` (convergence) | `n_edge_bearing_layers` | nb7 nodes |
| relationship / edge | a substrate edge | `data/processed/nb7_substrate_edges.csv` |
| edge `channels` / `n_channels` | edge `supporting_layers` / `n_supporting_layers` | nb7 edges |
| edge `sign` / `sign_conflict` | `merged_sign` / `sign_conflict` | nb7 edges |
| directed `sequence` | the endorsed directed causal chain (the "spine") | NB10/NB7 pathway; the ordered mechanism |
| per-entity `verdict.tier` | our per-entity classification tiers | NB8 buckets; NB10/NB12 direction calls; NB4 tiers |
| `verdict.strands` (channel+finding+source) | the convergent-evidence strands per entity | NB8 evidence matrix / per-node layer evidence |
| `benchmark` (culprits/innocents/decoys) | the validation sets w/ adversarial negatives | NB10 (22/22), NB12 (29/33), NB8 diagnostic |
| `contexts` (two cases) | the switchable axes | disease/phenotype context; or ancestry (NB11) |
| `provenance` / `references` | citation strings + provenance sidecars | `citation` cols; `data/external/db_responses/` |

## Flag mapping

| Toy flag | Real flag |
|---|---|
| `on_watchlist` / `watchlist_class` | `omim_disease_flag` / `omim_phenotype_class` |
| `physical_evidence` | `massspec_detected_flag` |
| `field_flagged` | `bajpai_hit_flag` (functional screen hit) |
| verdict tier `decoy_cleared` | an adversarial/bioactive decoy correctly rejected |

## Distribution parity (already matched by the toy)

- entity→#layers heavy tail (most 1–2, tiny 5–6 core) ✔
- 2 broad layers + selective tail ✔
- ~87% single-layer edges ✔
- mostly-unsigned edges + signed minority + 1 conflict ✔
- benchmark with adversarial decoys, clean scoreboard ✔

## Execution note

The real graph is already exported as `interactive/nb7_multilayer_graph.json`. To feed a prototype,
write one small adapter that emits the toy's JSON shapes (`entities/edges/sequence/verdict/benchmark/
contexts/references`) from our real tables using the mapping above. Everything the consultant builds
against the toy schema then renders the real data with no UI changes.
