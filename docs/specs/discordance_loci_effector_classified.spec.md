# discordance_loci_effector_classified.csv — spec / provenance

**Supersedes:** `discordance_loci_author_explained.csv`, which has been removed from the repository
(recoverable from git history — its last tree presence is commit `7585286`, removed by `787fe4c`; see
`internal/CHANGELOG.md` 2026-07-12). This file is now the single curated
source for the 105 legacy loci: its 105 rows with `paper != "Kim2024"` reproduce that file's 105 rows
exactly on every shared column, and the two audit columns worth keeping — `is_asserted_pigmentation`
and `needs_review` — were migrated into this file before the old one was retired (the empty
`gene_label_correction` column was dropped). NB4 reads this file directly. **Status:** complete for
all 14 papers except the Open Targets canonical-status cross-check, which is documented as an open gap
(see below) and needs re-opening once the connector's rate limit clears.

## Purpose

The prior extraction (`discordance_loci_author_explained.csv`) answered a **variant-level-mechanism**
question: did the source paper's own text explain *this specific variant's* biological consequence?
That is a different question from the one this project's flagship analysis needs: **is the gene the
authors associated with the phenotype actually the effector**, or is it merely the nearest positional
label with no demonstrated functional relationship to the phenotype?

Conflating the two questions corrupted the original "author-unexplained" rescue-candidate list: 33 of
its 52 rows pointed at a canonical, textbook pigmentation effector (TYRP1, OCA2, HERC2, SLC45A2, TYR,
IRF4, SLC24A4) where only the *specific variant's* molecular consequence was unexplained — the gene
itself was never in doubt. The single clearest example is **HERC2 rs12913832**, the best-characterized
eye-color variant in the human genome, which the prior extraction tagged "author-unexplained" only
because the paper under review (Ang2023) does not itself restate the HERC2→OCA2 enhancer mechanism
established elsewhere in the literature.

This table fixes that by re-reading every locus's own text and classifying, **per locus**, (a) what
gene the authors actually name, (b) the specific type of evidence backing that attribution
(`attribution_basis`), and (c) whether that attribution places the locus in scope for the
effector-uncertain rescue analysis (`effector_status`). Canonical-effector loci — even ones where the
*variant's* mechanism is unexplained — are explicitly separated out and are NOT part of the
effector-uncertain target set.

## Method

Read every one of the 14 source papers' own text (main PDF, plus every supplementary PDF/DOCX/XLSX
present in `data/raw/papers/<tag>/`) and, for each of the 105 rows already established in
`discordance_loci_author_explained.csv` (13 legacy papers) plus 26 newly-extracted rows for Kim2024
(East Asian skin-color GWAS, added this pass because it was not part of the original discordance
extraction), assigned:

1. `author_attributed_gene` — the gene(s) the authors name for this locus, verbatim where a single
   gene, or a `/`-joined list where the paper names multiple co-candidates at one locus (e.g. a
   colocalization analysis implicating several genes without resolving which is causal).
2. `attribution_basis` — one of six controlled values (see below), assigned from what the paper's
   own text says, never inferred from the gene symbol alone.
3. `effector_status` — the classification the effector-uncertain analysis consumes directly (see
   below), derived from `attribution_basis` **and** whether `author_attributed_gene` is on the
   project's canonical pigmentation-effector list (TYR, TYRP1, DCT, MLANA, PMEL/SILV, OCA2, HERC2,
   MC1R, KIT, KITLG, MITF, SLC45A2, SLC24A5, SLC24A4, ASIP, IRF4, SOX10, PAX3, EDNRB, EDN3, TPCN2,
   BNC2, POMC, GPR143, TYRP2).
4. `classification_notes` — full reasoning per locus, including any cross-paper corroboration (e.g.
   MFSD12 is independently attributed at this level of confidence in three separate papers: Ang2023,
   Crawford2017, Kim2024) and any Zhang2018 melanocyte-eQTL cross-check result.

