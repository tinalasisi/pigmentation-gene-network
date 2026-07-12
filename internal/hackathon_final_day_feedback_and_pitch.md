# Final-day directive for Claude Science — pitch north star, scope, and the GWAS plan

**From:** T. Lasisi (PI) · **Date:** 2026-07-12 · **Hard constraint: ~1 day of hackathon left.**
**Prime directive: ship the flagship *finding*, not the scaffolding.** Researcher Track — presentation serves the
finding. Build the flagship path, **STOP at the hero shortlist, and surface it to the PI.** Everything cosmetic
or infrastructural is Claude Code's, not yours (see §5).

## 1. The flagship (north star — install in START_HERE + a living PITCH.md)
A reproducible, convergence-graded **rescue screen**: take the pigmentation loci that are genuinely
**effector-uncertain** — which gene is causal is truly open (14 of 105 curated; 34 with Kim 2024 folded in;
this supersedes the coarse "52 author-unexplained" tag, which swept in 43 canonical-gene loci), resolve each to a causal gene
(Open Targets L2G + melanocyte-appropriate eQTL), and test whether it connects into the **melanogenesis
network** through a tagged multi-layer substrate — grading each rescue by how many **independent evidence lines
converge**, and naming **one confirming experiment** per rescued locus.

**It is ONE finding with layered evidence, not six notebooks.** Each layer earns its place by what it
rescues/corroborates:
- GRN regulons (NB6): loci that connect ONLY via an MITF/SOX10 regulatory edge → "regulon layer uniquely rescued K."
- Bajpai CRISPR: "J rescued genes are also CRISPR hits" (corroboration; asymmetric — absence ≠ evidence against).
- Melanocyte eQTL: "M resolutions used or were corrected by melanocyte-specific eQTL vs bulk skin."

**Keep these three pitch answers current in PITCH.md:**
1. *What did Claude Science help us do?* — curate author-explanation status of 105 loci from full PDFs; assemble
   a multi-layer substrate with per-edge provenance; resolve unexplained loci to causal genes in the right
   tissue; grade rescues by convergence — at weekend scale, fully reproducible.
2. *How are we closer to a finding?* — N effector-uncertain loci now connect to melanogenesis, each graded, each
   with a confirming experiment; anchored by one named **hero locus**.
3. *What is the flagship?* — the hero-locus rescue + the honest, reproducible convergence-graded catalog.

## 2. THE priority: turn RESOLUTION into RESCUE, then surface a HERO SHORTLIST
The 52 loci are already RESOLVED to causal genes (`data/processed/locus_causal_resolution.csv`). The missing
piece — the whole point — is the **rescue step**: for each resolved gene, test whether it connects into the
melanogenesis substrate (NB7/NB8), grade convergence, name the confirming experiment. Then **surface a ranked
shortlist of 3–5 hero candidates to the PI**, one line each: *locus · author's "unexplained" status · resolved
causal gene · the SPECIFIC route into melanogenesis (which layer/edge — flag if the GRN-regulon or
melanocyte-eQTL layer uniquely enabled it) · convergence grade · confirming experiment.* The PI picks the hero;
**only then is the hero card built.** Do NOT build the hero visual before a real network connection exists — we
need a rescue to hero about, not a bare gene assignment.

## 3. Build path (in order) — STOP at the hero shortlist
**NB4** (association base) → **NB5** (+ Bajpai node layer, lean) → **NB6** (promote the regulons already in
`omnipath_internal.json`; the optional UniBind ChIP-seq layer is genuinely optional — SKIP if pressed) →
**NB7** (harmonized substrate) → **NB8** (the deliverable: rescue + convergence grade + hero shortlist).
- One **rough, functional** figure per notebook to prove its result (see §8).
- Keep provenance discipline: frozen DB snapshots committed, per-edge citations, US spelling.
- **Report the honest count; do not force a headline.** Gate the Reactome-reaction class on sub-pathway tags
  (29 pigmentation-tagged reported separately from the 92 MITF-program genes) — never one inflated "N of 121."
- Supporting rigor (not the headline): keep NB5's network non-redundancy + STRING **~66% agreement / ~34%
  drift** finding foregrounded — *"the network you choose changes the answer."*

## 4. The GWAS Catalog — how to use it (recovered; role clarified)
- **Recovered + committed, offline:** `data/external/gwas_catalog/pigmentation_gwas_catalog.csv` (1,072 assoc,
  deduplicated to one lead row per rsID) + `gwas_pigmentation_associations.csv` (723 granular associations).
  **The EBI download endpoint is still HTTP 500 — work offline, do NOT live-pull.** These frozen copies are the
  reproducible input; regenerate later via `scripts/pull_gwas_associations.py`. Never write frozen data under
  gitignored `/output/` again (that gap is why the pull was lost).
