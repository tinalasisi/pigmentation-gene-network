# Figure evaluation for the website polish pass — 2026-07-12

**Scope.** Read-only critique by Claude Code (website/design owner) of the current NB1–NB6 figures.
**No figure was modified.** These are Claude Science's *rough functional* figures (correct data, correct
chart type) — which is exactly their remit; polishing is Claude Code's. This doc is the spec for the polished,
site-ready rebuilds and the later Claude Design handoff.

**Reviewed:** `notebooks/figures/{nb4_funnel, nb5_candidate_network_comparison, nb6_mitf_hub_grn,
step6_validation_verdict}.png`; `output/figures/{nb1_network_overview, nb1_validation_dashboard}.png`.
*(Not yet reviewed in detail: `step2/step4/step5` NB2-build figures — same family; review if they go on the site.)*

## Cross-cutting issues — fix once, as a design system
1. **Adopt ONE design system.** Every figure is raw matplotlib defaults (default font, tab10 palette, default
   spines). Define a single theme (font, palette, spines/grid, sizing, title/caption style) and apply to every
   rebuild so the site reads as one product. (Use the Claude Code `dataviz`-skill palette; then hand to Claude Design.)
2. **Fix color semantics — currently arbitrary AND inaccessible.**
   - Colors carry no consistent meaning across figures (a network is blue in one panel, green in another).
     Assign FIXED roles: one color per network/layer (Raghunath/D'Arcy/KEGG/Reactome/Bajpai), one fixed
     "rescue-target / highlight" accent, one fixed activation/repression pair.
   - **Red-green fails colorblind viewers** (activation=green / repression=red in the GRN + network figures).
     Switch to a colorblind-safe pair (blue=activation / orange=repression, or teal/vermillion).
3. **Titles must not truncate or do legend duty.** `nb4_funnel`'s title is **cut off** ("…GWAS Catalog r").
   `nb6_mitf_hub` crams the whole legend into the title text — move it to a real legend.
4. **Emphasize the "money" number in each figure.** The striking findings are visually equal-weight with
   context. Make them pop: the **27** rescue targets; the **All-5 = 1 gene** intersection; the **265/265**
   degree match; the **188 confirmed** edges.
5. **Strip internal jargon from audience-facing labels.** "pending (→NB2)", "Types only what the file fixes",
   "each-only vs full 5-way intersection" — rewrite for a judge / external viewer.

## Per-figure

### nb4_funnel — effector-status breakdown of the 105  ★ keep (reframed)
- **Shows (reframed 2026-07-12):** the 105 curated loci by effector status — 14 effector-uncertain (the rescue target) vs 75 canonical-effector variant-gaps, etc. Replaces the old "105 → 52 → 27" funnel, which presented the coarse (superseded) "author-unexplained" tag as the target.
- **Fix:** (1) **title truncated — critical.** (2) decreasing left-aligned bars, not a true funnel — center into a
  real funnel, or keep bars but add drop-off deltas (−53, −25) and % surviving each step. (3) Highlight **27** as
  the target (accent + "the rescue set"); mute 105/52 to context.
- **Site role:** opening "what we set out to rescue." **High priority.**

### nb5_candidate_network_comparison — networks disagree  ★ strong finding, weak execution
- **Shows:** left = genes unique to each network + **All-5 intersection = 1**; right = STRING recovers 60% of
  Raghunath edges / 66% agreement across STRING versions.
- **Fix:** (1) the punchline (**only 1 gene is in all 5 networks**) is nearly invisible (bar height 1) — call it
  out; it's the whole point. (2) default tab10 → fixed per-network colors. (3) right panel: 60% green vs 66% red
  is **misleading** (red reads "bad"; 66% isn't worse) — one neutral color for both. (4) relabel "each-only" →
  "genes unique to each source."
- **Site role:** "the network you choose changes the answer" — the rigor beat. **High priority.**

### nb6_mitf_hub_grn — MITF regulon  ★ informative, declutter
- **Shows:** MITF hub → 34 targets, sign-colored, gold = core pigmentation target
  (TYR/TYRP1/DCT/MLANA/PMEL/OCA2/MC1R/KIT/EDNRB). Genuinely good.
- **Fix:** (1) **legend out of the title.** (2) the many **gray** (ambiguous/unsigned) edges dominate and dilute
  the story — de-emphasize gray; make the **activation edges to the gold pigmentation genes** the visual focus
  (that IS the finding: MITF activates the core pigment program). (3) red-green → colorblind-safe. (4) fix label
  crowding at the bottom.
- **Site role:** "the regulatory core." Medium priority.

### nb1_validation_dashboard — reproducibility  ★★ best figure, light cleanup
- **Shows:** (a) degree matches published for **265/265** (y=x); (b) node types; (c) 429 edges signed
  (379/43/7); (d) few hubs, many leaves + top hubs.
- **Fix:** (1) panel (a) is the **reproducibility money-shot** (answers a reviewer's trust question) — consider
  pulling it out standalone. (2) fix panel-(b) title "Types only what the file fixes" → "Node types (only what
  the source file asserts)." (3) unify the b/c/d palette (b uses blue/green/red; c uses blue/orange/gray).
- **Site role:** "we rebuilt the network faithfully" — the trust beat. Keep; light polish.

### step6_validation_verdict — OmniPath check  ★ good, reframe the denominator
- **Shows:** 188 confirmed / 40 not-in-OmniPath / 3 sign-conflict / 198 out-of-scope, of 429 backbone edges.
  Semantic colors (green/yellow/red/gray) are appropriate here.
- **Fix:** "out-of-scope = 198" (≈half) buries the win. Reframe to the **in-scope confirmation rate**: 188
  confirmed of 231 in-scope protein-protein edges = **~81% confirmed, 3 conflicts** — a far stronger statement.
  Headline that; keep the breakdown as detail.
- **Site role:** "an independent database confirms our backbone." Medium priority.

### nb1_network_overview — the full network  ⚠ rework or demote
- **Shows:** 265-node force-directed melanogenesis network. **It's a hairball** — impressive but
  low-communication; a static 265-node force layout rarely conveys a finding.
- **Fix / decision:** for the site, either (a) make it **interactive/zoomable** (the one place interactivity
  earns its keep), (b) replace with a **simplified schematic** (signed backbone + payoff loci MC1R/OCA2 + the
  MITF hub), or (c) demote to a "scale" thumbnail. Do **not** use the raw hairball as a hero. Drop the
  "pending (→NB2)" internal label.
- **Site role:** low as-is; high if made interactive.

## What's missing — the figures that actually win (pending NB8)
The two most important site figures don't exist yet because NB8 (rescue + hero) hasn't run:
**(1) the convergence-graded rescue overview** (the 52 sorted into rescue classes, shaded by grade) and
**(2) the hero rescue card** (the money shot). Both are Claude Code builds once NB8 lands.

## Priority order for the polish pass
1. `nb4_funnel` — fix truncation, promote the 27 (opening).
2. `nb5_comparison` — surface the All-5 = 1 callout, fix palette (rigor beat).
3. `nb1_validation_dashboard` panel (a) pulled out standalone (trust beat).
4. `step6` reframed to 81%-in-scope (validation beat).
5. `nb6_mitf_hub` declutter (regulatory layer).
6. `nb1_network_overview` — interactive or demote.
7. *(pending NB8)* convergence overview + hero card — the winners.
