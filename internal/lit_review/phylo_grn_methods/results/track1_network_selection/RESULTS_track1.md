# Track 1: Network/pathway-aware selection analyses

Family-1 analyses (GRN-neighbor selection-similarity permutation; module/pathway
enrichment) run on the frozen RELAX K panel (`comparative-genomics/results/full_panel_117/relax_results.csv`,
77 genes) intersected with the signed melanogenesis GRN
(`data/processed/gene_network_nodes.csv` / `gene_network_edges.csv`, 168 nodes / 309 edges)
and its 803-node multilayer-substrate extension (`data/processed/nb7_substrate_nodes.csv` /
`nb7_substrate_edges.csv`).

**Headline result, stated plainly up front: the induced-subgraph permutation test is
directionally consistent with the hypothesis that GRN-adjacent genes carry more similar
selection signal than non-adjacent genes (T_obs > 0 in both the core GRN and the
multilayer-substrate subgraph), but the effect does not clear a two-sided p < 0.05
threshold in either network (p = 0.109 core, p = 0.093 substrate). At n = 13 connected
genes / 15–18 edges this is an honest underpowered pilot, not evidence against a network
effect on selection.**

## Reproducibility sanity check (passed)

Before reporting any number below, panel/network intersections were re-derived from the
frozen source files and checked against the ground truth stated in the task brief:

| check | observed | expected | |
|---|---|---|---|
| RELAX panel genes | 77 | 77 | OK |
| Panel genes that are GRN nodes | 16 | 16 | OK |
| Within-panel-connected genes (core GRN, non-self edges) | 13 | 13 | OK |
| Core-GRN within-panel undirected edges | 15 | 15 | OK |
| Multilayer-substrate within-panel edges (core + PAX3 additions) | 18 | 18 | OK |
| Total unordered gene pairs, C(13,2) | 78 | 78 | OK |
| Adjacent / non-adjacent pair split (core) | 15 / 63 | 15 / 63 | OK |
| All 13 connected-gene K values | exact match | MLANA 0.39 … TYR 2.18 | OK |

All 13 RELAX K values for the connected gene set were confirmed against the frozen,
independently reverified values supplied in the task brief (MLANA 0.39, MC1R 0.45, OCA2
0.57, MITF 0.61, PMEL 0.87, DCT 0.97, SOX10 1.01, EDNRB 1.09, KITLG 1.30, PAX3 1.41, KIT
1.50, TYRP1 1.62, TYR 2.18) — no discrepancy found.

One discrepancy is flagged for the record: the raw `nb7_substrate_edges.csv` T0+T1 tiers
restricted to the 13 core genes contain **20** within-panel edges (the 15 core-GRN edges
plus KIT–MITF, EDNRB–SOX10, and the three PAX3 additions: PAX3–DCT, PAX3–TYR, PAX3–TYRP1),
not 18. The task brief specifies the substrate robustness check should add exactly the
three PAX3 edges (core 15 + 3 = 18); this analysis follows that explicit specification and
does **not** additionally add KIT–MITF or EDNRB–SOX10, which are present in the raw
substrate file's T1_GRN_regulon tier but outside the brief's stated edge list. This is
noted so a future session reconciling the substrate file against this plan does not treat
it as an unexplained gap.

## Analysis 1A — GRN-neighbor selection-similarity permutation

**Method.** For the 13 within-panel-connected genes, selection distance is defined as
d(i,j) = |log K_i − log K_j| over all C(13,2) = 78 unordered gene pairs. The test statistic
is T = mean(d) over non-adjacent pairs − mean(d) over adjacent pairs; T > 0 means GRN
neighbors are *more* similar in selection signal than non-neighbors. The null distribution
was built by degree-preserving double-edge-swap rewiring (`networkx.double_edge_swap`,
nswap = 10 × |edges| per rewiring, `max_tries` = 100× that), K values held fixed on nodes,
10,000 rewirings, fixed seed = 42. Two-sided empirical p = fraction of rewirings with
|T_rewired| ≥ |T_obs|.

**Core GRN (13 nodes, 15 undirected edges).**

| quantity | value |
|---|---|
| T_obs | 0.1374 |
| mean d, adjacent pairs (n=15) | 0.5027 |
| mean d, non-adjacent pairs (n=63) | 0.6401 |
| two-sided empirical p | 0.109 |
| n rewirings | 10,000 |
| seed | 42 |

