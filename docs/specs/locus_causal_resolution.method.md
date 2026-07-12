# NB7 Locus-Resolution Module: Causal Gene Resolution for Rescue Candidates

**Generated:** 2026-07-12T02:43:45.868074Z
**Scope:** the 52 "rescue candidate" loci from `data/processed/discordance_loci_author_explained.csv`
(rows where `author_explanation_status` in {stated_unknown, nearest_gene_only} — i.e. the original
authors did NOT give a mechanistic explanation for the locus). This module is independent of the
network-substrate work running in parallel (NB5); it only resolves causal genes.

## Goal and non-negotiable rule

Move each candidate from its **nearest/positional gene label** to a **likely causal gene**, backed
by an independent, citable basis. A positional label is *never* promoted to "causal" without
supporting functional-genomics evidence. The canonical cautionary case, which this pipeline
correctly reproduces: the blue-eye lead SNP **rs4778249** near **HERC2** shows Open Targets L2G
top-scoring gene = **HERC2** (score ≈0.32) but with **OCA2** as a close second (score ≈0.11) for
the "Eye color (saturation)" GWAS — i.e. even the L2G algorithm itself does not cleanly resolve
HERC2 vs. OCA2 at this locus, which is exactly the kind of nuance a naive nearest-gene call would
have hidden. See `data/external/db_responses/open_targets_l2g_rescue_loci.json` → `rs4778249`.

## Method

1. **Input.** 52 rescue-candidate rows extracted from the 105-row curated discordance table.
   Primary rsIDs (41 unique) extracted by regex from each locus's free-text `rsid`/`locus_id`
   fields; 3 loci had no extractable rsID (MC1R region "21 signals" locus, a non-genetic
   Gender/Sex covariate row, and an OCA2-region cluster whose rsIDs were "not obtained" per
   the source paper) — these are recorded as `unresolved` with an explicit reason, not silently
   dropped.

2. **Open Targets L2G (direct GraphQL API).** The `mcp-open-targets` connector's shared server
   was persistently rate-limited ("Rate limit exceeded for client: global") across ~1 hour of
   exponential-backoff retries (two separate backoff runs, ~1287s and ~2300s wall time, all
   attempts exhausted). We pivoted to calling the same backend directly via HTTP POST to
   `https://api.platform.opentargets.org/api/v4/graphql`, which is **not** subject to the shared
   MCP server's rate limit. For each rsID: `search(entityNames:["variant"])` resolves rsID →
   GRCh38 variant ID, then `variant(variantId) { credibleSets { l2GPredictions, colocalisation,
   ldSet, study } }` retrieves all GWAS/QTL credible sets overlapping that variant, their L2G
   gene-target scores, colocalization evidence (h4) against QTL studies, and in-sample LD sets.
   7/41 rsIDs were not found by OT's `search` endpoint; for these we built the GRCh38
   `chr_pos_ref_alt` variant ID directly from dbSNP placements and queried `variant()` — none
   resolved in OT either (0 credible sets), consistent with these being rare/under-powered
   variants absent from GWAS Catalog's harmonized credible-set index.

3. **eQTL Catalogue (`mcp-human-genetics`, `eqtl_associations`).** For loci where OT gave no
   pigmentation-relevant L2G/coloc signal, we queried the three skin-tissue eQTL Catalogue
   datasets (QTD000311 GTEx skin suprapubic n=517, QTD000316 GTEx skin sun-exposed n=602,
   QTD000544 TwinsUK skin n=370) directly for the candidate rsID. No dedicated "melanocyte" eQTL
   dataset exists in the Catalogue (758 datasets / 99 tissues surveyed; none contain "melano" in
   tissue or sample-group label) — skin (whole-tissue) is the closest available proxy and this
   caveat applies to every eQTL_coloc-basis resolution below.

4. **LD (direct Ensembl REST, no MCP tool available).** Neither `mcp-genomes` nor `mcp-variants`
   expose a dedicated LD/r² tool. We called the Ensembl REST LD endpoints directly
   (`/ld/human/pairwise/{rs1}/{rs2}/{population}` and `/ld/human/{rs}/{population}?window_size=500`)
   for candidates whose top OT/eQTL leads were weak or absent, to test "LD-rescue": is the lead
   SNP in high LD (r²) with a variant at a known pigmentation gene the study may have missed.
   Population = 1000 Genomes phase 3 CEU (test population; not population-matched to every
   source cohort — see gaps ledger).

