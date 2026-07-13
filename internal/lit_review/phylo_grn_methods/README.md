# Phylogenetic-scale gene (regulatory) network analysis — methods lit review

**Purpose.** Survey the methods space for analysing a gene / gene-regulatory network on a
**phylogenetic (cross-species) scale**, and decide how to run such an analysis on the pigmentation
project's *existing* primate data. Deliverable is a two-tier plan:
- **Tier 1** — a defensible new finding runnable now with data already in hand.
- **Tier 2** — a short analysis to launch on the Great Lakes cluster.

**Isolation.** This folder is a self-contained workspace opened by the PI orchestrator
(frame 9c7c28bf). It writes ONLY under `internal/lit_review/phylo_grn_methods/`. It does NOT touch
`comparative-genomics/analysis/module_selection/` (active mol-evo work) or `internal/network-evo-explore/`.

## Layout
- `survey/`      — literature/methods survey + papers table (GENETICS_LIT_REVIEWER)
- `feasibility/` — method→our-data feasibility mapping + tiered plan (MOL_EVO_SPECIALIST)
- `CONCLUSION.md` — PI synthesis: the two-tier recommendation (written last)

Created: 20260713T (PI orchestrator, frame 9c7c28bf)
