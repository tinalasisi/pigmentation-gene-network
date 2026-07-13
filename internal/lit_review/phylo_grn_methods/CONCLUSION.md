# Conclusion — how to run a gene-(regulatory)-network analysis on the primate data we have

**Author:** PI orchestrator (Claude Science, frame 9c7c28bf), synthesizing two delegated specialists
(GENETICS_LIT_REVIEWER → `survey/`, MOL_EVO_SPECIALIST → `feasibility/`).
**Date:** 20260713T152500Z
**Isolation:** all work lives under `internal/lit_review/phylo_grn_methods/`. Nothing here touches the
in-flight `comparative-genomics/analysis/module_selection/` or `internal/network-evo-explore/`.

---

## The question, and where it lands in our data

The ask: what exists in the space of **gene-(regulatory)-network analysis on a phylogenetic scale**,
and how do we run one on the primate data we already hold — Tier 1 a new finding from data in hand,
Tier 2 a short cluster job.

The data we hold sits at a specific seam: we have **cross-species selection statistics** (HyPhy RELAX
per-gene K, aBSREL per-branch ω) on an ~80-gene pigmentation × sex-hormone panel across 117 primates,
codon alignments for every panel gene, a **signed directed melanogenesis GRN** (168 nodes / 309 edges),
and a species tree with 14 independent dichromatism origins. We do **not** hold cross-species
expression data. That single absence removes an entire class of methods (WGCNA / GENIE3 / SCENIC
expression-GRN inference, coexpression-network comparison, cis-regulatory/chromatin turnover, per-species
network rewiring) from the runnable-now menu — confirmed against the literature, not assumed.

## What the field does (5 method families, 25 PMID-verified papers)

The survey (`survey/phylo_grn_methods_survey.md`, table `survey/phylo_grn_methods_papers.csv`) organizes
the space into five families and marks each against our inventory:

1. **Network/pathway-aware selection tests** — aggregate a per-gene selection score over pathway/module
   gene sets (PolySel; Daub 2013 PMID 23625889, and its primate-lineage application Daub 2017
   PMID 28333345). **Feasible now.**
2. **Coevolution of interacting partners across a phylogeny** — do interacting genes' rate profiles
   move together (mirrortree, Pazos & Valencia 2001 PMID 11707606; ERC, Clark 2012 PMID 22287101;
   RERconverge, Kowalczyk 2019 PMID 31192356). **Best-matched family to our data.**
3. **Phylogenetic comparative methods on network-derived traits** — PGLS of selection rate on network
   position (Pagel 1999 PMID 10553904; phytools, Revell 2024 PMID 38192598), with the hard confound
   that **expression level, not connectivity, dominates evolutionary rate** (Zhang & Yang 2015
   PMID 26055156) — and we cannot control for it. **Partial / caveated.**
4. **GRN rewiring & topology evolution across species** (Thompson 2015 PMID 26355593 and family).
   **Ruled out** — needs per-species regulatory/expression data we lack.
5. **Network propagation of an evolutionary signal** (Vanunu 2010 PMID 20090828; HotNet2, Leiserson
   2014 PMID 25501392; Cowen 2017 PMID 28607512). Adaptable in principle, but our network-connected,
   selection-scored subgraph is too sparse to diffuse over. **Infeasible on this data.**

Full "feasible / partial / no" calls per method are in `feasibility/feasibility_matrix.csv`.

## The one number that shapes everything: n = 15 edges

Independently re-counted from the frozen files: of 77 genes with a RELAX result, only **16** are nodes
in the signed melanogenesis GRN, and only **15 directed non-self edges** connect two panel genes (13
genes; LEF1/POMC/TFAP2A have no within-panel edge). The hormone half of the panel is absent because it
was never curated into a *pigmentation* network — not because no regulatory link exists. **This small
edge count, not the choice of statistic, is the binding constraint at both tiers.** It rules out network
propagation (Family 5) and makes any topology test a pilot, not a confirmatory analysis.

## Recommendation — the two tiers

### TIER 1 — a defensible new finding, runnable now, locally, from frozen outputs

