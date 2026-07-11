# Research synthesis — what the honest data says, and the MVP recommendation

_Session 2026-07-11. Three parallel research tracks (locus resolution, literature + prior art,
integration+build spec). No plan-deconvolutor; these are working analyses grounded in live data._

**Direction labels (glossed everywhere):**
- **D1 = "genotype-present, phenotype-absent"** — canonical causal variant present, expected pigmentation
  phenotype absent (reduced penetrance; modifier nodes block the path).
- **D2 = "phenotype-present, genotype-absent"** — phenotype present without the canonical variant
  (an alternative gene/route reaches the same endpoint).

---

## 1. The hypothesis I set out to test — and its honest result

**Hypothesis:** the 15 "dark-matter" case genes are largely GWAS loci labelled by *nearest gene*, whose true
functional target is a different gene already in our network (regulatory/eQTL redirect) — flipping "missing
biology" into "mislabeled pointers." Canonical seed: rs12913832 is intronic in **HERC2** but regulates
**OCA2** (in-network) via a long-range enhancer.

**Result (Track A, GWAS Catalog + eQTL Catalogue, per-locus, self-reviewed): the strong form is FALSE.**
Of the 15 dark-matter genes, **zero** resolve to an already-in-network gene through GWAS+eQTL evidence. The
one true positional-pointer-to-in-network case, **HERC2 → OCA2**, is a *D'Arcy-recoverable* gene, not a
dark-matter gene — and it is rare, not the dominant pattern.

**The dark matter decomposes into five cited classes instead:**

| class | n | genes |
|---|---|---|
| no pigmentation GWAS signal at all | 6 | ATRN, EMCN, LTO1, MANBA, SLC39A8, TACR3 |
| genuine signal, no eQTL redirect found | 3 | KALRN, MSX2, SYT6 |
| redirects to another gene **also absent** from the network | 2 | NPLOC4→TSPAN10, SIK1→LINC01679 |
| genuinely novel (own best-supported causal gene, just missing) | 4 | MFSD12, PKHD1, SLC24A4, TSPAN10 |

Crucially, **4 of the 6 "no-signal" genes** (EMCN, MANBA, SLC39A8, TACR3) were flagged only because they sit
in a chromosome-4 homozygous-by-descent segment shared by chance in one Kalinago albino individual (Ang 2023)
— **the source paper itself excluded them as non-causal.** The other two are rejected on different grounds:
ATRN's single literature candidate (chr20, Quillen 2012) was retested directly in the case cohort and was not
significant, and LTO1 is a Morgan 2018 hair-colour candidate with no locus-level pigmentation record found.
None of the six is a nearest-gene mislabeling; they are absences of pigmentation signal, correctly identified.

**Why the falsification makes the finding stronger, not weaker:** the interesting result is the *principled
decomposition* — refusing to call a gene "unexplained biology" when it is really an LD passenger, a
no-signal hitchhiker, or a genuinely-missing-but-correctly-labelled gene. That is a refuse-to-overclaim
posture, and it is the design principle the MVP is built to demonstrate (below).

## 1a. Where each paper fits (the decomposition above is corpus-wide, not Ang-centric)

The falsification test and the four-class decomposition in §1 draw on the full 13-paper, 694-record
validation-case set. Ang 2023 (53 records) supplies 7 of the 15 dark-matter genes (ATRN, EMCN, KALRN, MANBA,
SLC39A8, SYT6, TACR3) and anchors the worked examples, but it is only the fourth-largest paper — Meyer 2020
(211 records), Kastelic 2013 (105 records), and Morgan 2018 (63 records) are all larger. The 13 papers
cluster by phenotype system, and every cluster has a role:

| cluster | papers | role in the framing |
|---|---|---|
| Eye-colour / forensic panel | Abbatangelo 2026, Meyer 2020, Pospiech 2016, Kastelic 2013, Salvo 2023 | The nearest-gene≠causal story (HERC2→OCA2); IRF4, SLC24A4, TSPAN10 dark matter live here |
| Skin pigmentation (population) | Crawford 2017, Yang 2016 | The genuinely-novel dark-matter story: MFSD12 (cited expression mechanism) + SLC24A5/SLC45A2 |
| Albinism / hypopigmentation | Ang 2023 | The LD-passenger / no-signal dark-matter story (chr4 hitchhikers Ang itself excluded) plus the OCA2 D1/D2 anchor |
| Blond hair (TYRP1) | Kenny 2012, Norton 2014, Norton 2016 | D2 depth on one in-network gene (TYRP1 R93C) — not dark matter |
| Red hair (MC1R) | Morgan 2018 | D1 penetrance-matrix depth on MC1R and a second dark-matter engine (LTO1/MSX2/PKHD1/SIK1/TSPAN10 — TSPAN10 also contributed by Abbatangelo 2026, so paper-level counts overlap) |
| Syndromic | Morell 1997 (Waardenburg, PAX3) | The clean D1 anchor on an in-network gene (incomplete penetrance) |

Two honest caveats regardless of framing: Kastelic 2013 extracted **0 gene symbols** (model/marker paper,
105 records, no gene column) — it must not imply 13 independent gene contributions; and the three TYRP1
papers (Kenny 2012, Norton 2014, Norton 2016) collapse to a single in-network gene — D2 depth, not breadth.
Full detail: `FRAMING_EVALUATION_dark_matter.md` §1–2.