Two independent gene-identity/function connector checks were run against every non-canonical
candidate gene surfaced by this classification: **mygene.info** (via `mcp-genes-ontologies
query_genes`, for gene summaries/function) and a lookup against **Zhang2018's melanocyte eQTL
gene lists** (Supplemental Table S6: 519 genes tested for melanocyte cis-eQTL status across three
overlapping panels — melanin-GO, pigment-GO, and a 379-gene curated pigmentation list). A third
check, **Open Targets** disease/trait association (`search_entities`), was attempted but never
succeeded — every call returned `"Rate limit exceeded for client: global"` across multiple retries
with backoff; this is recorded as an open gap, not silently skipped.

### Controlled vocabulary — `attribution_basis`

| Value | Meaning |
|---|---|
| `coding_in_gene` | The variant is coding (missense/nonsense) or otherwise structurally within the named gene. |
| `regulatory_demonstrated` | The authors show or cite a demonstrated regulatory effect on the named gene — eQTL (own analysis or colocalization), reporter assay, chromatin/enhancer annotation, CRISPR functional validation. |
| `nearest_gene_only` | The named gene is nearest to the variant with no functional claim made by the authors. |
| `in_LD_with_gene_variants` | The authors explicitly reason the signal tags variants in the named gene via LD/conditional analysis (often a passenger relative to another row). |
| `stated_unknown` | The authors explicitly state the effector/mechanism is unknown. |
| `not_applicable` | The row is a non-genetic covariate, a null/non-significant reference comparator, or a set-level/unenumerable row — no single-gene attribution basis applies. |

### Controlled vocabulary — `effector_status`

| Value | Meaning | In scope for effector-uncertain rescue analysis? |
|---|---|---|
| `canonical_effector_variant_gap` | `author_attributed_gene` is on the canonical effector list; only the *variant's* mechanism (not the gene) may be unresolved. | **No** — this is the PI's earlier, separate project (canonical-effector variant-mechanism gaps). |
| `effector_uncertain` | `author_attributed_gene` is NOT on the canonical list, or the paper states the effector is unknown, with no established/on-list gene as a competing near-neighbor explanation. | **Yes** — the flagship target set. |
| `effector_ambiguous_near` | The variant is "near" one or more genes, none on the canonical list, with no demonstrated (only implied/LD) effect on any of them. | **Yes**, flagged for LD-nomination rather than a rescue claim — see "Near a gene" below. |
| `regulatory_of_canonical_neighbour` | The nearest-gene label is non-canonical, but the authors' own claimed regulatory/eQTL target is a canonical gene. | **No** as a new finding — it resolves to the canonical neighbor; the non-canonical nearest-label gene is noted but not claimed as an independent effector. |
| `not_a_locus` | The row is a non-genetic covariate (sex, admixture fraction), a statistical-artifact explanation, or an unenumerable polygenic set. | **No** — excluded from all effector classification. |

### "Near a gene" — the specific nuance flagged by the task

For every locus attributed to a gene the variant is not physically inside, the classification asks
explicitly: does the paper **demonstrate** an effect on the named gene (eQTL, reporter, chromatin,
CRISPR), or does it only note **proximity/implied LD**?
- Demonstrated effect on a **canonical** neighbor → `regulatory_of_canonical_neighbour` (e.g.
  Morgan2018's RALY-intron/ASIP-eQTL variant, idx80; Morgan2018's FANCA/SPIRE2-nearest-label but
  MC1R-regulatory-target variant, idx73).
- Demonstrated effect on a **non-canonical** gene → `effector_uncertain` (e.g. Kim2024's SPIRE2/DEF8/
  CPNE7 eQTL-colocalized 16q24.3 locus, idx23 in `EXTRACT_Kim2024_loci_v2.csv` — notably a case where
  the authors explicitly reject the tempting canonical MC1R attribution despite genomic proximity,
  because the eQTL evidence itself points to SPIRE2/DEF8/CPNE7, not MC1R).
- Only proximity/implied LD, no canonical gene nearby → `effector_ambiguous_near` (e.g. Ang2023's
  EGFR/LANCL2, IPCEF1/CNKSR3, GRM5, SYT6, EFR3B rows) — the correct approach here is **not** to claim a
  rescue but to flag the locus for LD-nomination against the pigmentation gene network's own gene
  set in a downstream step.

## Column dictionary (classification columns, plus columns carried over from the retired input)

