# Traceability audit: what "case gene" hides, and what "resolution" actually measures

_Created 2026-07-11 by Claude Code (main session, model claude-opus-4-8). This is an **audit document written
to be fact-checked**. It changes no committed data and no framing docs. Every claim below names the exact file
(and line, where stable) it rests on, and §1 gives a future Claude the commands to re-verify each one. It
documents both (a) what this session did, and (b) the specific mistakes it found in prior Claudes' work — with
sources — so nothing here has to be taken on trust._

> **Scope / concurrency:** documents only committed data + the two network notebooks. Does **not** touch the
> in-flight resolution-engine work (`internal/handoffs/HANDOFF_ANY_TO_ANY_resolution_engine_plan.md`). §7 is a
> guardrail *for* that engine.

---

## 0. The two findings in one paragraph each

**Finding 1 — the unit of analysis silently changes resolution.** The 13 papers reported **loci / statistical
associations** (rsIDs, coordinates, effect sizes, p-values) — and in some cases only **genomic segments**
(shared haplotype blocks). Those are preserved in `data/case_records/EXTRACT_*.csv`. But the analysis layer
(`data/processed/case_gene_coverage_master.csv`, built by `notebooks/04_darcy_coverage_finding.ipynb`) is
**keyed on a bare gene symbol and drops every locus-level column**. Once you are at that layer, a validated
causal gene (OCA2) and a non-causal passenger gene sitting inside an albino haplotype (EMCN) are
indistinguishable — both are "a gene with a `coverage_tier`." The pipeline then makes gene-level claims about
entries whose raw finding was never gene-level. **You raised this; it is correct, and §3 shows exactly where
the information is lost.**

**Finding 2 — "coverage" and "resolution" are two different axes reported as one number.** `coverage_tier`
(which of the three source layers already contains the gene) is pure set membership; `resolution_class`
(chasing a SNP to a cited functional target) is analytical work. The scratchpad script `pilot_rate.py` runs
the second over genes classified by the first and reports a single "59% resolved / 86% characterized" rate —
counting 7 genes that were **already in D'Arcy** as if they were engine discoveries. §5 gives the corrected
reading.

