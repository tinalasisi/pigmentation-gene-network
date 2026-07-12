# Primary-source papers — references, not redistributed

Full-text articles for the subscription / non-redistributable sources are **deliberately not committed to
this repository**. They are cited here by DOI/PMID so a rebuilder can obtain the identical article from the
publisher. Only openly-licensed material is committed (see the redistribution policy in `DATA_SOURCES.md`).

| Source | Full text | Supplements in repo | DOI / PMID | License of the article text |
|---|---|---|---|---|
| **Raghunath et al. 2015**, *BMC Res Notes* | data tables committed — MOESM1–5 (`data/raw/raghunath2015/`). Article PDF not stored here; open-access at the DOI (CC BY 4.0, redistribution permitted) if a local copy is wanted. | MOESM1–5 (`data/raw/raghunath2015/`) | 10.1186/s13104-015-1128-6 | **CC BY 4.0** (open access — redistribution permitted) |
| **Bajpai et al. 2023**, *Science* | **not redistributed** — obtain from publisher | Table S1 (`data/raw/bajpai2023/science.ade6289_table_s1.xlsx`) | 10.1126/science.ade6289 · PMC10901463 | © 2023 The Authors, exclusive licensee AAAS; CC BY 4.0 covers the author-accepted manuscript (PMC), not the typeset article. Table S1 kept as a factual data table (owner-authorized); typeset PDF/text NOT committed |
| **Baxter et al. 2018/2019**, *Pigment Cell Melanoma Res* | **not redistributed** — obtain from publisher | **none committed** — Table S7 withheld (see stanza below) | 10.1111/pcmr.12743 · PMID 30339321 | Wiley subscription — article text AND SI tables NOT redistributable (no open-license copy) |
| **Chaitanya et al. 2018** (HIrisPlex-S), *Forensic Sci Int Genet* | **not redistributed** — obtain from publisher | Erasmus MC Webtool Manual v2 (`data/raw/hirisplexs2018/`) | 10.1016/j.fsigen.2018.04.004 | Elsevier subscription — article text NOT redistributable |
| **Walsh et al. 2017** (HIrisPlex-S skin model), *Hum Genet* | **not redistributed** — obtain from publisher | — | 10.1007/s00439-017-1808-5 | Springer subscription |
| **Kim et al. 2024**, *Nat Commun* | full-text in `data/raw/papers/Kim2024_NatCommun_EastAsianSkinColor/` — withheld by the `data/raw/papers/*` rule (article-PDF convention, not a license bar) | article + SI + Supplementary Data (26 lead variants, worldwide allele freqs, GWAS×eQTL coloc) | 10.1038/s41467-024-49031-4 · PMID 38849341 | **CC BY 4.0** (open access — redistributable) |
| **Zhang et al. 2018**, *Genome Res* | full-text in `data/raw/papers/Zhang2018_GenomeRes_MelanocyteEQTL/` — withheld by the blanket rule | article + Supplementary Material + Supplementary Tables (melanocyte cis-eQTL); full stats are dbGaP-controlled | 10.1101/gr.233304.117 · PMID to confirm | **CC BY-NC 4.0** (redistributable non-commercially) |
| **Martin et al. 2017**, *Cell* | **not redistributed** — obtain from publisher | article PDF + Supplementary PDF + Table S6 `.xlsx`, in `data/raw/papers/Martin2017_Cell_AfricanSkinPigmentation/`; extracted loci committed at `data/processed/EXTRACT_Martin2017_loci.csv` | 10.1016/j.cell.2017.11.015 | Elsevier/Cell Press subscription — article text NOT redistributable |
| **Nadeau, Burke & Mundy 2007**, *Proc R Soc B* | **not redistributed** — obtain from publisher; PDF + supplements S04–S08 on disk in `data/raw/papers/Nadeau2007_ProcRSocB_MC1R_dichromatism/`, withheld by the blanket rule above | none committed (PDF-derived methods memo instead, see below) | 10.1098/rspb.2007.0174 · PMC2270924 · PMID 17504743 | Royal Society — article text NOT redistributable |

