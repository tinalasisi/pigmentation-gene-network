# Anchor reference: Nadeau, Burke & Mundy (2007) — MC1R × sexual dichromatism in birds

**Full citation.** Nadeau NJ, Burke T, Mundy NI (2007) "Evolution of an avian pigmentation
gene correlates with a measure of sexual selection." *Proceedings of the Royal Society B*
274(1620):1807–1813. doi:10.1098/rspb.2007.0174. PMCID: PMC2270924. PMID: 17504743.

**Source access note.** All details below are drawn from the **full-text PDF** (7 pp.) that
Tina downloaded to `data/raw/papers/Nadeau2007_ProcRSocB_MC1R_dichromatism/Nadeau2007_main.pdf`
(+ supplements S04–S08), and were verified by extracting and quoting the primary text. (An
earlier draft of this memo labeled the test/result "confirmed" from search snippets before
the body was retrieved — that overstatement is corrected here; everything below is now checked
against the PDF itself.)

---

## What they did (the design we are replicating)

**System.** 36 galliform species in 25 genera (samples of soft tissue, blood or feather;
taxa selected by sample availability while spanning the dichromatism range). Melanin- and
structure-based plumage; carotenoids not used in galliform plumage — so pigmentation genetics
is dominated by the melanin pathway, which is why MC1R is the a-priori candidate.

**Core question.** Does per-lineage dN/dS at pigmentation loci track the strength of sexual
selection, indexed by sexual plumage dichromatism, across the galliform phylogeny?

**Loci (6 total, all verified from text).**
- **MC1R** — melanocortin-1 receptor (the a-priori candidate; pheomelanin/eumelanin switch)
- **TYR, TYRP1, DCT** — tyrosinase gene family, melanogenesis enzymes (DCT = TYRP2)
- **AGRP** — agouti-related protein, endogenous melanocortin antagonist
- **CYTB** — mitochondrial cytochrome b, **the control locus** (not involved in pigmentation)
- (TYRP1 is Z-linked in chicken; all other nuclear loci autosomal.)

**Phenotype scoring (verified).** Sexual plumage dichromatism scored from field guides
(Madge & McGowan 2002) on a **0–6 scale**: three body regions (head+neck; back+wings+tail;
chest+belly+legs), each scored 0–2 (0 = no male/female difference). Scores reconstructed over
the phylogeny in **MacClade v.4**; branches assigned to **seven dichromatism categories**
(one per level 0–6). A second person independently scored dichromatism (acknowledgements).

**Selection metric (verified).** dN/dS by maximum likelihood, **codon-based model in PAML
v.3.14** (Yang 1997). **Branch-specific models** estimated dN/dS separately for lineages
grouped into the seven dichromatism categories; **heterogeneity tested by LRT against a
one-ratio null** (single dN/dS across the tree). A genus-level re-analysis used **free-ratio
PAML models** (dN/dS for every branch) to get branch-length-weighted mean dN/dS per genus.
Values based on ≤3 nucleotide changes were excluded. Site models (M1,M2,M3,M7,M8) were also
run on MC1R (no positive-selection site class detected — low power, noted).

**Statistical test (verified).** Genus-mean dN/dS and genus-mean dichromatism analysed as
traits in **CONTINUOUS** (Pagel 1999) — a maximum-likelihood **generalized least squares
(GLS)** model of trait evolution that corrects for phylogeny (independent contrasts as a
special case). Covariance between dN/dS and dichromatism tested by **LRT** (covariance fixed
at 0 vs. free).

**Key results (verified, quoted from text).**
- **Heterogeneity in dN/dS across dichromatism levels at MC1R:** LRS = 26.8, d.f. = 6,
  p < 0.001. Per-locus (Fig. 3): MC1R 26.82 (p<0.001); TYR 7.38 (p=0.287); TYRP1 8.90
  (p=0.179); DCT 1.96 (p=0.923); AGRP 3.74 (p=0.712); CYTB 7.68 (p=0.263).
- **Positive regression** dichromatism vs. dN/dS at MC1R: r² = 0.81, p = 0.006 (survives
  Bonferroni, corrected α = 0.008 for six tests).
- **Genus-level GLS covariance (CONTINUOUS):** MC1R **LRS = 8.5, p = 0.004** (significant
  after Bonferroni); no other locus significant. Robust across seven alternative phylogenies
  (LRS ≥ 6.2, p ≤ 0.013).
