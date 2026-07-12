# Findings memo — what the assembled data actually support, ranked

_Independent exploration session, 2026-07-12T07:10Z. Separate from the concurrent NB4–NB8 rescue-screen
session; **no repo file or committed CSV modified.** This memo compares every candidate finding turned up in
this pass — the ones that held and the ones that did not — and names the single most interesting result the
project's own assembled data can defend._

> **UPDATE 2026-07-12T17:00Z — verdict softened after a literature audit.** Candidate 1 below was originally
> named "the most interesting finding." A claim-by-claim literature check (in
> `notebooks/12_direction_law_expanded.ipynb`) found the *biology* is largely textbook — "LoF of a positive
> melanin regulator → hypopigmentation" is close to the definition of albinism; Bajpai et al. already tied the
> screen's sign to common-variant skin colour. What remains genuinely ours is **methodological**: a single
> convergent functional readout orders a clinical property (disease direction) across a whole category with a
> quantified null and a *partly-predictable failure boundary*. Re-read candidate 1 as **"the most interesting
> *demonstration of the convergence thesis*," not a biological discovery.** A pre-registered expansion (NB12)
> took it from 22/22 to 29/33 and, more importantly, located the boundary (misses are systemic-route genes). The
> failure-boundary reading rests on n=4 and one high-confidence miss (ATP7B). A **primate-phylogenetics**
> direction is now under parallel exploration and may displace this as the flagship. Framing is up in the air.

## The bar

The project's own audits set a high bar: a prior "finding" (a network-degree difference between phenotype
groups) was retracted once it was shown to be a literature/study-bias artifact. So every candidate below is
judged on the same three axes: **novelty**, **robustness against study bias**, and **usefulness to the
pigmentation-genetics community** — and a candidate that only survives on the study-biased STRING layer is
scored as *not robust*, by the project's own standard.

## The candidates, ranked

### 1. ★ The mechanism→direction law (NB10) — the most interesting finding

**Claim.** A gene that is a *positive regulator of melanin* (loss reduces pigment), mutated by a
*loss-of-function* allele, causes **hypo**pigmentation; a negative regulator causes hyperpigmentation. The rule
is defined *only* under loss of function.

**Evidence.** 22/22 recessive/X-linked genes with a direction call are concordant, against a loss-of-function
base rate of 54 % hypopigmentation (permutation *p* < 1×10⁻⁵; Fisher loss-of-function-vs-dominant *p* ≈
1×10⁻³). Three independent direction sources — CRISPR screen, GRN sign, signed network — each agree within
their coverage (19/19, 4/4, 4/4). Every dominant discordance has a documented non-loss-of-function mechanism;
*TYR* flips direction within a single gene across its allelic series.

**Why it wins.**
- **Robust.** It does *not* live on the STRING layer. Its strongest line is the Bajpai CRISPR screen —
  literature-independent, functional. The other two lines are mechanistic (Raghunath/GRN), not co-citation
  association. It is the one candidate this pass produced that clears the project's own study-bias bar.
- **Novel and directional.** It is not "these two gene lists overlap." It predicts *which way* the phenotype
  moves and states the exact condition (loss-of-function allele) under which the prediction is valid — and its
  own falsification rule (positive regulator + hyperpigmentation ⇒ look for a non-LoF allele).
- **Useful.** It is the project's convergence thesis made directional and predictive, on the cleanest
  substrate (high-penetrance Mendelian disorders). It composes with the rescue screen: that screen says *which*
  gene; this law says *which direction*.

**Limits (stated, not hidden).** Small n (22 LoF, 13 dominant); inheritance taken from OMIM curation as given;
the three sources share the Raghunath backbone (independent of the *clinical* phenotype, which is what the test
requires); endpoint is a shortest-path proxy.

### 2. Cancer-gene pleiotropy in the network — real but small, mostly a study-bias artifact

**Claim tested.** Are positive melanin regulators / network hubs enriched for cancer genes, with a directional
(oncogene vs tumor-suppressor) pattern?

