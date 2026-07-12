# Source spec — HIrisPlex-S (Chaitanya et al. 2018), eye/hair/skin color prediction markers

**Status:** ACQUIRED (marker set); model coefficients PARTIALLY documented — see the gap below.

## Identity
- **Citation:** Chaitanya L, Breslin K, Zuñiga S, Wirken L, Pośpiech E, Kukla-Bartoszek M, Sijen T, de
  Knijff P, Liu F, Branicki W, Kayser M, Walsh S. "The HIrisPlex-S system for eye, hair and skin colour
  prediction from DNA: Introduction and forensic developmental validation." *Forensic Science International:
  Genetics* 35:123–135, 2018.
- **DOI:** 10.1016/j.fsigen.2018.04.004 · ScienceDirect PII S1872497318302205.
- **Companion model reference (skin model):** Walsh S et al., "Global skin colour prediction from DNA,"
  *Hum Genet* 136:847–863, 2017 (the HIrisPlex-S 36-SNP skin model and its coefficients originate here).
- **Web tool:** https://hirisplex.erasmusmc.nl/ (the operational model + coefficients live here as an Excel
  prediction macro).
- **Source files used:** paper PDF (`1-s2.0-S1872497318302205-main.pdf`, marker list on p3–5) + the
  ScienceDirect supplement bundle (`mmc1.docx`…`mmc4.xls`).
- **Access method:** paper + supplements provided by the project owner. Programmatic fetch returned only the
  abstract (green-OA metadata); the full-text tables came from the author-provided PDF.
- **Access date:** 2026-07-08.
- **License:** Elsevier/FSI:Genetics copyright (subscription). Marker rsIDs are factual data; the prediction
  model + web tool are freely usable for prediction via the Erasmus MC site. Cite Chaitanya 2018 + Walsh 2017.

## System structure (from the paper, verified)
HIrisPlex-S = **41 SNPs total** across two SNaPshot multiplex assays (a novel 17-plex for skin + the prior
24-plex HIrisPlex for eye/hair; 19 skin SNPs overlap the 24-plex), feeding **three prediction models**:
- **IrisPlex** — eye color, **6 SNPs**, multinomial logistic regression (blue / intermediate / brown).
- **HIrisPlex** — hair color, **22 SNPs** (brown / red / black / blond + shade).
- **HIrisPlex-S** — skin color, **36 SNPs** (very pale / pale / intermediate / dark / dark-black).

## What we extracted (the marker set)
`data/processed/hirisplexs2018_markers.csv` — **36 gene→rsID marker pairs** parsed from the paper text,
across 16 genes (ANKRD11, ASIP, BNC2, DEF8, HERC2, IRF4, KITLG, MC1R, OCA2, PIGU, RALY, SLC24A4, SLC24A5,
SLC45A2, TYR, TYRP1), with a `in_novel_17plex_skin` flag marking the 17 skin-specific SNPs listed on p3.

**Payoff-locus coverage:**
- **MC1R red-hair markers:** rs1805007, rs1805008, rs1805006, rs11547464, rs885479, rs2228479, rs1110400,
  rs3212355 — the full red-hair set.
- **Blue-eye markers:** HERC2 **rs12913832** (the eye-color master switch) + OCA2 rs1800407.

## Gaps / assumptions (no undocumented claims)
1. **36 of 41 markers captured.** The parse pulled gene→rsID pairs from the running text; the remaining ~5
   SNPs plus full primer/allele detail are in the paper's formatted **Table 1** (image-like layout not fully
   linearized by text extraction). For the MC1R/OCA2/HERC2 payoff loci the set is complete; if the full 41
   are needed, Table 1 must be transcribed from the PDF (flagged, not silently dropped).
2. **Model coefficients are NOT in this paper.** Chaitanya 2018 introduces the assay and validates it; the
   per-SNP β coefficients and intercepts for the three models are published in the model papers (IrisPlex —
   Walsh 2011; HIrisPlex hair — Walsh 2013; HIrisPlex-S skin — Walsh 2017) and operationalized in the
   Erasmus MC Excel macro. **To attach quantitative likelihood ratios / prediction probabilities**, pull the
   coefficient table from Walsh 2017 (skin) + the web-tool macro. This is a documented follow-up, not an
   acquired artifact — the marker→gene mapping (what the network needs to place the loci) is complete.
3. One OCR fix applied: `rs228479`→`rs2228479` (MC1R R163Q); one OCR duplicate (`rs18004141`) dropped.

## Reported accuracy is population-specific (the interpretive frame)
The Erasmus MC Webtool User Manual v2.0 (2018) — pinned as
`data/raw/hirisplexs2018/hirisplex.erasmusmc.nl.pdf`, extracted to
`data/processed/hirisplexs2018_population_provenance.json` — states the model-training databases:
- **Eye** (n=9,466): 9,188 from **eight European countries** (Liu 2009 + Walsh 2012) + 278 US-based → ~97% European.
- **Hair** (n=1,878): 1,601 from **Ireland/Greece/Poland** (Walsh 2013) + 50 Japanese + 277 US-based → ~85% European.
- **Skin** (n=1,423): Ireland/Greece/Poland + US-based (diverse parental origins) + CEPH-HGDP Senegal/Nigeria/
  Kenya/Papua New Guinea (Walsh 2017) → the only ancestrally diverse model.

**Consequence for how we cite the numbers.** The manual's headline accuracies — red-hair AUC 0.92; eye 80%
correct (96% brown/blue only); hair 77%; the skin AUC table (Very Pale 0.83 → Dark-to-Black 0.99) — are
**European-derived accuracies**, especially for eye and hair. **They must never be cited bare**; every figure
carries its population provenance. Discordance between predicted and observed phenotype is therefore expected
to be **structured by genomic background (ancestry), not random** — which is precisely this project's thesis:
the same genotype yields a different phenotype because the surrounding network differs, and that network
background differs across populations. This is the **interpretive frame**, documented from the manual; it does
**not** pull population/allele-frequency data into this week's build (still out of scope) — it is the
bridge to the downstream research program.

## Result / pinned artifacts
- `data/processed/hirisplexs2018_markers.csv` — 36 markers, gene + 17-plex-skin flag.
- `data/processed/hirisplexs2018_population_provenance.json` — model training-set composition + reported
  (European-derived) accuracy figures, with the population caveat attached.
- `data/raw/hirisplexs2018/` — **committed:** the Erasmus MC Webtool User Manual v2.0 (2018, freely usable)
  and the transcribed raw marker table `hirisplexs2018_markers_raw_transcribed.csv` (factual rsIDs, with the
  Table 1 page citation). The Chaitanya 2018 paper PDF (Elsevier subscription) + mmc1–4 supplements are
  **not redistributed** (obtain via DOI 10.1016/j.fsigen.2018.04.004; see `data/raw/papers/REFERENCES.md`).

## Note for the build
The marker→gene mapping is what a proposed loci-placement step would need to **place** the HIrisPlex loci on the network. The model
coefficients become necessary only to quantify *how confident* a given genotype's prediction is (the "high
likelihood ratio that still fails" framing) — acquire from Walsh 2017 + the web tool when that quantitative
step is reached.
