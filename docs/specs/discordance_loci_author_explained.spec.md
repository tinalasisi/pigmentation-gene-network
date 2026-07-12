# discordance_loci_author_explained.csv — spec / provenance

## Purpose

Extends `data/processed/discordance_loci.csv` (105 loci across the 13 curated
genotype→phenotype-discordance papers) with a **per-locus author-explanation
status**: whether the paper's own text proposes a biological/statistical
mechanism for the locus, states outright that the mechanism is unknown, gives
only a nearest-gene positional label with no discussion, or leaves the status
genuinely mixed/indeterminate. The rescue-candidate finding this build depends
on requires correctly separating loci the authors *actively explained* from
loci they *did not* — this table is that separation, made auditable back to a
page/table/quote in each source PDF.

## Method

Every paper's main-text PDF was parsed page-by-page (`pypdfium2` text
extraction) and, where present in the paper's own folder under
`data/raw/papers/<tag>/`, every supplementary file was parsed as well (DOCX
via `python-docx`, XLSX via `openpyxl`, additional PDFs via `pypdfium2`). No
`_fulltext.md` truncated capture was used as a source — only the parsed PDFs/
Office files. Extraction was per-**locus** (not per-paper): each of the 105
rows in `discordance_loci.csv` was searched for individually across its
paper's own text (by rsID, gene symbol, and locus description), and a
classification was assigned from what THAT paper's own prose says about THAT
locus — never inferred from what is generally known about the gene, and never
imported from a different paper's discussion of the same variant (see
`Ang2023`/`rs12913832` note in the ledger below for the case this discipline
was built to catch).

### Controlled vocabulary — `author_explanation_status`

| Value | Meaning |
|---|---|
| `mechanism_proposed` | The paper proposes a concrete biological, statistical, or historical mechanism for the locus (missense/regulatory consequence, in-silico damage prediction, functional assay, LD/conditional-independence account, population-history argument, or an explicit account of *why* a null result was observed). Hedged hypotheses ("it is possible that...") still count if a concrete mechanism is named. |
| `stated_unknown` | The paper explicitly says the mechanism, function, or explanation is not known / not found — an affirmative admission of ignorance, not silence. |
| `nearest_gene_only` | The locus is reported with a positional/nearest-gene label and a significance value, but the paper's own text gives no mechanistic account and does not say the mechanism is unknown — it simply isn't discussed. |
| `ambiguous` | The evidence for a single locus (or a locus row that groups several distinct variants) points in genuinely different directions across sub-variants or annotation sources, and a single controlled-vocabulary value could not be assigned without over-claiming. |

### Non-negotiables applied

- Every classification carries a verbatim quote (≤25 words, non-redistributive) and a
  `source_location` naming the exact PDF filename + page (or supplementary table).
- `author_explanation_status` is assigned **per row of `discordance_loci.csv`**, i.e. per
  locus/representative-SNP, not per paper. A paper with 15 loci can (and several do) carry
  four different status values across its own rows.
- A locus that is a *set/cluster representative* (`gene_assignment_basis` = `segment_member`)
  is classified on what the paper says about the SPECIFIC representative variant/cluster
  named in `discordance_loci.csv`, not on the general topic of the region.
