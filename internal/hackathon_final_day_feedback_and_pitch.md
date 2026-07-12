# Feedback to Claude Science — final-day recalibration + the pitch north star

**From:** T. Lasisi (PI) · **Date:** 2026-07-12 · **Hard constraint: ~1 day of hackathon left.**
**Prime directive: ship the flagship finding, not the scaffolding. Presentation serves the finding (Researcher Track).**

## 1. Install this as the north star (update START_HERE, project_dashboard, CHANGELOG, and a new living PITCH.md)

**FLAGSHIP:** A reproducible, convergence-graded **rescue screen** that takes pigmentation loci their own
authors reported but **could not mechanistically explain** (52 author-unexplained of 105 curated), resolves
each to a causal gene (Open Targets L2G + **melanocyte-appropriate** eQTL), and tests whether it connects into
the **melanogenesis network** through a tagged multi-layer substrate — grading each rescue by how many
**independent evidence lines converge**, and naming **one confirming experiment** per rescued locus.

**It is ONE finding with layered evidence, not six notebooks.** Each layer must earn its place by what it
rescues or corroborates:
- GRN regulons (NB6): loci that connect ONLY via an MITF/SOX10 regulatory edge → "regulon layer uniquely rescued K."
- Bajpai CRISPR: "J rescued genes are also CRISPR hits" (functional corroboration; asymmetric — absence ≠ evidence against).
- Melanocyte eQTL: "M resolutions used or were corrected by melanocyte-specific eQTL vs bulk skin."

**The three pitch questions — keep answered and current in PITCH.md:**
1. *What did Claude Science help us do?* Curate author-explanation status of 105 loci from full PDFs; assemble a
   5-layer substrate with per-edge provenance; resolve unexplained loci to causal genes in the right tissue;
   grade rescues by convergence — at weekend scale, fully reproducible.
2. *How are we closer to a finding?* N author-unexplained loci now connect to melanogenesis, each graded, each
   with a confirming experiment; anchored by one named **hero locus**.
3. *What is the flagship?* The hero-locus rescue + the honest, reproducible convergence-graded catalog.

## 2. THE priority for tomorrow: turn RESOLUTION into RESCUE, then surface a HERO SHORTLIST
The 52 author-unexplained loci are already RESOLVED to causal genes
(`data/processed/locus_causal_resolution.csv`). The missing piece — and the whole point — is the **rescue
step**: for each resolved causal gene, test whether it connects into the melanogenesis substrate (NB7/NB8),
grade the convergence, and name the confirming experiment. Do that, then **surface a ranked shortlist of 3–5
hero candidates to the PI**, each as one line: *locus · author's original "unexplained" status · resolved
causal gene · the SPECIFIC route into melanogenesis (which layer/edge — ideally one the GRN-regulon or
melanocyte-eQTL layer uniquely enabled) · convergence grade · confirming experiment.* The PI picks the hero
from that shortlist; **only then is the hero card built.** Do NOT build the hero visual before the rescue step
exists — we need a real network connection to hero about, not a bare gene assignment. One vivid rescue beats a
flat comprehensive catalog.

## 3. Build vs. cut (given ~1 day)
**BUILD — the flagship path, in order:** NB4 base **from the curated 52** → NB5 (+ Bajpai node layer, lean)
→ NB6 (**promote the regulons already in `omnipath_internal.json`**; the optional UniBind ChIP-seq layer is
genuinely optional — SKIP if time-pressed) → NB7 harmonized substrate → **NB8 rescue + convergence grade +
hero locus.** NB8 is the deliverable.

**DEFER / DO NOT BUILD:**
- **GWAS-Catalog expansion — RECOVERED (2026-07-12).** The lost frozen pull was found in Downloads and
  **restored to a committed, non-gitignored path: `data/external/gwas_catalog/pigmentation_gwas_catalog.csv`
  (+ `.meta.json`)** — 1,072 pigmentation associations, 22 cols, queried 2026-07-08T01:15:41Z over 10
  EFO/OBA/MONDO roots. The EBI download endpoint is still HTTP 500, so **this frozen copy is the reproducible
  input — no live pull needed.** COMMIT it via the normal gate; never write frozen data under gitignored
  `/output/` again (that gap is why it vanished).
  **Use it in NB4** as the unified reported-associations base: rsID-join the 1,072 to the curated set,
  build-tag, keep both provenance rows — the overlap gives **replication counts that feed the convergence
  grade.** BUT keep scope honest for the one day left: the **flagship rescue still runs on the 52 curated
  author-unexplained loci** (already resolved in `data/processed/locus_causal_resolution.csv`). Full
  author-explanation-status mining of the 36 Catalog PMIDs is a **stretch, not a tomorrow requirement** — the
  1,072 give NB4 scale + replication context without it.
- **GWAS replication = a CONFIDENCE SIGNAL, never a candidate filter (PI-corrected — this changes the plan):**
  compute per-gene replication from the frozen granular file
  `data/external/gwas_catalog/gwas_pigmentation_associations.csv` (723 assoc): group by `gene` → `gwas_n_assoc`;
  `gwas_replicated = gwas_n_assoc >= 2` (→ 83 replicated genes, mirrors
  `melanogenesis-constraints/analysis/pool_venn_gene_lists.py:98–102`). Compute **OFFLINE** (EBI is HTTP 500);
  do NOT use the deduplicated 1,072 for counts. **CRITICAL: this annotation must NOT drop any rescue candidate.**
  A gene-level ≥2 filter used as a *gate* is backwards for our thesis — it keeps the well-replicated *canonical
  nearest-genes* and discards the singleton / off-canonical / novel loci, which are exactly the rescue targets.
  Our sell is *"GWAS is missing important loci and the network can rescue them,"* so the strongest story is a
  locus that is **replicated (real signal) + off-canonical (GWAS/authors couldn't explain it) + rescued (we
  found the route).** So: feed `gwas_replicated` into the **convergence grade as one additive evidence line —
  never as a gate.** Gene-level is sufficient (per PI); per-SNP not required.
