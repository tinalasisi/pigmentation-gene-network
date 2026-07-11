# PROJECT EVOLUTION — how we got here, and the decisions still open

_A guide (not a plan) for a Claude joining this project, written 2026-07-11T22:51Z by Claude Code. It narrates
how the framing evolved — what was tried, what was abandoned, and why — so you can help settle the two things
that are still genuinely open: **exactly how to frame the contribution, and what the flagship demo visual
should be.** Those two are linked. Only the goal (in `START_HERE.md`) is fixed; everything here is context._

## The arc in one paragraph

The project began by building a mechanistic pigmentation network and testing it against published cases of
genotype→phenotype discordance. It then spent a day cycling through several ways to FRAME that into a
"finding" — each chasing a defensible-sounding novelty claim, each over-investing in one headline number. A
critical audit showed those headline numbers were artifacts of how the data had been extracted (genes
manufactured from loci) and how small the network was. A locus-first rebuild dissolved most of the supposed
finding. The PI then redirected the project away from defending a boundary and toward a generative goal —
grading confidence in variant→phenotype links by evidence convergence, and rescuing the many associations that
sit unvalidated. The repo was cleaned to a minimal, framing-neutral set. **We are now choosing the
contribution's exact shape and its flagship demo, deliberately, from a clean slate.**

## Phase by phase (with the lessons)

**1. Build the substrate.** Reconstructed the Raghunath 2015 melanogenesis model as a 168-gene signed directed
network; assembled 13 published discordance papers as test cases. *Solid and reusable — materials, not a
framing.*

**2. The framing churn (the cautionary tale).** In one day the "finding" was reframed repeatedly: a
network-ranked modifier list ("GWAS by node") → a three-stratum "dark-matter decomposition" with headline
percentages → a "resolution-rate engine" → a "portability failure-mode taxonomy." Each chased a
defensible-novelty claim and leaned on a single headline metric. **Lesson: optimizing for a novel-sounding
headline number pulled the project away from the science and toward defending a boundary.**

**3. The audits (the correction).** A critical review (`internal/handoffs/HANDOFF_CRITICAL_limitations_and_framing_issues.md`,
`internal/TRACEABILITY_coverage_and_resolution_logic.md`) found the headline decomposition was an artifact: a
gene-first extraction had manufactured "genes" from haplotype segments, SNP clusters, and null retests, and
"% explained by mechanism" was really a measure of how small the single-paper backbone was. **Lesson: the unit
of analysis and the completeness of the substrate silently determined the "finding." Work locus-first; never
let a headline number ride on an unexamined pipeline.**

**4. The locus-first rebuild.** Re-extracted all 13 papers with the variant/region as the unit, carrying each
paper's own verdict. Most of the "dark matter" dissolved into extraction artifacts (segment passengers, null
retests, author-set-aside rare variants). Output: `data/processed/discordance_loci.csv` — *one processed view
of one route, not a mandated foundation.*

**5. The reorientation (the current goal).** The PI redirected from the defensive/boundary framing (and from a
later "compare what each network substrate can assert" detour, which was inward and abstract) to the goal now
in `START_HERE.md`: **know how much to trust a variant→phenotype link by making independent evidence converge;
grade and rescue reported associations; use population differences to reveal conditional structure.** Only the
goal is fixed; the execution is open.

**6. The cleanup.** Every retired framing, plan, and derived artifact was archived to `internal/archive/`
(gitignored). The visible repo is now a minimal, framing-neutral set: the goal, the lessons, the materials,
the tools.

## The two decisions still open (and why they are one decision)

The PI is deliberately wavering on:
- **The exact contribution framing** — the goal is fixed, but *how* we cut a demonstrable contribution from it
  (a graded catalog? a convergence map? a rescue engine? a population-conditionality result?) is open.
- **The flagship demo visual / site** — what a viewer sees and does.

These are **one decision, not two**: the flagship visual should *embody* the thesis, so the framing and the
visual are chosen together. Pick the sharpest defensible thesis, then build the demo that makes it undeniable.

## What we already have that is demo-worthy

- **A multi-layer network** (mechanistic + curated-pathway + expandable) → a striking convergence-map visual
  (nodes coloured by how many independent evidence layers support them).
- **A ready-made hard-case set** — the "dark matter" that dissolved (segment passengers, null retests,
  author-set-aside rare variants). These are exactly where a careful convergence method should hold back and a
  naive single-source lookup would over-call — useful for showing due diligence (not over-calling), not as a
  gimmick.
- **Population differences** — the same phenotype reached by different genes/alleles across ancestries
  (TYRP1/Oceania, OCA2/East Asia, MFSD12/Africa) → a compelling population visual and the seed of the
  conditionality story.
- **A per-locus prescription** — for each association: a confidence grade + the converging evidence + the next
  experiment that would confirm it.

## Principles for the demo (grounded in scientific usefulness, not showmanship)

The demo must read as **useful to the pigmentation-genetics community**, not as a clever gimmick — this is the
PI's main concern. What makes it credible and useful:
- **Ground it in a real gap the community feels.** Show we go one honest step past where standard practice
  stops (GWAS → GO/pathway lookup → stop) — e.g. explaining a replicated-but-unexplained locus through the
  network layers. Usefulness to colleagues is the point, not a slogan.
- **Guard against the two things that make people distrust this kind of work — reinventing the wheel and false
  positives.** Where it's natural, show our calls survive the hard cases a naive single-source lookup would
  over-call. Frame it as due diligence, not a gotcha, and do not force it.
- **Cede prior art honestly** (Open Targets L2G / cS2G, Kim 2024, …) and map where the method does not reach —
  credibility comes from showing the limits, not only the wins.
- **Separate the auditable core from the LLM.** A deterministic, reproducible computation makes any call; an
  LLM writes the per-item synthesis with citations and never changes the computation.
- **Let the notebooks carry the rigor.** The site is a readable, honest front door to them — interactive only
  where it genuinely helps (look up a locus → its converging evidence and the concrete next step).
- **Use our real scientific assets** — the multi-layer network and the population picture — because they show
  the biology, not because they look impressive. Keep it scannable; the depth lives in the notebooks.

(These are understated on purpose: the science and its usefulness lead; presentation follows.)

## How to use this document

Orientation, not instruction. Hold the goal in `START_HERE.md` as the anchor; use the lessons to avoid
re-making the mistakes; help the PI choose the sharpest thesis and the demo that proves it. If you believe the
goal itself should move, say so explicitly rather than quietly redesigning around a different one.
