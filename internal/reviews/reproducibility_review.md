# Reproducibility review — NB4, NB5, NB9, NB11 (+ expansion), NB12

**Scope.** Static disk audit of the four notebooks built this session, checked against the standard this
project adopted after NB2's own inputs were once uncommitted and irreproducible: (1) every input is either
committed in-repo or pulled in a visibly-marked live cell whose response is frozen to disk under
`data/external/db_responses/`; (2) no absolute-path or workspace-only dependency; (3) figures are written via
`fig.savefig(...)` (not bare `plt.savefig`); (4) any live Ensembl/STRING/EBI/Reactome/KEGG/GO pull has its raw
response frozen so an offline re-run still works. Not re-executed (time-boxed); every claim below is a file-system
check (`git ls-files`, `os.path.exists`, source-cell inspection) — no notebook was run.

## Summary table

| Notebook | Inputs committed/frozen | No absolute/workspace paths | `fig.savefig` only | Live API frozen | Verdict |
|---|---|---|---|---|---|
| NB4 — unified association base | ✅ | ✅ | ✅ | ✅ (n/a — no live pull in-notebook) | **PASS** |
| NB5 — compare candidate networks | ✅ | ✅ | ✅ | ✅ | **PASS** |
| NB9 — Bajpai orphan reconciliation | ✅ | ❌ hardcoded `/Users/tlasisi/...` | ✅ | ✅ | **GAP (portability)** |
| NB11 — cross-ancestry conditionality + expansion | ✅ | ✅ | ✅ | ✅ | **PASS** |
| NB12 — direction-law expansion | ⚠️ derived columns not regenerable in-repo | ✅ | n/a (embeds a pre-rendered PNG, no `plt`/`fig` calls) | ❌ **no frozen GO/UniProt response** | **GAP (provenance)** |

## NB4 — `04_unified_association_base.ipynb` — PASS

- **Inputs.** Cell 2 resolves `ROOT` via `Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()` (no
  hardcoded path) and asserts each input exists before proceeding:
  - `data/processed/discordance_loci_author_explained.csv` — tracked, on disk.
  - `data/external/gwas_catalog/pigmentation_gwas_catalog.csv` (+ `.meta.json`) — tracked, on disk.
  - `data/external/gwas_catalog/gwas_pigmentation_associations.csv` — tracked, on disk.
- **Live pull.** Cell 4 carries a `REQUERY = False` guard around the GWAS Catalog re-pull (`scripts/gwas_catalog.py`,
  `scripts/pull_gwas_associations.py`); the notebook loads only the already-frozen CSVs when `REQUERY` is false. The
  notebook itself documents one open gap: *"exact CLI args used for the frozen pull are not recorded in-repo
  (documented gap, Step 6)"* — pre-existing, already self-flagged, not introduced this session.
  Comment note: as of this build the EBI download endpoint used for the re-pull returns HTTP 500, per the
  notebook's own comment.
- **Figure.** Cell 18: `matplotlib.use("Agg")` → `fig, ax = plt.subplots(...)` → `fig.savefig("figures/nb4_funnel.png", dpi=120)`.
  No bare `plt.savefig`.
- **Output.** Cell 22 writes `data/processed/nb4_unified_association_base.csv`, then reloads it and asserts the
  reload reproduces row/column/`source_type` counts exactly (`nb4_unified_association_base.csv` — tracked, on disk).

## NB5 — `05_compare_candidate_networks.ipynb` — PASS

- **NB2-lesson check, built into the notebook.** Cell 3 explicitly asserts existence of every frozen/raw input
  before anything else runs, with the comment *"NB2-lesson check FAILED — missing frozen inputs (not just
  referenced, must be on disk)"*. Verified on disk and tracked:
  - `data/raw/darcy2023/Table S{1,2,4,5,6} Bioengineering FINAL.xlsx` (5 files)
  - `data/external/db_responses/kegg_hsa04916.json`
  - `data/external/db_responses/reactome_R-HSA-5662702_participants.json`
  - `data/external/db_responses/reactome_pigmentation_curated_union.json`
  - `data/external/db_responses/reactome_mitf_subpathway_structure.json`
  - `data/external/db_responses/string_network_pulls_v12.json`