5. **Cross-checking (`mcp-variants` dbSNP).** Every rsID was resolved against NCBI dbSNP
   (`dbsnp_get_rsids`) for GRCh37/GRCh38 coordinates, overlapping-gene symbols, consequence
   annotations, and (where present) ClinVar pigmentation-phenotype flags. This is the fallback
   coordinate source for the 7 rsIDs OT's search could not resolve, and the source of the
   `coding` resolution basis (missense/synonymous/coding-sequence variants directly inside a
   gene body — the strongest, least inferential category).

6. **Decision logic** (implemented in the analysis notebook, not hand-curated):
   - `coding`: dbSNP reports a coding consequence (missense/synonymous/coding_sequence_variant)
     directly attributable to one gene → high confidence, resolved gene = that gene.
   - `L2G`: OT L2G top-scoring gene across all credible sets at that variant, score ≥0.5 → high
     (score ≥0.75) or moderate (0.5–0.75) confidence. Scores 0.2–0.5 are still reported (never
     silently dropped) but flagged `confidence=low`. The GWAS trait of the top-scoring credible
     set is always recorded; where that trait is not itself a pigmentation trait (e.g. an L2G
     hit at a pigmentation locus driven by a "Refractive error" or chronotype GWAS signal
     colocalizing at the same position), this is flagged explicitly in `evidence_value` — the
     score is real L2G output, but the trait context should be weighed by the reader.
   - `eQTL_coloc`: no qualifying L2G score, but OT colocalization (h4) between a GWAS credible
     set and a QTL study points to a specific target gene.
   - `same_as_reported`: resolved gene (via coding/L2G/coloc) **matches** the paper's original
     positional label — i.e. independent evidence happens to corroborate the nearest-gene call.
     This is recorded separately from a bare positional label per the project rule: the label
     is never "causal by default," but here it *is* independently confirmed, and
     `resolution_basis_detail` retains which method did the confirming.
   - `unresolved`: no qualifying L2G/coloc/coding signal and no LD-rescue partner found. This is
     reported as data, not omitted.

## Per-connector query strings (representative)

- OT variant search: `search(queryString: "rs...", entityNames: ["variant"])`
- OT variant detail: `variant(variantId: "15_28135372_T_A") { credibleSets { ... } }`
- eQTL Catalogue: `eqtl_associations(dataset_id="QTD000316", rsid="rs...", nlog10p_min=3)`
- LD pairwise: `GET /ld/human/pairwise/rs.../rs.../1000GENOMES:phase_3:CEU`
- LD region window: `GET /ld/human/rs.../1000GENOMES:phase_3:CEU?window_size=500`
- dbSNP: `dbsnp_get_rsids(rsids=[...])`

## Resolution counts (52 rescue candidates)

resolution_basis
same_as_reported    32
unresolved          16
L2G                  4

(`same_as_reported` rows carry `resolution_basis_detail` showing whether coding, L2G, or coloc
evidence did the confirming — they are not bare "trust the label" calls.)

## Notable reassignments (label ≠ resolved causal gene)

- **rs6816819** (locus label "LOC107986284 intronic", chr4) → **TECRL**, L2G score 0.484
  (sub-threshold, low confidence), trait = Skin pigmentation.
- **rs11198112** (locus label "near EMX2", chr10) → **RAB11FIP2**, L2G score 0.348 (sub-threshold,
  low confidence), trait = Facial pigmentation measurement (UV light).
- **rs17184781** (locus label "TYR", chr11 TYR-region LD cluster) → **GRM5**, L2G score 0.757
  (high confidence) — but the top-scoring credible set's GWAS trait is "Skin changes due to
  chronic exposure to nonionising radiation," not a canonical pigmentation GWAS; TYR itself
  scored only 0.055 at this variant. Flagged for manual review — GRM5 is the L2G answer, but the
  trait context is a UV-damage phenotype rather than constitutive pigmentation.