- **Denominator (NB4):** fold the 1,072 in as the reported-associations base — rsID-join to the curated set,
  build-tag, keep both provenance rows. The rsID overlap with the 52 gives a cross-source replication signal.
- **GWAS replication = a CONVERGENCE SIGNAL, never a candidate filter.** Compute per-gene replication from the
  *granular* file: `group by gene → gwas_n_assoc`; `gwas_replicated = gwas_n_assoc >= 2` (→ 83 replicated
  genes; mirrors `melanogenesis-constraints/analysis/pool_venn_gene_lists.py:98–102`). Do NOT use the
  deduplicated 1,072 for counts. **Attach `gwas_replicated` / `gwas_n_assoc` as an annotation and feed
  `gwas_replicated` into the convergence grade as ONE additive evidence line — NEVER as a gate that drops
  candidates.** A ≥2 filter used as a gate is backwards for our thesis: it keeps canonical nearest-genes and
  discards the off-canonical / singleton / novel loci that ARE the rescue targets. The strongest story = a
  locus that is **replicated (real signal) + off-canonical (GWAS/authors couldn't explain it) + rescued (we
  found the route).** Gene-level is sufficient (per PI); per-SNP not required.
- **OPTIONAL stretch — rescue off-canonical GWAS loci (the scaled thesis):** beyond the 52, you MAY take GWAS
  Catalog loci whose mapped gene is NOT a canonical melanogenesis gene, resolve each to its *causal* gene via
  L2G/eQTL (fixes nearest-gene-mislabeled / effectively-intergenic loci), and rescue-test. Label as a stretch;
  **the effector-uncertain curated set remains the flagship** (14 of 105; 34 with Kim 2024 — not the coarse 52-tag). Do NOT gene-filter these out.

## 5. KEEP OUT of your plan — Claude Code does these (don't spend agents/tokens)
- the **website / Quarto site** (`index.qmd`) — do not build or touch it;
- **figure polish / final design / shared palette** — rough functional figures only; the PI + Claude Code perfect them;
- the polished flagship visuals (hero rescue card, convergence overview, substrate schematic, layer bar);
- **GWAS-Catalog 36-paper author-explanation mining** — skip (post-hackathon);
- **NB9 population allele-frequency-across-layers computation** — write a short "future directions /
  population-conditionality" NARRATIVE only (effector-rerouting is already curated: SLC24A5 / TYRP1-Oceania /
  OCA2-E.Asia / MFSD12-Africa). It's the parked network-FST-adjacent thread = R21/future material.

Produce functional figures + the hero shortlist, then **STOP and surface to the PI.**

## 6. Cost — cheap agents
Default all worker/subagents to **Sonnet 5** (`model: 'sonnet'`) for mechanical work (extraction, resolution,
wrangling, rough figure code). Use **Opus only** for the hard synthesis (convergence-grading logic, hero
selection, final narrative). **Never below Sonnet 5.** The cheapest agent is the one you don't spawn — the
biggest saver is NOT expanding beyond the 52 (skip the 36-paper mining).

## 7. Legibility — every notebook PI-readable in 30 seconds
Each notebook gets a **TL;DR header**: *what it establishes · what data it pulls (named sources + counts) ·
what it contributes to the flagship · the one number/figure that matters.* (This fixes surprises like "I didn't
know OmniPath had regulons in NB2.") Maintain a single living **PITCH.md**, updated every time a notebook lands.

## 8. Visuals — rough functional only (Claude Code polishes)
Every notebook + key result gets ≥1 clear visual — the picture that *proves its one result* (correct data,
correct chart type, a title matching the data). If a key result can't be shown as a simple picture, it isn't a
key result. Suggested: NB4 = effector-status breakdown of the 105 (14 effector-uncertain vs 75 canonical-variant-gap); NB5 = network-overlap UpSet + the FALSIFIED hypothesis; NB6 = MITF
hub with its 34 signed targets; NB7 = tiered substrate; NB8 = rescue results + convergence grades. **Rough
only — no palette/aesthetic/website work.**

## 9. Positioning (cheap, protects credibility)
State the flagship inside the systems-population-genetics lineage — cite **Fagny & Austerlitz 2021**, **Daub
2013**, **signet / Gouy 2017**, the network-propagation family — and be explicit that this rescue/convergence
contribution is **distinct** from the R21's gene-property prediction, so it does not read as "not novel."

## 10. Process + docs
- Don't let overhead eat the day: **batch** the DATA_SOURCE_AUDITOR / REPRODUCIBILITY / SCICOMM / VISUAL
  reviews + compliance gate into ONE pass at the end. Don't serialize sign-off between notebooks.
- **Docs to update (your side):** START_HERE (north-star section), a living **PITCH.md**,
  `internal/project_dashboard.md`, `internal/CHANGELOG.md`, `internal/TODO.md`. (The Quarto site is Claude
  Code's, not yours.) Run the plan-sync; archive superseded plans.
