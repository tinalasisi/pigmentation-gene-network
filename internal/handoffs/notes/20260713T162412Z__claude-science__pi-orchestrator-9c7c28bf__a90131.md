---
from: claude-science/pi-orchestrator-9c7c28bf
to: claude-code/greatlakes-hpc
date_utc: 2026-07-13T16:24:12Z
platform: claude-science
subject: RUN SPEC — definitive GRN-edge coevolution (ERC/RERconverge) test on the pigmentation panel
---

# RUN SPEC → greatlakes-hpc: does selection coevolve along melanogenesis GRN edges?

**From:** claude-science / pi-orchestrator (frame 9c7c28bf)
**To:** claude-code / greatlakes-hpc
**Repo:** github.com/tinalasisi/pigmentation-gene-network — branch `main`
**Depends on:** the phylo-GRN methods review + two local pilots already committed under
`internal/lit_review/phylo_grn_methods/` (read `CONCLUSION.md`, `feasibility/TIERED_PLAN.md`,
and `results/track1_network_selection/`, `results/track2_coevolution/` there first).

---

## Why this run exists (the science, in one paragraph)

We asked whether cross-species selection on melanogenesis genes is *structured by the gene
regulatory network* — i.e. do genes that are direct regulator→effector partners in the signed
melanogenesis GRN evolve in a coordinated way that non-adjacent genes do not. Two local pilots
ran to completion on data already on disk. **Track 1** (RELAX-K neighbor similarity) found
GRN-adjacent genes are directionally *more* similar in selection intensity than non-adjacent
genes in both the core (T_obs=0.137, p=0.109) and multilayer-substrate (T_obs=0.185, p=0.093)
subgraphs — the same direction in both networks, the substrate check strengthening it, but
neither crossing p<0.05 at n=13 connected genes / 15–18 edges. **Track 2** (local coevolution)
was a clean non-result: mirrortree edge pairs were no more correlated than non-edge pairs
(p_perm=0.61), and the ERC-from-aBSREL test was **structurally degenerate** — the 7-gene /
6-edge aBSREL-covered subgraph has exactly one realizable graph, so its permutation null is a
point mass (p=1.000 by construction). **The binding limit at both tiers is the tiny edge count,
not the statistic.** This run replaces the local pilots' shortcuts (single scalar K per gene;
protein p-distance; raw aBSREL branch lengths; degenerate rewiring null) with the definitive
design: per-gene ML branch-length trees for all 77 panel genes on the shared topology, the full
RERconverge relative-evolutionary-rate transform, the complete 77×77 pairwise rate-correlation
(ERC) matrix, and a valid null tested across the independent origins — the analysis whose
p-value can actually be trusted for a coevolution claim.

---

## What to run (three stages, in order)

Everything keys off the existing panel and the alignments already produced by the panel run.
No new genomes, no new alignments required.

### Stage 1 — per-gene ML branch-length trees (job array)

- **Input:** `comparative-genomics/results/full_panel_117/aln117_codon.tar.gz` (79 files
  `aln/<GENE>.codon.aln.fa`; 77 correspond to panel genes with a RELAX result).
- **Task:** for each gene, estimate ML branch lengths on the **fixed primate topology**
  (`comparative-genomics/config/primate_species_tree.nex`), re-estimating branch lengths only
  (topology fixed) — this is exactly the machinery `comparative-genomics/scripts/04_rerconverge.R`
  sets up but has **not yet been run to completion** (no `report/rer_results.csv` exists). Use
  that script's tree-building step (phangorn `pml`/`optim.pml`, or RERconverge's
  `estimatePhangornTreeAll`) as the basis; do not hand-roll a new method.
- **Array design:** one task per gene, `--array=1-77`, PANEL row lookup by
  `SLURM_ARRAY_TASK_ID` (same pattern as `relax_array.sbatch` / `absrel_full_panel_array.sbatch`).
- **Resources (smoke-test first, per repo convention):** per-gene alignments run 36–91 tips over
  a few hundred codon columns, so ML branch-length optimization is light. Start point:
  `--partition=standard --account=tlasisi0 --cpus-per-task=4 --mem=4G --time=00:30:00`.
  **Smoke-test the single largest alignment first** (largest `n_tips`×`n_sites` in
  `results/full_panel_117/fit_health.csv`) as one short job, read `seff`, then size the full
  array from that + ~25% headroom.
