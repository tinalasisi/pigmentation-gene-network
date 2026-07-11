# Plan Deconvolutor — combined report for the PI (both forward tracks, under a 48-hour deadline)

**Date:** 2026-07-10. **Status:** pre-approval critique only — no plan edits, no build, no commit.
**What this is:** the plan deconvolutor was run on both currently-unauthorized forward tracks, with a
PI-imposed hard **2-day (48-hour)** deadline as the dominant lens. This page is the synthesis; the two
full critiques are separate artifacts (linked at the end).

---

## Bottom line

**Neither track produces a scientific result in 48 hours.** Both bottom out at *disclosure material*, not a
finding — but they are blocked for different reasons, and the honest 2-day floor differs in kind.

| | **Sex-hormone × pigmentation expansion** | **Downstream NB4–NB8 chain** |
|---|---|---|
| 48h scientific result? | **No** (none of Stages A–D) | **No** (no notebook NB4–NB8) |
| Blocked by | **Scale** — its hardest steps are multi-week research problems the plan understates as lookups | **A decision + a dead edge source** — an unwritten causal-gene tie-break rule, and OmniPath not covering the genes the design depends on |
| Largest honest 48h floor | A **labeled Stage-A skeleton**: mechanically imported hormone-pathway layer + a citation-gap list | An **NB4 manifest without causal resolution**: case-gene × network inventory (`already-in-network`/`absent`) + a "no-OmniPath-edge-found" list |
| Substrate to build on | Only NB1/NB2 (the coupling target); everything else is new | NB1/NB2 **plus** the complete 694-record case dataset — data is done, only the analysis is missing |
| Fewer open unknowns to unblock the floor | No | **Yes** — a join methodology, not a phenotype-construction research program |

If you can only unblock one floor before the deadline, the NB4-manifest floor requires resolving fewer
unknowns — but it is also the smaller deliverable (an inventory table vs. an installed toolchain + a
species-name mismatch list + a bounded orthology audit). Neither is a result; the choice is about which kind
of day-2 disclosure material is more useful.

---

## The load-bearing findings (both grounded in live checks this session, not memory)

**Expansion plan:**
- **The bridge-edge table's central claim has zero database support.** A live OmniPath query across all 11
  aggregated resources for AR/ESR1/ESR2 → a 14-gene melanogenic/melanocortin set returned **0 direct edges**
  out of 344 interactions pulled. Every coupling edge must be hand-curated from the ~2 named papers — a
  10–40 hour task done honestly, or citation-padding done fast.
- **Stage D's dependent variable does not exist.** A standardized cross-primate dichromatism score is a
  multi-week methods contribution (the plan's two anchor papers measure different traits in different clades),
  not a data lookup.
- **The orthology "hard gate" doesn't scale to 48h.** A live Ensembl Compara pull found CYP17A1/CYP19A1/
  HSD17B3 clean 1:1 but HSD3B2 genuinely complex — i.e. real per-gene adjudication, feasible for a handful of
  genes, not the full gene universe.
- Plus: a multiplicative "confidence = product of three layers" framing with no calibrated inputs; and one
  concrete citation error (the demoted Ríos backbone paper is mis-cited — wrong year/journal/DOI).

**Downstream chain:**
- **HERC2 — the chain's own headline example — has zero melanogenesis-relevant OmniPath edges.** All 145 of
  its OmniPath interactions are DNA-damage/ubiquitin-ligase; none touch MITF/TYR/OCA2/MC1R/etc. The edge the
  chain needs would have to come entirely from curated literature — the half of the rule with no evidentiary
  bar defined.
- **OmniPath barely covers the NB5 candidate genes.** OCA2 has 6 edges (all incoming regulators); the 8
  other named candidates return 0–9 edges each (SLC24A5/SLC24A4/MFSD12/TMEM138 at 0; ASIP highest at 9), and
  **none** of the 9 candidates is already in the 168-gene network or connects candidate-to-candidate. NB5 is
  a literature-construction project, not a connection step with occasional backstops.
- **The causality gate has no rule to execute.** No tie-break exists for when nearest-gene / L2G / ClinVar
  disagree — and HERC2/OCA2 is a *real* instance of that disagreement, so the chain can't resolve even one
  worked example.
- **Connector reality check:** ClinVar is live and current; **Open Targets L2G was rate-limited on every
  attempt** (so §5a's L2G anti-leakage question can't even be tested right now); **Complex Portal/CORUM
  errored/timed out** — treat the STRING+Reactome fallback as the operative path, not a backup.
- The NB4/NB8 circularity gets *worse* under time pressure (fastest edge source = the same paper that
  classified the case); the D2 degree-preserving null is artifact-prone at this graph's skew (max degree 26,
  median 3, 140/168 non-isolated).

---

## What I recommend you decide (the questions that actually gate the 48 hours)

1. **Pick the 48h target:** the NB4-manifest floor, the expansion Stage-A skeleton, both in parallel, or
   **neither — spend the 48h on housekeeping** (the buildable-now items: DATA_SOURCES.md reconciliation, NB3
   change-log backfill, duplicate-CSV retirement). Given both scientific floors are disclosure-only, the
   housekeeping option is genuinely competitive for a 2-day window.
2. If a scientific floor is chosen, whose sign-off guarantees the mandatory "this is QC/disclosure, not a
   result" caveat travels with the artifact wherever it's shown?
3. The deadline sharpens **§6-F / TODO #0 sequencing:** the only fully-settled thing is NB1/NB2. Both forward
   tracks are unauthorized, and the expansion couples to a substrate whose own downstream chain isn't settled.

The full question sets (deliverability + the plans' own open questions, re-asked in light of the live
findings) are in the two reports below.

---

## Full critiques (artifacts)

- **`2026-07-10_1808_DECONVOLUTOR_REPORT_sex_pigment_primate.md`** — expansion plan, full critique.
- **`2026-07-10_1859_DECONVOLUTOR_REPORT_NB4-NB8_downstream_chain.md`** — downstream chain, full critique.

*Pre-approval critique only. No repository commit is made from these documents; any commit goes through the
compliance gate.*
