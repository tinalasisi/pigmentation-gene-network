# HANDOFF — Critical limitations, framing errors, and required remediations

_From: Claude Code (main session, claude-opus-4-8), 2026-07-11. For: the PI and any Claude working the
findings/framing/resolution-engine tracks. **This is an exhaustive issues register, written to be acted on and
fact-checked.** It recomputes no numbers and edits no findings docs — it tells you what is wrong in them and
what to change. Companion: `internal/TRACEABILITY_coverage_and_resolution_logic.md` (the deep-dive with
verbatim evidence and reproduction commands). Do not treat any of the flagged claims as
publication-ready until the BLOCKING items are resolved._

## How to read this

Each issue has: **severity**, **what's wrong**, **evidence** (exact file/line/verbatim so you can check it),
**why it matters**, **fix**. Severity: 🔴 BLOCKING (a claim is wrong or misleading as written) · 🟠 MAJOR
(materially weakens the finding) · 🟡 MINOR (should be stated, not load-bearing).

Verify anything here with the appendix commands (§ Fact-check) or the companion doc's §1.

---

## Executive summary — the five things that must not ship as-is

1. **The stratum labels "Mechanistic" and "Association-recoverable" are scientifically misleading** (§A1). They
   impute an *evidence type* the sources don't have. D'Arcy S1 is an **OMIM Mendelian disease-gene** table, not
   association data — "association-recoverable" wrongly reads as GWAS.
2. **"Dark matter" overclaims** (§A2). It means "absent from two small curated lists," not "biologically
   unexplained." Several "dark" genes have strong published mechanism (e.g. MFSD12, *Science* 2017).
3. **The backbone was never actually expanded** (§A3). KEGG, Reactome, and OmniPath-curated mechanism were
   available and *not* incorporated (OmniPath used for validation only; KEGG for a scope cross-check; Reactome
   never touched). So the 29/23/48% three-strata split is an artifact of a **single-2015-paper backbone**, not
   a measurement of biology.
4. **The extractions must be redone** (§B1). A gene-first schema forced loci, haplotype segments, and SNP
   clusters into single-gene rows they don't fit, manufacturing "genes" the papers never asserted.
5. **The headline "resolution rate" conflates two different axes** (§C1) and double-counts genes already in
   D'Arcy as if newly resolved.

---

## A. Framing & terminology errors (highest priority — these are in the findings docs now)

### 🔴 A1. "Mechanistic" vs "Association-recoverable" is a false and misleading dichotomy
**What's wrong.** The three strata are named by *evidence type* — "Mechanistic" (layer 1) vs
"Association-recoverable" (layer 2) — but that is **not what separates the layers.** What separates them is
simply *which curated source lists the gene*:
- Layer 1 = the **Raghunath 2015** melanogenesis pathway model (one paper).
- Layer 2 = **D'Arcy & Kiel 2023 Table S1**, a **243-gene OMIM-backed *Mendelian disease-gene* table**.

Both are curated knowledge. Calling layer 2 "association-recoverable" is wrong twice over:
1. **It evokes GWAS / statistical association.** D'Arcy S1 is **OMIM** — Mendelian disease genes, many with
   established molecular mechanism (e.g. SLC45A2→OCA4, SLC24A5→OCA6 are causal coding-variant genes). Labeling
   curated Mendelian mechanism as "association" inverts the evidence hierarchy.
2. **The only association/predicted data in D'Arcy (the STRING PPI in S4/S5) is the part the project deliberately
   BARRED** (locked decision 5). So the "association" the label evokes isn't even used.

**Evidence.** `internal/DISCORDANCE_DECOMPOSITION_FINDING.md` lines 23–24, 28–29, 37–38 (stratum table + gene
lists); line 24 verbatim: *"absent from the network, present in the D'Arcy **OMIM-backed** disease-gene
compendium."* `internal/FINDINGS_darcy_coverage.md` lines 28–40. STRING bar: `DATA_SOURCES.md` entry 7;
`HANDOFF_ANY_TO_ANY_resolution_engine_plan.md` §2 (locked decision 5).