- Where a paper cites a mechanism established by cited PRIOR work (not its own finding), that
  still counts as `mechanism_proposed` for this paper — the field records whether an
  explanation exists in the paper's text, not whether it is a novel discovery of that paper.
  This is flagged explicitly in `notes` wherever it applies (e.g. Yang2016/SLC24A5,
  Kastelic2013's five non-HERC2 IrisPlex SNPs).
- Nearest/mapped gene vs. causal/functional-target gene are never conflated: where a paper
  names a nearest-gene label but attributes the mechanism to a different (neighbouring)
  gene — e.g. Morgan2018 rs34357723 (nearest-gene label FANCA/SPIRE2, hypothesized functional
  target MC1R via long-range regulation) — the status reflects whether *that hypothesized
  mechanism* is present in the text, and `notes` documents the nearest-gene/functional-target
  split explicitly.

## Column dictionary (new columns added to `discordance_loci.csv`)

| Column | Description |
|---|---|
| `author_explanation_status` | One of the four controlled values above. |
| `author_explanation_quote` | Verbatim excerpt from the paper (≤25 words) supporting the classification. Multiple key phrases are occasionally concatenated with `...` where a single short quote would not carry the argument; each fragment remains ≤25 words as extracted, and the field never exceeds what is needed to justify the classification. |
| `author_explanation_section` | Named section of the source document the quote was drawn from (e.g. "Discussion", "Results (Appendix 2, Table 1)", "Supplementary Table 1"). |
| `source_location` | Exact PDF/DOCX/XLSX filename (as stored under `data/raw/papers/<tag>/`) + page number or table/sheet name. |
| `extraction_method` | How the source text was obtained. All 105 rows are `parsed_text_pdf` (or the DOCX/XLSX equivalent parse, tagged the same for this build) — none were OCR'd or hand-transcribed from a scan. |
| `extraction_status` | `extracted` for all 105 rows (see Completeness ledger — no row was left unclassified). |
| `gene_label_correction` | Populated only where the source PDF showed a different gene label than `nearest_gene_label` in the upstream `discordance_loci.csv`; blank (105/105) — see Gene-label corrections below. |
| `notes` | Free-text flags: nearest-gene vs. functional-target splits, hedged/contradicted mechanisms, cross-paper mechanism borrowing, honest-gap caveats, set-level (non-enumerable) loci. Populated on 52/105 rows. |

All 12 original `discordance_loci.csv` columns (`paper`, `locus_id`, `rsid`, `coord_build`,
`nearest_gene_label`, `gene_assignment_basis`, `paper_verdict`, `is_asserted_pigmentation`,
`pvalue`, `population`, `needs_review`, `evidence_quote`) are carried through unchanged.

## Status distribution (105 loci)

| Status | Count |
|---|---|
| `mechanism_proposed` | 50 |
| `nearest_gene_only` | 37 |
| `stated_unknown` | 15 |
| `ambiguous` | 3 |

## Rescue-candidate ledger (`stated_unknown` + `nearest_gene_only`, n = 52)

These are the loci for which the source paper itself provides no mechanistic account — the
population this build's rescue-candidate analysis should draw from. Full per-locus quotes and
page citations are in the CSV; counts by paper:

| Paper | `nearest_gene_only` | `stated_unknown` | Combined |
|---|---|---|---|
| Ang2023 | 16 | 3 | 19 |
| Kastelic2013 | 5 | 0 | 5 |
| Morgan2018 | 5 | 1 | 6 |
| Meyer2020 | 3 | 3 | 6 |
| Pospiech2016 | 3 | 3 | 6 |
| Abbatangelo2026 | 3 | 2 | 5 |
| Salvo2023 | 1 | 3 | 4 |
| Yang2016 | 1 | 0 | 1 |
| **Total** | **37** | **15** | **52** |

Notable individual entries (see CSV for full quotes/citations):
- Abbatangelo2026 `rs7853779` (TYRP1, AA+AG background): *"more difficult to interpret as
  there are no other studies... which have investigated the role of TYRP1 SNPs"* — `stated_unknown`.
- Meyer2020 `rs62538956` (TYRP1 enhancer, YY1 site): authors explicitly state *"we found no
  explanation of the effect of rs62538956:C"* — direction of the predicted mechanism
  contradicts the observed association — `stated_unknown`.
- Pospiech2016 `rs1393350`/`rs12203592` (TYR/IRF4, IrisPlex panel): *"the most puzzling... the
  pattern of association is ambiguous"* — `stated_unknown`.
- Morgan2018 chr16 conditional signal set (21 signals within ~1 Mb of MC1R): authors attribute
  the signals to statistical artifact — *"likely that they are synthetic associations caused
  by low linkage disequilibrium"* — not a biological mechanism, classified `stated_unknown`.
- Salvo2023 four of the five novel OCA2/HERC2 candidates (`rs74409036`, `rs78544415`,
  `rs72714116`, `rs551217952`): *"the functional role of these variants in eye colour
  formation is still unknown"* — `stated_unknown`/`nearest_gene_only`; the fifth
  (`rs191109490`) is the one exception with a SCREEN-predicted cis-regulatory element and is
  classified `mechanism_proposed`.
- Kastelic2013's five non-HERC2 IrisPlex markers (`rs1800407`, `rs16891982`, `rs1393350`,
  `rs12896399`, `rs12203592`): this is a pure validation study — the panel-marker status is
  cited from prior literature with no locus-specific account given in this paper itself,
  classified `nearest_gene_only`.

