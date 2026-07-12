# Demo — the mechanism→direction result (NB10 + NB12)

_One-page presentation script. Candidate demo for the convergence thesis; framing is deliberately
**methodological, not a biological discovery** (see the limits — they are load-bearing, not footnotes).
Fallback flagship while the primate-phylogenetics thread is evaluated. Last updated 2026-07-12._

---

## The one-sentence claim

> **A single convergent functional readout orders the *clinical direction* of an entire Mendelian disease
> category — and its failures aren't random.** A gene that is a *positive regulator of melanin* (loss reduces
> pigment), mutated by a *loss-of-function* allele, causes **hypo**pigmentation. On the loss-of-function subset
> the prediction is **22/22** (base rate 54%, permutation *p* < 1×10⁻⁵); a pre-registered expansion reaches
> **29/33**, and the misses concentrate in genes acting through *systemic* routes — which a phenotype-blind
> classifier partly anticipates.

## The one figure

`notebooks/figures/nb12_direction_law_expanded.png` — three panels, read left to right:

1. **It scales and stays significant** — 22/22 (network sources) → 29/33 (adding a blind mechanism source),
   both far above the 54% base rate, permutation *p* < 1×10⁻⁵.
2. **No ascertainment confound** — core-melanogenesis genes (14/16) and syndromic/trafficking genes (15/17) are
   concordant at the same rate; the law is not an artifact of well-studied core genes.
3. **The boundary, shown honestly** — confidence catches 3 of the 4 misses, but *ATP7B* (Wilson-disease copper)
   is a high-confidence miss it does **not** flag. The "predicts its own failures" pattern rests on n = 4 and is
   illustrative, not validated.

## The 90-second script

1. *The problem.* When a new pigmentation variant turns up, does it darken or lighten skin? Direction is a
   basic clinical question and there's no cheap way to call it a priori.
2. *The move.* We ask a functional CRISPR melanin screen for each gene's *sign* (does loss reduce pigment?),
   and condition on allele mechanism. Under a loss-of-function allele, sign predicts clinical direction: 22/22.
3. *The stress test.* This is exactly the kind of clean result that turned out to be a study-bias artifact once
   before in this project. So we audited it — STRING (the retracted-finding resource) contributes no sign,
   significance survives collapsing shared-complex genes to 15 independent units (*p* ≈ 3×10⁻⁶), the CRISPR
   line alone gives 19/19, and the loss-of-function condition is assigned blind to phenotype. It survives.
4. *The interesting part.* Expanding it didn't just add n — it found the **edge**: the law transfers for
   direct-melanocyte-function genes and breaks for systemic-route genes (copper metabolism, ACTH feedback), and
   a phenotype-blind molecular classifier separates most of those two classes in advance.
5. *The honest contribution.* The biology is textbook — this is not a discovery about pigmentation. What's ours
   is the *method*: convergent functional evidence can order a clinical property across a whole disease
   category, with a quantified null and a characterizable failure boundary. That is the project's "grade trust
   by evidence convergence" thesis, made concrete and bounded.

## Three honest limits (say these out loud — don't wait to be asked)

1. **The biology is known.** "LoF of a positive melanin regulator → hypopigmentation" is close to the definition
   of albinism; Bajpai et al. already tied the screen's sign to common-variant skin color. The contribution is
   methodological, not a new fact about pigmentation.
2. **The boundary story rests on n = 4.** Four discordances, and one (*ATP7B*) breaks the "confidence flags
   misses" reading. Treat it as illustrative, not a validated predictor.
3. **Near-circular for core genes; ascertainment reduced, not eliminated.** For melanin-synthesis genes the
   prediction restates the disease definition; the syndromic stratum is mostly partial-albinism trafficking
   genes, so it doesn't fully isolate systemic-route genes.

## What NOT to claim

- Not "we discovered a law governing pigmentation-disease direction."
- Not "the classifier reliably predicts its own failures."
- Not a common-variant result — the GWAS-beta axis was scoped and **shelved** (5/35 clean SNP→gene genes).

## Assets

- Notebook: `notebooks/12_direction_law_expanded.ipynb` (literature audit built in) + `10_mechanism_direction_law.ipynb`
- Figure: `notebooks/figures/nb12_direction_law_expanded.png`
- Due-diligence trail: `internal/deconvolutor/` (prior-art gate + validity audit); ranking in `internal/FINDINGS_MEMO.md`
- Backing data: `data/processed/nb12_direction_law_expanded.csv`, `nb12_expanded_summary.csv`