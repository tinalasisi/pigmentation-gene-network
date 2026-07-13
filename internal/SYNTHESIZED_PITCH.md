# The pitch — Researcher Track

**Status:** DRAFT for PI. Pitch copy is the HEADLINE + THESIS below; everything after is planning
scaffolding (beat spine, judge-defensibility notes) for the PI, not text a judge reads.

## HEADLINE

**"A striking male–female color difference sits on a single gene of major effect in birds. Across
primates the same kind of trait evolved ~15 times over — and not once through a single switch."**

*Alternates (same spine):*
- *"Why is there no 'dichromatism gene' in primates? We tested ~15 independent origins and got the
  same answer every time: many genes, no switch — the opposite of birds."*
- *"One phenotype, two ways to build it: in the best-studied birds a color sex-difference rests on a
  gene of major effect; the primate version is polygenic in every lineage that evolved it."*

## THESIS (submittable prose — plain language, numbers one layer down)

In birds, a striking male–female color difference typically rests on a **gene of major effect** for
one pigment system in one clade — MC1R for melanin in gamefowl, BCO2 for carotenoids in finches —
each hormonally regulated. We asked whether primates, where the comparable trait (sexually
dichromatic hair) arose independently about **15 times**, reuse a switch like this. They don't: the
trait is **polygenic in every origin we could test** — MC1R is never the hit — and it is **lost
roughly 9× more readily than it is gained**. One phenotype, two fundamentally different genetic
architectures. To ask the question we built a comparative-genomics pipeline — 117 pulled primate
genomes, selection scans on a cluster, phylogenetic comparative statistics in Claude Science — in a
single week, most of it first-time bench work. We also tested the idea the project began with — that
selection on a coupled pigment–hormone gene set tracks the trait across lineages — and got a clean
**negative**; we report it as such. What ships is only what held up when the pipeline was made to
check itself.

## BEAT STRUCTURE (the deck spine)

1. **Hook — one trait, two ways to build it.** Birds (best-studied cases): a gene of major effect.
   Primates: ~15 independent origins, polygenic every time, no switch. The counterintuitive result in
   the first breath, before any method. — *layer down: MC1R/galliforms Nadeau 2007; BCO2/finches
   Gazda 2020 Science; hormonal regulation Griffith et al. 2026 — which is explicit that avian
   dichromatism mechanisms are "highly diverse across the avian clade," so "gene of major effect" is
   a per-case statement, not "birds are simple."*
2. **The instrument — how we got to ask it.** A pipeline from genome assemblies to a statistical
   verdict, with an explicit what-ran-where split: CDS extraction, MAFFT codon alignment, HyPhy
   RELAX/aBSREL on an HPC cluster; network/panel curation and the comparative tests (Pagel's λ,
   ancestral-state reconstruction, fitPagel) in Claude Science. *We pulled 117 published genomes; we
   did not assemble or align genomes ourselves.*
3. **The result that holds.** ~15 independent origins; polygenic everywhere tested; MC1R never the
   hit; loss ≈ 9× gain (ARD vs ER, ΔAIC 19.79); Pagel's λ = 0.6547, p = 1.1×10⁻⁶ (real signal).
4. **The question we posed and answered with a null.** The coupled pigment–hormone selection idea —
   the project's original thesis — does not track dichromatism across lineages: fitPagel prefers the
   independent model. We state the negative plainly; under this rubric a well-specified null is a
   result, not a hole.
5. **Calibration — the credibility beat (NOT the headline).** Every shipped claim was held to a power
   standard the pipeline checks on itself: an audit re-derived three statistics and scoped down a
   bolder architecture claim the data couldn't support — χ² homogeneity p = 0.42; P(zero cross-origin
   overlap by chance) = 0.87; hormone-tilt binomial p = 0.17. Verdict: "underpowered to resolve,"
   not "heterogeneous." Re-derivation code is in the repo. *Made confidently mid-pitch — "these
   people check their own work" — never the opening sell.*
6. **The resource left behind.** A curated, provenance-sealed gene resource: an ~800-gene ×
   74-feature harmonized substrate over cited public networks (STRING, OmniPath, curated regulons,
   Raghunath pathway), a focused 78-gene selection panel (26 pigment + 52 hormone), a 200-gene
   OMIM/GWAS disorder layer, and an interactive explorer — every input loaded through a manifest
   recording its source and a SHA256 of the exact bytes. *Stated honestly: it is a reusable panel and
   feature table, not a run-ready coupled network — the network layer is a 15-edge pilot substrate,
   and the explorer covers the pigmentation genes (the hormone genes live in the panel and its
   notebooks).*
7. **The "how," as evidence not story.** One person, ~7 bench domains, one week, 220 commits
   (2026-07-09 → 2026-07-13), most first-time — cited to establish the pipeline is real and
   reproducible, paired with beat 5 so "new to the bench" reads as "capable and self-checking."
8. **Close on the honest open question.** Do the ~15 origins that lose color so readily share the
   pigment × hormone coupling birds are known to show? Our within-primate test was underpowered to
   settle it; the cross-taxon comparison (birds already reconstruct dichromatism ancestral states
   across 8,800 species) is the natural next step — and the honest home for extending the explorer to
   the hormone layer.

## DEFENSIBILITY — the questions a domain judge will ask, and our answers

- **"How is this different from Badyaev et al. 2015?"** *(Biol Direct, PMID 26289047 — abstract
  reviewed; full-text PDF on file.)* It is the closest *adjacent* work — network + phylogeny +
  repeated avian color evolution — but the overlap is thinner than it first looks. Badyaev models the
  **carotenoid
  metabolic pathway** (nodes = pigment compounds, edges = enzymatic conversions) across ~159 species
  to explain **color elaboration and diversification** — it does **not** test sexual dichromatism and
  is **not** a gene-regulatory or architecture network. Ours tests a **male–female trait's genetic
  architecture** via a **regulatory pigment–hormone gene panel** read **per independent origin in
  primates**, with per-branch selection tests. Different phenotype, different network type, different
  clade. We cite it as the nearest prior art and claim a new *question, instance, and instrument* —
  appropriate for the Researcher Track.
- **"Isn't the coupled-network story your headline?"** No — we demoted it. It's a tested null (beat
  4). The one line we will NOT say: *"we found a coupled pigmentation–hormone architecture across
  lineages"* — the exact sentence a reviewer breaks first (χ² p = 0.42). The disease/pharmacology
  reading and the KITLG/TYR triangulation are, at most, one clearly-labeled illustration each.
- **"Is the resource really reusable?"** As a panel + feature table + provenance manifest, yes. As a
  coupled network you can run coevolution on, no — that layer is an explicit 15-edge pilot, and we
  say so.

## THE ONE LINE THAT MUST STAY

*"Every claim that ships was held to a power standard the pipeline could check on itself — the
re-derivation code is in the repo, and the claims that didn't clear it were scoped down accordingly."*

## THE ONE LINE TO CUT

Any phrasing of "we found a coupled pigmentation–hormone architecture across lineages" as an achieved
result.

## Reproducibility status (resolved this session)

- NB9 (`09_bajpai_reconciliation.ipynb`) — checked: paths already repo-root-anchored, no fix needed.
- NB12 (`12_direction_law_expanded.ipynb`) — the mygene.info/QuickGO pulls are now frozen to
  `data/external/db_responses/nb12/` behind a `REQUERY_NB12=False` guard; validated offline
  (all cells run, numbers match). Committed + pushed (0b1aec8).