## Validation-case papers (13 genotype→phenotype-discordance papers) — FILES withheld, science used freely

These 13 papers are the empirical case base for the discordance finding. Each was supplied by the PI in a
per-paper subfolder under `data/raw/papers/<folder tag>/` containing the publisher PDF, any machine-readable
supplements, and (for open-access papers) a PubMed-Central text capture. **The copyrighted files are not
redistributed**; our own extracted records are committed under `data/case_records/EXTRACT_*_records.csv` and
carry every genetic fact the build consumes. **No notebook reads these paper files** — the repo rebuilds from
the committed EXTRACT records (see `docs/NB3_case_assembly_provenance.md` §8); the papers are needed only to
manually verify a record against the typeset source. DOIs below were read from
`data/processed/discordance_case_classification.csv`; journal / access status from the collection's
`DOWNLOAD_MANIFEST.md`.

| Folder tag (expected path `data/raw/papers/<tag>/`) | DOI | Journal | Year | Access | Phenotype system |
|---|---|---|---|---|---|
| Abbatangelo2026_SciRep_eyecolour_discordance | 10.1038/s41598-026-44580-8 | Sci Rep | 2026 | OA (CC-BY) | eye colour |
| Ang2023_eLife_Kalinago | 10.7554/eLife.77514 | eLife | 2023 | OA (CC-BY) | skin (albinism/hypopig) |
| Crawford2017_Science_AfricanPigmentation | 10.1126/science.aan8433 | Science | 2017 | Author manuscript free via PMC (publisher paywalled) | skin |
| Kastelic2013_CroatMedJ_IrisPlex | 10.3325/cmj.2013.54.381 | Croat Med J | 2013 | OA | eye colour |
| Kenny2012_Science_TYRP1 | 10.1126/science.1217849 | Science | 2012 | Author manuscript free via PMC (publisher paywalled) | hair (blond) |
| Meyer2020_PLoSONE_GGbrowneyes | 10.1371/journal.pone.0239131 | PLoS ONE | 2020 | OA (CC-BY) | eye colour |
| Morell1997_JMedGenet_Waardenburg | 10.1136/jmg.34.6.447 | J Med Genet | 1997 | Free via PMC (abstract-only capture) | syndromic (Waardenburg) |
| Morgan2018_NatCommun_HairColour_MC1R | 10.1038/s41467-018-07691-z | Nat Commun | 2018 | OA (CC-BY) | hair (red) |
| Norton2014_AJPA_MelanesianBlond_TYRP1 | 10.1002/ajpa.22466 | Am J Phys Anthropol | 2014 | **Paywalled, no OA copy** — institutional proxy / ILL / author request | hair (blond) |
| Norton2016_AJHB_Bougainville_TYRP1 | 10.1002/ajhb.22795 | Am J Hum Biol | 2016 | **Paywalled, no OA copy** — institutional proxy / ILL / author request | hair (blond) |
| Pospiech2016_IntJLegalMed_IrisPlex_population | 10.1007/s00414-016-1388-2 | Int J Legal Med | 2016 | Free via PMC | eye colour |
| Salvo2023_Genes_AAAGblueeyes | 10.3390/genes14030698 | Genes (Basel) | 2023 | OA (CC-BY) | eye colour |
| Yang2016_MBE_OCA2_EastAsian | 10.1093/molbev/msw003 | Mol Biol Evol | 2016 | OA | skin |

**Exact-filename note.** The build reads none of these paper files, so no single PDF filename is load-bearing.
Save each re-obtained file under its per-paper folder `data/raw/papers/<folder tag>/` (the tag matches the
`EXTRACT_<tag>_records.csv` name in `data/case_records/`). The two **Norton** papers (Wiley) have no
open-access copy and must be obtained via institutional proxy, interlibrary loan, or author request.

## How to re-obtain the non-redistributed texts
Each is reachable at its DOI above. The processing this build performed on those texts (marker parsing,
hit-threshold calls, symbol filters) is fully specified in `docs/specs/`, so the derived tables in
`data/processed/` can be reproduced from the publisher's copy without the text being present here.

