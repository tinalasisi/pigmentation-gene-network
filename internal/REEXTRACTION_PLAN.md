# Careful re-extraction plan — fixing the "author-unexplained" foundation

**Status: EXECUTED & PI-SIGNED-OFF (2026-07-12).** The effector re-classification is committed as
`data/processed/discordance_loci_effector_classified.csv` and is now the spine of NB4, `index.qmd`, and PITCH.
Verified same-grain numbers on the 105 curated loci: of the **52** "author-unexplained" loci, only **9** are
genuinely effector-uncertain — **32** are canonical-effector variant-gaps, 6 ambiguous-near, 3
regulatory-of-neighbour, 2 not-a-locus. The full effector-uncertain target set is **14** within the 105 (5 more
were mis-tagged `mechanism_proposed`) and **34** once Kim 2024 (26 loci) is folded in.

**Caveat on the HERC2 example below (integrity note).** rs12913832 is tagged `mechanism_proposed` where it is a
locus's *primary* variant (Abbatangelo / Kastelic / Pospiech); it also appears as a *member* SNP of an Ang2023
`nearest_gene_only` locus. So "HERC2 rs12913832 was tagged author-unexplained" is **messy, not cleanly true** —
NB4 therefore uses the unambiguous *TYR* (rs1393350) / *SLC45A2* (rs16891982) / *OCA2* (rs1800407)
`nearest_gene_only` mis-tags as the worked examples instead.

## The problem we are fixing

The `discordance_loci_author_explained.csv` extraction defined **author-unexplained** as *"did the authors
functionally annotate this specific variant?"* — a variant-level-mechanism test. The PI's actual research
question is different: **"is the gene the authors associated with the phenotype actually the EFFECTOR?"**

These are two distinct questions, and conflating them corrupted the target set:

| Question | Example | In scope for THIS project? |
|----------|---------|----------------------------|
| Does this specific canonical variant cause the phenotype? (maybe another variant in the same gene; maybe compound-het) | TYRP1 rs2733836 "2 kb upstream, consequence unknown" | **NO** — this was the PI's *first* project. TYRP1-as-effector is textbook. |
| Is the associated / nearest gene even the effector? | Morgan's "ORAOV1" locus; Ang's Kalinago "EGFR/LANCL2" | **YES** — this is the current flagship question. |

Consequence of the error: **33 of 52 "author-unexplained" loci point at a canonical effector** (TYRP1, OCA2,
HERC2, SLC45A2, TYR, IRF4, SLC24A4). The most egregious case: **HERC2 rs12913832** — the blue-eye master
switch, the single best-characterised pigmentation variant in the genome — was tagged "author-unexplained"
because no SIFT/PolyPhen score was tabulated in one paper. That is indefensible and it revealed the systematic
flaw.

## Why the current extraction is too cheap

It matched gene-name tokens programmatically against text and assigned a status. It did not:
- record the **precise locus → association → attributed-gene claim** the authors actually made (the PI wanted
  precise builds with locus/association/build/effect, not gene-name scraping);
- distinguish **"variant IN gene X"** from **"variant NEAR gene X"** — and for "near" cases, it never asked the
  critical question: *are the authors claiming a demonstrated biological effect on gene X, or are they merely
  naming the nearest gene and implicitly assuming LD with variants in it?*
- capture the **effect direction / allele / population / build** with enough fidelity to treat each row as a
  precise locus record.

## The fix — a careful per-paper re-extraction (locus-first, claim-faithful)

### Principle
Read every paper's own words per locus. Do NOT scrape gene names. For each locus, record what the authors
**actually claimed**, then classify the claim — never infer the claim from the gene symbol.

### Per-locus fields to extract (the precise build)
1. `paper`, `locus_id`, `lead_rsid` (+ any credible-set / tag SNPs), `chr:pos`, `coord_build` (explicit),
   `effect_allele`, `effect_direction/size`, `pvalue`, `population/ancestry`, `trait`.
2. `author_attributed_gene` — the gene the authors name for this locus, **verbatim**, with the exact quote.
3. `attribution_basis` — one of:
   - `coding_in_gene` (variant is coding/functional IN the named gene),
   - `regulatory_demonstrated` (authors show/cite a demonstrated regulatory effect on the named gene —
     eQTL, reporter, chromatin, etc.; record WHAT evidence),
   - `nearest_gene_only` (authors name it only because it is nearest; NO functional claim),
   - `in_LD_with_gene_variants` (authors explicitly reason the signal tags variants IN a named gene via LD),
   - `stated_unknown` (authors explicitly say the effector/mechanism is unknown).