- **Other read inputs**, all present and tracked: `data/external/db_responses/hgnc_gene_groups.json`,
  `data/processed/gene_network_nodes.csv`, `data/processed/gene_network_edges.csv`,
  `data/processed/bajpai2023_crispr_hits.csv`, `data/raw/bajpai2023/science.ade6289_table_s1.xlsx`,
  `data/processed/baxter2018_650_pigmentation_genes.csv`, `data/processed/discordance_loci.csv`.
- **Live pulls, all REQUERY-guarded and frozen.**
  - Cell 11 (`REQUERY_REACTOME`): Reactome participants/detail/version endpoints → frozen to
    `reactome_R-HSA-5662702_participants.json` when re-run.
  - Cell 14 (`REQUERY_REACTOME_UNION`): 4-component Reactome pull → frozen to
    `reactome_pigmentation_curated_union.json`; the notebook also *replay-asserts* that recomputing the union
    from the frozen per-component gene lists reproduces the frozen `curated_union_genes` list exactly.
  - Cell 29 (`REQUERY_STRING`): documents that this MCP call must be run from the `repl` tool (not reachable from
    a notebook kernel), with the exact `host.mcp("protein-annotation", "get_string_network", ...)` call shown as
    a comment, writing to `string_network_pulls_v12.json`.
- **Figure.** Cell 44: `matplotlib.use("Agg")` → `fig, axes = plt.subplots(1, 2, ...)` →
  `fig.savefig(FIGDIR / "nb5_candidate_network_comparison.png", dpi=150)`. Tracked, on disk.
- **10 processed outputs** (`nb5_*.csv`) all written under `PROC` (repo-relative) and all present/tracked on disk.

## NB9 — `09_bajpai_reconciliation.ipynb` — GAP (hardcoded absolute path)

- **Inputs** (cell 2), all present and tracked: `data/external/db_responses/string_union_symmetric_pull_v12.json`,
  `data/external/db_responses/string_network_pulls_v12.json`,
  `data/external/db_responses/reactome_pigmentation_curated_union.json`,
  `data/processed/bajpai2023_crispr_hits.csv`, `data/processed/nb5_gene_set_membership.csv`,
  `data/processed/nb6_grn_edges.csv`, `data/processed/nb7_substrate_edges.csv`. Cell 2 also computes and prints a
  sha256 prefix for each frozen file as an integrity check — a stronger provenance guarantee than the other three
  notebooks provide.
