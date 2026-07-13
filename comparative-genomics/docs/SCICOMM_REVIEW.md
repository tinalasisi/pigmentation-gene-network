# Communication review — dichromatism_selection.ipynb

**Audience assumed:** public-facing reproducible supplement — a reader with no project
context, running from frozen data. Held to that standard throughout.

Scope: self-containment, comprehensibility, captions, citations, conclusion currency,
spelling, and the "honest"-word pass. Figure *design* critiques were delegated to the
Visual Data reviewer (see VISUAL_REDESIGN.md) and are folded in below by reference.

## Findings (by severity)

### Critical — a reader cannot read the figures
1. **No standalone captions.** Every "caption" is a section header *before* the code that
   says what *will* be plotted, not a caption *under* the figure stating what it shows and
   what was found. Fix: a caption markdown cell immediately after each of the 4 figure cells.
   Draft captions supplied by the Visual reviewer (VISUAL_REDESIGN.md).
2. **`log2 K` never defined in plain language.** The central quantity of the whole notebook.
   A reader who has not heard of RELAX's K cannot read a single figure. Also undefined on
   first use: BH (12 cells), SUMSTAT, assortativity, aln_ref_ratio, subs/site. Fix: a "How to
   read this notebook" glossary cell up front (K, log2 K, BH, RELAX, one sentence each) + a
   plain-language anchor on every colorbar/axis.

### High — figure encodings (from Visual Data reviewer, folded in)
3. **Tree (Fig 3):** complete vs. partial dichromatism both drawn as solid red, distinguished
   only by marker shape at tip scale → reads as "all red." Fix: solid red circle = complete,
   hollow red square = partial (two redundant channels) + phytools-style clade bars
   (Okabe–Ito, never red) marking the 4 independent origins. No per-tip K strip (K is a
   group-level parameter).
4. **Module network (Fig 4):** certified-hit vs. neighbor encoded only by ring line-width →
   indistinguishable at a glance. Fix: outline presence/absence + size + `★` label suffix;
   add plain-language colorbar anchor; fix title/subtitle margin.
5. **Two networks (Fig 2):** leftover "INTERIM" tag in the shipped title; same ring ambiguity;
   colorbar scope ambiguous (looks Panel-B-only). Fix: remove INTERIM, apply the Fig-4 hit
   encoding, center/annotate the shared colorbar.
6. **Lollipop (Fig 1):** category colors (crimson/blue) collide with the red/blue = K-direction
   convention used in Figs 2 & 4 — blue "hormone" dots sit on the intensified side. Fix:
   recolor categories to purple/orange.

### Moderate — prose
7. **"honest"-word pass: 3 occurrences**, all editorializing filler:
   - cell 16: "We report both honestly" → "We report both"
   - cell 19: "**Honest caveats:**" → "**Caveats:**"
   - cell 19: "The honest headline is…" → "The headline is…"
8. **Consistency:** colorbar wording differs across figures (`K=1` vs `0`). Pick one anchor
   phrasing and use it verbatim on every colorbar/axis.

## Not defects
- Citations: the notebook cites methods (HyPhy RELAX, SUMSTAT, BH) by name; the bird-anchor
  DOI (10.1098/rspb.2007.0174) lives in the docs, not this notebook — acceptable for a
  methods supplement, but a one-line "Methods & data sources" cell with the RELAX and
  Nadeau-2007 references would strengthen it.
- Conclusion currency: verified the set-level p (0.87) and certified-hit counts (17→9) in the
  prose match the current cell outputs. No stale numbers found after the earlier 0.5→0.87 fix.