- **OPTIONAL stretch — rescue OFF-CANONICAL GWAS loci (the scaled thesis):** beyond the 52 curated, you MAY take
  GWAS Catalog loci whose mapped gene is NOT a canonical melanogenesis gene, resolve each to its *causal* gene
  via L2G/eQTL (which fixes nearest-gene-mislabeled / effectively-intergenic loci), and rescue-test them. Label
  as a stretch; **the 52 curated remain the flagship.** Do NOT gene-filter these out.
- **Reproducibility:** the granular file regenerates via `scripts/pull_gwas_associations.py` (GWAS Catalog
  associations endpoint; re-run when EBI recovers) + a trivial column subset to `efo_id,trait,gene,snp_id,pvalue`.
  Until then the committed frozen file is the offline input.
- **NB9 allele-frequency-across-network-layers** — **do NOT compute the per-tier differentiation summary.**
  Write NB9 as a short "future directions / population-conditionality" NARRATIVE only (the effector-rerouting
  story is already curated: SLC24A5/TYRP1-Oceania/OCA2-E.Asia/MFSD12-Africa). Rationale: this is the parked
  network-FST-adjacent thread; half-built, it is exactly what the R21's population-genetics study section
  flagged. It is R21/future material, not a hackathon deliverable.

**PROCESS — do not let overhead eat the day:** batch the DATA_SOURCE_AUDITOR / REPRODUCIBILITY /
SCICOMM / VISUAL reviews + compliance gate into ONE pass at the end. Do NOT serialize full sign-off between
every notebook; build the flagship path fast, then review the set once.

## 4. Legibility mandate (fixes "I didn't know OmniPath had regulons in NB2")
Every notebook gets a **PI-readable TL;DR header** at the top: *what it establishes · what data it pulls
(named sources + counts) · what it contributes to the flagship · the one number/figure that matters.* The PI
must be able to know, in 30 seconds per notebook, what is inside and why. Maintain a single living **PITCH.md**
updated every time a notebook lands.

## 5. Positioning (cheap, protects credibility)
State the flagship inside the systems-population-genetics lineage — cite **Fagny & Austerlitz 2021**, **Daub
2013**, **signet/Gouy 2017**, the network-propagation family — and be explicit that this rescue/convergence
contribution is **distinct** from the R21's gene-property prediction, so it does not read as "not novel."
Keep the project's own discipline: **report the honest count; do not force a headline.** Gate the
Reactome-reaction class on sub-pathway tags (29 pigmentation-tagged reported separately from the 92
MITF-program genes) — never one inflated "N of 121."

## 6. Secondary (supporting rigor, not the flagship)
NB5's network non-redundancy + STRING **~66% agreement / ~34% drift** finding is a good honesty caveat — "the
network you choose changes the answer" — keep it foregrounded as rigor, not as the headline.

## 7. VISUAL MANDATE — every result gets a picture (this is not optional)
The PI does not want to read text and tables. **Every notebook and every key result must have at least one
clear visual.** The visual is how a notebook *proves its one result* — it is the caption's partner to the
TL;DR header (§4). Rule of thumb: **if a key result can't be shown as a simple picture, it isn't a key
result.** Two allowed kinds:
- **(a) Data figure** — generated from the actual analysis (funnel, UpSet/Venn, network, bar, Sankey).
- **(b) Concept SVG / schematic** — hand-built diagram, explicitly labeled "schematic (not data)".

**Claude Science does ROUGH figures ONLY — one functional visual per notebook to PROVE its result** (correct
data, correct chart type, a title that matches the data). That is the whole bar. Suggested per notebook: NB4 =
105→52 funnel; NB5 = network-overlap UpSet + the FALSIFIED hypothesis; NB6 = MITF hub with its 34 signed
targets; NB7 = the tiered substrate; NB8 = rescue results + convergence grades.

## 8. OUT OF SCOPE for Claude Science — Claude Code owns these (do NOT put them in your plan)
The PI + Claude Code handle everything cosmetic and infrastructural, from your rough prototypes. **Do NOT** do
any of the following — they will be done in Claude Code, where the PI has more token budget and design tooling:
- the **website / Quarto site** (`index.qmd`) — do not build or touch it;
- **figure polish / final design** and the shared **palette / visual system** — do not invest in aesthetics;
- the polished flagship visuals (hero rescue card, convergence overview, substrate schematic, layer bar).
Produce functional figures + the hero shortlist, then **STOP and surface to the PI** — Claude Code takes it
from there.

## Docs to update when done
START_HERE (north-star section), new **PITCH.md**, `internal/project_dashboard.md`, `internal/CHANGELOG.md`,
`internal/TODO.md`, and the **Quarto site** (`index.qmd`) as the visual walkthrough. Run the plan-sync;
archive superseded plans.
