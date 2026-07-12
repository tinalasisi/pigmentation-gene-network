# Interim selection findings — primate hair dichromatism

**Status: INTERIM.** Computed on the current 117-primate RELAX panel (commit `d2602ba`),
which still carries ~10 QC-flagged genes. A stricter-QC rerun (v3, `e227b87`, array
`53382777`) is running on the cluster and will convert the flagged genes into clean
rescue/kill calls. Every number below is provisional and must not be cited outside this
working analysis until the v3 certification.

Prepared by: mol-evo-specialist (Claude Science, frame 0d1cda86).
Data: `comparative-genomics/results/full_panel_117/` at `d2602ba`
(`relax_results.csv`, `fit_health.csv`), curated network `data/processed/nb7_substrate_*.csv`,
hormone seed (53 genes, axis-annotated).

---

## 1. Design recap — why this has power

Hair dichromatism arose **four independent times** across the 117 primates with usable
genomes: Lemuridae (*Eulemur*), Cebidae, Hylobatidae (gibbons, the flagship clade), and
Cercopithecidae. Independent origins — not species count — are what a convergence-based
test draws on. The Leakey species topology was cross-checked against an independent Open
Tree of Life synthesis: all four dichromatism clades are monophyletic in both trees, so the
branching structure the analysis rests on is not a local-source artifact. Neither RELAX nor
RERconverge uses the tree's (time-dated) branch lengths — both re-estimate substitution
branch lengths and use only the topology.

## 2. Method

RELAX (HyPhy) per gene, foreground = the dichromatic lineages, background = monochromatic.
K > 1 = **intensified** selection on the foreground; K < 1 = **relaxed**. Per-gene BH
correction across the panel. A gene is only trusted if it clears a QC gate:
`pct_gaps ≤ 25`, `1e-3 < K < 10`, `n_foreground ≥ 3`, `tree_len ≤ 50`,
`aln_ref_ratio ∈ [0.8, 1.2]`. The `aln_ref_ratio` gate is what correctly rejects TYR — its
alignment is only 65% of the reference protein length (a truncated extraction, not a
biological signal).

## 3. Certified per-gene result (21 BH-significant → tiered)

| Tier | Definition | Genes |
|---|---|---|
| **A — robust** | clean by every QC gate | **KIT** (pig, K=2.04, intensified) · **HSD17B12** (hor, K=2.39) · **HSD17B7** (hor, K=1.47) · **CYP7B1** (hor, K=1.27) — all intensified |
| **B — rescue-pending** | passes aggregate gate, trips per-branch flag; v3 resolves | KITLG, EDN3 (pig) · HSD17B1, FKBP5, AKR1C4 (hor) |
| **C — artifact** | fails QC; **not** reported as biology | TYR (aln 65% short), ASIP/PMEL/SCARB1/MFSD12/GNA11 (branch-length blowup), FOXD3 (K=17.8 degenerate), KISS1R (K→0 boundary), HSD17B2/NCOA1/OCA2 (gaps/truncation) |

**Honest headline:** intensified selection in dichromatic lineages is real and it is **not
pigmentation-only** — three of the four robust hits are sex-hormone genes.

## 4. Where the pigmentation signal sits — a connected module

The intensified pigmentation genes are not scattered. **KIT, KITLG and EDN3 form one
connected module** (KIT–KITLG signaling + EDN3–EDNRB endothelin axis, converging on
SOX10/MITF — the melanoblast development/migration pathway). Selection is remodeling a
coherent functional unit, not random pigmentation genes. See
`docs/figures/selection_two_networks.png` (panel A).

## 5. Where the hormone signal sits — a gene SET, by axis

**Why the hormones look absent in a network view:** the curated substrate network is a
*pigmentation* network. Of the 53 hormone genes, only 3 have any edge in it (1 hormone–hormone
edge). The hormone genes are a defensible, axis-annotated **set**, not yet a connected
network — so they are shown grouped by functional axis (panel B), not as a graph. This is a
structural fact about the current network build, not a lack of hormone signal.

The hormone signal is concentrated in **steroid-metabolism enzymes**: HSD17B12, HSD17B7,
CYP7B1 (all Tier-A, intensified), plus HSD17B1, AKR1C4, FKBP5 (Tier-B). These are the
enzymes that interconvert and clear active androgens/estrogens — biologically coherent for a
sexually dimorphic trait. The receptor/HPG-axis genes (AR, ESR1/2, the gonadotropins) are
largely null or QC-flagged.

## 6. Set-level test (SUMSTAT) — no significant difference YET

After QC, 9 pigmentation and 28 hormone genes are retained (small, unbalanced). Pigmentation
trends toward more intensified selection (mean signed score 1.42 vs 0.46), but neither the
100k-permutation label-swap test (**p = 0.470**) nor the Wilcoxon secondary (**p = 0.111**)
is significant. **There is no certified network-vs-network difference yet** — this is
underpowered until v3 fills the ~10 flagged genes back in. The pigmentation-leaning trend is
well within the null.

## 7. MC1R anchor — divergence from the bird result, not replication

Nadeau et al. 2007 (Proc R Soc B 274:1807, doi:10.1098/rspb.2007.0174) found that in 36
galliform birds, **MC1R alone** carried a dN/dS signature tracking plumage dichromatism
(genus-level GLS LRS ≈ 8.5, p ≈ 0.004), with the tyrosinase genes and AGRP null. In our
primates, MC1R is QC-clean but shows only weak, non-significant **relaxation**
(K = 0.50, p = 0.053, p_BH = 0.126) — not the bird's intensification. The clean, strong
primate hits are KIT/KITLG (melanoblast axis), a **different node** of the pigmentation
pathway. This is a genuine cross-taxon divergence in the molecular architecture of
dichromatism — more interesting than a replication — but must not be overstated: at
p_BH = 0.126 MC1R itself does not clear significance. Full per-locus table:
`docs/figures/` companion + the MC1R anchor memo.

## 8. What v3 changes

The cluster's v3 adds a stricter column trim (30% vs 50% gaps) and, critically,
**per-sequence outlier removal** (nearest-neighbor distance metric — validated to drop
misaligned/paralogous sequences while preserving genuinely divergent lemurs). This converts
the ~10 Tier-B/flagged genes into clean rescue/kill calls, at which point the SUMSTAT
network-vs-network test becomes valid and everything here is re-certified.

## Figures
- `selection_two_networks.png` — pigmentation network (A) + hormone set by axis (B), one K scale.
- `primate_dichromatism_tree.png` — the four independent origins.
- `certified_selection_summary.png` — all 21 BH-sig genes, tiered.
