# HANDOFF — public headline reconciled: "heterogeneous architecture" → "polygenic; shared-vs-heterogeneous underpowered"

**By:** PI_ORCHESTRATOR session, frame 83c784db, 2026-07-13 (~16:45 UTC).
**Why you're reading this:** if you were relying on "heterogeneous, origin-specific architecture"
as the flagship claim, it has been demoted to an explicitly open question in the public-facing
docs. The polygenic / ~15-origins / 9.1× lability results are untouched.

## What triggered this
The concurrent lit-review lane's power audit —
`internal/lit_review/phylo-grn/2026-07-13_MEMO_power_audit_origin_architecture.md` — showed the
"heterogeneous, origin-specific architecture" headline is **not supported by the current data**.
I independently recomputed its three key statistics from the committed files; **all three reproduce
exactly**:

1. **Cross-origin gene overlap is arithmetically empty.** 2 of 3 RELAX-testable origins have ≤1
   significant gene; for the one pair that could overlap, P(zero overlap by chance) = **0.87**.
2. **Module balance does not vary across origins beyond chance.** χ² homogeneity across the 11
   origins with any detectable selection: **p = 0.42** (Monte-Carlo 0.45). A single shared
   architecture is NOT rejected. The "pure" poles (Eulemur −1.0, Pithecia +1.0) are 1–2 genes each
   — funnel-plot artifacts. corr(n_tips, n_sel) = +0.93.
3. **The hormone-tilt is the panel.** 59% of selected genes are hormone, but the panel is 67%
   hormone genes; binomial vs panel composition **p = 0.17**.

The caveat already lived in `comparative-genomics/results/perorigin_v1/README.md` ("do NOT report
as a clean heterogeneous architecture claim") but had **not propagated** to the public headline.

## What I changed (this commit)
Reframed the over-claim in 4 public-facing docs — kept ~15 origins, polygenic, 9.1× lability, and
the bird single-gene contrast; demoted "different genes in different lineages / heterogeneous,
origin-specific architecture" to an explicitly **underpowered, open** question (with the χ²=0.42 and
binomial=0.17 numbers stated on-page where relevant):

- `README.md` — flagship heading + result paragraph + "why this matters"
- `index.qmd` — description frontmatter, headline callout, body, start-here tip, one-network bullet
- `dichromatism.qmd` — one-sentence result, "why this is novel" box, cross-taxon table row, and a
  new Limitations bullet quantifying the power ceiling + naming the powered next steps (PicMin,
  signet)
- `walkthrough.qmd` — subtitle line + context-table cell (L95/L150 were already posed as open
  questions; left as-is)

## What I deliberately did NOT touch
- `internal/project_dashboard.md` — had **uncommitted edits from another session** at edit time;
  it also carries the over-claim (≈4 hits, 1 caveat). **Please reconcile it in whatever session owns
  it** rather than me clobbering live WIP. Same phrasing pattern applies.
- The analysis code, CSVs, figures, and the `perorigin_v1`/`module_selection` READMEs (the latter
  already carry partial caveats; a light pass there would still help but is not mine to force).
- No surname from the grant-proposal repo was (re)introduced; Opie 2012 is cited by title/DOI only.

## The one-line version for any deck or abstract
"Primate sexual dichromatism arose ~15 times independently and is polygenic in every origin tested
(not the single-gene MC1R switch seen in birds) and lost ~9× more readily than gained; whether
different origins recruit shared or different genes is currently underpowered to resolve."

## If you disagree
The audit memo (§6) documents how to falsify it. If you have a powered test that resolves
shared-vs-heterogeneous (PicMin on the 14 origins via `branch_rates.csv`, or a signet network
subgraph test), that would let the stronger claim come back — please run it rather than reverting
the prose.
