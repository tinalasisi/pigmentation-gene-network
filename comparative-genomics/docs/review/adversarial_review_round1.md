# Adversarial review — Round 1 exploratory figures (with verified method citations)

Reviewer: Molecular Evolution Specialist. Every critique below is grounded in a real reference verified against CrossRef this session. Each track gets ONE strongest objection + required revision. All four tracks are fundamentally sound; these are the objections a hostile reviewer WILL raise, and addressing them pre-empts rejection.

---

## Track 1 — Lability (fig_lability_final, 3caa7c4e)
**Result:** ~16 independent origins (500 simmaps, 95% range 12-21), ARD preferred (ΔAIC=18.9), loss:gain=9.1x (CI 5.4-21.1).

**Strongest objection — origin count and rate asymmetry are model-dependent, and a 2-rate Mk may be inadequate.**
The number of origins and the 9.1x loss:gain ratio both come from a single 2-state ARD Mk model. Two real problems:
1. The simmap origin count is conditioned on the ARD rates; if rate heterogeneity across the tree is present (very likely across 224 spp spanning strepsirrhines to catarrhines), a homogeneous 2-rate model will mis-estimate both origin number and the loss:gain ratio. This is exactly the case for a hidden-rates model: Beaulieu (2013) Systematic Biology, doi:10.1093/sysbio/syt034 shows a hidden-rates Markov model (corHMM) often fits binary morphological traits far better than ER/ARD and changes transition-rate inferences.
2. Trait-dependent diversification: if dichromatic lineages diversify at a different rate, a plain Mk model can mistake diversification-rate shifts for character transitions (Rabosky (2015) Systematic Biology, doi:10.1093/sysbio/syu131).

**Required revision:**
- Fit a hidden-rates model (corHMM, 2 rate categories) alongside ER/ARD; report AICc for all three. If HRM is preferred, re-derive the origin count and loss:gain ratio under it. If ARD still wins or the ratio is stable, SAY SO — that strengthens the result.
- Report the origin-count distribution under BOTH the ER and ARD simmaps (you already have ER-ish; make the model-dependence explicit on the figure or caption), so the "~16 origins" claim carries its model dependence honestly.
- Keep the figure; add a one-line caption note on model choice + that loss>>gain is robust across models (assuming it is).

---

## Track 2 — Convergence/divergence (fig_convergence_divergence, edd027a8)
**Result:** phenotype convergent (14-15 origins); molecular Jaccard overlap 0.028, indistinguishable from a degree-preserving (curveball) null (p=0.62). Clean dissociation.

**Strongest objection — the null model IS the entire result, and "no convergence" from a sparse 39-gene panel is the textbook false-negative trap.**
The agent did the right thing using a degree-preserving null (Strona curveball) — but the interpretation ("divergent mechanism, no convergent signature") is precisely the claim that Thomas (2015) Molecular Biology and Evolution, doi:10.1093/molbev/msv013 and Zou (2015) Molecular Biology and Evolution, doi:10.1093/molbev/msv014 warn is most easily gotten wrong: apparent molecular convergence (or its absence) is dominated by the null model and by how many sites/genes are examined. With only 39 genes and median per-lineage selected-gene count of 1-3, the test has almost no power to DETECT convergence even if it existed — so "indistinguishable from null" cannot be reported as "mechanism is divergent." It can only be reported as "no detectable convergent signature at this panel size/power."

**Required revision:**
- Reframe the verdict from "divergent mechanism" to "no DETECTABLE convergent molecular signature, and the test is power-limited" — cite Thomas & Hahn 2015 and Zou & Zhang 2015 for why the null and panel size dominate.
- Add a power/sensitivity statement: given 39 genes and the observed selection sparsity, what convergent fraction COULD have been detected? Even a back-of-envelope (e.g. how many shared genes would be needed to exceed the curveball null) quantifies the ceiling.
- CRITICAL UPGRADE: this figure uses tip-level aBSREL. The per-origin RELAX results now exist (per_origin_K.csv: origin_7 Trachypithecus 12 genes both modules, origin_8 Nomascus 1 gene POMC, origin_14 Eulemur 0). Rebuild the mechanism panel using the 3 powered origins' RELAX hits — that shows divergence (12 vs 1 vs 0 genes) with the CORRECT intensity test, which is far more defensible than tip-level aBSREL. Keep the tip-level matrix as a supplement.

---