**Result.** 33/803 (4.1 %) network nodes are cancer genes — consistent with the qualitative Pavan & Sturm 2019
"shared backbone," but below the "~1 in 6" figure (which reflects a more STRING/literature-biased node set).
Raw hub enrichment is large (5.7×, *p* = 4×10⁻¹²) but **>80 % attributable to the STRING layer**; it shrinks to
2.3× (OR 3.59, *p* = 7.6×10⁻⁴) on mechanistic-only edges and to **non-significant** on the unbiased CRISPR layer
(2/29, *p* = 0.34). No clean oncogene-vs-tumor-suppressor direction: overlapping genes run both ways.

**Verdict.** A partially real but modest signal that mostly recapitulates the known overlap and largely
dissolves under the study-bias control — the same failure mode the project already retracted once. Not a
flagship; a good honest bound. `robust = False`.

### 3. The layer-convergence prior itself — a negative result that matters

**Claim tested.** Does agreement across independent evidence layers (the project's *core organizing
assumption*) predict ground-truth causal genes?

**Result.** With all six layers, layer count predicts causal status well (AUC 0.67–0.72, OR/layer 1.66–1.86,
*p* < 1×10⁻⁵). But two of the six "independent" layers (STRING_ours, D'Arcy_STRING) cover 99.6 %/78 % of OMIM
genes — because those networks were built by querying STRING *around the project's own pigmentation gene list*,
which already contains the OMIM genes. Drop those two layers and the relationship **reverses** for OMIM (AUC
0.29) and **collapses to chance** for CRISPR hits (AUC 0.49, *p* = 0.23).

**Verdict.** The convergence prior, as currently operationalized, is substantially circular: "more layers"
largely means "queried against a network built from the disease-gene list itself." This is the most
consequential negative result of the pass — it says the project must define convergence over *genuinely
source-independent* layers (as NB10 does: function vs clinic) rather than over STRING supersets of its own
input. `robust = False` (as a positive claim); **highly useful as a methodological correction.**

### 4. (Prior-session context) The two methodological findings already on record

The concurrent session's honest pivot produced two "the choice changes the answer" results — *network choice*
(NB5: our STRING recovers 60 % of Raghunath edges, 34 % drift vs D'Arcy) and *tissue choice* (NB8-diag:
melanocyte-vs-bulk eQTL retracts false causal calls). These are real and valuable, but they are **cautionary /
methodological** — they tell you what *not* to trust. NB10 is the pass's one **constructive, predictive**
result.

## The pick

**The mechanism→direction law (Finding 1, NB10) is the most interesting finding the assembled data support.**
It is the only candidate that is simultaneously (a) a positive, directional, predictive claim rather than a
caution, (b) robust against the study-bias confound that killed the earlier degree finding and that findings 2
and 3 both succumb to, and (c) a direct, sharpened instance of the project's fixed goal — trusting a
gene→phenotype link where independent evidence converges — with an explicit validity condition and its own
falsification rule.

Findings 2 and 3 are not failures; they are the due-diligence backdrop that makes Finding 1 credible. In
particular, Finding 3 reframes the project's convergence story: convergence is predictive **when the layers are
genuinely source-independent (function vs clinic, as in NB10)** and misleading when they are STRING supersets
of the input gene list. That is a useful sharpening of the thesis, not just a negative.

## Artifacts produced this pass

- `notebooks/10_mechanism_direction_law.ipynb` — the standalone mini-manuscript (NB10).
- `notebooks/figures/nb10_direction_law.png` — the two-panel figure.
- `data/processed/nb10_direction_law_annotation.csv`, `nb10_direction_law_summary.csv` — backing tables.
- `cancer_gene_enrichment_results.csv` + `cancer_gene_enrichment.png` — Finding 2 (probe).
- `layer_convergence_causal_summary.csv` + `layer_convergence_auc.png` — Finding 3 (probe).
- `crispr_omim_convergence_memo.md` (earlier this session) — the original 23-gene version of Finding 1.
