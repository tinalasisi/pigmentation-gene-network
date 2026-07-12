# Systems-level layer + certification handoff (from Claude Science / MOL_EVO_SPECIALIST)

For the HPC-side Claude Code. Adds the analyses that answer the paper's *central* claim,
plus my certification checklist for the flagship report. Nothing here blocks the flagship —
it's staged for after certification.

## New scripts added to `scripts/`
| script | what it does | when to run | needs |
|---|---|---|---|
| `02b_branch_rates.py` | per-BRANCH dN/dS (aBSREL) per gene → `report/branch_rates.csv`. Feeds the selection-painted network figure. | after `02`, on the full panel | hyphy |
| `05_polysel_geneset.py` | SUMSTAT gene-SET enrichment: is the pigmentation network as a whole more dichromatism-selected than the hormone network? Pure Python stdlib. | after `03` (reads `report/relax_results.csv`); optionally after `02b` | none |
| `04_rerconverge.R` | convergent relative-rate test — do the independent dichromatic origins shift the SAME genes? | after `02` (reads `aln/*.codon.aln.fa`) | R + phangorn, ape, `remotes::install_github("nclark-lab/RERconverge")` |

**Please add to `envs/environment.yml`:** `r-base`, `r-phangorn`, `r-ape`, `r-geiger`,
`r-remotes` (RERconverge itself installs from GitHub). PolySel needs nothing extra.

**Why these exist:** per-gene RELAX/aBSREL die to multiple testing (PoC: nothing survived BH)
because network selection is diffuse. The claim is a SET-level question, so `05` tests it at
the set level (primary test of the central claim); `04` tests convergence across independent
origins (the strongest evidence, and it turns "few independent origins" from a power caveat
into the statistic). All three validated locally: `02b`/`05` run against real HyPhy 2.5.100
output; `04` parses clean (not yet run end-to-end — needs the R packages).

## My certification checklist for the flagship report (what I check, in order)
When you commit `report/` (SUMMARY.md + tip_roster.csv + extraction_qc.csv), note the SHA and
I read it at that SHA. Gate order:
1. **MC1R present across the gibbon foreground.** `ls cds/MC1R/*.cds.fna` or the MC1R row in
   `tip_roster.csv` — do the 5 dichromatic gibbons (Nomascus leucogenys/concolor/gabriellae,
   Hylobates pileatus/muelleri) have MC1R? MC1R is the anchor gene (see below); it was dropped
   in the Ensembl PoC only as a coverage artifact — miniprot should rescue it (single-exon,
   conserved). **This is the first thing I check.**
2. **Foreground integrity** — ≥3 of 5 dichromatic + a balanced monochromatic set per gene, and
   non-trivial tagged branch lengths (guard against the near-zero-foreground K artifact).
3. **Extraction trust** — miniprot %identity to reference reasonable (flag <~70%), aln_len ≤
   1.2× ref_len (assembly-indel inflation check).
4. **Only then** the RELAX/SUMSTAT/RER signal, pigmentation vs hormone.

I will NOT read K/p off a partial (<9 gibbon) run — a 2–3-tip foreground gives the same
single-branch artifact we saw in the PoC.

## Anchor reference (the bird paper this project replicates + extends)
Nadeau, Burke & Mundy (2007) Proc R Soc B 274:1807–1813, doi:10.1098/rspb.2007.0174. Verified
from the full PDF (in the main repo at `data/raw/papers/Nadeau2007_ProcRSocB_MC1R_dichromatism/`).
Their design: 6 galliform loci (MC1R, TYR, TYRP1, DCT, AGRP + CYTB control), dichromatism 0–6,
dN/dS via PAML branch models, GLS in CONTINUOUS. Result: signal **specific to MC1R**
(genus-level LRS=8.5, p=0.004; heterogeneity LRS=26.8; regression r²=0.81), none at the other
loci. **MC1R, TYR, TYRP1, DCT are all in our panel** — so we reproduce their test in primates,
then extend with RELAX/aBSREL/RERconverge/SUMSTAT and the hormone-network contrast (none of
which existed in 2007). A `06_mc1r_anchor.R` (their GLS test as PGLS on our per-lineage dN/dS)
is the natural next script — say the word and I'll add it.

## Scope reminders (from the scientist)
- Full run is **all 117 recoverable genomes across 4 families**, not just gibbons — gibbons are
  the flagship validation clade only.
- Keep as many genes as possible; genes drop only on per-gene QC failure, never pre-emptively.
