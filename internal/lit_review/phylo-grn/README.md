# `phylo-grn/` — gene regulatory networks on a phylogenetic scale

**Owner:** this folder. Nothing outside `internal/lit_review/phylo-grn/` is touched by this line of work.
If you are another session, you can read this freely; do not expect it to modify your files, and please
do not modify it without leaving a note in `## Log` at the bottom.

**Created:** 2026-07-13. **Status:** first pass complete.

---

## What this is

A methods-oriented literature review of the space where **regulatory network analysis meets phylogenetic
comparative methods** — i.e. everything relevant to the question *"we have a network, a tree, and a trait
that arose ~15 times independently; what can we actually run?"*

Two scopes, both requested:

1. **Cross-species GRN comparison / network evolution** — take a network in ≥2 species, ask how the network
   itself changed (edge turnover, module conservation, network alignment, rewiring rate).
2. **Phylogenetic comparative methods on network features** — treat expression, evolutionary rate, or network
   position (degree, centrality, module membership) as traits evolving on a tree.

## Contents

| File | What it is |
|---|---|
| **`2026-07-13_MEMO_power_audit_origin_architecture.md`** | ⚠ **Read this first.** The flagship "heterogeneous, origin-specific architecture" claim is a power result, not a biological one. Three controls, recompute code inlined, and what to run instead. **Unreviewed — asks to be checked.** |
| `2026-07-13_METHODS_MAP_phylo_grn.md` | The annotated bibliography. 71 verified methods papers in 9 families, each with what it does, what it eats, and whether code exists. |
| `2026-07-13_REPLICATION_TRIAGE.md` | The actionable half: which of these we can actually run **this week** on assets already in this repo, ranked. |
| `bibliography/2026-07-13_phylo_grn_refs.csv` | Machine-readable. One row per reference, DOI + PMID, verified. 71 rows, no duplicates. |

Announced to the other sessions at
`internal/handoffs/notes/20260713T160929Z__claude-cowork__lit-reviewer-phylo-grn__6d243d.md`, with an
explicit request that they check the audit. Replies come back as new notes, not edits.

## ⚠ Collision notice — read before using this folder

**A concurrent session produced an independent review of the same topic** at
`internal/lit_review/phylo_grn_methods/` (note the underscore; this folder uses a hyphen), timestamped the
same day. That was not visible when this folder was created and neither folder has modified the other.

The two are **complementary, not redundant**, and they **agree on the central constraint** — which is the
strongest evidence either of them is right:

| | `phylo-grn/` (this folder) | `phylo_grn_methods/` (other session) |
|---|---|---|
| Refs | 71, 9 families | 25, 5 families |
| Emphasis | Broad map + what the field has *not* done | Tighter, decision-first, tiered run plan |
| Independent conclusion | Overlap between the primate selection panel and the core network is **16 of 168 genes** — a data-coverage gap, not a methods gap | Same seam, from the other direction: **no cross-species expression data** removes an entire class of methods |

**Someone should merge these, and it should be a human.** My recommendation: keep the other session's
`CONCLUSION.md` / `TIERED_PLAN.md` as the operative plan, and fold this folder's §7 (module-level selection:
signet / PicMin / HotNet / SUMSTAT), §9 (the Badyaev 2015 carotenoid precedent), and the Conte 2012
calibration point in as additions — those are the parts most likely to be unique to this pass. Do not
silently delete either; check what the other contains first.

## The one-paragraph finding

**The field has a hole exactly where this project sits.** There are mature methods for comparing networks
*between* species (edge turnover, module preservation, network alignment), and mature methods for testing
whether a *gene's* evolutionary rate tracks a trait across a tree (RERconverge, PhyloAcc, aBSREL/RELAX).
But there is almost nothing that asks the question in between: **does a trait's repeated independent origin
recruit the same region of a regulatory network, even when it recruits different genes?** The one tool that
takes a phylogeny plus per-species networks and returns an evolutionary statement (MRTLE, Koch 2017) is
nine years old and yeast-only. The one paper that combines pathway topology + phylogeny + repeated trait
evolution is about carotenoid networks in birds (Badyaev 2015) — structurally the closest analog to our
design that exists, and it is a decade old and metabolic rather than regulatory.

Our `comparative-genomics/` finding — dichromatism arose ~15×, polygenic in every origin, *no shared genetic
signature across origins* — is currently stated at the **gene** level. The obvious next move, and the one the
literature has left open, is to re-ask it at the **network** level: the origins may use different genes and
still converge on the same module, the same pathway depth, or the same position in the signed melanogenesis
graph. That is a testable, publishable claim, and §"Tier 1" of the triage doc lists the four tools that
would test it with data already sitting in this repo.

## Standing rules (inherited from `internal/lit_review/README.md`)

- **Never cite a paper not retrieved through a connector.** Every reference here carries a DOI/PMID pulled
  from an actual PubMed result.
- **DOI/PMID only, no copyrighted full text.** This folder is public.
- Every PMID below was **independently verified** against PubMed metadata (author, year, title) after
  collection. 66/69 passed on first check; the 2 corrections and 2 unverifiable preprints are flagged inline.

## Log

- 2026-07-13 — created; 71 verified refs, triage written. No files outside this folder modified.
- 2026-07-13 — discovered concurrent `phylo_grn_methods/` from another session; collision notice added
  above. Their files were read, not modified.
- 2026-07-13T16:09Z — power audit memo added after recomputing the per-origin and module-balance results
  from committed files. Finding: the heterogeneous-architecture headline is not supported (χ² homogeneity
  p=0.42; P(zero gene overlap by chance)=0.87; module tilt explained by panel composition, p=0.17).
  Posted to the notes channel with a request for review. **No file outside this folder modified** —
  correcting the headline is Claude Science's lane and Tina's call.
