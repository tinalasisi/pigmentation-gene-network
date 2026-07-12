# EXTRACT_Martin2017_loci — Extraction Specification

## Source

Martin AR, Lin M, Granka JM, Myrick JW, Liu X, Sockell A, Atkinson EG, Werely CJ,
Möller M, Sandhu MS, Kingsley DM, Hoal EG, Liu X, Daly MJ, Feldman MW, Gignoux CR,
Bustamante CD, Henn BM. "An Unexpectedly Complex Architecture for Skin Pigmentation
in Africans." *Cell* 171:1340-1353, November 30, 2017.
DOI: https://doi.org/10.1016/j.cell.2017.11.015

Source files (gitignored, not redistributed — see repository root README and this
directory's README for the withholding statement and exact expected filenames):
- `data/raw/papers/Martin2017_Cell_AfricanSkinPigmentation/Martin2017_Cell_AfricanSkinPigmentation.pdf` (main text, 29 pp.)
- `data/raw/papers/Martin2017_Cell_AfricanSkinPigmentation/Martin2017_Supplementary.pdf` (Tables S1-S5, S7, S8 as prose/tables; 8 pp.)
- `data/raw/papers/Martin2017_Cell_AfricanSkinPigmentation/Martin2017_Supplementary_Tables_S6.xlsx` (Table S6, two sheets: S6A per-SNP replication association table, S6B fine-mapping/HaploReg annotation table)

Deposited raw data (per paper's Data and Software Availability statement): Mendeley
Data, DOI 10.17632/98mh8z78m3.1. Data access requires South African San Council
approval per the San Code of Research Ethics; not re-hosted here.

## Study design (paper-level context, not duplicated per row)

- **Cohort**: 465-479 KhoeSan individuals (zKhomani San, N≈277-278; Nama, N≈202,
  depending on the specific data modality — see Table S4 genotyping/phenotyping
  matrix) from southern Africa.
- **Phenotype**: M index = log10(1/%red skin reflectance), measured with a
  DermaSpectrometer DSMII on the inner upper arm (baseline/constitutive
  pigmentation) and wrist (tanning status = wrist minus baseline).
- **Genotyping platforms**: Illumina 550k, OmniExpress, OmniExpressPlus, Omni2.5,
  and MEGA arrays (471 total KhoeSan samples across all arrays; see Table S4).
- **Imputation**: Shapeit2 v2.r778 phasing against the full Phase 3 1000 Genomes
  reference panel (2,535 individuals) plus 53 HGDP medium-coverage genomes;
  Impute2 v2.2.2 in 5 Mb windows; post-imputation filter of Impute2 info metric
  ≥0.8 and MAF≥0.01.
- **Association model**: EMMAX mixed-model association for imputed genotype data;
  GCTA mixed-model association for targeted-resequencing genotype data. Covariates:
  European and Bantu ADMIXTURE global-ancestry proportions (selected by forward
  stepwise regression) plus a REAP-derived kinship covariance matrix; age and sex
  added as covariates for the tanning-status phenotype only.
- **Multiple-testing thresholds actually used by the paper**: genome-wide
  significance p < 5e-8 (standard threshold, used for the paper's own explicit
  "genome-wide significant" call on SLC24A5 rs2470102, and matching the alpha used
  in the paper's own Table S8 power analysis); resequencing Bonferroni threshold
  p < 1.08e-6 (46,429 SNPs/indels with MAF>1% passing QC in the 7.1 Mb targeted-
  resequencing capture).
- **Meta-analysis**: METAL, inverse-variance-weighted, across phase 1 (107
  zKhomani + 109 Nama imputed) and phase 2 (240 additional genotyped individuals).
- **Two-stage design**: Phase 1 GWAS (top 50 associated loci = Table S5) →
  targeted resequencing of 36 candidate regions (7.1 Mb total, Table S7) in up to
  441 KhoeSan samples → phase 2 genotyping/meta-analysis for follow-up.
- **Known-locus replication panel**: 42 previously-published pigmentation-
  associated SNPs (Table 2 / Supplementary Table S6A) re-tested in this cohort.
  The paper's own conclusion: **"We do not replicate the vast majority of
  previously observed skin pigmentation associations in our dataset"** — only 4
  SNPs (SLC45A2 rs16891982, KITLG rs12821256, SLC24A5 rs1426654 and rs2470102)
  "marginally replicate."
- **Regulatory-annotation tool**: HaploReg, used to infer enhancer/DNase/motif
  annotations for fine-mapped/LD-linked variants (Table S6B).
- **Ontology / enrichment**: MGI Mammalian Phenotype ontology (via enrichR),
  chosen over Human Phenotype Ontology because pigmentation genetics is
  under-studied outside Europeans; top-50 phase-1 closest genes enriched for
  "abnormal extracutaneous pigmentation" (p=2.3e-3), "abnormal melanocyte
  morphology" (p=5.8e-3), "abnormal skin morphology" (p=3.5e-2).
- **Explicit polygenicity framing**: the paper states pigmentation architecture
  is more complex/polygenic at lower latitudes; known genes explain a minority of
  heritable variance even after gene-set enrichment testing (Table 1/S3), and the
  Discussion explicitly estimates "more than 50 loci (and indeed, likely far
  more...)" of mostly small effect contribute to KhoeSan pigmentation variation.
- **Cross-population transferability limitation (explicit in paper)**: a European
  9-SNP predictive model (Liu et al. 2015, up to 16% variance explained in
  Europeans) and a 7-SNP forensic model (claiming >99% prediction accuracy;
  Hart et al. 2013, Spichenok et al. 2011) both show **no significant association**
  with the KhoeSan M index (p=0.31 for the forensic model, Figure S5B) — direct
  evidence that prediction models trained in one ancestry group fail to transfer
  to another, cited here for the NB11 cross-ancestry discoverability analysis.

## Schema and design decisions

This extraction mirrors the field set and controlled vocabulary of
`data/processed/discordance_loci_effector_classified.csv` (see
`docs/specs/discordance_loci_effector_classified.spec.md`) so the two tables can
be concatenated/joined downstream, extended with paper-specific frequency,
resequencing, and GWS-vs-suggestive fields this paper's design requires.

**Single harmonized CSV** (`EXTRACT_Martin2017_loci.csv`, 51 rows) was chosen over
separate per-table CSVs because the task requires per-locus GWS/suggestive
flagging and effector classification uniformly across both the known-locus
replication panel (S6A, 42 rows) and the paper's own novel/suggestive findings
(9 rows drawn from main-text prose, cross-referenced against S6B where possible).
Splitting these into separate files would have forced a downstream user to
re-merge them to answer the single question this extraction exists to answer:
*which of this paper's loci are genuine, population-specific, confidently
attributed hits, vs. suggestive/unexplained/non-replicating signals?*

### Row provenance (`source_set` column)
- `known_locus_replication_Table2_S6A` (42 rows): the paper's replication test of
  42 previously-published pigmentation SNPs against the KhoeSan cohort.
- `novel_locus_targeted_resequencing_phase1_main_text` (5 rows): SMARCA2/VLDLR
  (×2 lead SNPs), TYRP1-upstream (rs34803545), EPM2A/FREM1 combined — signals
  identified in the phase-1 targeted-resequencing QQ-plot analysis (p<1e-3
  low-frequency outliers), described only in main-text prose (not itemized by
  rsID in either supplementary table for most of these).
- `novel_locus_phase2_meta_analysis_main_text` (2 rows): TYRP1-upstream
  (chr9:12088112, matched to S6B rs76413115) and SNX13 (rs2110015) — suggestive
  hits from the phase1+phase2 meta-analysis.
- `novel_variant_in_canonical_gene_null_result` (1 row): OCA2 rs1800417, a
  KhoeSan-enriched missense variant explicitly reported as NOT associated with
  pigmentation (p=0.87) — included for completeness, not a discordance/candidate.
- `known_locus_resequencing_expanded_main_text` (1 row): SLC24A5 rs2555364, the
  single most-associated SNP in the resequencing analysis (LD-tag of the
  causal rs1426654, not itself coding).
- `phase2_tanning_status_flagged_spurious` (1 row): two unnamed genome-wide-
  significant tanning-status hits that the paper's own text calls "most likely
  spurious" — retained purely as an honesty flag, `effector_status=not_a_locus`.

### GWS-vs-suggestive discipline (critical per task requirements)
- `genome_wide_significant` (bool) = `p_joint < 5e-8`, computed directly from the
  reported p-value wherever one exists.
- `gws_threshold` (string) records the exact threshold and its justification per
  row (5e-8 throughout; the resequencing Bonferroni threshold of 1.08e-6 is noted
  in prose where relevant but 5e-8 is used as the uniform GWS bar across all rows
  for cross-row comparability).
- `significance_tier` gives a plain-language tier: `genome_wide_significant`,
  `nominal_p_lt_0.05`, `not_significant`, `not_tested_no_data` (5 S6A rows where
  the paper's own `dataset` column = "none", i.e. the paper itself performed no
  test — not an extraction gap), `suggestive` (explicitly called "suggestive" by
  the paper's own text), `suggestive_qq_outlier` / `suggestive_qq_outlier_p_lt_1e-3`
  (flagged only via a QQ-plot visual/threshold criterion, not a locus-level GWS
  claim), and `genome_wide_significant_but_author_flagged_spurious` (the two
  tanning-status hits — GWS by the numeric threshold, but the paper itself
  disclaims them; downstream users must not treat this tier as a genuine hit).
- Four rows total meet `genome_wide_significant=True`: SLC24A5 rs1426654 (S6A,
  p_joint=9.77e-9), SLC24A5 rs2470102 (S6A, p_joint=1.05e-8; **note**: a
  *different* resequencing analysis of the same signal, reported only in
  main-text prose, gives p=3.6e-12 — both are retained and the discrepancy is
  documented in `classification_notes`, not reconciled, since they are genuinely
  different statistical tests on different underlying samples), SLC24A5
  rs2555364 (main-text resequencing analysis, p=6.7e-9), and the two
  author-flagged-spurious tanning-status hits (excluded from any genuine-hit
  count by their `not_a_locus` status).
- Six rows carry a `suggestive*` tier — these are the paper's own polygenic,
  largely-unresolved signals (SMARCA2/VLDLR ×2, TYRP1-upstream ×2, SNX13,
  EPM2A/FREM1) and are the primary candidates for
  `martin2017_noncanonical_loci.csv`.

### Attribution basis / effector status (mirrors discordance schema vocabulary)
- `attribution_basis` ∈ {coding_in_gene, regulatory_demonstrated,
  nearest_gene_only, in_LD_with_gene_variants, stated_unknown}. No row in this
  paper met the `regulatory_demonstrated` bar (a specific eQTL/reporter/CRISPR
  effect on a *named* gene at *this* SNP) — the paper's HaploReg-based regulatory
  annotations (Table S6B) are generic organ/tissue enhancer-DNase-mark overlaps,
  not gene-target-resolved eQTLs (confirmed: the `eQTL` column in S6B is null for
  all 271 rows). This is the paper's own evidentiary ceiling, not an extraction
  shortfall.
- `effector_status` ∈ {canonical_effector_variant_gap, effector_uncertain,
  effector_ambiguous_near, not_a_locus} per the "near GENE" nuance rule: rows
  attributed (even by proximity) to a canonical pigmentation gene are
  `canonical_effector_variant_gap` regardless of evidentiary strength (34/51
  rows); non-canonical genes with only nearest-gene/implied-LD support are
  `effector_ambiguous_near` (16 rows); the one row with a paper-stated novel
  gene assignment and no counter-evidence (SNX13) is `effector_uncertain`
  (1 row); the author-flagged-spurious tanning hits are `not_a_locus` (1 row).
  No row reached `regulatory_of_canonical_neighbour` status (that would require a
  *non-canonical*-gene-labeled SNP demonstrated to regulate a *canonical*
  neighbour — this paper's regulatory evidence does not resolve to that level of
  specificity for any locus).
- `is_canonical_effector_gene` flags membership in the fixed exclusion list
  (TYR, TYRP1, DCT, MLANA, PMEL, OCA2, HERC2, MC1R, KIT, KITLG, MITF, SLC45A2,
  SLC24A5, SLC24A4, ASIP, SOX10, PAX3, MFSD12, BNC2, EDNRB, EDN3, POMC, TPCN2,
  GPR143).

### `martin2017_noncanonical_loci.csv` (16 rows)
Filtered to `effector_status IN (effector_uncertain, effector_ambiguous_near)`
AND `is_canonical_effector_gene = False`. This includes both (a) 12 of the
S6A known-locus-replication rows whose *tested* SNP happens to be nearest a
non-canonical gene (VASH2, UGT1A, PAPD7/POLS, IRF4 ×2, 6p25.3, OPRM1, EGFR,
GATA3, NTM/HNT, GNG2, APBA2) — all of these are **null/non-significant** in
this KhoeSan cohort and are retained here only as candidates for downstream
cross-ancestry comparison, not as KhoeSan-specific findings — and (b) the 4
genuinely suggestive/novel non-canonical signals this paper itself reports
(SMARCA2/VLDLR ×2 leads, SNX13, EPM2A/FREM1 combined). Use the
`is_martin2017_novel_discovery` and `significance_tier` columns together to
distinguish these two very different categories before treating any row as a
"candidate" for NB11.

## Gaps and completeness

See `data/processed/martin2017_HONEST_GAPS.csv` (8 items) and
`data/processed/martin2017_COMPLETENESS_LEDGER.csv` (per-field-group population
rates). Headline gaps: exact genomic coordinates for 5 of the paper's own novel/
suggestive loci (SMARCA2/VLDLR ×2 leads, TYRP1-upstream rs34803545, SNX13
rs2110015, and the EPM2A/FREM1 combined row) could not be recovered from the
provided PDF/xlsx sources by rsID cross-reference against S6A/S6B; Table S5's
p-value column was truncated in both text- and image-based PDF extraction and
was not used as a primary source for this reason (it is also secondary to
S6A/S6B for this task's required schema, since it lacks the 3-population
frequency breakdown). Two internal inconsistencies in the source paper itself
(SLC24A5 rs2470102 p-value cited as both 1.1e-8 and 3.6e-12 in different
sections; Nama resequencing N cited as both 172 and 182) are documented
verbatim in `classification_notes`/the gaps ledger rather than silently
reconciled.

## Files produced

- `data/processed/EXTRACT_Martin2017_loci.csv` — 51 rows, 51 columns, all loci.
- `data/processed/martin2017_noncanonical_loci.csv` — 16-row filtered subset
  (non-canonical + effector_uncertain/ambiguous_near) for NB11.
- `data/processed/martin2017_HONEST_GAPS.csv` — 8-item gaps ledger.
- `data/processed/martin2017_COMPLETENESS_LEDGER.csv` — per-field-group
  completeness scoring to guide a future re-open pass.
- `docs/specs/EXTRACT_Martin2017_loci.spec.md` — this document.

## Handoff

Extraction complete; pending a provenance-completeness pass by the
Reproducibility Specialist per this project's standing workflow. Any field
flagged untraceable in that pass should be re-opened here and either filled or
explicitly marked `not_reported` with the reason, per the gaps
convention above.
