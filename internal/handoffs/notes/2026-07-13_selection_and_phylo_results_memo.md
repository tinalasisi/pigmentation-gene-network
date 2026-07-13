# Results memo — selection + phylogenetic tests on the latest cluster data

_By: Claude Science (PI_ORCHESTRATOR, frame 83c784db), 2026-07-13._
_Ties together (a) the v3-certified selection hits, (b) the Opie-analog trait-dynamics_
_results, (c) the per-lineage pigment-vs-hormone metric, and (d) the fitPagel correlated-_
_evolution test, on the latest data (perorigin_v1, commit 4c07317; 238-species / 26-_
_dichromatic coding). Numbers are read from committed files, not memory._

## Data baseline
- Phenotype: `config/primate_dichromatism_coding.csv` — 238 species, 26 dichromatic
  (10 complete + 16 partial). (Earlier "24 dichromatic" is superseded.)
- Selection: `results/perorigin_v1/` — per-origin RELAX (`per_origin_K.csv`) and full-panel
  aBSREL (`branch_rates.csv`, 78 genes x 288 branches).
- Trees: 235-tip Leakey phenotype tree; 304-tip genome-sampled tree.

## 1. Certified selection hits (v3 QC gates applied) — `analysis/certified_hits.csv`
Nine genes pass the certification gates (K boundary, foreground branch length, gap
fraction, alignment ref-ratio). Split by module:

**Sex-hormone module (6):** HSD17B1 (K=2.93), HSD17B12 (K=2.52), SRD5A1 (K=2.32,
gaps>20% flag), CYP7B1 (K=1.37), HSD17B7 (K=1.32) — all intensified; SHBG (K=0.24) —
relaxed. The intensified hits are steroid-metabolism **enzymes**, not receptors.

**Pigmentation module (3):** TFAP2A (K=1.93, p_BH=1e-4), KITLG (K=1.30), EDN3 (K=1.28,
branch-length-blowup flag) — all intensified, all on the melanoblast-development axis.

**Correction vs. the interim doc:** KIT is NOT certified in v3 (K=1.50, p_BH=0.95, 4
foreground tips); POMC and TYR FAIL alignment QC (aln_ref_ratio 0.68 / 0.65); MC1R is a
weak non-significant relaxation (K=0.45, p_BH=0.144) — the opposite of the bird
single-gene MC1R intensification model (Nadeau et al. 2007).

## 2. Opie-analog trait dynamics (dichromatism) — `analysis/module_selection/opie_analog_results.csv`
Replicating the *method* of Opie, Atkinson & Shultz (2012, "The evolutionary history of
primate mating systems," *Commun Integr Biol*, doi:10.4161/cib.20821) on our phenotype:

| Opie test | their mating-system result | our dichromatism result |
|---|---|---|
| Phylogenetic signal / model | lambda=0.996; RJ-MCMC best model 71% PP | Pagel's lambda=0.65 (p<1e-6); ARD asymmetric preferred |
| Gain rate (0->1) | strong into monogamy | 0.0273 |
| Loss rate (1->0) | ~zero reverse | 0.248 |
| Directional asymmetry | into monogamy (absorbing) | **loss 9.1x gain** (out of dichromatism) |
| Model support | asymmetric favored | dAIC(ARD-ER) = 19.79 |

Independently reproduced from raw data (see `2026-07-13_independent_check_module_selection.md`):
loss 9.10x gain, dAIC 19.79 — exact.

**Reading:** dichromatism has strong phylogenetic signal but is evolutionarily **labile**,
lost far more readily than gained. This is the closest structural analog to Opie — an
asymmetric, directional trait — though the direction is opposite (they found a trait
building toward an absorbing state; ours decays).

## 3. Per-lineage pigment-vs-hormone metric — `analysis/module_selection/module_balance_results.csv`
For each of 11 independent origins, balance = (nP - nH)/(nP + nH) over distinct genes under
aBSREL episodic selection along that origin's tip branches (+1 = all pigment, -1 = all
hormone). Independently verified exact for all 11 origins. Highlights:
- **Hormone-leaning:** Eulemur flavifrons origin (-1.0, hormone only), Alouatta caraya and
  Colobus guereza (-0.5).
- **Pigment-leaning:** Pithecia pithecia (+1.0, pigment only), Cercopithecus hamlyni and
  Colobus angolensis (+0.33).
- **The two RELAX-powered radiations:** Trachypithecus origin_7 (8P/18H = -0.38, hormone-
  leaning) and Nomascus origin_8 (7P/5H = +0.17, slightly pigment-leaning).

**Power caveat (from the perorigin_v1 README):** only 3 origins have enough foreground tips
for RELAX (7 / 3 / 2); the other 8 are aBSREL-only (single tip). The gene-count gradient
tracks power, so "different modules per origin" is confounded with "different power."
Boundary Ks (e.g. KISS1R ~15, SHBG ~0.017) need the QC gates before individual trust.

## 4. fitPagel correlated-evolution test — `analysis/coevolution_test/`
The one Opie test not in `module_selection/`: does module selection co-evolve with
dichromatism? Two binary traits per genomic tip (dichromatic y/n; module under aBSREL
selection y/n), independent vs dependent model via `phytools::fitPagel` (ML analog of
Opie's BayesTraits *Discrete* Bayes-factor test), 102 tips, 21 dichromatic.

| module | indep AIC | dep AIC | LR p | preferred |
|---|---|---|---|---|
| pigmentation | 216.09 | 219.78 | 0.37 | **independent** (by dAIC 3.7) |
| sex-hormone | 199.55 | 205.27 | 0.68 | **independent** (by dAIC 5.7) |

**Result:** module selection does NOT co-evolve with dichromatism at the lineage level — the
independent model is AIC-preferred for both modules. This reinforces the project's
non-significant set-level contrast (permutation p=0.87). **Power caveat:** only 21
dichromatic tips and selection is common across the panel, so this is "no detectable
coupling," not "coupling excluded."

## Synthesis
The certified per-gene signals are real and module-split (TFAP2A-KITLG-EDN3 on the pigment
side; steroid enzymes HSD17B1/12/7, SRD5A1, CYP7B1 on the hormone side). But the stronger,
lineage-level claims do not survive: (i) the genes under selection differ across origins in a
way confounded with power (§3); (ii) whether a lineage is dichromatic does not predict which
module is selected (§4, §the set-level p=0.87). The defensible statement is architectural,
not correlational: **primate sexual dichromatism is polygenic, module-split, origin-specific,
and evolutionarily labile — unlike the single-gene MC1R switch documented in birds.** That is
the novel finding; the pigment-vs-hormone coupling is a hypothesis the current data are
under-powered to confirm or reject.

## Caveats to carry into any write-up
1. Certified hits use v3 gates — do not cite KIT, POMC, or TYR as hits (§1).
2. Per-origin power is unequal (7/3/2 vs single tips); do not report the module gradient as a
   clean "heterogeneous architecture" result without the power caveat (§3).
3. fitPagel and the set-level test are both non-significant AND under-powered — report as
   "no detectable coupling," never as evidence of independence (§4).
4. Origin count: ~15 phenotypic origins on the tree, but only 3-4 are genome-powered for
   selection inference — keep the phenotypic-origin and selection-tested-origin counts distinct.
