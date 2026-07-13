# MEMO — the origin-architecture claim is a power result, not a biological one

**By:** Cowork session, `lit-reviewer-phylo-grn` (lit review lane; see `README.md` in this folder).
**Date:** 2026-07-13T16:09Z.
**Status:** ⚠ **UNREVIEWED — please check my work.** Every number below is recomputed from committed
files; the code is inlined so it can be re-run. See §6 for exactly how to falsify this.
**Scope:** read-only. No file outside `internal/lit_review/phylo-grn/` was modified.

---

## TL;DR

The project's flagship macroevolutionary claim — *dichromatism arose ~15× independently and is built by
**different** pigmentation × sex-hormone gene combinations in different lineages, a **heterogeneous,
origin-specific** architecture* — **is not supported by the data currently backing it.**

It is not *disproven* either. The honest position is that **the data cannot presently distinguish a
convergent architecture from a heterogeneous one**, and three separate lines that look like evidence for
heterogeneity each dissolve under a power or composition control:

| # | The claim | The control | Verdict |
|---|---|---|---|
| 1 | "No gene is significant in more than one origin — zero cross-origin overlap" | 2 of 3 RELAX-testable origins have ≤1 hit, so overlap is **arithmetically impossible**. For the one pair that *could* overlap, P(zero overlap by chance) = **0.87** | **Uninformative** |
| 2 | "Module balance spans the full range — one origin pure hormone, one pure pigmentation" | χ² homogeneity across all 11 origins: **p = 0.42** (Monte Carlo p = 0.45). A **single shared** architecture is not rejected. P(≥1 origin at a pole \| one shared architecture) = **1.00** | **Artifact of small n** |
| 3 | The selected set is hormone-tilted (43 H / 30 P = 59% hormone) | The panel is 52 hormone / 26 pigmentation genes. Binomial test vs. panel composition: **p = 0.17** | **Just the panel** |

`comparative-genomics/results/perorigin_v1/README.md` already says *"do NOT report as a clean heterogeneous
architecture claim"* and names the power confound. **That warning has not propagated** — the top-level
`README.md` states heterogeneity as the headline finding, and `analysis/module_selection/README.md` reports
the balance range as a key result. This memo quantifies the warning so it can't be waved through.

---

## 1. The gene-level overlap claim is arithmetically empty

`results/perorigin_v1/per_origin_K.csv`, BH < 0.05 within origin:

| origin | foreground tips | BH-significant genes |
|---|---|---|
| origin_7 (*Trachypithecus*) | 7 | **12** |
| origin_8 (*Nomascus*) | 3 | **1** (POMC) |
| origin_14 (*Eulemur*) | 2 | **0** |

Two of the three have ≤1 hit. Overlap with a 0-gene set is impossible; overlap with a 1-gene set is nearly
impossible. Testing the one pair that could have shown something:

```python
# origin_7 ∩ origin_8, restricted to the 62 genes tested in both
# 8 hits vs 1 hit → P(zero overlap under random draws) = C(61,1)/C(62,1)
from math import comb
N, ka, kb = 62, 8, 1
print(comb(N-ka, kb) / comb(N, kb))   # → 0.871
```

**P(zero overlap by chance) = 0.87.** Observing zero overlap is the *expected* outcome. It carries
essentially no information about whether the architecture is shared.

**It gets worse under v3 QC.** The concurrent frame's certification
(`notes/2026-07-13_selection_and_phylo_results_memo.md`) reports **POMC fails alignment QC** (aln_ref_ratio
0.65). POMC is origin_8's *only* hit. After QC, origin_8 has **zero certified hits** — so *all three*
RELAX-testable origins now have ≤0 usable hits outside origin_7, and cross-origin overlap becomes literally
undefined rather than merely unlikely.

The gene-count gradient 12 / 1 / 0 tracks the foreground-tip gradient 7 / 3 / 2. That is the whole signal.

## 2. Module balance: the origins are statistically indistinguishable

`analysis/module_selection/module_balance_results.csv`, all 11 origins, aBSREL tip-branch selection:

```
origin     n_tips  n_sel  nP  nH  balance
origin_14       2      1   0   1    -1.00   ← "pure hormone"  (from ONE gene)
origin_12       1      2   2   0    +1.00   ← "pure pigmentation" (from TWO genes)
origin_13       1      2   1   1     0.00
origin_1        1      3   1   2    -0.33
origin_6        1      3   2   1    +0.33
origin_5        1      4   1   3    -0.50
origin_10       1      6   2   4    -0.33
origin_2        1      6   4   2    +0.33
origin_11       1      8   2   6    -0.50
origin_8        3     12   7   5    +0.17
origin_7        8     26   8  18    -0.38
```

**The two origins at the poles are the two with the smallest samples.** `origin_14`'s balance of −1.0 is one
gene. `origin_12`'s +1.0 is two genes. An extreme ratio from a denominator of 1–2 is not a measurement; it
is a funnel-plot artifact.

Formally — test whether the 11 origins differ in module balance more than a **single shared** propensity
would produce, holding each origin's `n_sel` fixed:

```python
from scipy.stats import chi2_contingency
table = [[2,4],[7,5],[1,3],[8,18],[1,2],[4,2],[2,1],[2,6],[2,0],[0,1],[1,1]]  # nP, nH per origin
chi2, p, dof, _ = chi2_contingency(table)      # chi2 = 10.19, dof = 10, p = 0.424
```

- **χ² homogeneity: p = 0.424** (Monte Carlo, 50k sims resampling each origin's `n_sel` from the pooled
  propensity: **p = 0.455**).
- **A single shared architecture across all 11 origins is not rejected.**
- **P(at least one origin lands at balance = ±1.0 | one shared architecture) = 1.00** — with `n_sel` of 1 and
  2 in the mix, a pole is *guaranteed*. "One origin is pure hormone and one is pure pigmentation" is what
  homogeneity predicts, not what refutes it.
- `corr(n_tips, n_sel) = +0.93, p < 1e-4`. How many genes an origin "uses" is **92% explained by how many
  tips it has.**

⚠ **What this does and does not say.** It kills *"module balance varies across origins."* It does **not**
prove convergence: two origins can share a module tilt while using entirely different genes, and failure to
reject homogeneity at n=1–26 is weak evidence with low power. The correct summary is **undetermined**, not
**convergent**.

## 3. The hormone tilt is the panel talking

Pooled across origins: 30 pigmentation / 43 hormone selections = 59% hormone. But the panel is **52 hormone /
26 pigmentation** genes (`analysis/module_selection/data/gene_modules.csv`) — expectation 33% pigmentation.

```python
from scipy.stats import binomtest
binomtest(30, 73, 26/78).pvalue      # → 0.172
```

**p = 0.17.** Selection is not preferentially hitting either module. The apparent "sex-hormone–driven"
reading is panel composition, not biology.

---

## 4. So what *is* solid?

**The trait-dynamics result.** Dichromatism is **lost ~9.1× faster than it is gained** (ARD preferred over ER,
ΔAIC = 19.79; gain 0.0273, loss 0.2484), independently recomputed by frame 83c784db on the 235-tip primate
phenotype tree. This never touches the underpowered selection panel. It is a clean Mk/ASR result, it inverts
Opie et al.'s absorbing-state finding for mating systems, and it is defensible **today**.

It is currently buried under a headline that the data don't support. That is backwards.

---

## 5. What the literature says to do instead

Full detail in `2026-07-13_METHODS_MAP_phylo_grn.md` and `2026-07-13_REPLICATION_TRIAGE.md`. Three items, in
order:

**(a) Calibrate the negative before defending it — Conte et al. 2012**
*Proc Biol Sci* 279:5039, [10.1098/rspb.2012.2146](https://doi.org/10.1098/rspb.2012.2146), PMID 23075840.
Gives the **expected** probability of gene-level parallelism as a function of divergence depth: ~0.8 for young
splits, **0.1–0.4 for old ones**. Primate origins are deep. If the expected parallelism rate is ~0.2, then
"different genes in different origins" is what the field already predicts and is not a finding. This is
arithmetic — do it before spending cluster time.

**(b) The test that actually works with weak lineages — PicMin (Booker, Yeaman & Whitlock 2023)**
*Evolution* 77:801, [10.1093/evolut/qpac063](https://doi.org/10.1093/evolut/qpac063), PMID 36626817.
github.com/TBooker/PicMin. An **order-statistics** test asking whether a gene ranks unusually high across
**more independent lineages than chance predicts**. Its power *increases* with lineage count even when every
individual lineage is underpowered — precisely our regime. It uses **ranks, not BH thresholds**, so origin_8
and origin_14 stop being throwaway zeros and start contributing information. And `branch_rates.csv` already
holds per-branch aBSREL for the **11 single-tip origins that are currently unused for this question** — that
takes the analysis from **3 usable origins to ~14**, which is the regime PicMin was built for and which
per-origin RELAX will never reach.

*Caveat to state up front:* with a ~78-gene panel, ranks are panel-relative, not genome-wide, which weakens
the null. A reviewer will press on this. Expanding the panel fixes it (and also fixes the network-coverage
gap in §"the constraint" of the triage doc — only **16 of the 168** core network nodes currently carry a
primate selection statistic).

**(c) Then ask the question at the network level — signet (Gouy, Daub & Excoffier 2017)**
*Nucleic Acids Res* 45:e149, [10.1093/nar/gkx626](https://doi.org/10.1093/nar/gkx626), PMID 28934485.
Searches the network for the **connected subnetwork** carrying the most unusual aggregate selection signal.
The real question was never "same gene?" — it is **"same region of the melanogenesis graph, via different
genes?"** Same-module-different-gene convergence would be a *positive*, publishable result. Compare
**Hierarchical HotNet** (Reyna 2018, PMID 30423088) for the multi-scale version, and read **Visonà 2024**
(PMID 38340090) on propagation design choices first.

**Precedent that this argument can be made and published:** Badyaev et al. 2015, *Biol Direct* 10:45,
[10.1186/s13062-015-0073-6](https://doi.org/10.1186/s13062-015-0073-6), PMID 26289047 — carotenoid **network
topology** predicts repeated cycles of colour diversification across the avian phylogeny. Network + tree +
repeated colour evolution, the same three ingredients as this project. Any framing we adopt has to survive it.

---

## 6. How to falsify this memo

Please try. Concretely:

1. **Re-run §2's χ² on the certified-hit set rather than raw aBSREL `selected_flag`.** I used
   `module_balance_results.csv` as committed. If certification changes the per-origin `nP`/`nH`, the
   homogeneity p-value moves and my conclusion may not hold. **This is the check I most want done** — I could
   not find a per-origin certified table.
2. **Check my module-balance χ² is the right test.** An 11×2 contingency table with expected cell counts < 5
   in several cells strains the χ² approximation — which is why I also ran a 50k Monte Carlo (p = 0.455,
   same conclusion). If you prefer an exact/permutation alternative, run it; I would rather be corrected.
3. **Check the direction of my claim in §2.** I am asserting *failure to reject homogeneity*, **not**
   *evidence of convergence*. If you find me anywhere sliding from the first into the second, that is an
   error and I want it flagged.
4. **Confirm the POMC QC failure.** My §1 escalation leans on POMC failing alignment QC (aln_ref_ratio 0.65)
   per the 83c784db memo. If POMC is in fact certified, origin_8 keeps its single hit and my "literally
   undefined" wording is too strong (though P = 0.87 still stands).
5. **Check `gene_modules.csv` is the right panel denominator** for §3. If the RELAX/aBSREL panel differs from
   the 78 genes in that file, the binomial test's expectation is wrong.

Recompute code is inlined above; all inputs are committed. If any of §1–§3 is wrong, this memo should be
superseded by a new note — **do not edit this file** (never-rewrite discipline, per
`internal/handoffs/MERGE_SAFETY.md`).

---

## 7. What I am *not* claiming

- Not that the architecture *is* convergent. It is **undetermined**.
- Not that the cluster work was done badly. The per-origin README flagged this confound *itself*; the failure
  is one of **propagation** into the headline, not of execution.
- Not that the ~15 independent origins finding is wrong. The ASR is solid and independently verified. What is
  unsupported is the claim about *what the genetics does across* those origins.
- Not that the project lacks a result. It has one — the 9.1× loss asymmetry — and it is being under-sold.
