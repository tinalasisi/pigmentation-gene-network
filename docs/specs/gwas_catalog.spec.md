# Source spec — NHGRI-EBI GWAS Catalog (pigmentation associations)

**Status:** ACQUIRED and pinned.

## Identity
- **Source:** NHGRI-EBI GWAS Catalog, download endpoint (associations, with child traits).
- **Endpoint:** `https://www.ebi.ac.uk/gwas/api/search/downloads`
- **Query per root:** `q=shortForm:"<EFO/OBA/MONDO id>"&includeChildTraits=true&efo=true&facet=association`
- **Access method:** `scripts/gwas_catalog.py v1.0` (config-driven; roots frozen in `scripts/traits_pigmentation.json`).
- **Access date (UTC):** 2026-07-08T01:15:41Z (stamped in every row's `queried_utc` and in the `.meta.json`).
- **Catalog version:** the GWAS Catalog is a live resource, not internally versioned by release number on
  this endpoint, so **the access timestamp is the version key**. The frozen pull is committed at
  `data/external/gwas_catalog/pigmentation_gwas_catalog.csv` (restored 2026-07-12 after the original
  gitignored `/output/` copy was lost; in-row `queried_utc` 2026-07-08T01:15:41Z is the version key).
- **License:** NHGRI-EBI GWAS Catalog data are released under EMBL-EBI terms (reuse with attribution); cite
  the catalog (Sollis et al. 2023) plus the per-association study PubMed IDs in the `pubmed` column.

## Query design (an explicit decision, not a default)
Ten ontology **root** traits, each expanded to its child traits via `includeChildTraits=true`, so the pull
captures every locus filed under an umbrella concept — including studies added after the root list was
authored:

| short form | label | axis |
|---|---|---|
| OBA_VT0002095 | skin pigmentation | skin |
| OBA_2045282 | facial pigmentation | skin |
| EFO_0003963 | freckles | skin |
| MONDO_0005326 | sunburn | skin/photo |
| EFO_0004279 | suntan | skin/photo |
| MONDO_0005434 | skin sensitivity to sun | skin/photo |
| EFO_0021835 | melanin measurement | skin |
| EFO_0003949 | eye color | eye |
| EFO_0009764 | eye colour measurement | eye |
| EFO_0003924 | hair color | hair |

**Why query by trait, not a static gene list:** a hardcoded gene list goes stale and hides its provenance.
Naming ontology roots and pulling with child-trait expansion is complete at authoring time and auditable at
score time; the config fails loud if a new mapped trait appears under a root that has not been reviewed.

## Result
- **1,072 lead SNPs** (one row per reported association), 22 columns.
- **Anchor assertions passed** (pull aborts if any is absent): SLC24A5 rs1426654, HERC2 rs12913832,
  MC1R rs1805007 — presence checks on well-known pigmentation SNPs (rs12913832 is the nearest gene HERC2 to
  the OCA2-regulated blue-eye signal, not a causal locus).
- Per-root counts: hair 397, skin-pigmentation 156, eye-colour-measurement 150, eye-color 147, suntan 83,
  sunburn 80, facial 38, freckles 12, skin-sensitivity 9.
- Payoff coverage: **MC1R 16** (incl. red-hair rs1805005/rs1805006/rs1805007), **OCA2 67**, **HERC2 65**.

## Columns pulled (all 22) and meaning
`axis`, `source_trait`, `source_short_form` (queried root), `mapped_trait`, `reported_trait`, `rsid` (join
key), `chr`, `pos_hg38` (**build GRCh38/hg38**), `risk_allele`, `direction_raw`, `risk_freq`, `or_beta`,
`pvalue` (**string** — see below), `mapped_gene`, `pubmed`, `study_accession`, `effect_type`,
`standard_error`, `ci_text`, `ancestry`, `sample_size`, `queried_utc`.

## Normalization decisions (no undocumented assumptions)
1. **No p-value threshold applied** at pull time; significance filtering is deferred to analysis.
2. **p-value stored as string**, not float. Values like `2E-9237` (HERC2) underflow to 0.0 as floats and
   `-log10(0)=inf` silently destroys the strongest loci; `-log10(p)` is computed from the string exponent by
   `vizhelpers.neglog10p()`.
3. **Coordinates GRCh38/hg38** as served (`pos_hg38`).
4. **Effect size left as reported** (`or_beta` + `effect_type`); OR vs beta not harmonized here.
   Cross-source harmonization (`harmonize.py`, `HARMONIZED_COLS`) is a separate step that flags rows whose
   units/SE/ancestry are untrustworthy from the source table alone (`needs_sumstats`) rather than coercing.
5. **Grouping-node trap avoided:** the REST `/efoTraits/{id}/associations` endpoint does NOT expand children
   and returns empty for OBA grouping nodes; the download endpoint with `shortForm:` + `includeChildTraits`
   is used instead (verified behavior).

## Independent cross-check (documented method mixing)
Both payoff anchors were re-queried through the **human-genetics MCP connector**
(`gwas_associations_for_variant`, GWAS Catalog REST associations endpoint) — a different access path to the
same catalog. Result (`mcp_anchor_crosscheck.json`, 2026-07-08T01:16:11Z): rs1805007 → MC1R (hair color +
skin-cancer traits, api_total 98); rs12913832 → HERC2 (eye color + pigmentation, api_total 90). Both agree
on gene identity and trait. The **download-endpoint pull is authoritative** for the atlas (expands child
traits); the MCP connector is the per-variant cross-check.

## Pinned artifacts
- `data/external/gwas_catalog/pigmentation_gwas_catalog.csv` — the 1,072-row table (committed; restored 2026-07-12).
- `data/external/gwas_catalog/pigmentation_gwas_catalog.csv.meta.json` — machine-readable provenance.
- `mcp_anchor_crosscheck.json` — the independent MCP cross-check.
- `scripts/gwas_catalog.py`, `scripts/traits_pigmentation.json`, `scripts/harmonize.py`,
  `scripts/vizhelpers.py` — pull engine, config, schema, plot helpers.