**Why it matters.** A reviewer who reads "association-recoverable" will assume a GWAS layer and mistrust the
whole decomposition. It also flattens the real, defensible distinction (curated pathway *model* vs curated
*disease-gene list*) into a fake mechanism-vs-association gradient.

**Fix.** Rename the strata by **source**, not evidence type. Proposed:
- Layer 1 → *"in the Raghunath melanogenesis model"* (or "curated pathway backbone").
- Layer 2 → *"in the OMIM/D'Arcy disease-gene set"* (or "curated Mendelian disease genes").
- Layer 3 → *"not in either reference set (yet)"* — see A2/A3.
State plainly that both layers are curated; they differ in **breadth and source format**, not evidence quality.

### 🔴 A2. "Dark matter" imputes ignorance the data doesn't support
**What's wrong.** "Dark" is defined operationally as *absent from the 168-gene backbone AND absent from D'Arcy
S1* — i.e. absent from **two specific, narrow lists.** The metaphor then imports the connotation "biologically
unexplained / mysterious," which is false for much of the set. MFSD12 has a *Science* mechanism paper
(Crawford 2017, PMID:29025994, melanosome/lysosome regulation); SLC24A4 is an established melanosomal cation
exchanger; TSPAN10/PKHD1 have dominant self-eQTLs. These are not dark; they are *not-in-our-two-lists.*

**Evidence.** Definition: `FINDINGS_darcy_coverage.md` lines 42–48. MFSD12 mechanism: `locus_resolution_table.csv`
(MFSD12 row) + `dark_matter_ledger.csv`. The `genuinely_novel` class itself (4 of the 15) means "correctly
labelled, mechanism/identity known, just missing from the lists" — which is the opposite of dark.

**Why it matters.** Naming a gene with a *Science* paper "dark matter" is the kind of overclaim a reviewer will
seize on. It also confuses two different things — *absence from a reference list* vs *absence from knowledge* —
which is the same category error as the coverage-vs-resolution conflation (§C1), one level up.

**Fix.** Drop "dark matter" as a knowledge claim. If a catchy term is needed, make it explicitly relative:
*"outside the current reference sets."* Report the residual as "genes our two curated sources don't yet cover,"
and separate (i) genes with known mechanism not yet curated into the graph from (ii) genes that are genuinely
uncharacterized. They are being lumped today.

### 🔴 A3. The backbone was never expanded — the strata sizes are an artifact of that choice
**What's wrong.** The "48% dark" figure rests on a backbone that is **one 2015 paper**, plus an association
layer that is **one 2023 OMIM table.** Standard curated mechanistic resources that would have *grown the
backbone* — **KEGG** (hsa04916 Melanogenesis), **Reactome**, and the **curated (non-predicted) subsets of
OmniPath** — were available and **not used for expansion**:
- **OmniPath**: used only for *"validation, NEVER silent addition"* (`DATA_SOURCES.md` line 213). 11 datasets,
  2,949 internal edges frozen — for *checking* backbone edges, not adding any.
- **KEGG hsa04916**: used only as a *"curated-pathway membership scope cross-check"* (`DATA_SOURCES.md`
  line 225 / entry 6d).
- **Reactome**: **never used** (no reference in any notebook or data file; only named aspirationally in
  `internal/EXPANSION_PLAN_sex_pigment_primate.md`).
- **HIrisPlex edges**: *"staged for a proposed enrichment step… not run in NB2"* (`DATA_SOURCES.md` lines 51,
  145–148).

The conservatism about *predicted* edges (barring STRING) is correct and should stay. But KEGG/Reactome/
OmniPath-curated edges are **literature-curated mechanism**, not predictions — they are exactly the kind of
edge the project's own "curated mechanism only" rule would admit, with PI gating. They were deferred, not
incorporated, and then genes outside the un-expanded backbone were declared "dark."

**Why it matters.** The three-strata percentages (Mechanistic 29% / +D'Arcy 52% / dark 48%,
`DISCORDANCE_DECOMPOSITION_FINDING.md` lines 22–33) are presented as a *measurement of the trait's
architecture.* They are actually a **measurement of how small the chosen backbone is.** Expand the backbone
with one more curated pathway DB and the numbers move materially — which means they cannot carry a scientific
claim in their current form.