- **No dS–dichromatism covariance** across the five nuclear loci (LRS = 0.02, p = 0.88) —
  i.e. the signal is in dN/dS, not a mutation-rate (dS) effect.
- **Interpretation:** continuous/cyclical Fisherian or good-genes sexual selection at MC1R;
  explicitly refutes constant-purifying-selection and elevated-mutation-rate models.

---

## What is novel about our primate study vs. this anchor

| Dimension | Nadeau et al. 2007 (birds) | This project (primates) |
|---|---|---|
| Gene scope | 6 candidate loci | Curated **803-gene pigmentation network** + **53-gene hormone seed** |
| Comparator | none (pigmentation loci only) | **pigmentation vs. sex-hormone network contrast** — the new claim |
| Trait | graded plumage dichromatism | scored **hair dichromatism** (Leakey: binary + 5-state trajectory) |
| Selection test | GLS of dN/dS on dichromatism | HyPhy **RELAX/aBSREL** + **RERconverge** + **SUMSTAT** set test + PGLS |
| Convergence | cross-tree correlation | **independent origins** (gibbons, cercopithecids, lemurs, cebids) explicit |
| Level | single-gene | **systems / network / module** level |

The bird study is the **positive control and entry point**: if MC1R shows the same
dichromatism-associated dN/dS signal in primates, that anchors the pipeline against known
biology before the network and hormone-contrast analyses extend it into unclaimed territory.

---

## How we build on it (concrete plan)

1. **Reproduce the anchor first.** Their exact design maps directly onto ours: MC1R + TYR +
   TYRP1 + DCT are ALL in our pigmentation panel. Run their test in primates — per-lineage
   dN/dS grouped by dichromatism level, LRT for heterogeneity, then a genus/clade-level GLS
   (PGLS) of dN/dS on the dichromatism score. This is the "did we recover the known MC1R
   result" gate.
   - **Risk flagged:** in the Ensembl PoC, MC1R had only 12 primate orthologs (no dichromatic
     tip) and was dropped *from the PoC only* — an Ensembl-coverage artifact. The flagship
     miniprot run recovers MC1R directly from each assembly (MC1R is single-exon and highly
     conserved — easy to find); the smoke test pulled 79/80 genes from one gibbon. Confirming
     MC1R is among the recovered genes is the first check when the report lands.
2. **Match their statistic, then exceed it.** Their heterogeneity LRT ≈ our RELAX/aBSREL
   (both ask "does dN/dS differ on dichromatic lineages"); their CONTINUOUS GLS ≈ our PGLS on
   per-lineage rates. We ADD, beyond anything they did: RERconverge (convergent shifts across
   independent origins) and SUMSTAT (network-vs-network polygenic enrichment).
3. **Expand the gene set deliberately.** They tested 6 loci and found 1. We test a network,
   so we must correct for pleiotropy dilution (housekeeping/hub genes wash out) — which is
   exactly why the SET-level SUMSTAT test, not gene-by-gene counting, is the primary analysis
   for the network claim.
4. **Copy their control design.** CYTB (a non-pigmentation control) showed no signal —
   their internal null. We should carry an explicit null gene set (no pigmentation/hormone
   role) as the SUMSTAT background and a null band in the heatmap, so a network-wide signal
   is demonstrably above baseline. Their dS-vs-dichromatism null (LRS=0.02) is also worth
   copying: verify our signal is in dN/dS, not dS (a mutation-rate artifact).

## Direct design correspondences (their locus → our panel)
| Nadeau 2007 locus | role there | in our panel? |
|---|---|---|
| MC1R | a-priori candidate, the hit | YES (pigmentation core) — the anchor gene |
| TYR, TYRP1, DCT | melanogenesis enzymes | YES all three (pigmentation core) |
| AGRP | melanocortin antagonist | absent from network (noted earlier); ASIP is our analogue |
| CYTB | mitochondrial control | not applicable — but motivates an explicit null gene set |

## Supplements on disk (for cross-checking / extending)
- `Nadeau2007_S04_table.xls`, `S05_table.xls` — taxa list & per-locus data (their Table 1/2).
- `Nadeau2007_S06_figure.jpg`, `S08_figure.jpg` — figures incl. per-locus dN/dS-vs-dichromatism.
- `Nadeau2007_S07_text.doc` — supplementary methods (PCR primers etc.).
