# Track 2 — Coevolution of Interacting Partners (Local Pilot)

**Status:** local pilot, run to completion. Two complementary methods — mirrortree
(distance-matrix coevolution) and ERC-from-aBSREL (branch-rate coevolution) — both
restricted to GRN-edge vs. non-edge pairs among the 77 RELAX panel genes. This
document reports what was run, the numbers, and how to read them.

**The headline result is a null, and the null is underpowered, not informative.**
With only 15 (core) / 18 (substrate) true within-panel GRN edges among 13 connected
genes, this pilot has essentially no ability to detect a real coevolution signal even
if one exists. Absence of a permutation p < 0.05 here is not evidence that pigmentation
genes don't coevolve with their GRN partners — it is evidence that 13-15 data points
is not enough to say anything with confidence. See `CONCLUSION.md` and
`feasibility/TIERED_PLAN.md` in the parent directory for why the definitive version of
this analysis is scoped as cluster work (full 77-gene ML per-gene trees, RERconverge
permulations, all origins), not this pilot.

---

## 1. Methods

### 1.1 Mirrortree (Analysis 2A)

- **Input:** the 79 codon alignments in `aln117_codon.tar.gz` (77 of 77 panel genes
  have an alignment; extracted to a scratch directory, not tracked in this repo).
- **Distance metric:** each codon alignment was translated to protein (in-frame codon
  triplets → amino acid; incomplete/gapped/ambiguous codons and stop codons →
  missing/`X`, excluded pairwise) and a pairwise **protein p-distance** (proportion of
  mismatching ungapped-in-both-sequences sites) was computed for every taxon pair
  within each gene's alignment. Protein p-distance was chosen over a nucleotide
  (codon or all-sites) distance because pigmentation/hormone-panel genes span a
  ~40-Myr primate radiation with substantial synonymous-site saturation at third-codon
  positions; amino-acid identity is more conservative and comparable across genes of
  different length and base composition. This is a simple observed-differences
  distance (not a corrected/ML distance) — appropriate for a same-day local pilot; the
  cluster version should consider an ML (e.g. LG+ML) or maximum-likelihood branch-length
  distance for the definitive analysis.
- **Mirrortree score:** for every gene pair, the two per-gene distance matrices were
  restricted to their shared taxa (≥15 required to test the pair), the upper triangles
  vectorized, and correlated (Pearson and Spearman). 2,870 of 2,926 possible panel
  pairs (98.1%) cleared the ≥15-shared-taxa bar and were scored.
- **Edge labels:** the 15 within-panel directed non-self GRN edges (`network=core`)
  and the 3 additional edges present only in the 803-node multilayer substrate
  (`network=substrate_extra`; PAX3–DCT, PAX3–TYR, PAX3–TYRP1) are reported both
  separately and pooled (`core` ∪ `substrate_extra` = 18 edges), against all remaining
  panel pairs as `non_edge`. All 15 core and all 18 substrate edges cleared the
  shared-taxa filter and were testable.

### 1.2 ERC from aBSREL branch rates (Analysis 2B)

- **Input:** the existing `<GENE>.ABSREL.json` fits (no new tree-building or model
  fitting). 39 of 78 fitted genes are non-empty (the other 39 are empty/failed
  HyPhy runs, a pre-existing artifact of the panel-wide run, not something this
  pilot investigated).
