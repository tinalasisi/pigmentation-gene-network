# NB10 validity audit — does the mechanism→direction law survive its own weak legs?

_2026-07-12. Runs the `PLAN_DECONVOLUTOR`'s must-answer questions against the committed data before any
expansion. No new data pulled; no repo file modified. Verdict: **the law survives every validity check that
could have killed it, with two honest caveats that change the framing but not the result.**_

## Summary table

| # | Question the critic raised | Result | Verdict |
|---|---|---|---|
| 1 | Is the LoF conditioning variable assigned **blind to direction**? | `is_LoF` is a pure function of the OMIM `inheritance` field (AR/XL → True), using **zero** phenotype information. | ✅ Blind |
| 2 | Were indeterminate-sign genes **silently excluded**? | 50 of 72 LoF genes have **no** regulator call — all from *coverage* (no source annotates them), **0** dropped for conflicting/`mixed` sign. Exclusion is coverage, not survivorship. | ✅ Clean |
| 3 | Does the signed network (NB7) get its **sign** from STRING (the retracted-finding resource)? | **No.** STRING enters NB7 only as `association_unsigned_undirected` — it carries no sign by construction. All 318 signed edges trace to **Raghunath / GRN / OmniPath** (mechanistic). STRING cannot and does not sign any direction call. | ✅ Decisive |
| 4 | Is the permutation *p* inflated by treating **shared-complex genes as independent**? | The 22 genes collapse to **15 independent units** (BLOC-1/2/3, AP-3 subunits merged). Re-run at unit level: base rate 0.49, **15/15 target units hypo**, exact hypergeometric **p = 2.7×10⁻⁶** (vs the naïve gene-level 2.8×10⁻⁸). | ✅ Survives |
| 5 | Are the "3 independent sources" really independent? | For 19/22 genes the **Bajpai CRISPR screen** (functional, literature-independent) carries the call. Only **3 genes** (EDNRB, MC1R, TYRP1) rest on the GRN+SignedNet pair, which plausibly share MITF/SOX10/PAX3 logic → count as **~1.5 sources**, not 2, for that tier. | ⚠️ Downgrade noted |
| 6 | Does the result hinge on any **one source**? | Leave-one-source-out: without GRN → 22/22; without SignedNet → 22/22; **Bajpai alone → 19/19**; without Bajpai → 4/4. No single source drives it. | ✅ Robust |
| 7 | Honest **denominator**? | Law-applies (LoF + call): **22/22**. Dominant/non-LoF (law not asserted): 7/13. The 6 dominant discordances' non-LoF mechanisms were assigned **post-hoc** (after seeing which broke) — see caveat B. | ✅ / ⚠️ |

## The two caveats that change the framing (not the result)

**A. The three "independent sources" are really two-and-a-half.** The strong, honest claim is: *a
literature-independent functional CRISPR screen alone predicts 19/19 recessive/X-linked directions correctly*;
the GRN and signed-network lines corroborate and extend coverage to 3 further genes (EDNRB, MC1R, TYRP1) but
are not fully independent of each other. The headline should lead with the CRISPR line, not with "three
independent sources agree."

**B. The dominant exceptions were explained post-hoc.** The 6 dominant discordances (TYR, CDKN2A, PSENEN, BNC2,
KIT, FASLG) had their non-LoF mechanisms assigned *after* observing that they broke the pattern. This is
legitimate as *mechanistic interpretation* but is **not** a blind prediction, so the honest framing is:
"the law is asserted only for LoF alleles (a pre-specified, phenotype-blind condition); among genes it applies
to, 22/22 hold; the dominant genes it does not apply to each have a documented non-LoF mechanism." The 22/22
is the predictive claim; the 6 explanations are interpretation.

## What the audit did NOT change

- The **LoF condition is genuinely pre-specified and blind** — it is the load-bearing part of the claim and it
  is clean.
- Significance **survives the harshest reasonable non-independence correction** (complex-collapsed p ≈ 3×10⁻⁶).
- The result **does not touch the retracted STRING/degree resource** for any direction call.
- No gene was silently dropped for being discordant.

## Bottom line

The n=22 result is **more defensible after the audit than before it**, provided the framing is corrected to
(A) lead with the CRISPR line rather than "3 independent sources," and (B) state the 22/22 as the predictive
claim and the 6 dominant mechanisms as post-hoc interpretation. This is a reportable flagship as-is; expansion
is optional, not required, and should only be attempted in the narrow, pre-registered form the specialists
endorsed.