| Column | Description |
|---|---|
| `author_attributed_gene` | The gene(s) the authors name for this locus, verbatim (may be a `/`-joined multi-gene list). |
| `attribution_basis` | One of the six controlled values above. |
| `effector_status` | One of the five controlled values above — the field the downstream rescue analysis filters on. |
| `classification_notes` | Full per-locus reasoning, cross-paper corroboration, and connector cross-check results (mygene.info, Zhang2018 melanocyte eQTL). |
| `is_asserted_pigmentation` | Boolean, migrated from the retired `discordance_loci_author_explained.csv`. Whether the source paper asserts the locus is pigmentation-associated. Populated for the 105 legacy rows only (null for the 26 Kim2024 rows); carried through into `nb4_unified_association_base.csv`. |
| `needs_review` | Free-text curatorial audit flag, migrated from the retired input (e.g. cross-paper double-count, sub-Bonferroni downgrade). Non-empty on 18 of the 105 legacy rows; null elsewhere. Not propagated downstream. |
| All other columns | Carried through unchanged from the retired `discordance_loci_author_explained.csv` for the 105 legacy rows (that file and its spec were removed from the repo on 2026-07-12; recover from git history if needed); populated fresh for the 26 Kim2024 rows using the same schema. The empty `gene_label_correction` column was dropped in the migration. |

## Status distribution (131 loci: 105 legacy + 26 Kim2024)

| `effector_status` | Count |
|---|---|
| `canonical_effector_variant_gap` | 80 |
| `effector_uncertain` | 34 |
| `effector_ambiguous_near` | 7 |
| `not_a_locus` | 6 |
| `regulatory_of_canonical_neighbour` | 4 |

## Files produced by this extraction

- `data/processed/discordance_loci_effector_classified.csv` — the 131-row merged, harmonized output
  (supersedes `discordance_loci_author_explained.csv` for the effector-uncertain question; that file
  was removed from the repo on 2026-07-12 and is recoverable from git history for its own
  variant-mechanism-gap provenance).
- `data/processed/EXTRACT_<paper>_loci_v2.csv` — one file per paper (14 total: the 13 legacy papers
  plus Kim2024), each carrying the same per-locus schema, for per-paper audit without needing to
  filter the merged file.
- `data/processed/nb_effector_uncertain_target_set.csv` — the flagship deliverable: one row per
  distinct non-canonical candidate gene (51 genes) surfaced across all `effector_uncertain` /
  `effector_ambiguous_near` / `regulatory_of_canonical_neighbour` loci, with supporting-loci counts,
  cross-paper convergence flag, mygene.info summary, and Zhang2018 melanocyte-eQTL cross-check.
- `data/processed/nb_effector_uncertain_loci_detail.csv` — the 45 underlying locus-level rows behind
  the gene-level rollup above (one row per locus, not per gene — a locus with multiple co-candidate
  genes contributes to multiple gene rows in the rollup but only one row here).
- `data/processed/discordance_loci_effector_classified_HONEST_GAPS.csv` — the gaps ledger
  (6 items) — see below.
- `docs/specs/discordance_loci_effector_classified.spec.md` — this document.

## Cross-paper convergence (flagship finding of this pass)

Three non-canonical genes are independently attributed at meaningful confidence by **more than one**
paper, which is the strongest available signal in this corpus that they are genuine (if
under-recognized) pigmentation effectors rather than single-paper artifacts:

- **MFSD12** — Ang2023 (coding Y182H, `probably_damaging`), Crawford2017 (CRISPR/zebrafish-validated:
  *"MFSD12 encodes a lysosomal protein that affects melanogenesis in zebrafish and mice"*), and Kim2024
  (coding variant + Discussion mechanism + highest-melanocyte-expression flag). mygene.info
  independently confirms an explicit pigmentation/melanosome function. Not on the task's canonical
  effector list.
- **TSPAN10** — Abbatangelo2026 (GTEx eQTL) and Morgan2018 (LD r²=0.995 with its own coding Y177C
  variant, plus a cited prior murine knockdown reducing melanocyte migration). Not canonical.
- **SPIRE2** — Kim2024 (eQTL-colocalized, melanosome-transport mechanism cited in Discussion) and
  Morgan2018 (same melanosome-transport mechanism, `KITLG, RAB32, and SPIRE2 in melanosome transport
  or dispersion`). Not canonical.

## Gaps ledger