**Fix (before any decomposition claim):**
1. Expand the backbone with KEGG hsa04916 + Reactome pigmentation/melanogenesis pathways + OmniPath curated
   edges, under the existing PI-gated, citation-required, predicted-edges-barred discipline.
2. Re-derive the strata **after** expansion, and report the split as *"relative to backbone version X (sources:
   …)"*, with a sensitivity line: how much does the residual shrink per added source.
3. If expansion is out of scope for this pass, **do not report 29/23/48 as a finding** — report it as
   "coverage of a deliberately minimal single-model backbone" and say expansion is pending.

---

## B. Unit-of-analysis & extraction defects (the extractions must be redone)

### 🔴 B1. Gene-first extraction forced non-gene findings into gene rows — re-extraction required
**What's wrong.** Every `EXTRACT_*.csv` schema **leads with a `gene` column**; the analysis unit is a gene
symbol. But the papers' actual findings are often **not gene-level**:
- **Haplotype segments** → passenger genes. Ang 2023's ~1.7–11 Mb shared albino segment became four
  gene rows (EMCN, MANBA, SLC39A8, TACR3) with **empty rsID** and `effect_or_association` = *"…~1.7 Mb shared
  homozygous segment); **not causal**."* The finding was a *segment*; we manufactured genes from it.
- **SNP clusters** → nearest-gene label. *"SYT6 locus = ~20 SNPs w/ identical stats collapsed to
  representatives"* (Ang 2023 extract note). "SYT6"/"KALRN" are positional labels on clusters the authors
  *"does NOT warrant further investigation."*
- **Null retests** → gene rows. ATRN: *"P_adj=0.1395 (NOT significant)."*
- **Marker-only / frequency-only papers** don't fit at all: Kastelic 2013 extracted **0 genes** (per-individual
  rsID predictions, no gene column); Norton 2016 is per-population allele frequencies for one variant.
- **Co-mapped multi-gene loci** → forced single assignment (NPLOC4/TSPAN10 share one locus).

**Evidence.** All headers: `for f in data/case_records/EXTRACT_*.csv; do head -1 "$f"; done`. Verbatim quotes:
`EXTRACT_Ang2023_eLife_Kalinago.csv` (EMCN/MANBA/SLC39A8/TACR3/SYT6/KALRN/ATRN rows). Kastelic: header of
`EXTRACT_Kastelic2013_CroatMedJ_IrisPlex_records.csv` (no `gene`).

**Why it matters.** The unit of analysis silently determines the result. A gene-keyed pipeline *cannot*
represent "a segment," "a cluster," or "a null" faithfully, so it coerces them into genes and then counts them
as genes. Every downstream number that uses "31 case genes" or "15 dark genes" as a denominator inherits this
distortion.

**Fix — re-extract locus-first.** Re-do the extraction with the **variant/locus** (rsID + coord + build, or a
region for segments) as the primary key, carrying `effect_or_association`, p-value/effect, MAF, and the
paper's own verdict (causal / passenger / not-significant / set-aside) as first-class fields. Derive a
gene annotation from the locus *with a recorded basis* (`nearest_gene`, `eQTL_target`, `coding`, `segment_member`),
never as the primary key. Genes then aggregate up from loci, not the reverse. This is a substantial re-do, and
it is a prerequisite for any credible coverage/resolution claim — flag it to the PI as such.

### 🟠 B2. The coverage layer discards all locus information (loss becomes irreversible)
**What's wrong.** `notebooks/04_darcy_coverage_finding.ipynb` builds `case_gene_coverage_master.csv`, whose
columns are `gene,entrez,ensembl,in_nb2_network,in_darcy_union,in_darcy_S1,darcy_s1_phenotype_class,
coverage_tier,case_papers,case_discordance_direction`. **No rsID, no effect, no p-value, no "not causal" flag.**
After this step EMCN (non-causal passenger) and OCA2 (validated causal) are the same kind of object.
**Fix.** Once B1 is done, coverage should be computed on the locus table and retain the locus key + the paper's
verdict, so provenance survives.