## Track 3 — Developmental route (dev_route_dichromatism_tree, 74857c60)
**Result:** dynamic (maturational) ontogeny predicts dichromatism, phyloglm β=4.13 p=2.2e-6; ≥13 independent origins of dynamic ontogeny. Agent already flagged the Pagel LR as a boundary artifact.

**Strongest objection — quasi-complete separation in the phyloglm, and the deeper Maddison-Wren problem.**
Two issues:
1. The predictor nearly perfectly predicts the outcome (bidirectional 15/15, male 7/7 dichromatic; mono_stable 0/185). That is quasi-complete separation, which inflates logistic coefficients and their SEs — β=4.13 with a huge CI is the signature. This is a known statistical pathology with a known fix: Heinze (2002) Statistics in Medicine, doi:10.1002/sim.1047 (Firth penalized likelihood). The agent correctly rejected the Pagel LR for the analogous boundary artifact but did NOT apply the separation correction to the phyloglm it KEPT.
2. Both traits arising together repeatedly on the tree can produce a significant correlation from as few as one or two co-distributed shifts — the unsolved-challenge critique of Maddison (2014) Systematic Biology, doi:10.1093/sysbio/syu070: phylogenetic correlation tests for two binary characters can be driven by a single joint origin and cannot always distinguish real coupling from a shared singular event. Your Fitch ≥13 independent origins is the right defense — but it needs to be stated AS the defense against Maddison & FitzJohn.

**Required revision:**
- Refit the phylogenetic association with a separation-robust approach: either Firth-penalized logistic (Heinze & Schemper 2002) as a non-phylo robustness check, or report the phyloglm with an explicit note that separation inflates the point estimate and the SIGN + bootstrap CI exclusion of zero (not the magnitude) is the inference.
- Explicitly invoke the ≥13 independent origins as the answer to Maddison & FitzJohn (2014): the association is not driven by a single joint origin.
- Keep the figure; it's excellent. Add the Firth cross-check to the caption/table.

---

## Track 4 — Correlated evolution / ecology (correlated_evolution_figure, 84fe0b3d)
**Result:** dichromatism ~ natal_coat strongly correlated (Pagel LR=87.2 p=5.2e-18; phyloglm est=5.2, bootstrap CI excludes 0). hair_dimorphism null (n=6). PanTHERIA lacked mating system/SSD; group-size proxy null. No fabrication.

**Strongest objection — same separation + Maddison-FitzJohn issue, PLUS a circularity risk on natal coat.**
1. natal_coat: 24/25 dichromatic species have a natal coat vs 11/199 others — again near-separation; the LR=87 and est=5.2 are inflated by it (Heinze & Schemper 2002). The direction is bulletproof; the magnitude is not.
2. Deeper: is "natal coat" mechanistically independent of dichromatism, or are they two facets of the same ontogenetic color-change program? If the latter, the correlation is partly definitional, not evolutionary — the interpretation must be about developmental coupling, not two independent traits co-evolving (this connects to Track 3's developmental-route finding — they may be the same underlying axis). Uyeda (2018) Systematic Biology, doi:10.1093/sysbio/syy031 on how PCMs can mislead when predictor and response are not causally independent.
3. Pagel LR again risks the boundary artifact Track 3 flagged — check the dependent-model rate matrix for a runaway rate.

**Required revision:**
- Add a Firth-penalized non-phylo logistic as a separation robustness check; report that the SIGN and CI-exclusion, not the magnitude, are the inference.
- Check the Pagel dependent-model rate matrix for boundary rates (as Track 3 did); if present, demote the LR p-value and lead with phyloglm.
- Reframe natal_coat result as likely DEVELOPMENTAL COUPLING (tie to Track 3), not an independent sexual-selection correlate — and state plainly that the actual sexual-selection proxies (mating system, SSD) remain untested for lack of data (Opie et al. 2012 coding scheme noted; values not obtained).

---

## Cross-cutting notes
- Two tracks (Dev, Convergence) already self-flagged their boundary artifacts — good. The unifying methodological theme across all four is QUASI-SEPARATION / boundary-rate artifacts in discrete-trait models, and the fix is consistent: penalized likelihood + lead with sign/CI not magnitude + independent-origin count as the defense against single-joint-origin inflation.
- The per-origin RELAX results (landed this session) should be threaded into Track 2 specifically.
- MC1R framing correction (lineage-specific, not silent) is a narrative fix, separate from these figure revisions.
