# Visual data review — NB11 figures

**Scope.** Data-integrity and honesty review of the two NB11 figures ahead of presentation:
`notebooks/figures/nb11_cross_ancestry.png` and `notebooks/figures/nb11_expansion_wave1_screen.png`.
Both are the notebook's own "rough functional" figures (not yet run through the `figure-style`
polish pass) — per scope, only substantive data-integrity/honesty issues are flagged below, not
cosmetic styling. Values quoted in this review were re-derived directly from
`data/processed/nb11_cross_ancestry_fst.csv` and `data/processed/nb11_screen_mirror_results.csv`,
not read off the plots.

---

## Figure 1 — `nb11_cross_ancestry.png` (frequency heatmap + Fst lollipop)

**Verdict: PASS.** Titles, axis labels, and the visual message all check out against the underlying
data. One minor colorblind-legibility note.

| Check | Finding |
|---|---|
| Titles match data | Panel (a) "Associated-allele frequency across 1000G superpopulations" and panel (b) "Convergent variants vs genome-wide background" are both literal, non-overstated descriptions of what's plotted. No overarching claim-title is attached to the figure itself (the strong claims — "96th percentile", "every variant above baseline median" — live in the notebook's prose legend, not baked into the image), so there's no title/data mismatch to catch. |
| Axes + units | Heatmap x-axis: five 1000G superpopulation codes (AFR/AMR/EAS/EUR/SAS), y-axis: gene+rsID pairs; colorbar explicitly labeled "assoc. allele freq" and every cell carries a numeric text annotation, so the unit (allele frequency, 0–1 scale) is unambiguous even before reading the colorbar. Lollipop x-axis: "Hudson $F_{ST}$ (5 superpops)" — units and estimator named directly on the axis. Verified: heatmap cell values match `AF_AFR..AF_SAS` columns in `nb11_cross_ancestry_fst.csv` (e.g. BNC2 rs2153271 AF_EUR = 0.5805 → cell shows 0.58, the plot's brightest cell). |
| Honest message clear | The "mirror pattern" (each gene's two variants peak in opposite populations) is the heatmap's most visually salient feature by construction — adjacent-row pairs show a bright cell in one column and near-zero in the same column one row down, which is exactly the effect a reader would need to see to accept the claim. Not buried. |
| Legend/colour legibility | Panel (a) uses `viridis` (perceptually uniform, colorblind-safe) — no issue. Panel (b) color-codes points by gene using red/blue/green/purple (`#c0392b`/`#2980b9`/`#27ae60`/`#8e44ad`). This mixes a red and a green in the same categorical legend, which is a risk under deuteranopia/protanopia. **Mitigated**: every point also carries its gene name directly as a y-axis tick label, so no reader needs to resolve gene identity from color alone — the color is decorative/reinforcing, not the only channel. Not blocking, but flagging per the colorblind-safety check. |
| Scale honesty | Heatmap colorbar autoscales 0→data max (0.58) rather than a fixed 0–1 range. Not misleading here because every cell also carries its literal numeric value as text, so the color scale can't distort a reader's take on the underlying number. |

**No data-integrity flags for this figure.**

---

## Figure 2 — `nb11_expansion_wave1_screen.png` (max Fst vs mirror scatter, canonical vs non-canonical)

**Verdict: PASS with one labeling-precision flag.** The headline claim is strongly and correctly
supported by the data; one axis label overstates precision for a subset of points.

| Check | Finding |
|---|---|
| Title matches data | "mirror-signal strength is concentrated at canonical, known pigmentation effectors" is not just supported but *maximally* supported: re-sorting all 28 screened genes by `max_Fst` gives OCA2, SLC24A5, SLC45A2, HERC2, BNC2 as the top 5 — **every one of the top 5 is canonical** (verified directly from `nb11_screen_mirror_results.csv` + the notebook's `CANONICAL_GENES` set). The title does not overstate; if anything it's a conservative description of a very clean result. |
| Axes + units | X-axis "variants whose frequency peak falls in their own discovery ancestry (of up to 4)" is correctly labeled and the "(of up to 4)" qualifier is accurate — two genes (OCA2, HERC2) do have 4 screened variants, even though no gene's count of own-ancestry peaks exceeds 2 in this dataset (verified: `n_peak_in_discovery_anc` max = 2 across all 28 rows). Not misleading, just worth knowing the observed range is narrower than the stated ceiling. |
| **Y-axis label imprecision (flag)** | Y-axis reads "max Hudson $F_{ST}$ across **the gene's screened variant pair**." This is only literally true for the 23/28 genes with exactly 2 variants. Five genes — OCA2, HERC2, GRM5, SLC45A2, LURAP1L-AS1 — have 3 or 4 screened variants (verified from `n_variants` column), and `max_Fst` for those is the maximum of each variant's *own* Hudson Fst across ancestries (not a pairwise Fst *between* two variants — confirmed from the `detail` column, e.g. OCA2's four variants each carry an independently computed Fst, and 0.691 is simply the largest of the four). "Variant pair" implies a fixed 2-variant comparison structure that doesn't hold for these 5 genes, including OCA2 itself — the figure's own top data point. **Fix:** relabel to "max Hudson $F_{ST}$ across the gene's screened variants" (drop "pair"), or add "(2–4 variants per gene)" to the axis or caption. |
| Honest message clear | Visually unambiguous: the 3 largest markers by y-value (OCA2, SLC24A5, HERC2/SLC45A2/BNC2 cluster) are all filled red (canonical), directly labeled by gene name, and sit well above the grey non-canonical cloud. The message is the most prominent feature of the plot, not buried in a legend or caption. |
| Legend/colour legibility | Canonical = red (`#c0392b`), non-canonical = grey (`#7f8c8d`). This is a hue-vs-achromatic contrast, not a hue-vs-hue pairing — legible under all common CVD types (deuteranopia/protanopia/tritanopia), unlike Figure 1's panel (b). No issue. |
| Scale honesty | X-axis is a small-integer count (0/1/2) with `xlim` set to −0.3→2.6; this is a tight crop to the observed data range but doesn't clip or exaggerate any point (no data exists beyond 2, despite the "(of up to 4)" ceiling in the label). Y-axis is Fst on a linear 0–0.7 scale, not truncated or log-scaled — no distortion. |

**Data-integrity flag:** the y-axis label's "variant pair" phrasing should be corrected before this
goes into a presentation, since it visually and textually implies a uniform pairwise comparison
that doesn't hold for 5 of the 28 plotted genes (including the #1-ranked point, OCA2). This is a
labeling-precision issue, not a computation error — the underlying `max_Fst` values themselves are
verified correct against the source CSV.

*Secondary, non-blocking note:* the canonical/non-canonical split is computed by substring-matching
`CANONICAL_GENES` against composite GWAS-Catalog locus labels (e.g. `"GABRG3 - OCA2"`,
`"RNU6-366P - SLC24A4"` are flagged canonical because they contain a canonical gene's symbol). This
is a defensible heuristic disclosed in the notebook and doesn't affect the top-5 ranking that drives
the figure's headline claim (all 5 are single, unambiguous canonical-gene loci), but it could
misclassify a composite label in the middle of the ranking if the canonical gene named in the
composite label isn't actually the functional target at that locus. Not a data-integrity problem for
this figure's claim, just a modeling-choice caveat worth carrying into any write-up that cites
per-gene canonical/non-canonical counts individually.

---

## Summary

| Figure | Verdict | Blocking flags |
|---|---|---|
| `nb11_cross_ancestry.png` | PASS | None (minor: red/green used together in panel-b legend, mitigated by direct gene-name labels) |
| `nb11_expansion_wave1_screen.png` | PASS | Y-axis label overclaims a "pair" structure for 5/28 genes (OCA2 included) — relabel before presenting |

Both figures' underlying numbers were independently re-derived from the committed processed CSVs and
matched the plotted values in every case checked. No fabricated, cherry-picked, or mis-scaled data
was found in either figure.
