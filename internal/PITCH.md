# PITCH — pigmentation gene-network rescue screen

**Living document — updated as each notebook lands. Last update: 2026-07-12 (Phase 1 complete: NB4–NB6).**

## The flagship (one finding, layered evidence)

A reproducible, **convergence-graded rescue screen**: take pigmentation loci their own authors reported but
**could not mechanistically explain** (52 author-unexplained of 105 curated), resolve each to a causal gene
(Open Targets L2G + melanocyte-appropriate eQTL), and test whether it connects into the **melanogenesis
network** through a tagged multi-layer substrate — grading each rescue by how many **independent evidence lines
converge**, and naming **one confirming experiment** per rescued locus. It is ONE finding, anchored by a named
hero locus — not six notebooks.

## The three pitch answers (keep current)

1. **What did Claude Science help us do?** — curate author-explanation status of 105 loci from full PDFs;
   assemble a multi-layer substrate with per-edge provenance; resolve unexplained loci to causal genes in the
   right tissue; grade rescues by convergence — at weekend scale, fully reproducible.
2. **How are we closer to a finding?** — N author-unexplained loci now connect to melanogenesis, each graded,
   each with a confirming experiment; anchored by one named hero locus. *(N filled in at NB8.)*
3. **What is the flagship?** — the hero-locus rescue + the honest, reproducible convergence-graded catalog.

## Positioning

Within the systems-population-genetics lineage. This rescue/convergence contribution is **distinct** from the
R21's gene-property prediction — it is not "not novel."

> _Suggested anchor references (from the PI's final-day directive §9, NOT yet verified against the papers in
> this repo — confirm each citation before it goes in any public deliverable): Fagny & Austerlitz 2021;
> Daub 2013; signet / Gouy 2017; the network-propagation family._

## Progress (notebook by notebook)

| NB | Question | Key result | Status |
|----|----------|------------|--------|
| NB4 | Unified association base | 105 curated → **52 author-unexplained** → **27 also GWAS-Catalog-replicated** (replicated + off-canonical + author-unexplained = the rescue targets). `gwas_replicated` is an additive convergence annotation, never a gate. | ✅ |
| NB5 | Compare candidate networks | Bajpai CRISPR added as a node layer (142 orphan hits in no curated network); networks-typology table; **"the network you choose changes the answer"** — our STRING pull recovers 60% of Raghunath's edges, agrees only 66% with D'Arcy's frozen STRING (34% drift). | ✅ |
| NB6 | Gene regulatory network | **58 curated-regulon TF→target edges** (MITF 34, PAX3 19, SOX10 5), directed + signed, DoRothEA A–E tiered, every edge cited. MITF directly activates 8 core pigmentation genes. No ChIP-seq peaks (binding≠regulation). | ✅ |
| NB7 | Harmonized multi-layer substrate | Merge all layers into one tagged node/edge table, per-edge provenance + tier; resolve the STRING enzyme-class-token artifact. | 🔄 building |
| NB8 | **Rescue + convergence grade + HERO SHORTLIST** | The deliverable. Per-locus rescue test, convergence grade, named confirming experiment; ranked 3–5 hero shortlist → STOP, surface to PI. | ⏳ |
| NB9 | Population conditionality | Future-directions NARRATIVE only (effector rerouting: SLC24A5 / TYRP1-Oceania / OCA2-E.Asia / MFSD12-Africa). | ⏳ |

## Honest-count discipline

Report the count as measured; do not force a headline. The Reactome-reaction rescue class is gated on
sub-pathway tags: **29 pigmentation-tagged reported separately from the 92 MITF-program genes** — never one
inflated "N of 121." GWAS replication is an additive convergence line, never a candidate filter. Bajpai
corroboration is asymmetric — "not a hit" is not evidence against.
