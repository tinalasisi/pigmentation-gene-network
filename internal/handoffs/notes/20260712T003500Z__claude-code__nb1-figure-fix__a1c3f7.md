---
from: claude-code (nb1-figure-fix session)
to: claude-science
date_utc: 2026-07-12T00:35Z
platform: claude-code
subject: NB1 figures fixed + Phosphodiesterase source-typo corrected; NB2 has a SECOND missing-input blocker
---

Heads-up on files I just changed (shared working tree; commit pending). None of this touches your NB4–NB8
execution-route work, but two items intersect the shared substrate CSVs and NB2, so read on.

## What I changed (NB1 + one processed CSV)
1. **`notebooks/01_reconstruct_published_network.ipynb`** — the two figures never rendered on the site because
   the plotting cells `savefig()`'d but never *displayed* the figure, so the stored output was stdout only
   (nothing for Quarto's `execute:false` to embed). Fixed by appending `display(fig); plt.close(fig)`. Both
   figures now embed as `image/png` and render (verified via local `quarto render` → 2 `<img>` tags).
2. **Phosphodiesterase source typo (affects the substrate).** The node *Phosphodiesterase* is stored as
   **`PhosphodiesteHRASe`** in the shared-strings of BOTH published workbooks — MOESM1 (3 edges) and MOESM2
   (node list + node_properties). It is a data-entry error in the *source files*, not a pandas bug (the
   earlier "pandas-3.0 fragility" note was a misdiagnosis). I added a documented one-token correction
   (`fix_labels`, `{"PhosphodiesteHRASe":"Phosphodiesterase"}`) applied wherever labels are read; raw files
   untouched. Net effect on committed data: `raghunath_edges_typed_signed.csv` is unchanged (reverts to the
   already-correct value); `raghunath_nodes_typed.csv` changes only `Phosphodiesterase_melan` (restored) +
   `IRAK1_Active_kerat` state `""`→`active` (the committed CSV was stale vs the notebook's own regex). Counts
   unchanged (265/429). **If NB4–NB8 consume `raghunath_nodes_typed.csv`, pull the updated version.**

## What I did NOT touch (yours / PI-held)
`data/external/`, `internal/TODO.md`, `rescue_candidate_audit.csv`. If you're mid-write on any of these, no
conflict from me.

## NB2 — a SECOND blocker beyond the 7 frozen JSONs (please fold into your NB2 redo)
An audit found that even after the 7 `data/external/db_responses/*.json` are restored, **NB2 still can't
re-run**: cell 18 reads two intermediate CSVs that *no cell or script in the repo writes* and that are absent
on disk:
- `data/processed/nb2_projection_cited.csv`
- `data/processed/nb2_backbone_cited.csv`

(The only `to_csv` cell, 31, writes nb2_annotation / nb2_protein_enrichment / nb2_gene_layer_edges /
gene_network_nodes / gene_network_edges / nb2_omnipath_validation — never these two.) So NB2 needs: the 7
frozen JSONs **and** these 2 CSVs regenerated + committed, or cell 18 refactored to derive them in-notebook.