**GRN-neighbor selection-similarity permutation.** Do direct regulator→effector partners in the signed
GRN show more correlated cross-species selection intensity than non-adjacent panel-gene pairs?

- **Statistic:** on the 13-node / 15-edge induced subgraph, `d(i,j) = |log K_i − log K_j|`;
  `T_obs = mean d(non-adjacent) − mean d(adjacent)` over all C(13,2)=78 pairs (15 adjacent / 63 not).
- **Null:** degree-preserving double-edge-swap rewiring (10,000×), K fixed on nodes, two-sided empirical p.
  This is the correct null given the hub-dominated degree sequence (MITF degree 10, SOX10 degree 5).
- **Robustness:** repeat on the 18-edge multilayer-substrate subgraph; report as topology-dependent if it
  holds in only one.
- **Secondary descriptive split (no null):** regulators-as-sources vs their targets. The verified K values
  already show the shape a reviewer will ask about — the master regulators sit near neutral (MITF K=0.61,
  SOX10 K=1.01) while several downstream effectors are intensified (TYR K=2.18, p_BH<1e-4; KITLG K=1.30,
  p_BH=0.0015; PAX3 K=1.41) and others relaxed (MC1R K=0.45, MLANA K=0.39, OCA2 K=0.57). Reporting this
  regulator-vs-effector asymmetry is itself an honest topology-structured result independent of the p-value.

**Why Tier 1 is a real contribution even if null:** no prior analysis in this project has combined the
cross-species selection signal *with the GRN edge structure* — `module_selection/` tests pigmentation-vs-
hormone gene *sets*, `network-evo-explore/` tests centrality vs *human* constraint. This is the open seam.
A well-specified negative on n=15 edges is an honest, publishable pilot that motivates Tier 2; it is not
evidence of "no coordination." Spec: `feasibility/TIERED_PLAN.md` §Tier 1.

### TIER 2 — a short cluster job

**Pairwise coevolutionary-rate (mirrortree / ERC) test on GRN edges.** Same 15–18 true edges, but replace
each gene's single K with a full per-branch rate vector: build per-gene ML branch-length trees
(phangorn, extending the already-present `04_rerconverge.R`) from the existing codon alignments, compute
RER vectors, build the 77×77 pairwise rate-correlation matrix, and test whether true GRN-edge pairs have
higher |correlation| than the ~2,900 non-edge pairs — same degree-preserving null. This buys every one of
the same edges a far richer per-pair signal, from the same alignments and tree, with no new sequence data.

- **SLURM shape** (per repo convention: account `tlasisi0`, partition `standard`, smoke-test one unit first):
  Step 1 per-gene trees, `--array=1-77 --cpus-per-task=4 --mem=4G --time=00:30:00`; Step 2 aggregation
  `--cpus-per-task=1 --mem=8G --time=00:20:00`. Under an hour end-to-end.
- **Not recommended:** re-running `05_polysel_geneset.py` on topology-derived modules — with 13 genes split
  3 ways its label-permutation null repeats the small-n fragility already seen (existing SUMSTAT p=0.87).
- **Cheap add-on:** fill the remaining 11 of 14 origins for per-origin RELAX (`per_origin_relax_array.sbatch`),
  so a positive topology signal can be retested *within each independent origin* — the convergence-based,
  origin-not-species version of the claim this project already treats as the right unit of power.

Spec: `feasibility/TIERED_PLAN.md` §Tier 2.

## Confounds carried into any write-up (both tiers)

- **n = 15–18 edges is the dominant limit.** Tier 2 sharpens the per-edge statistic; it does not add edges.
- **Hub/pleiotropy dilution** of MITF/SOX10 K — the rewiring null preserves degree but not expression
  breadth, which we cannot measure here (echoes the no-centrality-effect result in `network-evo-explore/`).
- **Network curation bias** — the test is scoped to the melanogenesis subgraph someone already drew.
- **aBSREL missingness is non-random** (6 of 13 connected genes have empty JSONs), so per-branch analyses
  restricted to survivors risk an alignment-quality bias — a reason Tier 1 uses complete-coverage K, not ω.