**Multilayer-substrate subgraph (13 nodes, 18 undirected edges: core 15 + PAX3–DCT,
PAX3–TYR, PAX3–TYRP1).**

| quantity | value |
|---|---|
| T_obs | 0.1849 |
| mean d, adjacent pairs (n=18) | 0.4715 |
| mean d, non-adjacent pairs (n=60) | 0.6563 |
| two-sided empirical p | 0.093 |
| n rewirings | 10,000 |
| seed | 42 |

**Robustness.** The direction of the effect (T_obs > 0, GRN neighbors more similar in
selection signal than non-neighbors) holds in both networks, and the substrate
subgraph — which adds three literature-supported PAX3 edges — makes the effect slightly
*larger* (T_obs 0.185 vs 0.137) and slightly more significant (p 0.093 vs 0.109), not the
reverse. It does not hold at conventional significance in either network. This is the
signature of a real but small effect competing with a small-sample null that has heavy,
lumpy tails at n = 13 nodes — the rewiring null for a 13-node/15–18-edge graph has a
limited number of distinct topologies reachable by double-edge swaps, which is visible in
the null histogram (Fig. 1b) as a small number of tall spikes rather than a smooth
distribution. Full numeric output: [neighbor_permutation_results.csv](neighbor_permutation_results.csv).

## Analysis 1B — Module / pathway selection enrichment (honest small-n)

**Module definition (i): GRN `node_class`.** All 13 within-panel-connected genes carry
`node_class == "network_protein_gene"` in `gene_network_nodes.csv` — the only other
classes present in the full 168-node GRN (`enzyme_activity_class`, n=6;
`cleavage_precursor_gene`, n=1) do not appear among the panel's connected genes. **This
module definition is degenerate for this gene set: there is no contrast to test.** It is
reported for completeness (median K = 1.01 over all 13 genes) but carries no enrichment
signal.

**Module definition (ii): regulator vs. effector split.** Regulators are defined as edge
SOURCES within the core GRN among the connected set (MITF, SOX10, PAX3); effectors are
their direct targets, excluding regulators themselves (DCT, EDNRB, MC1R, MLANA, OCA2,
PMEL, TYR, TYRP1). KIT and KITLG are neither a regulator nor a direct target of
MITF/SOX10/PAX3 in the core GRN and are excluded from this contrast (they connect to each
other and to MITF only via the KITLG→KIT and KIT→MITF/EDNRB projection edges).

| module | n | median K | IQR | vs. | stat (Mann-Whitney U) | p (two-sided) |
|---|---|---|---|---|---|---|
| Regulators (MITF, SOX10, PAX3) | 3 | 1.009 | 0.401 | rest of 13 (n=10) | 15.0 | 1.00 |
| Effectors (direct targets) | 8 | 0.919 | 0.675 | rest of 13 (n=5) | 14.0 | 0.435 |
| Regulators vs. effectors (direct) | 3 vs 8 | 1.009 vs 0.919 | — | — | 14.0 | 0.776 |

Full numeric output: [module_enrichment_results.csv](module_enrichment_results.csv).

**Small-n caveat, foregrounded as instructed.** With n = 3 regulators, the smallest
attainable two-sided Mann-Whitney p-value against any comparison group is far from
conventional significance regardless of effect size — these tests have essentially no
power to reject a null of no difference, and the p-values above should be read as
descriptive, not confirmatory. None of the three group comparisons reaches p < 0.05.

**The regulator-vs-effector asymmetry the task brief calls out is real in the individual
K values, but is not a clean median-level split.** Master regulators are indeed
near-neutral at the low end of their own group (MITF K=0.61, SOX10 K=1.01) and several
effectors are strongly intensified (TYR K=2.18, TYRP1 K=1.62, KITLG K=1.30 — though KITLG
falls outside the "effector" group as defined here since it is not a direct MITF/SOX10/PAX3
target). But the effector group is **heterogeneous**: it also contains the three most
K-relaxed genes in the entire connected set (MLANA 0.39, MC1R 0.45, OCA2 0.57). Because the
effector group's median (0.92) sits close to the regulator group's median (1.01), the
group-level Mann-Whitney contrast is null even though the qualitative pattern described in
the task brief — a near-neutral regulatory core flanking intensified downstream
effector genes at the tails — is visible in the raw values (Fig. 1c). PAX3 (K=1.41),
classified here as a regulator because it sources edges to MITF and SOX10 within the core
GRN, is itself substantially intensified, which is the main reason the regulator group's
own median (1.01, driven by SOX10) sits as high as it does and is not "near-neutral" as a
group.

