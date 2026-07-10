# Source spec — Baxter et al. 2018, curated cross-species pigmentation gene list

**Status:** ACQUIRED and pinned.

## Identity
- **Citation:** Baxter LL, Watkins-Chow DE, Pavan WJ, Loftus SK. "A curated gene list for expanding the
  horizons of pigmentation biology." *Pigment Cell & Melanoma Research* 32(3):348–358, 2019 (published
  online 2018; DOI dates to 2018 — filed here as "2018/2019").
- **DOI:** 10.1111/pcmr.12743 · **PMID:** 30339321 · **PMCID:** PMC10413850 (not in the PMC OA subset).
- **Source file used:** Supporting Information **Table S7** — `pcmr12743-sup-0007-tables7.xlsx`, sheet
  "650 Pigmentation Genes".
- **Access method:** supplementary file provided by the project owner (downloaded from the publisher).
  Programmatic fetch of the main text succeeded via PMC, but the supporting-information tables are not in the
  PMC OA package; the author-provided copy is the reproducible input.
- **Access date:** 2026-07-08.
- **License / redistribution:** Wiley/PCMR **subscription** Version of Record. The Table S7 supplement is
  **NOT redistributed** — no open-license copy exists (PMC10413850 = not Open Access; Crossref license =
  VOR terms only; SI not in the PMC OA subset), and a curated gene list can carry compilation copyright in
  its selection/arrangement, so "factual data" is not a redistribution grant. The `.xlsx` is git-ignored;
  re-obtain via DOI 10.1111/pcmr.12743 and save as `data/raw/baxter2018/pcmr12743-sup-0007-tables7.xlsx`.
  Only the derived CSV is committed. Cite Baxter et al. and the underlying databases (OMIM, MGI, ZFIN, GO).

## Compilation design (what the list is)
A cross-species integration: genes annotated "pigmentation" in **OMIM (human), MGI (mouse), ZFIN
(zebrafish), and GO** were manually curated (each database is individually incomplete and species-biased),
then merged into a **single list of 650 genes** (Table S7 = the "Gene list integration" output). Table S6
holds eye-only genes that were moved to an eye-specific list; Tables S1–S5 are the per-database source lists.

## Columns in Table S7
`Gene stable ID` (Ensembl), `Human gene symbol`, `Mouse gene symbol`, `Zebrafish gene symbol1`,
`Orthologs across species2` (Y/N), `Pigment phenotype location` (e.g. body / eye), `GO`, `OMIM`, `MGI`,
`ZFIN` (evidence-source flags), `PubMed`, `Species with phenotype`.

## Normalization decision (the one that matters for this project)
- The sheet has **656 gene rows** (rows carrying a Gene stable ID; pandas reads the file as 659 rows with 3
  trailing blank rows). "650 Pigmentation Genes" is the curated headline count.
- **Only 635 rows carry a human gene symbol**; the remainder are mouse/zebrafish genes with no listed human
  ortholog. **We take the 635 human-symbol genes** as the usable set for a human network — which exactly
  matches the "Baxter 635 genes" figure used elsewhere in this project, confirming the human-symbol filter is
  the intended normalization (not an arbitrary cut).
- The evidence-source flags (GO/OMIM/MGI/ZFIN) and `Pigment phenotype location` are retained as annotation
  columns — useful for a proposed functional-axis annotation step (notebook placement pending PI agreement).
- **Note:** HERC2 is **not** in the Baxter list (consistent with it being absent from the Raghunath network
  too); OCA2, MC1R, TYR, SLC24A5, SLC45A2 are present.

## Result / pinned artifacts
- `data/processed/baxter2018_650_pigmentation_genes.csv` — full Table S7 (656 gene rows, all columns); the
  human-symbol filter (→635) is applied downstream, not destructively here.
- `data/raw/baxter2018/pcmr12743-sup-0007-tables7.xlsx` — raw Table S7, pinned as an artifact but **git-ignored**.
- **NOT committed to repo:** the Table S7 `.xlsx` supplement AND the paper PDF (Wiley subscription) are
  **not redistributed** — obtain from DOI 10.1111/pcmr.12743 (see `data/raw/papers/REFERENCES.md` for the
  exact expected filename). Only the derived `data/processed/baxter2018_650_pigmentation_genes.csv` is committed.

## Note for the build
This is the **largest and lowest-directionality** source: a membership list, no interaction direction or
effect size. It fits as gene-set membership + cross-species evidence annotation (a proposed gene-set /
annotation step, not yet an agreed notebook), not as edges.