## UPDATE 2026-07-13T16:25Z — local analyses RUN; cluster job specced

Both annotated method families were executed locally (in parallel), plus the Tier-1 headline test.
Results are honest and mutually consistent — a suggestive-but-underpowered positive on the K signal,
a clean null on local coevolution, and a clear reason the definitive coevolution test needs the cluster.

**Track 1 — network/pathway-aware selection** (`results/track1_network_selection/`).
GRN-neighbor selection-similarity permutation: GRN-adjacent genes are directionally MORE similar in
RELAX K than non-adjacent genes — core GRN T_obs=0.137, p_perm=0.109 (15 edges); multilayer substrate
T_obs=0.185, p_perm=0.093 (18 edges). Same direction in both networks; the substrate check strengthens
it. Neither clears p<0.05 at n=13 connected genes. **An honest underpowered pilot, not a null.** Module
enrichment: node_class is degenerate (all 13 one class); the regulator-vs-effector asymmetry is real at
the extremes (MITF K=0.61, SOX10 K=1.01 near-neutral vs TYR 2.18, TYRP1 1.62 intensified) but diluted at
the group median (Mann-Whitney p=0.78, n=3 regulators).

**Track 2 — partner coevolution** (`results/track2_coevolution/`).
Mirrortree (2,870 pairs from the 79 codon alignments): edge pairs are NOT more correlated than non-edge
pairs — mean|r| edge=0.167 vs non-edge=0.404, p_perm=0.61; direction opposite the hypothesis in all four
core/substrate × Pearson/Spearman tests, none significant, consistent with a shared-ancestry rate-
covariation floor swamping any GRN-specific signal at this scale. ERC from aBSREL branch rates (39 genes,
post-QC): p_perm=1.000 but **structurally degenerate** — the 7-gene/6-edge covered subgraph has exactly
one realizable graph, so the rewiring null is a point mass by construction. Local coevolution is therefore
uninformative, by design at this edge count — which is exactly why it is the cluster job.

**Net read:** the K-based topology signal (Track 1) is the strongest thing the data supports today and is
worth reporting as a suggestive pilot; the coevolution question (Track 2) cannot be answered locally and
is handed to the cluster with the definitive design.

### What now needs to run on the cluster

A run-spec was written to `internal/handoffs/notes/` (addressed to `claude-code / greatlakes-hpc`,
project paste-back contract): **the definitive ERC/RERconverge coevolution test** — per-gene ML
branch-length trees for all 77 panel genes on the shared topology (Stage 1, job array), the full
RERconverge RER transform + 77×77 ERC matrix + edge-vs-non-edge test with a **gene-label-permutation
null** (Stage 2, single task; the rewiring null degenerated locally), and cheaply-queued completion of
the remaining 11 of 14 per-origin RELAX fits (Stage 3). SLURM shape: account `tlasisi0`, partition
`standard`, smoke-test one unit first; under an hour end-to-end. This replaces every shortcut the local
pilot took (single scalar K; protein p-distance; raw branch lengths; degenerate null) and is the analysis
whose p-value can be trusted for a coevolution claim.

## Deliverables in this folder

- `results/track1_network_selection/` — RESULTS_track1.md, figure, permutation + module CSVs (Track 1, run).
- `results/track2_coevolution/` — RESULTS_track2.md, figure, mirrortree + ERC CSVs (Track 2, run).
- `internal/handoffs/notes/20260713T162412Z__...__a90131.md` — the cluster run-spec (Tier 2).
- `survey/phylo_grn_methods_survey.md` — the methods survey (5 families, ruled-out vs runnable).
- `survey/phylo_grn_methods_papers.csv` — 25 PMID-verified papers with feasibility calls.
- `feasibility/feasibility_matrix.csv` — per-method inputs / n / tier.
- `feasibility/TIERED_PLAN.md` — the exact statistic, null, and SLURM shape for both tiers.
- `CONCLUSION.md` — this synthesis.
