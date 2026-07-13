---
from: claude-cowork/lit-reviewer-phylo-grn
to: all
date_utc: 2026-07-13T16:09:29Z
platform: claude-cowork
subject: ⚠ The origin-architecture headline is a power result — please check my work
---

**Platform token note:** I am a Cowork session, a platform not yet in `notes/README.md`'s token list
(`claude-science` | `claude-code`). The README says to extend the list as new platforms join, so I am using
`claude-cowork`. If that is wrong, rename in a follow-up note — I am not editing the README from this lane.

## What I did

Tina asked for a lit review of gene-regulatory-network analysis at phylogenetic scale, in an isolated folder.
That is at **`internal/lit_review/phylo-grn/`** (hyphen). 71 PMID-verified refs, a methods map, and a
replication triage. Nothing outside that folder was modified by me.

**Collision, for the record:** a concurrent frame independently produced
`internal/lit_review/phylo_grn_methods/` (underscore) on the same topic the same day. Neither folder has
touched the other. They are complementary and they **agree on the central data constraint**, which is
reassuring. Merging them is a human's call; my recommendation is in my folder's `README.md`.

## The thing you actually need to read

While triaging what we could run, I audited the data behind the flagship macroevolutionary claim and I think
**it does not survive.** Memo, with inlined recompute code:

> **`internal/lit_review/phylo-grn/2026-07-13_MEMO_power_audit_origin_architecture.md`**

The claim — *"~15 independent origins, different gene combinations in each, heterogeneous origin-specific
architecture"* — rests on three lines that each dissolve under a control:

1. **"Zero cross-origin gene overlap."** 2 of the 3 RELAX-testable origins have ≤1 hit, so overlap is
   arithmetically impossible. For the single pair that *could* have overlapped (origin_7 × origin_8, 8 hits
   vs 1 in a shared pool of 62), **P(zero overlap by chance) = 0.87**. Zero overlap is the *expected*
   outcome. It carries no information. Worse: per frame 83c784db's v3 certification, **POMC fails alignment
   QC** — and POMC is origin_8's only hit, so after QC the comparison is undefined, not merely underpowered.

2. **"Module balance spans the full range."** χ² homogeneity across all 11 origins: **p = 0.42** (Monte
   Carlo, 50k sims, `n_sel` held fixed: **p = 0.45**). A **single shared architecture is not rejected.**
   The two origins at the poles are the two with the smallest samples — origin_14's balance of −1.0 is
   **one gene**, origin_12's +1.0 is **two**. `P(≥1 origin at a pole | one shared architecture) = 1.00`:
   a pole is *guaranteed*, not informative. And `corr(n_tips, n_sel) = +0.93` — gene count is 92% power.

3. **The hormone tilt (43H/30P).** The panel is 52H/26P. Binomial vs. panel composition: **p = 0.17.**
   Selection is not preferentially hitting either module. That tilt is the panel, not biology.

`results/perorigin_v1/README.md` **already says all of this** — *"do NOT report as a clean heterogeneous
architecture claim"*, power confound named explicitly. The failure is **propagation**, not execution: the
warning did not make it into the top-level `README.md`, which now states heterogeneity as the headline, nor
into `analysis/module_selection/README.md`, which reports the balance range as a key result.

**I am claiming "undetermined," not "convergent."** The data cannot currently distinguish the two. If you
catch me sliding from the first into the second anywhere, flag it — that would be an error.

## Please check my work — specifically these five things

I am a lit-review lane auditing someone else's compute. I would rather be corrected than believed.

1. **Re-run my §2 χ² on the *certified* hit set**, not raw aBSREL `selected_flag`. I used
   `module_balance_results.csv` as committed because I could not find a per-origin certified table. **If one
   exists, this is the check that matters most** — certification could move the homogeneity p-value.
2. **Is χ² even the right test** on an 11×2 table with several expected counts < 5? I ran a 50k Monte Carlo
   as backup (same conclusion, p = 0.455). If you prefer an exact/permutation form, run it.
3. **Confirm POMC fails alignment QC** (aln_ref_ratio 0.65, per
   `notes/2026-07-13_selection_and_phylo_results_memo.md`). My §1 escalation depends on it. If POMC is
   certified, my "undefined" wording is too strong — though P = 0.87 stands either way.
4. **Confirm `gene_modules.csv` (52H/26P) is the right panel denominator** for §3. If the RELAX/aBSREL panel
   differs from those 78 genes, my binomial expectation is wrong.
5. **Sanity-check the direction of the Opie-analog result I am promoting.** I am arguing the **9.1× loss
   asymmetry** (ARD, ΔAIC 19.79) is the project's strongest defensible finding and is being under-sold
   beneath an unsupported headline. Frame 83c784db already verified the numbers *and* warned that
   `ace(model="ARD")$rates` is easy to mis-label by direction. I did not re-derive it — I am taking that
   verification on trust. Someone should confirm I am promoting a result that points the way I think it does.

## What the literature says to do about it (not just "your claim is broken")

- **Conte et al. 2012** (PMID 23075840) — expected gene-level parallelism is only **0.1–0.4** at deep
  divergences. Run this arithmetic *first*: if expected parallelism is ~0.2, "different genes per origin" is
  what the field already predicts, and the negative is not a finding. This is the calibration that turns
  "we found nothing" into "here is why the gene level was never the right level."
- **PicMin** (Booker et al. 2023, PMID 36626817, github.com/TBooker/PicMin) — order-statistics test built for
  **many independently-weak lineages**; power *rises* with lineage count; uses **ranks, not BH thresholds**.
  `branch_rates.csv` already holds per-branch aBSREL for the **11 single-tip origins nobody is using for this
  question** → takes us from **3 usable origins to ~14**. This is the single highest-value item in the review.
- **signet** (Gouy et al. 2017, PMID 28934485) — then ask it at the network level: do the *different* genes
  fall in the *same connected subnetwork*? Same-module-different-gene convergence is a **positive**,
  publishable result. Precedent it must survive: **Badyaev et al. 2015** (PMID 26289047) — carotenoid network
  topology predicts repeated colour evolution across birds. Same three ingredients as us, ten years earlier.

## Blocking dependency you should know about

Only **16 of the 168** core melanogenesis network nodes currently carry a primate selection statistic
(77-gene RELAX panel ∩ 168-node network = 16). Every network-level selection test needs a score *on the
network's nodes*. **This is a data-coverage gap, not a methods gap** — extending the miniprot → MAFFT → HyPhy
panel from 117 to 168+ genes is more of the same compute, and it unlocks signet, PicMin, and HotNet at once.
Triage: `internal/lit_review/phylo-grn/2026-07-13_REPLICATION_TRIAGE.md`.

I have **not** edited `README.md`, `TODO.md`, `CHANGELOG.md`, `project_dashboard.md`, or any
`comparative-genomics/` file. Correcting the headline is Claude Science's lane and Tina's call, not mine.
Reply with a new note rather than editing this one (`MERGE_SAFETY.md` never-rewrite discipline).
