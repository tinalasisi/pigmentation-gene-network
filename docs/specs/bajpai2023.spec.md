# Source spec — Bajpai et al. 2023, genome-wide CRISPR screen for pigmentation

**Status:** ACQUIRED and pinned.

## Identity
- **Citation:** Bajpai VK, Swigut T, Mohammed J, Naqvi S, Arreola M, Tycko J, Kim TC, Pritchard JK, Bassik
  MC, Wysocka J. "A genome-wide genetic screen uncovers determinants of human pigmentation." *Science*
  381(6658):eade6289, 2023-08-11.
- **DOI:** 10.1126/science.ade6289 · **PMCID:** PMC10901463 (NIH author manuscript NIHMS1964433).
- **Source file used:** Supplementary **Table S1** — `science.ade6289_table_s1.xlsx`, sheet
  "Low SSC FACS enriched genes" (from the `science.ade6289_tables_s1_to_s10.zip` supplement).
- **Access method:** supplementary file provided by the project owner (downloaded from the publisher). A
  programmatic fetch was attempted first (publisher site behind a Cloudflare JS challenge, PMC behind a
  reCAPTCHA challenge) and deliberately not circumvented; the author-provided copy is the reproducible input.
- **Access date:** 2026-07-08.
- **License:** the *Science* article is "Copyright © 2023 The Authors, some rights reserved; exclusive
  licensee American Association for the Advancement of Science" (article PDF, pp.12–13). The same PDF (p.12)
  states the article "is subject to HHMI's Open Access to Publications policy" under which "the
  author-accepted manuscript (AAM) … can be made freely available under a CC BY 4.0 license" — i.e. CC BY 4.0
  covers the **AAM** (via PMC10901463), **not** a blanket CC BY on the publisher's typeset article or its
  supplementary package.
  Table S1 is committed here as a **factual gene-screen data table** (data, not copyrightable expression),
  with the project owner's authorization and full attribution to Bajpai et al. 2023; the typeset article
  PDF/text is not redistributed.

## Screen design (what the numbers mean)
Genome-wide CRISPR screen in human melanocytes using melanin's light-scattering (side-scatter, SSC) to sort
cells by pigment level; guides enriched in the **low-SSC (low-melanin)** gate mark genes whose perturbation
**reduces pigmentation**. Effect/score computed with **casTLE** across two replicates.

## Hit-calling (the normalization decision)
- Table S1 contains the **full screen (4,956 genes)**, one row per gene, with `Combined_casTLE_Effect`
  (direction/magnitude), `Combined_casTLE_Score`, `p_value`, and `q_value` (FDR).
- **Hit threshold: `q_value < 0.10`** on the combined casTLE score → **169 genes**, which reproduces the
  paper's reported "169 functionally diverse genes." (For reference: q<0.05→149, q<0.15→208.) This threshold
  is the single hit-calling assumption and is applied in `scripts/extract_bajpai.py`-equivalent processing.
- All 169 hits have **positive casTLE effect** (enriched in the low-melanin gate) → uniform direction:
  *knockout/knockdown reduces pigmentation*. Recorded as `direction_note` in the processed table.
- Known pigmentation positive controls recovered among the hits: TYR, DCT, SLC45A2, OCA2, KLF6, COMMD3.

## Columns kept in the processed table
`GeneID` (Ensembl), `Symbol`, `GeneInfo`, `Localization`, `Process`, `Function`,
`Combined_casTLE_Effect`, `Combined_casTLE_Score`, `Minimum_Effect_Estimate`, `Maximum_Effect_Estimate`,
`p_value`, `q_value`, `direction_note`.

## Result / pinned artifacts
- `data/processed/bajpai2023_crispr_hits.csv` — **169 unique hit genes** with score, direction, q-value.
- `data/raw/bajpai2023/tables_s1_s10/science.ade6289_table_s1.xlsx` — raw Table S1 (full 4,956-gene screen),
  pinned so the threshold can be re-derived.
- **Committed to repo:** Table S1 supplement only (`data/raw/bajpai2023/science.ade6289_table_s1.xlsx`; factual data table, see license note above).
  The typeset paper PDF, SM PDF, full Tables S1–S10 bundle, and MDAR checklist are **not redistributed** —
  obtain from DOI 10.1126/science.ade6289 (see `data/raw/papers/REFERENCES.md`).

## Note for the build
Gene identity is already Ensembl-ID + HGNC-symbol in the source, so this list joins to the network's gene
layer directly. The uniform "reduces pigmentation" direction is usable as an edge-sign prior toward the
melanin endpoints in a proposed downstream connection step (notebook placement pending PI agreement).