- **Output:** one Newick per gene (all with branch lengths on the shared topology), collected
  into a single multi-tree file for Stage 2.

### Stage 2 — RERconverge RER transform + 77×77 ERC matrix + edge test (single task)

- **Task:**
  1. Load the per-gene trees; run RERconverge's `getAllResiduals` to produce per-gene,
     per-branch **relative evolutionary rate (RER)** vectors (this is the correct RER transform,
     replacing the pilot's per-tip mean-subtraction shortcut).
  2. Compute the full **77×77 pairwise RER-correlation matrix** (ERC), Pearson and Spearman.
  3. Label pairs as GRN-edge vs non-edge using the **15 core within-panel edges** (from
     `data/processed/gene_network_edges.csv`) and, as a robustness check, the **18-edge
     multilayer-substrate** set (`data/processed/nb7_substrate_edges.csv`; core 15 + PAX3–DCT,
     PAX3–TYR, PAX3–TYRP1). The 13 connected genes are: DCT, EDNRB, KIT, KITLG, MC1R, MITF,
     MLANA, OCA2, PAX3, PMEL, SOX10, TYR, TYRP1.
  4. Test whether edge pairs have higher |ERC| than non-edge pairs. **Use two nulls, not the
     degree-preserving rewiring alone** (the pilot showed rewiring degenerates at this node
     count): (a) a **gene-label permutation** null — shuffle the gene→RER-vector assignment,
     recompute the edge-vs-non-edge statistic, 10,000×, fixed seed; and (b) the degree-preserving
     rewiring null for comparability with the pilots. Report both p-values and say which is
     primary (gene-label permutation is the trustworthy one here).
- **Resources:** `--partition=standard --account=tlasisi0 --cpus-per-task=1 --mem=8G --time=00:20:00`.

### Stage 3 (queue in the same submission, cheap) — fill the remaining 11 of 14 origins

- Per-origin RELAX has only been completed for 3 of the 14 independent dichromatism origins
  (`results/perorigin_v1/per_origin_K.csv` → origin_7, origin_8, origin_14). The other 11 are
  single-tip origins that per-origin RELAX cannot fit — but they are recoverable per-branch.
  `per_origin_relax_array.sbatch` already exists and follows the same array pattern (~1h/task).
- **Why:** if the Stage 2 edge test is positive, the persuasive follow-up is to retest the
  coordination pattern *within each independent origin* (the convergence-based, origin-not-species
  version of the claim — this project already treats independent origins, not species, as the unit
  of power). This is not required for Stages 1–2 but is the natural next move and is cheap to queue.

---

## The paste-back contract (unchanged project convention)

You have the data; the chat does not. After each stage, **commit the small report CSV/MD +
`git push`, then paste the report file back into the chat.** Never send alignments, trees, genomes,
or JSON blobs. Route the commit through the compliance gate per repo convention. The exact files to
paste back:

- **Stage 1:** a short `SUMMARY.md` (per-gene tree built? n_tips, tree length, any failures) +
  the `seff` line from the smoke test so we can confirm the array was sized correctly.
- **Stage 2:** `erc_edge_vs_nonedge.csv` (network × correlation-method × null-type rows: mean|ERC|
  edge, mean|ERC| non-edge, n_edge, n_nonedge, p_perm) and a one-paragraph `RESULTS.md`. The full
  77×77 matrix stays on the cluster; paste only the summary.
- **Stage 3 (if run):** the extended `per_origin_K.csv` + a note on which origins fit.

## What "done" looks like

Stage 2's edge-vs-non-edge ERC test, with the gene-label-permutation p-value, is the deliverable
that answers the original question at a scale that can be trusted. A positive result = selection
coevolves along melanogenesis GRN edges (upgrades Track 1's suggestive n=15 pilot to a real
finding). A null result at this scale = a genuine, well-powered negative (unlike the pilots),
which is itself a reportable, honest outcome. Either way, paste the summary back and we integrate
it into `internal/lit_review/phylo_grn_methods/CONCLUSION.md`.

## Isolation / non-collision note

This run writes only under `comparative-genomics/results/` (new subfolder, e.g. `erc_v1/`) and
`internal/lit_review/phylo_grn_methods/results/`. It does NOT touch
`comparative-genomics/analysis/module_selection/` (active mol-evo work) or
`internal/network-evo-explore/`. The `04_rerconverge.R` machinery is reused, not modified in place
without a note here first.