- **GAP.** Cell 2 sets `REPO = '/Users/tlasisi/GitHub/pigmentation-gene-network'` — a literal, author-specific
  absolute path — rather than deriving it the way NB4/NB5/NB11/NB12 all do
  (`Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()`, or the `os.path.dirname(...)` /
  `__file__` fallback NB11 uses). `DBR`, `PROC`, the output path in cell 18, and the figure path in cell 19 are
  all built from this hardcoded `REPO`. **On any machine where the repo is not cloned to exactly this path (any
  public clone, any CI runner, any other contributor's machine), every cell in this notebook fails at the first
  `assert os.path.exists(p)` in cell 2** — this is exactly the class of failure the project's founding NB2 lesson
  was meant to prevent, this time as a path problem rather than a missing-file problem.
- **Fix required before public push:** replace the hardcoded string with a repo-root resolution pattern
  consistent with the other three notebooks, e.g.
  `REPO = str(Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd())`.
- **Figure.** Cell 19: `fig, (ax1, ax2) = plt.subplots(...)` → `fig.savefig(f'{REPO}/notebooks/figures/nb9_orphan_reconciliation.png', ...)`
  — correct `fig.savefig` usage, only the path construction is the problem.
- **Output.** `data/processed/nb9_orphan_reconciliation.csv` — tracked, on disk.

## NB11 — `11_cross_ancestry_conditionality.ipynb` (+ expansion) — PASS

- **Path resolution** (cell 3): `REPO = os.path.dirname(os.path.dirname(os.path.abspath("__file__"))) if "__file__" in dir() else os.path.abspath("..")`
  — no hardcoded machine path.
- **Live Ensembl pulls, all REQUERY-guarded with the exact endpoint documented in a comment above each guard, and
  all frozen under `data/external/db_responses/nb11/`** (README.md in that directory documents query-UTC
  `2026-07-12T15:18Z` and the endpoint/row-count for each file):
  - Cell 4 (`REQUERY`): `POST rest.ensembl.org/variation/human?pops=1` → `nb11_convergent_variants.json` (tracked).
  - Cell 7 (`REQUERY_BASELINE`): `overlap/region/human/...` + `variation/human?pops=1` batched pulls →
    `nb11_baseline_candidate_ids.json` + `nb11_baseline_variants.json` (both tracked).
  - Cell 12 (`REQUERY_LD`): `GET rest.ensembl.org/ld/human/pairwise/...` → `nb11_ld_pairwise.json` (tracked).
  - `nb11_baseline_stats.json` (derived baseline Fst summary) also tracked.
- **Figure.** Cell 15: `fig.savefig(os.path.join(FIGDIR, "nb11_cross_ancestry.png"), dpi=300, bbox_inches="tight")`.
  Tracked, on disk.
- **Output.** Cell 21 writes and reloads `data/processed/nb11_cross_ancestry_fst.csv` (tracked, on disk).
- **Expansion (Wave 1 + Wave 2), cells 22–30.** Reads four already-committed processed tables by explicit,
  repo-relative path, with the section's own markdown stating plainly *"read by absolute [i.e., resolved, not
  hardcoded] path — no live re-pull in this section"*:
  - `data/processed/nb11_screen_mirror_results.csv`, `data/processed/nb11_screen_candidates.csv` — tracked, on
    disk; backing frozen response `data/external/db_responses/nb11_screen/ensembl_1000g_screen_freqs.json` —
    tracked, on disk.
  - `data/processed/nb11_martin_khoesan_freqs.csv`, `data/processed/martin2017_noncanonical_loci.csv`,
    `data/processed/EXTRACT_Martin2017_loci.csv` — all tracked, on disk.
  - **Soft note (not a blocking gap):** the transform from the frozen Ensembl JSON to the derived
    `nb11_screen_mirror_results.csv`/`nb11_screen_candidates.csv` (Hudson Fst + mirror-pattern scoring) has no
    generating script or notebook cell in-repo — the notebook's own closing markdown (cell 31) states these
    tables "were built and committed by prior sessions, not regenerated here." The *inputs* satisfy the
    committed-or-frozen bar (criterion 1), but a reader cannot regenerate these two derived CSVs from the frozen
    JSON using anything on disk. Flagging for visibility, not blocking the push, since it mirrors NB4's own
    self-documented Step 6 gap and the raw frozen JSON is present.
  - **Figure.** Cell 30: `fig2, ...` → `fig2.savefig(fig2_path, dpi=300, bbox_inches="tight")` where
    `fig2_path = os.path.join(FIGDIR, "nb11_expansion_wave1_screen.png")`. Tracked, on disk.

## NB12 — `12_direction_law_expanded.ipynb` — GAP (unfrozen live pull)

This is the one notebook here that reproduces the *exact* failure class NB2 was founded to prevent: a value on
disk that cannot be regenerated or audited because the query that produced it was never frozen.

- **Frozen-input assertions** (cell 3) check three files exist and match expected shape:
  `data/processed/nb10_direction_law_annotation.csv` (from NB10, shape `(200, 18)`),
  `data/processed/nb12_direction_law_expanded.csv` (72 rows), `data/processed/nb12_expanded_summary.csv`. All
  three are present, tracked, and the shape assertions are consistent with what's on disk.