## Ambiguous entries (n = 3)

- **Ang2023**, OCA2 cluster (`rs1800404`/`rs1800414`/`rs4778219`/`rs7495174`): the row groups
  four variants of mixed annotation type (one synonymous with no in-silico prediction, one
  missense with conflicting Polyphen/SIFT calls, two intronic) with no per-variant prose
  discussion — a single status would over- or under-claim for at least one member.
- **Morgan2018**, blonde-hair polygenic set (213 lead variants) and brown-hair polygenic set
  (56 lead variants): both are `discordance_loci.csv` rows representing an unenumerated SET of
  variants, not a single locus; individual-variant mechanism status varies within each set
  (some of the 64 PICS-resolved candidates from the blonde set are coding/informative, most are
  not individually discussed) and cannot be collapsed to one value without disaggregating the
  set — flagged for a downstream re-open if per-variant status is needed.

## Gene-label corrections

**None.** All 105 `nearest_gene_label` values in the upstream `discordance_loci.csv` were
checked against the source PDF's own gene annotation for that locus during this extraction
pass (e.g. Ang2023's Appendix 2 table, Morgan2018's Supplementary Table 1, Meyer2020's Table 3)
and no discrepancy was found requiring correction. `gene_label_correction` is blank on all 105
rows.

## Honest-gaps ledger

The task brief characterized three papers as having limited-access source text (Norton2014 and
Norton2016 as paywalled/PDF-only with no supplement; Morell1997 as abstract-only). On actually
opening the PDFs stored in this repo's `data/raw/papers/` folders, **all three papers'
downloaded PDFs contain the complete full text** (Morell1997: 6 pages, Abstract through
References; Norton2014: 10 pages; Norton2016: 5 pages) — not abstracts or truncated captures.
This is recorded here rather than silently treated as "no gap" because it corrects an
assumption stated in the task brief, and because `REFERENCES.md` in this repo separately notes
the Norton papers as "Paywalled, no OA copy" for the purpose of *redistribution* (they cannot be
committed to the repo as files) — that is a distinct fact from *this extraction's access*,
which used the PI-supplied local copies already present in the folder and found them complete.

Given full-text access, all three papers were classified with the standard method and carry no
`not_reported`/`unresolved` extraction_status:

- **Morell1997** (PAX3, Waardenburg syndrome type 1): classified `mechanism_proposed` — the
  paper cites PAX3's transcription-factor/neural-crest-expression role as established
  background. Flagged in `notes`: this paper's own novel contribution is about penetrance of
  the *deafness* phenotype (modifier-gene hypothesis), not about the pigmentary phenotype's
  molecular mechanism — the mechanism_proposed classification reflects that a mechanism IS
  stated in the paper's text, not that it is this paper's novel finding.
- **Norton2014** (TYRP1 R93C, no rsID at time of publication): classified `mechanism_proposed`
  — the coding change (Arg→Cys) is stated explicitly, citing Kenny et al. 2012 for the original
  functional characterization.
- **Norton2016** (rs387907171 = the same TYRP1 R93C variant, dbSNP-identified by this later
  paper): classified `mechanism_proposed` on the same basis, citing Norton2014/Kenny2012.

No other honest-gaps were required. One residual data-completeness note not risen to the level
of a gap: Yang2016's locus row 2 ("OCA2-region SNP cluster; 6 of 8 tested; rsIDs in suppl.
table S4") could not have its 6 individual rsIDs resolved, because Yang2016's supplementary
table S4 is not present in this repo's paper folder (only the main PDF was downloaded for this
paper) — the row is classified `nearest_gene_only` from the main-text discussion of the group
(non-significant, no individual mechanism), and the missing rsIDs are noted in that row's
`notes` field for anyone who obtains the supplement later.