### 🔴 B3. Passenger genes are asserted to "carry discordance signal" — internal contradiction
**What's wrong.** `FINDINGS_darcy_coverage.md` lines 50–53: *"Every one of these genes is cited by at least one
case paper as carrying a discordance direction … so this is **not a set of peripheral genes** — it is the set
that **carries discordance signal in the literature**."* For the four §B1 segment passengers this is false, and
**the same document contradicts it at line 98**: *"the chr4 hitchhikers Ang itself excluded."* The
`case_discordance_direction=both` label is inherited at paper level (EMCN's only source is Ang 2023), not from
gene-specific evidence.
**Fix.** Correct lines 50–53 to exclude the passengers; the direction label must be gene/variant-specific or
marked as paper-inherited.

### 🟠 B4. Dark-stratum rsIDs were re-derived from GWAS Catalog and can disagree with the paper
**What's wrong.** `locus_resolution_table.csv` rsIDs were looked up by gene symbol in GWAS Catalog, not carried
from the extract. For SYT6 the resolver adjudicates **rs183827287** (study GCST90269965), which appears
**nowhere** in Ang 2023's SYT6 records (the paper reported rs115102845 / rs185469828). The mapping from
"what the paper said" to "what we resolved" is unrecorded.
**Fix.** Store both the paper-reported rsID and the resolved rsID; verify they are the same locus.

### 🟡 B5. Marker/frequency papers silently under-contribute
Kastelic (0 genes) and Norton 2016 (frequencies) don't populate the gene table, so "13 papers" overstates
gene-level contribution. Already noted in the docs (`FINDINGS_darcy_coverage.md` 103–107) but must be repeated
wherever "13 papers / 694 records" appears.

---

## C. Metric & reporting defects

### 🔴 C1. The "resolution rate" conflates coverage (Axis A) with resolution (Axis B)
`pilot_rate.py` (uncommitted scratchpad) tallies `resolution_class` over all 22 non-backbone genes and reports
*"positive 13/22 = 59% · characterized 19/22 = 86%."* The 13 "positive" **include the 7 `darcy_recoverable`
genes, which were never dark** — they were already in D'Arcy. Honest split: the 7 are a **coverage** fact; the
resolution rate is over the **15 dark genes only → 6/15 (40%) positive, 12/15 (80%) characterized.**
Full detail + corrected table: companion doc §5. **Fix.** Never mix the axes; state the denominator's
provenance inline.

### 🟡 C2. `coverage_tier` and `resolution_class` vocabularies blur
A gene can be `darcy_recoverable` (Axis A) *and* `genuinely_novel` (Axis B) — non-contradictory only once you
know they are different axes. Keep the vocabularies visibly separate in every table and figure.

---

## D. Evidence-quality issues

### 🟠 D1. Citation QC is fragile — three PMIDs were already wrong
MFSD12 (29489754→29025994), MSX2 (30595370→30531825), KALRN (mis-attributed) were corrected against NCBI PubMed
on 2026-07-11 (`docs/dark_matter_ledger_README.md` §"Citation corrections"; `dark_matter_ledger.csv`). The
corrections were applied in the ledger but **not upstream in `locus_resolution_table.csv`** per that README —
verify which artifacts still carry the wrong PMIDs. Every PMID must be NCBI-verified, none typed from memory.

### 🟡 D2. eQTL evidence is used inconsistently
Some "positive" calls rest on eQTL, others explicitly do **not**: IRF4 `genuinely_novel` rests on a mechanism
paper (PMID:24267888) while its top eQTL hit is a different gene (EXOC2); the HERC2 proxy row notes
*"inconsistent across replicate entries"* for GOLGA8M. The evidence basis per call (eQTL vs mechanism-paper vs
coding) should be a typed field, not prose in `notes`.

### 🟠 D3. Papers' own caveats are captured in extracts but dropped downstream
"not causal," "does NOT warrant further investigation," "MAF<2%," "excluded" all live in the extract
`effect_or_association`/`note` fields and vanish by the coverage layer (§B2). This is why a paper's *exclusion*
can resurface downstream as a *finding*.

---

## E. Design caveats to carry (mostly already acknowledged — collected so none is lost)

- 🟡 **E1.** Three-strata axis and D1/D2 axis are correlated, not orthogonal (14/15 dark carry `both`); labels
  often paper-inherited (`FRAMING_EVALUATION_dark_matter.md`; companion §3d).
- 🟡 **E2.** ORAOV1↔LTO1 one-gene enumeration edge case (`project_dashboard.md` §3).
- 🟡 **E3.** 13 papers ≠ 13 gene contributions (Kastelic 0; 3×TYRP1→1).
- 🟢 **E4.** Barring D'Arcy S4/S5 STRING edges (predicted, not curated) is **correct** — keep it. (Listed so the
  A3 expansion recommendation is not misread as "add STRING." Add *curated* mechanism only.)