- **rs638640** (locus label "ORAOV1 region") → **CCND1**, L2G score 0.575 (moderate confidence),
  trait = "Estimated glomerular filtration rate, serum creatinine" — **not** a pigmentation trait;
  flagged accordingly in the CSV (`l2g_trait_is_pigmentation=False`). CCND1 (cyclin D1) is a
  plausible candidate on general cell-biology grounds (it sits in a pathway implicated in several
  cancers, melanoma included), but that plausibility is NOT supported by the GWAS trait context of
  this specific L2G call, which is a kidney-function phenotype. Reported as a genuine positional
  reassignment (label ≠ resolved gene) but the evidential basis is weaker than the wording above
  first suggested — treat as moderate-confidence L2G only, not as melanoma-pathway corroboration.

## Honest-gaps ledger

- **7/41 rsIDs unresolvable in Open Targets** even after coordinate-based fallback: rs10594259,
  rs12233134, rs191109490, rs551217952, rs59334502, rs78544415, rs79380392. Several of these are
  HERC2/OCA2-region "novel" candidates from Salvo2023 that the source paper itself flagged as
  failing MAF QC or having low significance — their absence from GWAS Catalog's credible-set
  index is consistent with (not contradictory to) the original paper's own caveats.
- **eQTL Catalogue has no melanocyte-specific dataset.** All eQTL/coloc evidence uses whole-skin
  tissue (GTEx/TwinsUK) as the closest proxy; a true melanocyte eQTL resource would likely sharpen
  several `low`-confidence L2G calls and might resolve some `unresolved` rows.
- **LD-rescue population mismatch.** LD checks used 1000 Genomes CEU; several source GWAS used
  admixed-American, East Asian, or multi-ancestry cohorts (Ang2023, Abbatangelo2026, Kastelic2013)
  where CEU-based r² is not necessarily representative. No LD-rescue succeeded above r²≥0.5 for
  any of the tested unresolved loci: rs79380392 vs. rs12913832 r²=0.103 (CEU); rs59334502 vs.
  TYRP1-region SNPs r²=0.19–0.24 (CEU); several other candidate SNPs (rs191109490, rs551217952,
  rs78544415, rs676091 near-anchor pairs) returned **zero rows** from the Ensembl LD endpoint,
  likely because these rare variants are absent from the 1000 Genomes phase 3 panel used by the
  endpoint.
- **OT MCP connector was flaky; direct GraphQL API was not.** The shared `mcp-open-targets`
  server hit a persistent "Rate limit exceeded for client: global" across two backoff runs
  totalling ~1 hour; the identical GraphQL backend at `api.platform.opentargets.org` answered
  immediately when called directly via HTTP. This is recorded as a connector issue, not treated
  as "Open Targets is unavailable."
- **Build note.** The 105-locus source table's `coord_build` field is mostly GRCh37/hg19; Open
  Targets and dbSNP both report GRCh38 coordinates/variant IDs. No liftover was performed — all
  cross-build comparisons in this table are done by rsID (build-independent identifier), not by
  raw coordinate matching, except where explicitly noted (e.g., the GRCh37-anchored Ensembl LD
  calls use `grch37.rest.ensembl.org` and take rsIDs directly, avoiding the need to liftover
  coordinates).
- **3 loci excluded from rsID-based querying entirely** (recorded as `unresolved`, not dropped):
  the MC1R region locus described only as "21 conditional synthetic-association signals" with no
  single representative SNP; a "Gender/Sex" non-genetic covariate row that is not a genetic locus
  at all; and an OCA2-region SNP cluster whose rsIDs the source paper did not report (only in a
  supplementary table not available to this pipeline).

## Output files

- `data/processed/locus_causal_resolution.csv` — one row per rescue-candidate locus (52 rows),
  with resolved gene, basis, confidence, evidence value, connector accession, and notes.
- `data/external/db_responses/open_targets_l2g_rescue_loci.json` — frozen verbatim OT GraphQL
  responses (search + full variant/credibleSets/L2G/colocalisation) for all 41 queryable rsIDs.
- `data/external/db_responses/dbsnp_rescue_loci.json` — frozen verbatim dbSNP records for all 41
  rsIDs (plus the 7-rsID supplementary fetch used for OT coordinate fallback).