## Completeness ledger

| Check | Result |
|---|---|
| Rows in `discordance_loci.csv` | 105 |
| Rows classified in output | 105 |
| Rows with `extraction_status = extracted` | 105 / 105 |
| Rows with non-empty `author_explanation_quote` + `source_location` | 105 / 105 |
| Papers whose supplementary files were parsed (where present in the folder) | Abbatangelo2026 (DOCX SI), Crawford2017 (Supp PDF, 88 pp.), Kastelic2013 (3 supp PDFs), Kenny2012 (DOCX SI), Meyer2020 (S4 regulatory-table PDF), Morgan2018 (Supp Info PDF 44 pp. + Peer Review File 21 pp.), Salvo2023 (Supplement zip: figures PDF + tables XLSX) |
| Papers with no supplementary file in the repo folder (main PDF only) | Ang2023, Morell1997, Norton2014, Norton2016, Pospiech2016, Yang2016 |
| Duplicate (paper, locus_id) pairs in output | 0 |
| Gene-label corrections required | 0 |

No row was left with an unresolved or `not_reported` `author_explanation_status`. The three
items noted in the Honest-gaps ledger above (Morell1997/Norton2014/Norton2016's originally
assumed access limitation, and Yang2016's unretrieved supplementary rsIDs) are the only
deviations from a fully clean extraction and are surfaced here for re-opening if a downstream
step needs the Yang2016 S4 table specifically.

## Files

- `data/processed/discordance_loci_author_explained.csv` — the 105-row output table described
  above.
- `docs/specs/discordance_loci_author_explained.spec.md` — this document.

## Source papers referenced (DOI / local filename)

See `data/raw/papers/REFERENCES.md` for the full DOI/journal/access table. Local main-PDF
filenames used in `source_location` throughout the CSV:

| Paper key (as in `discordance_loci.csv`) | Local main PDF |
|---|---|
| Abbatangelo2026 | `Abbatangelo2026_SciRep_eyecolour_discordance.pdf` |
| Ang2023 | `Ang2023_eLife_Kalinago.pdf` |
| Crawford2017 | `Crawford2017_Science_AfricanPigmentation.pdf` |
| Kastelic2013 | `Kastelic2013_CroatMedJ_IrisPlex.pdf` |
| Kenny2012 | `Kenny2012_Science_TYRP1.pdf` |
| `Meyer et al. 2020,` | `Meyer2020_PLoSONE_GGbrowneyes.pdf` |
| Morell1997 | `Morell1997_JMedGenet_Waardenburg.pdf` |
| Morgan2018 | `Morgan2018_NatCommun_HairColour_MC1R.pdf` |
| Norton2014 | `Norton2014_AJPA_MelanesianBlond_TYRP1.pdf` |
| Norton2016 | `Norton2016_AJHB_Bougainville_TYRP1.pdf` |
| Pospiech2016 | `Pospiech2016_IntJLegalMed_IrisPlex_population.pdf` |
| Salvo2023 | `Salvo2023_Genes_AAAGblueeyes.pdf` |
| Yang2016 | `Yang2016_MBE_OCA2_EastAsian.pdf` |

No PDF prose is redistributed in the CSV or this document beyond quotes under 25 words each,
consistent with the copyright constraints documented in `REFERENCES.md`.