4. `effector_status` — the classification the FLAGSHIP needs, derived from `attribution_basis` + whether the
   named gene is an established pigmentation effector:
   - `canonical_effector_variant_gap` (named gene is a textbook effector; only the variant mechanism is open —
     OUT of scope, report separately as the PI's first-project category),
   - `effector_uncertain` (named gene is NOT an established effector, or authors state unknown — IN scope),
   - `regulatory_of_canonical_neighbour` ("near GENE" where evidence points to the canonical neighbour — treat
     as canonical, NOT a finding),
   - `effector_ambiguous_near` ("near GENE" with NO demonstrated effect — candidate for LD-nomination: hand
     back to authors "check whether network genes in this LD block are the effector").
5. `notes` — any nuance (synthetic-association warning, admixture/portability comment, etc.).

### "Near a gene" — the specific nuance the PI flagged
For every locus attributed to a gene the variant is not physically in, decide explicitly:
- **Demonstrated effect on the target gene?** (authors cite eQTL / reporter / Hi-C / known enhancer) →
  `regulatory_demonstrated`; effector known.
- **Only proximity / implied LD?** → `effector_ambiguous_near`; the honest move is NOT to claim a rescue but to
  NOMINATE (via our network + LD) which genes in the region the authors should check. This is the secondary
  "consolation" contribution the PI described.

### Process (per paper, all 15 incl. Kim2024, Zhang2018 context)
1. Read the paper's main text + the association/GWAS table(s) in the SI (the precise builds live there).
2. Extract every reported pigmentation locus with the fields above, each tied to a **verbatim quote + section
   /table + page**.
3. Classify `attribution_basis` and `effector_status` from the quote, not the symbol.
4. Cross-check against the melanocyte-eQTL layer (Zhang 2018 T-S6/T-S10) where a locus has an eQTL proxy.
5. Emit `EXTRACT_<paper>_loci_v2.csv` + a per-paper README documenting decisions; then a merged
   `discordance_loci_effector_classified.csv` that supersedes `discordance_loci_author_explained.csv`.
6. Route through DATA_SOURCE_AUDITOR / GENETICS_LIT_REVIEWER for a correctness pass before it becomes the base.

### Papers, in priority order for the effector-uncertain question
1. **Ang 2023 (Kalinago, Dominica)** — most of the effector-uncertain loci; admixed population; the portability
   story lives here. Read the GWAS table + fine-mapping carefully.
2. **Morgan 2018 (UK Biobank)** — the 4 contested loci (MSX2, PKHD1, ORAOV1, SIK1) + the MC1R-5' regulatory
   signal. The SI association table is the source of truth (already confirmed the 4 are SI-table-only).
3. **Crawford 2017** — the portability exemplar the PI named (a locus not variable enough in Europeans to
   associate, but variable/associated in Africans → effector question via population-conditionality).
4. Abbatangelo, Meyer, Pospiech, Salvo, Kastelic, Yang, Kenny, Norton×2, Morell — mostly canonical-effector
   eye-colour panel loci; re-extract to confirm they land in `canonical_effector_variant_gap`, cheaply.
5. **Kim 2024** — newly added; extract its 12 known + 11 novel loci as a fresh source (was a documented gap).

### Deliverables of the fix
- `discordance_loci_effector_classified.csv` (supersedes the author_explained file; both provenance kept).
- Corrected NB4 funnel: 105 curated → N effector-uncertain (the real flagship target) + M
  canonical-effector-variant-gap (separate, honest) + Kim additions.
- Re-resolution of the effector-uncertain set against **melanocyte eQTL** (Zhang), not bulk skin.
- Then re-run NB8 rescue on the corrected, precise set.

## What is running tonight (diagnostic, does NOT depend on the fix)
A diagnostic rescue test on the **provisional 18 effector-uncertain loci** (programmatic first pass) to answer
"do we even have a finding?" — try-hard connection (substrate + GRN + Reactome-tagged + melanocyte eQTL +
<=2-hop paths + verifiable biology), honest negatives. Result to be reviewed alongside this plan. If the
diagnostic says "almost nothing connects even trying hard," that is important signal about feasibility BEFORE
we invest in the full careful re-extraction.