- `data/external/db_responses/eqtl_catalogue_skin_rescue_loci.json` — frozen eQTL Catalogue skin
  associations for 20 ambiguous loci, plus a targeted KITLG check.
- `data/external/db_responses/ensembl_ld_rescue_loci.json` — frozen Ensembl LD pairwise and
  region-window query responses used for LD-rescue testing.

Not committed to git per task instructions.


## Addendum: eQTL tissue-appropriateness tagging (PI-requested refinement)

A genetics-reviewer note flagged that bulk-tissue eQTL (whole skin, generic GTEx tissues) can
misassign the causal gene at pigmentation loci, because melanocytes are <5% of a skin biopsy and
melanocyte eQTL signal differs from all 44 GTEx tissues. Per that request, every eQTL-coloc-based
resolution in this table now carries two additional columns:

- `eqtl_tissue`: the specific tissue/cell type + dataset the signal came from.
- `eqtl_tissue_class` in `{melanocyte_specific, skin_bulk, other_tissue}`.

**Melanocyte-dataset availability check.** We surveyed the eQTL Catalogue connector across all
quant methods (`ge`, `tx`, `txrev`, `exon`, `microarray`, `leafcutter`) — 757 datasets total, 98
unique tissue labels — and found **zero** melanocyte-specific or melanocyte-derived datasets. The
closest available proxies are bulk-skin datasets: GTEx skin (suprapubic, not sun exposed;
QTD000311), GTEx skin (sun exposed, lower leg; QTD000316), and TwinsUK skin (QTD000544, bulk
biopsy). Every eQTL-based call in this pipeline is therefore built on `skin_bulk` evidence, not
`melanocyte_specific` evidence — there was no melanocyte-specific option to prefer.

**Impact on this run.** Of the 52 rescue candidates, only **one** locus ended up resolved on an
eQTL basis: **rs6917661** (OPRM1-region label, chr6). Open Targets returned zero formal GWAS↔QTL
colocalization at this variant (no pigmentation-trait credible set overlaps it in OT's index), so
this call rests on a direct cis-eQTL association rather than a coloc test, and the two candidate
target genes disagree across datasets — TwinsUK bulk skin points to **CNKSR3** (p=9.2e-8), GTEx
bulk skin (sun-exposed) points to **IPCEF1** (p=9.7e-9). Per the tissue-appropriateness rule, this
row is downgraded from a firm resolution to `confidence=lower_confidence_tissue_mismatch` and
flagged as an eQTL-coloc call needing melanocyte-specific follow-up — it is NOT treated as settled.

**Melanocyte-specific vs. bulk/other-tissue eQTL resolutions in this run:**

| eqtl_tissue_class | n loci |
|---|---|
| melanocyte_specific | 0 |
| skin_bulk | 1 (rs6917661 → CNKSR3, `lower_confidence_tissue_mismatch`) |
| other_tissue | 0 |
| n/a (L2G/coding/LD/unresolved — tissue tag does not apply) | 51 |

**L2G and LD-based calls are explicitly unaffected** by this refinement, per the PI's
instruction — Open Targets' L2G score already integrates its own internal QTL colocalization
features (including, where available, tissue-matched evidence) into a single learned score, and is
not re-scored here by raw tissue label. The 4 `L2G`-basis rows (rs6816819→TECRL, rs11198112→
RAB11FIP2, rs17184781→GRM5, rs638640→CCND1) and the 32 `same_as_reported` rows whose
`resolution_basis_detail` is `L2G` or `coding` retain their original confidence.

**Follow-up flagged for the melanocyte-specific QTL pass** (Zhang 2018 eQTL / Zhang 2021 meQTL, as
referenced by the PI): re-examine rs6917661 (CNKSR3 vs. IPCEF1 disagreement) with true melanocyte
eQTL/meQTL data once that pass lands. No other locus in this run rests on eQTL evidence, so the
revisit scope for this refinement is narrow (1 locus) — the larger caveat is structural: this
pipeline currently has no melanocyte-specific molecular-QTL resource at all, so any future
eQTL-basis call in later reruns of this pipeline will need the same tissue tag and the same
default downgrade until a melanocyte dataset is added upstream.