**Finding 3 — the layer *labels* are misleading, and the backbone was never expanded (see the full issues
register in `internal/handoffs/HANDOFF_CRITICAL_limitations_and_framing_issues.md`).** Three framing errors sit
on top of the data problems above and are BLOCKING for any external claim:
- **"Mechanistic" vs "Association-recoverable"** names the strata by evidence *type*, but what separates them is
  only *which curated source lists the gene*. Layer 2 is **D'Arcy S1 = an OMIM Mendelian disease-gene table**,
  not association data — "association-recoverable" wrongly reads as GWAS (and the only association/predicted
  data in D'Arcy, the STRING PPI, is the part the project deliberately *bars*). Rename by source, not evidence
  type.
- **"Dark matter"** means "absent from two small curated lists," not "biologically unexplained" — MFSD12 has a
  *Science* mechanism paper yet is called dark. It conflates *absence from a reference list* with *absence from
  knowledge*.
- **The backbone is a single 2015 paper (Raghunath).** KEGG, Reactome, and OmniPath-curated mechanism were
  available and **not incorporated** (OmniPath = validation only; KEGG = scope cross-check; Reactome = never
  used). So the 29/23/48% three-strata split measures **how small the chosen backbone is**, not the trait's
  architecture. It cannot be reported as a finding until the backbone is expanded (curated mechanism only;
  predicted/STRING edges still barred) and the split re-derived.

**And the extractions must be redone (Finding 1's root cause).** The gene-first schema *forced* low-quality,
ill-fitting records — segments, SNP clusters, nulls, marker-only papers all coerced into single-gene rows. A
locus-first re-extraction is a prerequisite for every coverage/resolution number, not an optional cleanup. See
the handoff doc §B1.

---

## 1. How to fact-check this document (for a future Claude)

Run these from the repo root. Each maps to a claim below.

| Claim | Command to verify |
|---|---|
| Extracts preserve locus-level truth; schema is gene-first | `for f in data/case_records/EXTRACT_*.csv; do head -1 "$f"; done` — every file leads with `gene`, but also carries `rsid`/`genomic_coord_build`/`effect_or_association` |
| 4 dark genes have NO rsID and are "not causal" passengers | `python3 -c "import csv;[print(r['gene'],'|rsid=',repr(r['rsid']),'|',r['effect_or_association']) for r in csv.DictReader(open('data/case_records/EXTRACT_Ang2023_eLife_Kalinago.csv')) if r['gene'] in {'EMCN','MANBA','SLC39A8','TACR3'}]"` |
| Coverage master drops all locus columns | `head -1 data/processed/case_gene_coverage_master.csv` — no `rsid`, no p-value, no effect column |
| SYT6 rsID re-derived ≠ paper's rsID | compare `grep SYT6 data/case_records/EXTRACT_Ang2023_eLife_Kalinago.csv` (rs115102845/rs185469828) vs `grep SYT6 data/processed/locus_resolution_table.csv` (rs183827287) |
| Internal contradiction in FINDINGS doc | read `internal/FINDINGS_darcy_coverage.md` lines 50–53 ("carries discordance signal … not peripheral") vs line 98 ("hitchhikers Ang itself excluded") |
| pilot_rate conflation | the script buckets `resolution_class` over all 22 rows incl. the 7 `darcy_recoverable`; see §5 |
| Kastelic contributed 0 genes | `head -1 data/case_records/EXTRACT_Kastelic2013_CroatMedJ_IrisPlex_records.csv` — no `gene` column; per-individual rsID predictions only |

Everything else is a Read of the named file.

---

## 2. Where the genes come from (the extraction layer)

**The papers were extracted into `data/case_records/EXTRACT_<paper>.csv`, one row per record.** The schemas
(verified 2026-07-11 by reading all 13 headers) fall into two shapes:

- **Gene-first record files** (Abbatangelo, Ang, Crawford, Kenny, Meyer, Morell, Morgan, Norton×2, Pospiech,
  Salvo, Yang): first column is `gene`, followed by locus detail — `variant_protein`, `variant_cdna`,
  `genomic_coord_build`, `rsid`, `effect_or_association`, and (in several) a `gene_assignment` +
  `extraction_method` column recording *how* the gene label was attached.
- **No-gene files**: `EXTRACT_Kastelic2013_*.csv` has **no `gene` column at all** — it is per-individual eye
  colour with marker rsIDs as columns (`rs16891982`, `rs12203592`, …). This is the documented "Kastelic
  extracted 0 gene symbols" case. `EXTRACT_Norton2016_*.csv` is per-population allele frequencies for a single
  variant (`rs387907171_T_freq`).

**Key point:** the extract layer *does* retain the locus-level truth. The loss happens downstream. So the raw
information is still traceable today — it was simply not carried into the gene-keyed analysis tables.

**Fair attribution — what the extraction did right:** it faithfully transcribed each paper's own caveats into
`effect_or_association` and `note` (including "not causal", "does NOT warrant further investigation", and MAF
warnings — quoted verbatim in §3). The problem is not the extract; it is that the analysis layer ignored those
fields.

---

## 3. Finding 1 in detail — three lossy conversions from locus → "gene"

All quotes below are verbatim from `data/case_records/EXTRACT_Ang2023_eLife_Kalinago.csv` (53 records; Ang 2023
supplies 7 of the 15 dark genes). Ang 2023 is the clearest case, but the pattern generalizes to any
nearest-gene-labelled GWAS row.

### 3a. Segment → genes (EMCN, MANBA, SLC39A8, TACR3) — the manufactured-gene case
These four rows have **`rsid` = empty**. Their `source_table` = **"Appendix 1-table 4B"**. Their
`effect_or_association` is, verbatim:

> "albinism-candidate co-segregating with OCA2 albino haplotype (~1.7 Mb shared homozygous segment); **not
> causal**"

and `note`: "Non-coding/synonymous; within/near ~1.7-11 Mb African-origin albino haplotype".

**What the paper actually found here was a *segment*** — a ~1.7–11 Mb block that is homozygous-by-descent in
one albino individual and carries the real OCA2 causal variant. EMCN/MANBA/SLC39A8/TACR3 are genes that happen
to lie inside that block. Ang 2023 lists them **in order to exclude them**. Our pipeline transcribed them
correctly (with the "not causal" note), but the coverage layer then promoted them to **case genes** and, worse,
to genes that "carry discordance signal" (§3d). A segment is not a set of gene-level findings; treating its
passengers as genes is the exact error you flagged.

### 3b. SNP-cluster → nearest-gene label (SYT6, KALRN)
These carry real rsIDs and real association stats (SYT6 `P_adj=1.24E-07`; KALRN `P_adj=1.78E-06`), but the
`note` records a second collapse, verbatim:

> "SYT6 locus = ~20 SNPs w/ identical stats collapsed to representatives"

and, for both: the authors say it "does NOT warrant further investigation" (MAF < 2%, "inconsistent with an
AFR/NAM-differentiating causal variant"). So a **cluster of ~20 SNPs** was collapsed to a representative rsID
and then labelled by its **nearest gene**. "SYT6" is a positional label on a SNP cluster the authors themselves
set aside — not an assertion that the *gene* SYT6 does anything.

### 3c. Null retest carried as a gene (ATRN)
`effect_or_association` = "BETA_a(linreg,10PC)=0.85 MI; **P_adj=0.1395 (NOT significant)**"; `note` = "Previously
reported pigmentation variant; ref: Quillen 2012 … interpreted as not warranting follow-up". ATRN is a
**non-significant retest** of an old candidate, carried into the case set as a gene.

### 3d. Where the loss becomes irreversible, and the resulting overclaim
`notebooks/04_darcy_coverage_finding.ipynb` builds `case_gene_coverage_master.csv`, whose header is:

`gene,entrez,ensembl,in_nb2_network,in_darcy_union,in_darcy_S1,darcy_s1_phenotype_class,coverage_tier,case_papers,case_discordance_direction`

**No `rsid`, no p-value, no effect, no "not causal" flag.** At this layer EMCN is just
`EMCN,…,dark_matter,Ang2023_eLife_Kalinago,both`. The `case_discordance_direction = both` label is **inherited
at the paper level** (EMCN's only source is Ang 2023, a "both" paper) — it is *not* gene-specific evidence, and
it directly contradicts the extract's "not causal".

That inherited label then drives an overclaim. `internal/FINDINGS_darcy_coverage.md` lines 50–53 states:

> "Every one of these genes is cited by at least one case paper as carrying a discordance direction … so this
> is **not a set of peripheral genes** — it is the set that **carries discordance signal in the literature**…"

For the four §3a passengers this is false — they are exactly peripheral genes; the paper excluded them. The
**same document contradicts itself** at line 98, which correctly calls them "the chr4 hitchhikers Ang itself
excluded." Both sentences are in `FINDINGS_darcy_coverage.md`. The honest one (line 98) should govern; the
overclaim (lines 50–53) should be corrected.

### 3e. The rsID re-derivation seam (traceability break)
The dark stratum's rsIDs in `locus_resolution_table.csv` were **re-derived from GWAS Catalog by gene symbol**,
not carried forward from the extract. For SYT6 the two disagree:

| source | rsID | position |
|---|---|---|
| `EXTRACT_Ang2023…csv` (what the paper reported) | rs115102845 / rs185469828 | chr1:114619521 / chr1:114656630 (b37) |
| `locus_resolution_table.csv` (what we "resolved") | rs183827287 | chr1:114619521 (from GWAS Catalog GCST90269965) |

The position of one matches, but the resolver adjudicated a **different variant identifier from a different
study** than the paper the gene entered from. Nothing records the mapping "Ang's rs115102845 → the resolved
rs183827287", so the chain from *what the paper said* to *what we resolved* is implicit and, for this gene, not
reconstructable without redoing the lookup. KALRN (rs676091) does match across both, so this is a
per-gene seam, not a blanket break — which is exactly why it must be checked per gene, not assumed.

---

## 4. The three source layers and the databases (context for Finding 2)

| Layer | What / source | Membership column | On disk |
|---|---|---|---|
| **1. Raghunath (2015) backbone** — the 168-gene signed melanogenesis network. Identity via MyGene+UniProt; edges *validated* (never added) vs OmniPath+KEGG hsa04916. | mechanism | `in_nb2_network` | `gene_network_nodes.csv` (NB1→NB2) |
| **2. D'Arcy & Kiel (2023)** *Bioengineering*, PMC9854651, Table S1 = 243-gene OMIM disease-gene table. STRING edges (S4/S5) **barred** from backbone. | association | `in_darcy_union`, `in_darcy_S1` | `data/raw/darcy2023/Table S1…xlsx` |
| **3. 13 curated case papers** → 31 case genes (the §2 extracts). | literature | `case_papers` | `data/case_records/EXTRACT_*.csv` |

`coverage_tier` is derived purely from layer-1/2 membership: `in_network` (in Raghunath; 9) /
`darcy_recoverable` (not in Raghunath but in D'Arcy; 7) / `dark_matter` (in neither; 15).

**Databases used to *resolve* a locus (Axis B, §5), via the human-genetics connector, GRCh38:** GWAS Catalog
(`gwas_associations_for_variant/gene/trait`) for the association + nearest-gene label; eQTL Catalogue
(`eqtl_associations`) for the regulatory target — 5 datasets queried: GTEx skin sun-exposed **QTD000316**,
TwinsUK skin **QTD000544**, GTEx skin suprapubic **QTD000311**, GENCORD fibroblast **QTD000100**, GTEx
fibroblast **QTD000216**; mechanism literature via OpenAlex (DOI-verified); PMIDs verified via NCBI PubMed
`esummary`.

---

## 5. Finding 2 in detail — coverage vs. resolution, and the pilot_rate conflation

**Two axes; a rate is only meaningful within one.**
- **Axis A — coverage:** which layer already contains the gene. Set membership. Output `coverage_tier`.
- **Axis B — resolution:** for a gene *not in the backbone*, chase its SNP to a cited functional target. Output
  `resolution_class` ∈ {`resolves_to_in_network_gene`, `resolves_to_other_gene`, `genuinely_novel` (all
  "positive"); `no_pigmentation_GWAS_signal` ("cited-negative"); `no_regulatory_evidence_found` ("still-open")}.

`locus_resolution_table.csv` has Axis-B verdicts for **all 22 non-backbone genes = 7 `darcy_recoverable` + 15
`dark_matter`**. `pilot_rate.py` tallies `resolution_class` over all 22 and prints:

```
positive : 13/22 = 59%   |   characterized : 19/22 = 86%   |   still-open : 3/22 = 14%
```

**The 13 "positive" include the 7 `darcy_recoverable` genes — which were never dark; they were already in
D'Arcy.** Separating the axes gives the honest picture (the script prints this correct sub-number too, just
under the misleading headline):

| population | positive | cited-neg | still-open | characterized |
|---|---|---|---|---|
| 7 `darcy_recoverable` (already in D'Arcy — a **coverage** fact, not a resolution) | 7/7 | 0 | 0 | 7/7 |
| **15 `dark_matter`** (the engine's real scope) | **6/15 = 40%** | 6/15 | 3/15 | **12/15 = 80%** |

Only the dark-matter row is a resolution finding. The 7 D'Arcy genes belong in a coverage statement — which is
exactly how `DISCORDANCE_DECOMPOSITION_FINDING.md` and `FINDINGS_darcy_coverage.md` report them (9→16 of 31 =
29%→52%). The two are consistent **iff** the axes are kept apart; `pilot_rate.py`'s headline is the one place
they were merged.

The **falsified-hypothesis result is unaffected**: 0/15 dark genes carry `resolves_to_in_network_gene`
(`target_in_168_network = False` for all 15). The lone `resolves_to_in_network_gene` case is HERC2→OCA2, and
HERC2 is `darcy_recoverable`, not dark. That negative result is the asset — keep it out of the 7-gene
conflation.

---

## 6. Ledger — what prior Claudes got right vs. wrong (with sources)

| # | Item | Status | Source(s) |
|---|---|---|---|
| R1 | Extraction preserved locus-level truth + paper caveats verbatim | ✅ right | all `EXTRACT_*.csv`; quotes in §3 |
| R2 | Nearest-gene≠causal discipline applied (HERC2→OCA2 not added; routed to OCA2) | ✅ right | `README.md`; `HANDOFF_…resolution_engine_plan.md` rule 2 |
| R3 | Dark chr4 genes classified as LD-passenger / no-signal at the *resolution* stage | ✅ right | `dark_matter_ledger.csv`; `DISCORDANCE_DECOMPOSITION_FINDING.md` |
| R4 | "31 genes ≠ 13 papers"; Kastelic 0 genes; 3 TYRP1 papers → 1 gene | ✅ right | `FINDINGS_darcy_coverage.md` 103–107 |
| W1 | Analysis layer is gene-keyed; drops rsID/effect/p-value/"not causal" — locus truth not carried past extract | ❌ wrong | `case_gene_coverage_master.csv` header; `notebooks/04_darcy_coverage_finding.ipynb` |
| W2 | Passenger genes (EMCN/MANBA/SLC39A8/TACR3) promoted to "carries discordance signal, not peripheral" — contradicts the extract ("not causal") and the same doc's line 98 | ❌ wrong (internal contradiction) | `FINDINGS_darcy_coverage.md` 50–53 vs 98; extract §3a |
| W3 | Dark-stratum rsIDs re-derived from GWAS Catalog by gene symbol; SYT6 resolves a different variant than the paper reported; mapping not recorded | ⚠️ traceability seam | `locus_resolution_table.csv` vs extract; §3e |
| W4 | `pilot_rate.py` reports one "59%/86% resolved" rate mixing coverage (7 D'Arcy) with resolution (15 dark) | ❌ wrong (misleading headline) | scratchpad `pilot_rate.py`; §5 |

W1–W4 are **not yet corrected in committed files**; this document only records them. Correcting them is a
decision for the PI / the concurrent engine, not this audit.

---

## 7. Guardrails (for the resolution engine and any writeup)

1. **Carry the locus identity, not just the gene.** Any dark/resolution table should key on rsID (+ coord +
   build) and *retain* `effect_or_association` and the paper's own caveat, so "not causal passenger" cannot be
   silently re-read as "gene carrying discordance signal."
2. **Do not assert a dark entry "carries discordance signal" unless the evidence is gene/variant-specific.**
   Paper-level `both`/`mixed` labels inherited onto a passenger gene are not signal. Correct
   `FINDINGS_darcy_coverage.md` 50–53 to match its own line 98.
3. **Record the rsID mapping.** When a gene's variant is re-derived from GWAS Catalog, store both the paper's
   reported rsID and the resolved rsID, so the chain is auditable (§3e).
4. **Never mix Axis A and Axis B in one number.** Rate = over genuinely-dark genes only; state the denominator's
   provenance inline ("6 of 15 dark genes", not "59% of previously-unresolved loci").
5. **"positive `resolution_class`" ≠ discovery.** HERC2→OCA2 is positive but is applied discipline, not new
   biology.

---

## 8. Per-gene trace (all 31 case genes)

Axis A from `case_gene_coverage_master.csv`; Axis B from `locus_resolution_table.csv`. `NB2` = Raghunath
backbone. "raw unit" flags entries whose paper-level finding was **not** a gene-level association (§3).

### in_network — 9 (in Raghunath; no Axis-B question)
EGFR, KITLG, MC1R, OCA2, PAX3, POMC, PPP3CA, TYR, TYRP1 — all `in_nb2_network=True`.

### darcy_recoverable — 7 (already in D'Arcy — coverage, not a resolution)
| gene | NB2 | D'Arcy | resolution_class | target | citation |
|---|:-:|:-:|---|---|---|
| HERC2 | ✘ | ✔ | resolves_to_in_network_gene | OCA2 (in network) | PMID:22234890 (Visser 2012, 3C) |
| RALY | ✘ | ✔ | resolves_to_other_gene | ASIP | eQTL TwinsUK QTD000544 p=2.3e-16; Duffy 2018 |
| IRF4 | ✘ | ✔ | genuinely_novel | IRF4 self | PMID:24267888 (mechanism, not eQTL) |
| BNC2 | ✘ | ✔ | genuinely_novel | BNC2 self | Visser 2014 HMG |
| SLC24A5 | ✘ | ✔ | genuinely_novel | SLC24A5 self (coding) | PMID:16357253 (Lamason 2005) |
| SLC45A2 | ✘ | ✔ | genuinely_novel | SLC45A2 self (coding) | Graf 2005 |
| LRMDA | ✘ | ✔ | genuinely_novel | LRMDA self (rare LoF, OCA7) | PMID:23395477 |

### dark_matter — 15 (in neither layer)
| gene | resolution_class | bucket | raw unit (§3) | citation / caveat |
|---|---|---|---|---|
| MFSD12 | genuinely_novel | positive | GWAS variant | PMID:29025994 (Crawford 2017) |
| PKHD1 | genuinely_novel | positive | GWAS variant | eQTL TwinsUK p=3.0e-14 |
| SLC24A4 | genuinely_novel | positive | GWAS variant | Sulem 2007 |
| TSPAN10 | genuinely_novel | positive | GWAS variant | eQTL p<1e-300 |
| NPLOC4 | resolves_to_other_gene | positive | GWAS variant | eQTL → TSPAN10 |
| SIK1 | resolves_to_other_gene | positive | GWAS variant | eQTL → LINC01679 (ncRNA) |
| ATRN | no_pigmentation_GWAS_signal | cited-neg | **null retest P=0.14** (§3c) | Ang 2023; Quillen 2012 |
| EMCN | no_pigmentation_GWAS_signal | cited-neg | **segment passenger, no rsID, "not causal"** (§3a) | Ang 2023 Appendix 1-table 4B |
| LTO1 | no_pigmentation_GWAS_signal | cited-neg | no locus-level record found | Morgan 2018 candidate |
| MANBA | no_pigmentation_GWAS_signal | cited-neg | **segment passenger, no rsID, "not causal"** (§3a) | Ang 2023 Appendix 1-table 4B |
| SLC39A8 | no_pigmentation_GWAS_signal | cited-neg | **segment passenger, no rsID, "not causal"** (§3a) | Ang 2023 Appendix 1-table 4B |
| TACR3 | no_pigmentation_GWAS_signal | cited-neg | **segment passenger, no rsID, "not causal"** (§3a) | Ang 2023 Appendix 1-table 4B |
| KALRN | no_regulatory_evidence_found | still-open | **SNP-cluster → nearest gene** (§3b) | Ang 2023 (MAF<2%, set aside) |
| MSX2 | no_regulatory_evidence_found | still-open | GWAS variant | PMID:30531825 (Morgan 2018) |
| SYT6 | no_regulatory_evidence_found | still-open | **~20-SNP cluster; rsID re-derived (§3e)** | Ang 2023 (MAF<2%, set aside) |

**Read this table honestly:** of the 15 "dark genes," at least **4 are segment passengers the paper excluded**
(EMCN, MANBA, SLC39A8, TACR3), **1 is a null retest** (ATRN), and **2 are low-MAF SNP-clusters the authors set
aside** (KALRN, SYT6). Whether those belong in a "case gene" set at all is the open scientific question your
message raises — and it cannot be answered from the gene-keyed tables alone; it requires going back to the
`EXTRACT_*` locus records.

---

## 9. Caveats
1. Axes A (three-strata) and D1/D2 (direction) are **correlated**, not orthogonal (14/15 dark genes carry
   `both`); the `both` label is often paper-inherited, not gene-specific (§3d).
2. ORAOV1↔LTO1 is a one-gene enumeration edge case; this list is LTO1-inclusive (`project_dashboard.md` §3).
3. 13 papers ≠ 13 gene contributions (Kastelic 0 genes; 3 TYRP1 papers → 1 gene).

## Provenance
Extract schemas + verbatim quotes: `data/case_records/EXTRACT_*.csv` (read 2026-07-11). Coverage/dark tables:
`case_gene_coverage_master.csv`, `dark_matter_ledger.csv`, `locus_resolution_table.csv`. Build step:
`notebooks/04_darcy_coverage_finding.ipynb`. Prior-Claude claims audited: `FINDINGS_darcy_coverage.md`,
`DISCORDANCE_DECOMPOSITION_FINDING.md`, `FRAMING_EVALUATION_dark_matter.md`, `README.md`,
`HANDOFF_ANY_TO_ANY_resolution_engine_plan.md`. This document recomputes no numbers and edits no other file;
it separates axes and surfaces provenance already present (or missing) in those sources.
