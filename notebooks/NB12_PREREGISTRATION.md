# NB12 pre-registration — expanding the mechanism→direction law

_Written 2026-07-12, **before** obtaining any new gene's direction call. This fixes the analysis rules in
advance so the expansion cannot be steered by seeing which genes fit. Required by the prior-art gate's two
conditions (build with explicit inheritance annotation; sensitivity-test the ascertainment confound)._

## Hypothesis (fixed, identical to NB10)

A **positive** regulator of melanin, mutated by a **loss-of-function** allele (OMIM inheritance AR or XL),
causes **hypo**pigmentation; a **negative** regulator causes hyperpigmentation. Asserted only under LoF.

## The expansion

Bring the ~50 LoF OMIM pigmentation-disorder genes that currently have **no** direction call into the test, by
adding a **fourth, independent** direction source: a molecular-mechanism regulator-sign call for each gene,
pulled with a resolvable citation (Open Targets / GO biological-process / UniProt function), **not** assigned
from memory.

## Pre-registered rules (fixed before seeing any new call)

1. **Direction-sign rule.** A gene is a **positive regulator** if its normal molecular function is *required for*
   melanin synthesis, melanosome biogenesis/maturation, melanosome transport, or melanocyte development/survival
   (loss → less pigment). A gene is a **negative regulator** if its normal function *represses* the pigment
   program or *removes/degrades* melanin machinery (loss → more pigment). This is a statement about the gene's
   **normal function**, made **without reference to the patient's phenotype direction**.
2. **Sign-conflict rule.** When sources disagree, majority vote across all available sources
   {Bajpai, GRN, signed-net, mechanism-call}. Ties → `mixed` → **excluded** from the concordance test (reported,
   not dropped silently).
3. **Inclusion.** A gene enters the test iff (a) OMIM phenotype_class ∈ {Hyper, Hypo}, (b) is_LoF (AR/XL), and
   (c) has a non-`mixed` direction call. Exactly the NB10 inclusion rule; only coverage grows.
4. **Blinding.** The mechanism-call annotator is instructed to classify normal molecular function only, and is
   **not** given the OMIM phenotype direction for any gene.
5. **Primary test.** Concordance of predicted vs observed direction on the expanded LoF set; permutation *p* vs
   the LoF base rate, computed at **complex-collapsed unit level** (shared protein complexes = one unit), as in
   the NB10 audit.
6. **Mandated sensitivity split (the gate's condition 2).** Report concordance **separately** for
   **core-melanogenesis-pathway** genes vs **syndromic/trafficking** genes. Core = melanin-synthesis enzymes,
   melanosomal transporters/structural, and the MITF/SOX10/PAX3 axis; syndromic/trafficking = HPS/BLOC/AP-3/CHS
   organelle-biogenesis and multi-system disorders where pigment is one of several affected systems. The split
   is assigned from gene function, **before** computing per-stratum concordance.

## Falsification / honesty conditions (fixed in advance)

- If the syndromic stratum concordance is materially lower than the core stratum, the conclusion is that
  the law is a **core-pathway** law and the CRISPR/mechanism call is unreliable outside it — reported as such,
  not explained away.
- If adding mechanism-call genes drops overall concordance below the LoF base rate + 2·SE, the expansion
  **weakens** the finding and that is the reported result.
- The mechanism-call source is a **fourth** line; it is not independent of the biology, so per-source
  concordance (including mechanism-call alone) is reported so a reader can down-weight it.

## Outputs

`nb12_direction_law_expanded.csv` (per-gene, with source of each call + citation + stratum),
`nb12_expanded_summary.csv` (overall + per-stratum + per-source concordance, permutation p), and a figure.
