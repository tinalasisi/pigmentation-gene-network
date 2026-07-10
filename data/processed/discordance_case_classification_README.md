# Discordance case classification — data dictionary

**File:** `discordance_case_classification.csv`
**Built:** 2026-07-09 · **Source:** 13 pigmentation genotype-phenotype-discordance papers supplied by the PI (`Reference_papers.zip`), each extracted from its **authoritative publisher PDF + machine-readable supplements** by the GENETICS_DATA_EXTRACTOR specialist (one agent per paper). This table is the consolidated top-level index; every row links to that paper's full `EXTRACT_<paper>.md` (per-record detail with per-field provenance) and, where present, `EXTRACT_<paper>_records.csv`.

This table is the validation-case index for the bidirectional genotype-phenotype discordance finding. It is **citation-only**: the papers' data records are cited, the copyrighted paper files are withheld from the repo (see `data/raw/papers/REFERENCES.md`).

## What each column means

| Column | Meaning |
|--------|---------|
| `paper` | Paper identifier = folder name in `Reference_papers/`, form `AuthorYYYY_Journal_tag`. |
| `doi` | Digital Object Identifier, verbatim from the paper's entry in `Reference_papers/DOWNLOAD_MANIFEST.md` (the PI's own retrieval manifest). Complete DOIs only — no placeholders. |
| `phenotype_system` | Which pigmentation phenotype the discordance concerns (skin / hair / eye colour / syndromic). |
| `discordance_direction` | The core classification. **D1** = the person/group HAS the usual causal variant but does NOT show the expected phenotype (reduced/incomplete penetrance). **D2** = the phenotype is PRESENT but the usual causal variant is ABSENT (alternative/atypical genotype, different gene, compound-het, or single-allele). **both** = the paper documents cases in both directions (often at one locus, e.g. OCA2 in Ang 2023). |
| `anchor_genotypes` | The specific genotype(s) that establish the discordance — gene, protein/cDNA change, rsID, and zygosity/genotype class where the paper reports them. This is the evidence, not a summary; full per-record genotypes are in the paper's `EXTRACT_*_records.csv`. |
| `mechanism_summary` | One-line statement of how the discordance arises, with the direction label(s) in parentheses. |
| `n_records_extracted` | Number of rows in this paper's canonical committed `EXTRACT_*_records.csv` — recomputed from the committed file, not frozen at classification time. Reflects extraction depth, not importance. |
| `record_grain` | What the count represents for this paper (e.g. "discordance records" vs "full 211-variant panel screened" vs "per-individual genotypes"). Grain differs by study design, so counts are not directly comparable across papers. |
| `records_csv_version` | 8-char version prefix of the canonical `EXTRACT_*_records.csv` the count was read from (the authoritative file where a paper has more than one in the store). |
| `extract_artifact` | Filename of the per-paper detailed extract (`EXTRACT_<paper>.md`) — open it for the full records table, direction evidence quotes, and per-field provenance/completeness ledger. |

## Direction tally (13 papers)
- **D1 only** (3): Morell 1997 (Waardenburg WS1/PAX3), Kastelic 2013 (IrisPlex reduced penetrance), Pospiech 2016 (IrisPlex reduced penetrance; source states "Not D2").
- **D2 only** (5): Yang 2016, Kenny 2012, Norton 2016, Meyer 2020, Salvo 2023.
- **both** (5): Ang 2023, Norton 2014, Crawford 2017, Morgan 2018, Abbatangelo 2026.

Total genetic records across all papers (sum of canonical committed `EXTRACT_*_records.csv` row counts): **694**, reproducible from the committed files. (An earlier headline of 511 was a count frozen at classification time that no longer matched the committed CSVs; it has been retired in favour of the reproducible 694. Note that the grain differs by paper — see `record_grain` — so the total is a sum of differently-scoped record sets, not a single comparable quantity.)

**Canonical-file policy.** Where a paper has more than one record CSV in the artifact store (md-era vs PDF-era, or a `_records`/`_stats`/`_gwas_leads` split), the file named in `records_csv_version` is canonical; the others are superseded/auxiliary and are not counted. Bulk full-panel tables (e.g. Morgan 2018 `_gwas_leads` = 309 GWAS lead variants) are kept as separate files, not folded into the discordance-record count.

## Provenance notes
- Every direction call traces to a quoted sentence or named table row inside the paper's `EXTRACT_*.md` (the specialist records the evidence verbatim).
- Extraction source is the **PDF** (pages read as typeset images where tables/genotypes render only in layout) plus machine-readable `.xlsx`/`.docx` supplements — never a lossy text capture.
- Morell 1997: the automated PMC text capture was abstract-only (PMC holds scanned page images), but extraction used the **full publisher PDF** the PI supplied.
- Norton 2014 / Norton 2016: paywalled with no open-access text; extraction used the PI-supplied PDF in full. Paywalled status restricts only file redistribution, never the scientific extraction.