## 2. The design standard this MVP is built to

The target is a principled, interactive, mechanistically-grounded reasoning demo: disease-stratified, every
displayed claim click-through-cited, narrated through named worked examples, and — the load-bearing part —
one that **visibly refuses easy-but-uncited inferences**. The reasoning it must make legible is that a
signal's magnitude is not its causal call: the two are deliberately decorrelated, so a heavily-flagged
locus with no curated mechanism is *not* asserted as causal, and a mechanism with a thin signal but curated
evidence *is* surfaced. Applied to gene attribution, that is exactly the nearest-gene-vs-causal discipline
below.

## 3. The reconciled finding — "the Locus-Resolution Ledger"

Both the literature track and the integration track independently recommend the same MVP, and it absorbs
Track A's honest result cleanly:

**Take every case gene our network doesn't contain and reclassify it by *gene-attribution status*, with a
citation for each call and a principled refusal to reattribute without one.** The categories (grounded, not
hypothetical):

- **positional pointer → in-network gene** (HERC2 → OCA2; chromatin-loop enhancer, PMID 22234890) — the
  nearest-gene≠causal case, rare but real.
- **redirects to another out-of-network gene** (RALY → ASIP; NPLOC4 → TSPAN10; SIK1 → LINC01679).
- **LD passenger / no-signal hitchhiker** (the 4 chr4 genes EMCN/MANBA/SLC39A8/TACR3 that Ang 2023 itself
  excluded, plus ATRN and LTO1 rejected on separate grounds — see §1).
- **genuinely novel, correctly labelled, simply missing** (MFSD12 expression-modulation, Crawford 2017;
  SLC24A4; PKHD1; plus recoverable IRF4/BNC2/SLC24A5/SLC45A2/LRMDA as their own causal genes).

The ledger's *value proposition is the principled-refusal argument applied to gene attribution*: just as a
principled reasoning demo refuses to let "high bioactivity" stand in for "curated cause," the ledger refuses
to let "absent from the network" stand in for "unexplained biology," **and** refuses to relabel a locus to
its functional target without that target's own citation (nearest-gene-vs-causal discipline).

## 4. How resolved loci enter the model honestly (integration spec)

A locus is a SNP, not a gene. Integration schema (Track C), respecting locked decision 5 (no association-only
mechanistic edges):
- New `locus` node type (keyed by rsID), carrying `nearest_gene_label` + `gene_label_basis`; **never merged**
  into the 168-gene node table, **never counted** in the NB2 figure or any D1/D2 path computation.
- A structurally separate `locus_annotation_edges.csv` with a mandatory `evidence_citation` column
  (blank = rejected at load) and a 5-value `edge_type` vocabulary: `nearest_gene_link`, `regulatory_target`,
  `eQTL_target`, `in_LD_with`, `dark_matter_association`.
- Visual separation wherever rendered: mechanistic edges solid/signed/colored; locus edges dashed/gray;
  locus nodes as diamonds. A `pd.concat` into the backbone becomes a schema error, not a silent merge.

## 5. Recommended MVP

**An interactive, client-side "Locus Resolver" walkthrough**, hosted on the existing Quarto→GitHub Pages
static site (no backend, no kernel — fits locked decision 10), walking two worked examples with every claim
click-through-cited and the D1/D2 call **computed from the pinned signed network, not asserted in prose**:

1. **rs12913832 / HERC2 / OCA2 — eye colour.** SNP → nearest-gene label (HERC2) → *cited* resolved target
   (OCA2) → OCA2's existing backbone path → D1/D2 readout. A toggle "nearest-gene only vs. resolved target"
   shows exactly what a naive tool misses.
2. **Kalinago OCA2 R305W / NW273KV (Ang 2023) — the D1 anchor + its D2 counterpart in one case.** R305W is
   correctly OCA2-labelled and in-network yet non-penetrant (D1: path exists, modifier blocks it); the
   albino individuals carry no catalogued OCA2 variant, only the novel NW273KV (D2: phenotype without the
   canonical genotype).

Together they cover **both discordance directions and both integration failure modes** (nearest-gene
mislabeling vs. modifier-driven penetrance) — the differentiator against a single-mechanism demo.
The 15-gene dark-matter ledger renders as the honest "not-yet-resolvable" backdrop (a `dark_matter_association`
state that is itself a finding, not a rendering gap).

**48h feasibility: high.** Backbone, case set, coverage table, and the frozen GWAS/eQTL pull already exist.
To build: the two-example locus-annotation tables, a frozen JSON export, the static page, and the review
passes. Static multi-panel figure is the fallback if time runs short.

## Sources
Ang 2023 eLife 10.7554/eLife.77514 · Kenny 2012 Science 10.1126/science.1217849 · Crawford 2017 Science
10.1126/science.aan8433 · Yang 2016 MBE 10.1093/molbev/msw003 · Morgan 2018 Nat Commun
10.1038/s41467-018-07691-z · Visser 2012 Genome Res 10.1101/gr.128652.111 · D'Arcy 2023 Bioengineering
10.3390/bioengineering10010013 · Abbatangelo 2026 Sci Rep 10.1038/s41598-026-44580-8.