- **Rate extraction:** per-branch **Baseline MG94xREV** branch lengths (the
  codon-model branch-length attribute fit under the null/baseline model before
  aBSREL's per-branch rate-class search) were pulled from `branch attributes` keyed
  by tip taxon name; internal `NodeN` labels were skipped because internal-node
  numbering is not comparable across independently-fit gene trees.
- **QC applied (undocumented in the task spec, added because the raw data required
  it):** 31 of 2,849 gene×tip branch-length cells (1.1%) were >1.0 substitutions/site
  — biologically implausible for these branch lengths (typical values are
  1e-4–0.5) and diagnostic of the aBSREL branch-length-blowup failure mode this
  project has already documented for near-zero-synonymous-change branches (values as
  extreme as 2057 and 1065 subs/site were observed, concentrated in
  AKR1C2/CYP11B1/CYP11B2/ESR2/OCA2/STS). These cells were masked to missing before any
  downstream statistic; leaving them in inflates every correlation involving the
  affected gene toward ±1 by injecting a shared extreme outlier tip into both vectors
  (raw, unfiltered Pearson |r| mean across all pairs was 0.68 with 520/718 pairs at
  |r|>0.995; after masking, mean |r| dropped to 0.45 with a normal-looking
  distribution — see `erc_absrel_pairs.csv`, computed post-QC).
- **Relative rate transform:** for each tip present in ≥5 genes, the cross-gene mean
  branch length at that tip was subtracted from every gene's branch length at that
  tip (a per-tip residual, following the RERconverge logic of removing the
  tip's overall depth/rate before comparing genes) — not raw branch lengths, per the
  task's stated preference, since raw lengths are dominated by each tip's overall
  distance from the root and would inflate cross-gene correlation for tree-topology
  reasons unrelated to coevolution.
- **ERC score:** per-gene relative-rate vectors were restricted to shared tips
  (≥15 required), then correlated (Pearson, Spearman) the same way as mirrortree.
  718 of 741 possible pairs among the 39 non-empty genes cleared the shared-tip bar.
- **Coverage — the binding constraint for 2B:** only 7 of the 13 core-connected genes
  (EDNRB, KIT, MITF, MLANA, OCA2, SOX10, TYRP1) have a usable aBSREL fit. Among these
  7 genes, only **6 of the 15 core edges** are even in principle testable (both
  endpoints fitted): MITF–EDNRB, MITF–TYRP1, MITF–SOX10, MITF–MLANA, MITF–OCA2,
  SOX10–TYRP1. All 6 cleared the shared-tip filter. **KIT is present but isolated** —
  its only core-network neighbor (KITLG) has no aBSREL fit, so KIT contributes no
  edge to this test.

### 1.3 Permutation null (both analyses)

Both edge-vs-non-edge comparisons use the **same degree-preserving double-edge-swap
rewiring null used in Track 1**: the observed graph (13 nodes / 15 edges for the core
mirrortree test, 13 nodes / 18 edges for the substrate mirrortree test, 7 nodes / 6
edges for the ERC test) is rewired via NetworkX `double_edge_swap` while holding every
node's degree fixed, the test statistic (mean |edge correlation| − mean |non-edge
correlation|, restricted to that graph's node set) is recomputed on the rewired graph
using the *unpermuted* observed correlations, repeated **10,000 times** with a fixed
seed (`seed=42`), and the two-sided empirical p-value is the fraction of rewirings with
|T_rewired| ≥ |T_observed|.

---

## 2. Results

### 2A — Mirrortree

| network | method | mean\|r\| edge | mean\|r\| non-edge | n edge | n non-edge | p_perm |
|---|---|---|---|---|---|---|
| core (15 edges) | Pearson | 0.167 | 0.404 | 15 | 63 | 0.608 |
| core (15 edges) | Spearman | 0.239 | 0.478 | 15 | 63 | 0.376 |
| substrate (18 edges) | Pearson | 0.145 | 0.422 | 18 | 60 | 0.488 |
| substrate (18 edges) | Spearman | 0.231 | 0.493 | 18 | 60 | 0.264 |

(non-edge n here is restricted to pairs among the same 13 connected genes —
C(13,2) − n_edge; the full 77-gene panel background, 2,852 non-edge pairs, has mean
|Pearson r| = 0.338, reported in `mirrortree_edge_vs_nonedge.csv` for context.)

**No significant excess |correlation| on GRN edges in either network, by either
correlation method.** If anything the observed edges have *lower* mean |r| than
non-edges (T_obs < 0) in every one of the four tests, opposite the coevolution
hypothesis's predicted direction — but none of the four differences survive the
degree-preserving null (all p_perm > 0.25), and a sign that flips depending on which
13-gene subgraph or correlation method you pick is itself a symptom of n=15-18 being
too few edges to resolve a direction, not evidence of a genuine depletion.

### 2B — ERC (aBSREL branch rates)

| network | method | mean\|r\| edge | mean\|r\| non-edge | n edge | n non-edge | p_perm | n genes w/ aBSREL |
|---|---|---|---|---|---|---|---|
| core (6 testable edges, 7 genes) | Pearson | 0.761 | 0.745 | 6 | 15 | **1.000** | 39 |
| core (6 testable edges, 7 genes) | Spearman | 0.623 | 0.656 | 6 | 15 | **1.000** | 39 |

**The ERC permutation p-value of 1.000 is a degenerate null, not a real result, and
must not be read as "definitely no effect."** The 7-gene aBSREL-covered subgraph has
degree sequence {MITF: 5, SOX10: 2, TYRP1: 2, EDNRB: 1, MLANA: 1, OCA2: 1, KIT: 0}.
MITF's degree of 5 equals the number of non-isolated non-MITF nodes, forcing MITF to
connect to every one of them; the remaining +1 degree budget on SOX10 and TYRP1 then
forces the SOX10–TYRP1 edge. **This degree sequence has exactly one realizable simple
graph** — the observed graph itself — so every double-edge-swap attempt fails (0/10,000
rewirings produced a distinct graph in a manual check) and the permutation null is a
point mass at T_obs, giving p_perm=1.000 by construction regardless of the true
biology. This is reported honestly rather than concealed: **2B, as run, cannot
distinguish signal from noise at n=6 edges over 7 genes** — this is a coverage failure
of the permutation test's design, not a null finding about coevolution. A valid test
at this coverage would need a different null (e.g., gene-label permutation, or pooling
across a less structurally over-constrained node set) — out of scope for this same-day
pilot, flagged for anyone extending this local track.

---

## 3. Interpretation

1. **No local evidence for excess coevolutionary-rate similarity on melanogenesis GRN
   edges**, in either the mirrortree (distance-matrix) or ERC (branch-rate) framing,
   at the only edge count this project's curated network currently supports (15-18
   edges / 13 connected genes for mirrortree; 6 edges / 7 genes for ERC).
2. **This is expected and uninformative, not a negative result.** A degree-preserving
   permutation test with 15-18 edges has very limited power to detect anything short
   of an enormous effect; the ERC test additionally hit a null-model degeneracy that
   makes its own p-value uninterpretable. Neither analysis should be cited as evidence
   against GRN-edge coevolution in melanogenesis genes.
3. **The direction even disagrees with the hypothesis in the powered test (mirrortree)**
   — edges show *lower*, not higher, mean |correlation| than non-edges, in both the
   core and substrate networks, by both correlation methods. Given the effect sizes
   involved (0.17 vs 0.40, roughly a 2.4-fold ratio) and the total absence of
   permutation significance, the most defensible reading is that mirrortree distance
   correlation is dominated by shared phylogenetic depth/taxon-sampling structure
   across *all* panel gene pairs (median non-edge |r| itself is not small — 0.24-0.46
   depending on method — consistent with a shared-ancestry/rate-covariation floor that
   swamps any GRN-specific signal at this scale), not that GRN partners evolve less
   alike than non-partners.
4. **MITF's hub status (degree 5-10 depending on network) is a structural confound
   this design only partially controls.** The degree-preserving null holds MITF's
   degree fixed under rewiring, so it does correct for "hub genes trivially look
   different" in the sense of comparing MITF-degree-10 subgraphs to other
   MITF-degree-10 subgraphs — but MITF is a well-documented pleiotropic melanogenesis
   master regulator, and pooled coevolution signal at any one of its edges could be
   diluted by non-pigmentation constraint acting on MITF's many other regulatory
   roles, exactly as this project's `internal/network-evo-explore/` work already found
   for centrality-vs-constraint more generally. This pilot has no cross-species
   expression data and cannot separate that dilution from a true absence of
   coevolution.

## 4. Confounds and caveats (explicit)

- **Alignment-quality bias in aBSREL missingness.** The 39/78 genes with usable aBSREL
  fits are not a random subsample of the panel — genes that failed to fit are
  systematically enriched for alignment/tree-estimation problems (short CDS, poor
  taxon coverage, or convergence failures under aBSREL's per-branch rate-class search).
  ERC's 7-gene, 6-edge coverage of the core network is therefore not a clean random
  dilution of Track 2A's already-small 15-edge sample — it's whichever core genes
  happened to fit cleanly, and MITF's centrality in that surviving subgraph is itself
  parlty an artifact of which genes fit rather than a property of the network.
- **Shared-taxa / shared-tip requirement (≥15).** All 15 core and 18 substrate
  mirrortree edges cleared this bar; only 3 core-genes' worth of KIT-MC1R,
  KIT-OCA2, KIT-PMEL panel pairs (not core/substrate edges) fell below it and were
  excluded from all summaries — a negligible loss for 2A. For 2B the bar is the
  reason KIT contributes zero edges (its only fitted-panel partner interactions
  don't include KITLG).
- **n=15 (or 18) true edges is the fundamental limit for 2A,** and n=6 for 2B. Both are
  far too few for any permutation test — degree-preserving or otherwise — to
  distinguish a moderate true effect from noise. Treat every p-value in this document
  as a pilot-scale sanity check, not a confirmatory statistic.
- **The protein p-distance and raw Baseline-MG94xREV branch length are simple, not
  ML-optimal, distance/rate choices**, appropriate for a same-day local run but a
  known simplification relative to what the cluster-scale RERconverge pipeline
  (`comparative-genomics/scripts/04_rerconverge.R`) would compute with per-gene ML
  trees.
- **The QC threshold (>1.0 substitutions/site) for aBSREL branch-length artifacts was
  chosen post hoc from inspection of the data**, not pre-registered; it removed 31 of
  2,849 cells (1.1%) and changed the ERC pairwise-correlation distribution from a
  degenerate near-±1 pileup to a plausible-looking distribution (see
  `erc_absrel_pairs.csv`). Anyone re-running this analysis should re-examine whether
  1.0 is the right cutoff for their use case.

## 5. What this pilot is not

**This is a local, same-day pilot bounded by the data already on disk — not the
definitive coevolution/ERC test.** The definitive version, as scoped in
`feasibility/TIERED_PLAN.md` (§ "Recommended test: pairwise coevolutionary-rate
(mirrortree/ERC) test on GRN edges"), is **cluster work**: per-gene maximum-likelihood
branch-length trees for all 77 panel genes on a shared topology (extending
`04_rerconverge.R`, which builds this machinery but has not yet been run to
completion), RERconverge's full relative-evolutionary-rate transform, the complete
77×77 pairwise rate-correlation matrix, and — critically — **permulations** (the
phylogenetic permutation scheme RERconverge uses to test convergent rate shifts across
**all 14 independent origins** of the trait/network structure of interest, not a
single degree-preserving rewiring of one 13-15-node subgraph). That cluster run is the
analysis whose p-value should actually be trusted for a coevolution claim; this
document's numbers are a feasibility/sanity check that ran to completion locally using
already-computed alignments and aBSREL fits, nothing more.

---

## 6. Files in this directory

- `mirrortree_pairs.csv` — all 2,870 testable panel gene-pairs: `gene_i, gene_j,
  n_shared_taxa, pearson, spearman, is_grn_edge, network` (`network` ∈
  {`core`, `substrate_extra`, `non_edge`}).
- `mirrortree_edge_vs_nonedge.csv` — the 4-row summary table above (core/substrate ×
  Pearson/Spearman), plus the full-panel non-edge context columns.
- `erc_absrel_pairs.csv` — all 718 testable gene-pairs among the 39 aBSREL-fit genes
  (post-QC): `gene_i, gene_j, n_shared_tips, pearson, spearman, is_grn_edge, network`.
- `erc_edge_vs_nonedge.csv` — the ERC summary row, plus `n_genes_with_absrel=39`.
- `track2_coevolution_edge_vs_nonedge.png` — deliverable figure: mirrortree (panel a)
  and ERC (panel b) edge-vs-non-edge |correlation| distributions, colorblind-safe
  (orange focal edge markers / grey non-edge violin), with permutation p-values
  annotated.
- `RESULTS_track2.md` — this document.