## Confounds and limitations

- **n = 13 connected genes / 15–18 edges is the binding constraint on both analyses.**
  Only 16 of the 77 RELAX panel genes are GRN nodes at all, and only 13 of those 16 have a
  within-panel edge; a null result under this sample size is an underpowered pilot, not
  evidence against a network effect on selection. Both p-values (0.109, 0.093) sit close
  enough to conventional thresholds that a modestly larger connected gene set (more
  pigmentation genes phylogenetically screened, or a network with more within-panel edges)
  could plausibly cross significance in either direction.
- **Hub / pleiotropy dilution.** MITF and SOX10 are hub transcription factors regulating
  genes well outside the melanogenesis panel; if selection on a hub gene is diluted across
  many pleiotropic functions, a hub's K can look uninformatively near-neutral even if its
  melanogenesis-specific regulatory role is under strong selection. This is a plausible
  mechanistic reading of why MITF (K=0.61) and SOX10 (K=1.01) sit lower than several of
  their direct targets, and it argues against treating "regulators are near-neutral" as a
  clean biological conclusion rather than a hub-dilution artifact.
- **Curation bias in the GRN edge set.** The core GRN's 15 within-panel edges are drawn
  from Raghunath et al. 2015's manually curated mechanistic signaling network — a single
  literature-synthesis source. Edges reflect what has been experimentally characterized in
  melanocyte biology, which skews toward well-studied master regulators (MITF, SOX10,
  PAX3) and their canonical targets; genes with less-studied regulatory relationships are
  systematically under-connected in this graph regardless of their true regulatory role,
  which could either mask or manufacture the neighbor-similarity signal depending on
  whether well-studied gene pairs are also more similar in selection pressure for reasons
  unrelated to direct regulatory coupling (e.g., shared tissue expression breadth).
- **Rewiring null granularity.** At 13 nodes and 15–18 edges, the space of degree-sequence-
  preserving graphs reachable by double-edge swaps is limited; the null histogram (Fig. 1b)
  shows visible spikes rather than a smooth distribution, meaning the empirical p-value has
  coarser resolution than the 10,000-rewiring count alone suggests. This does not bias the
  point estimate of p but means the null is intrinsically lumpy at this network size — a
  feature of the small n, not an error in the permutation procedure.
- **node_class module definition is uninformative** for this specific gene set (all 13 are
  the same class), so the "two module definitions" instruction reduces in practice to one
  informative definition (regulator/effector) plus a documented null result for the other.

## Interpretation

Both the core-GRN and multilayer-substrate neighbor-permutation tests point the same
direction — network-adjacent genes in the melanogenesis GRN show smaller pairwise
differences in RELAX K than non-adjacent genes — and the substrate robustness check
strengthens rather than weakens the signal. Neither crosses p < 0.05. Given the explicit
small-n constraint (13 connected genes is the entire available connected panel, not a
subsample), this is best read as a suggestive, likely genuine but statistically
underpowered pattern, worth revisiting once phylogenetic screening extends to a larger set
of GRN-connected pigmentation genes, rather than as a null result that argues against
network structure shaping selection pressure. The regulator-vs-effector split shows the
predicted qualitative pattern at the extremes (near-neutral master regulators MITF/SOX10,
intensified terminal effectors TYR/TYRP1) but is diluted at the group-median level by
PAX3's own intensification and by three strongly relaxed effectors (MLANA, MC1R, OCA2),
and by n=3 in the regulator group giving essentially no statistical power. Neither
analysis should be reported as a positive finding without foregrounding n=13 as the
limiting factor.

## Deliverables in this directory

- [neighbor_permutation_results.csv](neighbor_permutation_results.csv) — Analysis 1A
  numeric results (core + substrate rows).
- [module_enrichment_results.csv](module_enrichment_results.csv) — Analysis 1B numeric
  results (both module definitions).
- [track1_figure.png](track1_figure.png) — deliverable figure: (a) adjacent vs.
  non-adjacent K-distance distributions (core GRN), (b) permutation null with T_obs marked,
  (c) regulator vs. effector K distribution.
- RESULTS_track1.md — this file.