## F. Reproducibility & structure

- 🟠 **F1.** The headline number came from `pilot_rate.py`, an **uncommitted scratchpad script** — not a
  notebook, not version-controlled, not reviewed. Any reported rate must come from a committed, reviewed cell.
- 🟡 **F2.** The `locus`-annotation layer (`locus_nodes.csv` / `locus_annotation_edges.csv`) holds only 3 loci /
  4 edges — far too small to be the "honest locus layer" the MVP spec envisions; it needs to be built out from
  the re-extraction (§B1).

---

## Required remediations (ordered; BLOCKING = no external claim until done)

1. 🔴 **BLOCKING — Re-name the strata** (A1) and **drop/relativize "dark matter"** (A2) in
   `DISCORDANCE_DECOMPOSITION_FINDING.md`, `FINDINGS_darcy_coverage.md`, `dark_matter_ledger*`, `README.md`,
   `project_dashboard.md`. Labels name sources, not evidence types or knowledge states.
2. 🔴 **BLOCKING — Expand the backbone** (A3) with KEGG/Reactome/OmniPath-curated mechanism (predicted edges
   still barred), then re-derive strata; or, if deferred, stop reporting 29/23/48 as a finding.
3. 🔴 **BLOCKING — Re-extract locus-first** (B1) and rebuild coverage on loci (B2), retaining paper verdicts.
4. 🔴 **BLOCKING — Fix the passenger overclaim** (B3) and **never report a rate that mixes the two axes** (C1).
5. 🟠 Record rsID mappings (B4); typed evidence-basis field (D2); re-verify all PMIDs (D1); move any reported
   metric into a committed reviewed cell (F1).

## What is NOT wrong (do not over-correct)

- The extractions **preserved** the locus truth and the papers' caveats — the raw data is good; the *schema and
  downstream keying* are the problem (§B).
- The nearest-gene≠causal discipline (HERC2→OCA2) is correct and should stay.
- The falsified "mislabeled-pointers" result (0/15 dark resolve into the backbone) is real and is an asset.
- Barring STRING/predicted edges is correct (E4). A3 asks for *curated* expansion, not predicted edges.

## Fact-check appendix
```
# strata labels + OMIM source
grep -n "Mechanistic\|Association-recoverable\|OMIM" internal/DISCORDANCE_DECOMPOSITION_FINDING.md
# backbone never expanded
grep -rIl -i reactome . | grep -v .git            # only aspirational docs, no build use
grep -n "validation, NEVER\|scope cross-check\|staged for a proposed" DATA_SOURCES.md
# extraction unit
for f in data/case_records/EXTRACT_*.csv; do head -1 "$f"; done
# passenger genes / segment
python3 -c "import csv;[print(r['gene'],repr(r['rsid']),r['effect_or_association'][:50]) for r in csv.DictReader(open('data/case_records/EXTRACT_Ang2023_eLife_Kalinago.csv')) if r['gene'] in {'EMCN','MANBA','SLC39A8','TACR3'}]"
# coverage layer drops locus columns
head -1 data/processed/case_gene_coverage_master.csv
```

## Provenance
All quotes verified 2026-07-11 against the named files. Backbone-expansion status: `DATA_SOURCES.md` entries
6b/6c/6d/7 + Reactome grep (no build-time use). Strata labels: `DISCORDANCE_DECOMPOSITION_FINDING.md`,
`FINDINGS_darcy_coverage.md`. Extraction defects: `data/case_records/EXTRACT_*.csv`,
`notebooks/04_darcy_coverage_finding.ipynb`, `case_gene_coverage_master.csv`. Companion deep-dive:
`internal/TRACEABILITY_coverage_and_resolution_logic.md`. This document edits no other file.