## What IS committed and why it's allowed
- **Raghunath 2015 MOESM1–5** — the article is CC BY 4.0, so the supplementary data tables are
  redistributable with attribution.
- **Bajpai Table S1** — the *Science* article is © 2023 The Authors, exclusive licensee AAAS ("some rights
  reserved"); CC BY 4.0 applies to the author-accepted manuscript (PMC10901463) under HHMI policy, not to
  the publisher's typeset article/supplement. Table S1 is committed as a factual gene-screen data table
  (data, not copyrightable expression), with the project owner's authorization and attribution to Bajpai
  et al.; the typeset article PDF/text is not committed.
- **Bajpai Table S1** is committed on a stronger basis than "facts aren't copyrightable": the identical
  table is a supplementary file of the article's **CC BY 4.0** deposit in PMC (PMC10901463,
  `license_ref = ccbylicense`), so the data is redistributable with attribution to Bajpai et al.

### Baxter et al. 2018 — Table S7 — NOT redistributed (Wiley subscription copyright)
- Obtain via DOI: 10.1111/pcmr.12743 (PMID 30339321) — Supporting Information, Table S7.
- What it is: the "650 Pigmentation Genes" curated cross-species compilation (Ensembl IDs, human/mouse/
  zebrafish symbols, ortholog flag, pigment-phenotype location, GO/OMIM/MGI/ZFIN evidence flags, PubMed).
- Save as: `data/raw/baxter2018/pcmr12743-sup-0007-tables7.xlsx`  (Notebook 01b expects this exact name).
- Why withheld: the article is a Wiley Version of Record (Crossref license = VOR terms only) and has **no
  open-access copy** — PMC record PMC10413850 returns `idIsNotOpenAccess`, and the SI tables are not in the
  PMC OA subset. A curated gene list also carries potential compilation copyright in its selection and
  arrangement, so the "factual data" argument is not a redistribution grant. The **derived** table
  `data/processed/baxter2018_650_pigmentation_genes.csv` (produced by Notebook 01b) remains committed;
  it reproduces from the publisher's copy once re-obtained.
- **HIrisPlex-S Erasmus MC Webtool Manual v2 (2018)** — the prediction model + web tool are free to use;
  the manual documents the model's training-set composition (the population-provenance evidence this build
  cites). The Chaitanya paper text is not committed.

### Nadeau, Burke & Mundy 2007 — the comparative-genomics anchor reference
- Obtain via DOI: 10.1098/rspb.2007.0174 (PMC2270924, PMID 17504743) — Royal Society, subscription.
- What it is: the direct precedent for the primate pigmentation-vs-hormone selection analysis in
  `comparative-genomics/`. Galliform birds; dN/dS (PAML branch models) at 6 loci (MC1R, TYR, TYRP1, DCT,
  AGRP + CYTB mitochondrial control) regressed on a 0–6 sexual-plumage-dichromatism score via Pagel's GLS
  (CONTINUOUS). Signal specific to MC1R (genus-level LRS=8.5, p=0.004); none at the other five loci.
- Full-text article and supplements (S04 taxa/data tables, S05 table, S06/S08 figures, S07 methods text)
  are on disk in `data/raw/papers/Nadeau2007_ProcRSocB_MC1R_dichromatism/`, withheld by the blanket
  `data/raw/papers/*` rule (article-PDF convention, not a license bar — same treatment as Kim2024/Martin2017).
- **Derived methods memo committed:** `comparative-genomics/docs/BIRD_ANCHOR_REFERENCE.md` — verified
  against the full PDF (not search snippets), states exactly what's confirmed, maps their 6 loci onto our
  panel (MC1R/TYR/TYRP1/DCT overlap directly), and lays out how the primate analysis reproduces then
  extends their test (RELAX/aBSREL/RERconverge/SUMSTAT + the hormone-network contrast, none of which
  existed in 2007).
