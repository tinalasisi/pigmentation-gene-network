# Final synthesis — publication-defensibility ranking of four exploratory figures
**After two rounds (dispatch -> adversarial review with verified citations -> revision).** Reviewer: Molecular Evolution Specialist.

All four tracks survived adversarial review and were revised to address the strongest literature-grounded objection to each. Every method citation below was verified against CrossRef this session. Ranked by how defensible the figure is for publication RIGHT NOW.

---

## RANK 1 — Lability (fig_lability_final, v3: 17a2a076-b0e6-4d6d-855e-e5fa88eda4f5)  ⭐ PUBLICATION-READY
**Claim:** hair dichromatism is evolutionarily labile — ~16 independent origins (ARD; 12-21 range), loss:gain = 9.1x (95% CI 5.4-21.1).
**Why it's #1:** the result is a positive, model-robust finding that needs no selection data. Round-2 added a hidden-rates model (corHMM, Beaulieu et al. 2013): ARD still wins (AICc weight 61% vs HRM 39%), loss>>gain holds across models. Origin count is honestly reported as model-dependent (16 ARD / 24 HRM). Panel D shows the model comparison explicitly.
**Residual caveat:** origin count is model-sensitive (stated on figure). Trait-dependent-diversification (Rabosky & Goldberg 2015) not modeled — acknowledge in a sentence.
**Verdict:** defensible as a main-text figure as-is.

## RANK 2 — Convergence/divergence (fig_convergence_divergence, v-final: 7338aa5a-6816-473e-8e21-48f59b5e67c2)  ⭐ PUBLICATION-READY, now the strongest STORY
**Claim:** convergent phenotype (14-15 origins), divergent mechanism — shown with the per-origin RELAX test (Trachypithecus 12 genes both modules; Nomascus 1 gene POMC; Eulemur 0; ZERO overlap between origins).
**Why it jumped to #2:** round-2 replaced the underpowered tip-level Jaccard with the per-origin RELAX result (which landed this session), and added a detection-ceiling power analysis (Thomas & Hahn 2015; Zou & Zhang 2015). The headline is now honest ("power-limited, not evidence of divergent mechanism") and the well-powered origin-level comparison carries the divergence claim. Tip-level matrix demoted to supplement.
**Residual caveat:** the divergence claim rests on only 3 powered origins (2 informative). That's the real power limit — stated plainly.
**Verdict:** defensible; this is the figure that best embodies the project thesis.

## RANK 3 — Developmental route (dev_route_dichromatism_tree, v2: 077e3f67-34b4-4272-8804-b7f400c717a9)  ✓ DEFENSIBLE
**Claim:** dynamic (maturational) ontogeny predicts dichromatism (phyloglm beta=4.13, sign+CI; Firth cross-check beta=4.66, CI excludes 0); >=13 independent origins of dynamic ontogeny.
**Why #3 not higher:** the predictor quasi-perfectly separates the outcome. Round-2 handled this correctly — added Firth penalized likelihood (Heinze & Schemper 2002), reports sign+CI not magnitude, invokes >=13 origins against Maddison & FitzJohn (2014), and had already self-flagged the Pagel boundary artifact. Scientifically sound; the near-separation just means the effect is better shown as the raw rate table (100% vs 0%) than as a coefficient.
**Verdict:** defensible with the "sign not magnitude" framing kept explicit.

## RANK 4 — Correlated evolution / ecology (correlated_evolution_figure, v2: 8e1b4ea4-404a-4494-8b02-c22fd11d58a4)  ✓ DEFENSIBLE, with reframed claim
**Claim (reframed):** dichromatism and natal-coat are coupled — but as facets of ONE ontogenetic color-change program (100% overlap within the dynamic-trajectory group), NOT two independent sexually-selected traits. hair_dimorphism null (n=6). Mating system / SSD genuinely untested (no data).
**Why #4:** the strong natal_coat correlation, after review, is best read as developmental coupling (Uyeda et al. 2018), which partly collapses it into the Track-3 finding rather than standing as an independent result. The honest sexual-selection test (mating system, SSD) could not be run — PanTHERIA lacks those fields; the Opie, Atkinson & Shultz (2012) mating-system data is behind journal supplementary hosting not on the allowlist.
**Round-2 quality:** excellent — checked both Pagel rate matrices (natal_coat stable, hair_dimorphism runaway->demoted), Firth cross-check, reframed honestly.
**Verdict:** defensible as a developmental-coupling result; NOT a sexual-selection result. To make it the latter, obtain the Opie mating-system table (user has the paper) or an open SSD dataset.

---

## Cross-cutting methodological theme
All four discrete-trait analyses ran into the SAME failure mode — quasi-complete separation / boundary transition rates (the discrete-trait analogue of aBSREL's infinite-omega, which this lab already knows well). The consistent, literature-backed fix applied across tracks: penalized likelihood (Firth), lead with sign + CI-exclusion rather than inflated magnitude, and use the independent-origin count as the defense against single-joint-origin inflation (Maddison & FitzJohn 2014). Two tracks self-caught their boundary artifacts before review — a good sign for the underlying rigor.

## Recommended figure set for the paper/hackathon
- **Figure 1:** Lability (rank 1) — sets up "labile, many origins."
- **Figure 2:** Convergence/divergence (rank 2) — the thesis: convergent phenotype, divergent (per-origin) mechanism.
- **Figure 3 or supplement:** Developmental route (rank 3) — the "how" axis, ties to natal-coat coupling.
- **Supplement:** Ecology/correlated-evolution (rank 4) — developmental coupling + honest statement that sexual-selection proxies await data.

## Still open
- MC1R framing correction (lineage-specific, not silent) — narrative fix across walkthrough.qmd / dichromatism.qmd / README, separate from these figures.
- Mating-system test (Opie et al. 2012 data) — pending the user's supplementary table or an open SSD source.