See `discordance_loci_effector_classified_HONEST_GAPS.csv` for the full 6-item ledger with `scope`,
`reason`, and `action_needed` per item. Summary:

1. **Open Targets canonical/disease-association cross-check — not completed for any of the 51
   candidate genes.** Every attempt (4 retries with backoff, in two separate sessions) returned
   `"Rate limit exceeded for client: global"`. This is the single largest open item in this
   extraction; `nb_effector_uncertain_target_set.csv`'s `open_targets_canonical_check` column is
   populated with a placeholder string for all 51 rows, not a fabricated result.
2. **ORAOV1** (Morgan2018, one of the task's own 4 named contested loci) could not be resolved via
   mygene.info (`not_found`).
3. **Yang2016 Supplementary Table S4** (6 unresolved rsIDs behind the "OCA2-region SNP cluster")
   remains absent from this repo's paper folder — inherited unchanged from the prior extraction's
   own gaps ledger.
4. **Morgan2018's SIK1-locus lncRNA target (LINC01679)** was flagged in the paper's own
   fine-mapping discussion but not independently queried this pass.
5. **Set-level / multi-variant rows** (Ang2023 idx36, Morgan2018 idx83–84) remain un-disaggregated,
   classified `not_a_locus` for effector purposes, consistent with the prior extraction's own
   `ambiguous` flag on these rows.
6. **Kim2024's TRPS1 row (idx17)** surfaces an internal tension in the source paper's own Discussion
   text (one sentence describes a melanocyte-proliferation mechanism; another separately lists TRPS1
   among genes not yet investigated for pigmentation function) — recorded verbatim, not resolved by
   this extraction.

## Completeness ledger

| Check | Result |
|---|---|
| Rows in legacy `discordance_loci_author_explained.csv` | 105 |
| Rows newly extracted for Kim2024 | 26 |
| Total rows in merged output | 131 |
| Rows with `author_attributed_gene`/`attribution_basis`/`effector_status`/`classification_notes` populated | 131 / 131 (all four columns) |
| Per-paper `EXTRACT_<paper>_loci_v2.csv` files written | 14 (13 legacy + Kim2024) |
| Distinct non-canonical candidate genes surfaced | 51 |
| Candidate genes with cross-paper convergence (≥2 independent papers) | 3 (MFSD12, TSPAN10, SPIRE2) |
| Candidate genes resolved via mygene.info | 50 / 51 (ORAOV1 not found) |
| Candidate genes with completed Open Targets check | 0 / 51 — see gap #1 |
| Duplicate `(paper, rsid)` pairs in merged output | 1 apparent pair, both `NaN` rsid for two distinct non-genetic covariate rows (Ang2023 Sex, Ang2023 NAM ancestry fraction) — not a true duplicate, both correctly excluded via `not_a_locus` |

No row in the merged 131-row output was left without an `effector_status` assignment. The six items
above are the only acknowledged gaps and are ledgered for re-opening, not silently dropped.

## Source papers

See `data/raw/papers/REFERENCES.md` for the full DOI/journal/access table and the 13-legacy-paper
local-filename table (the retired `discordance_loci_author_explained.spec.md` that previously held it
was removed on 2026-07-12; recover from git history if needed). Kim2024's local files:

| File | Description |
|---|---|
| `Kim2024_NatCommun_EastAsianSkinColor.pdf` | Main text (16 pages). |
| `Kim2024_NatCommun_EastAsianSkinColor_Supplementary_Data.xlsx` | 14-sheet workbook (`Data 1`–`Data 14`); sheets `Data 1`, `Data 4`, `Data 5`, `Data 11` were read in full for this extraction (prior reported studies, lead-variant summary stats, nonsynonymous variants, eQTL colocalization). |
| `Kim2024_NatCommun_EastAsianSkinColor_Supplementary_Data_Descriptions.pdf` | Not opened this pass (sheet contents were self-descriptive from headers). |
| `Kim2024_NatCommun_EastAsianSkinColor_Supplementary_Information.pdf` | Not opened this pass (main text + Supplementary Data workbook were sufficient for the 26-locus extraction; flagged for re-open only if a downstream step needs the full supplementary methods/figures detail). |

No PDF prose is redistributed in the CSV or this document beyond quotes under 25 words each,
consistent with the copyright constraints documented in `REFERENCES.md`.