- **GAP.** The notebook's own markdown (cell 6, "Step 3 — A blind fourth source") states outright: *"For each
  uncovered gene we resolved a UniProt accession (mygene.info) and pulled its GO biological-process annotations
  from QuickGO. A classifier then labeled each gene's normal molecular function..."* — i.e., a live pull against
  `mygene.info` and QuickGO was made and fed through a classification step to produce the `mech_call`,
  `mech_conf`, and `mech_reason` columns for 11 genes in `nb12_direction_law_expanded.csv`. **No raw GO/UniProt
  response is frozen anywhere under `data/external/db_responses/`** (that directory has no `mygene`, `quickgo`,
  `go_bp`, or per-gene UniProt-accession file for these genes — checked against the existing
  `uniprot_annotation_direct.json`, which does not contain any of the 11 genes in question: `APC2`, `ATP7A`,
  `ATP7B`, `CTNS`, `LRMDA`, `MC2R`, `MLPH`, `MRAP`, `MYO5A`, `PAH`, `POMC`). **No cell in the notebook contains the
  live-pull code** (no `REQUERY`-style guard, no `requests.get`/`urllib`/`host.mcp` call anywhere in NB12's 7 code
  cells) — the notebook only loads the already-derived `nb12_direction_law_expanded.csv` in cell 3 as a plain
  frozen table. `mech_reason` values (e.g., for `ATP7B`: *"Copper transport essential for tyrosinase cofactor
  metallation in melanin synthesis."*) read as synthesized prose, not a verbatim GO/UniProt field — there is
  currently no way, from anything committed to the repo, to see what the actual GO terms or UniProt function text
  were, or to re-derive these 11 calls.
  - I traced this forward too: `build_nb10.py` (the generator script for NB10, currently **untracked** in the
    working tree) only builds NB10, not NB12 — it contains no `mech_call`/GO/UniProt logic. No other script or
    notebook in the repo references `mygene`, `quickgo`, or the 11 gene symbols above. `git log --all` shows
    `nb12_direction_law_expanded.csv` entered the repo pre-computed, in a single commit (`20768ac`), alongside the
    notebook that consumes it — the generating step happened entirely outside anything now on disk.
- **This is a decision point, not a decision I'm making for you:** two ways to close it before a public push —
  (a) re-run the GO/UniProt pull, freeze the raw mygene.info + QuickGO responses under
  `data/external/db_responses/`, and add a visible `REQUERY`-guarded query cell to NB12 that reproduces
  `nb12_direction_law_expanded.csv`'s `mech_*` columns from that frozen response (matching the pattern already
  used in NB4/NB5/NB11); or (b) if the original pull truly cannot be reconstructed, document the gap explicitly
  in the notebook (as NB4 already does for its own Step 6 gap) so a reader knows these 11 calls are asserted, not
  reproducible, and can weight them accordingly. **I have not chosen between these — that's a call for you.**
- **Figure.** NB12 does not call `matplotlib`/`plt`/`fig` at all; cell 17 simply displays a pre-rendered PNG
  (`IPython.display.Image(filename=... "nb12_direction_law_expanded.png")`). The `fig.savefig` criterion doesn't
  apply here since no figure is generated in this notebook — the PNG itself is tracked and on disk, but (per the
  point above) its generating code is likewise not present in NB12.

## Blockers for a reproducible public push

1. **NB9 — hardcoded absolute path (`REPO = '/Users/tlasisi/GitHub/pigmentation-gene-network'`, cell 2).** Blocks
   every downstream cell on any other machine. Mechanical fix, low risk: swap in the same `Path.cwd()`-relative
   pattern used elsewhere in the project.
2. **NB12 — unfrozen live GO/UniProt pull backing the `mech_call`/`mech_conf`/`mech_reason` columns for 11 genes
   in `data/processed/nb12_direction_law_expanded.csv`.** No raw response on disk, no query cell in the notebook.
   Needs either a frozen re-pull + visible query cell, or an explicit documented-gap note — your call, flagged
   above.

Everything else audited (NB4, NB5, NB11 main sections, all figure-writing cells project-wide) is PASS: inputs are
committed or frozen with visible, re-runnable, `REQUERY`-guarded query cells; no other workspace-only or
absolute-path dependencies were found; every figure-producing cell across all four notebooks uses
`fig.savefig`/`fig2.savefig`, never bare `plt.savefig`.

*Two files are currently untracked in the working tree and outside this review's scope but worth flagging before
push: `build_nb10.py` (NB10's notebook-generator script) and
`data/external/gwas_catalog/versions/pigmentation_gwas_catalog_refresh_20260712_20260712T144518Z.csv` (not
referenced by any of the four reviewed notebooks). Neither is `.gitignore`d — they're simply not yet committed.*
