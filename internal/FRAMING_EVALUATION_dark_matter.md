# Big-picture evaluation: should "dark-matter association" be the paper's framing?

_Evaluation only — no docs rewritten. Decision requested from PI before any rewrite. Session 2026-07-11._

**Direction labels (glossed):** D1 = "genotype-present, phenotype-absent" (canonical variant present, phenotype
absent — reduced penetrance). D2 = "phenotype-present, genotype-absent" (phenotype without the canonical
variant). Gene-level: `both` = D1+D2 evidence; `mixed` = direction varies across papers.

## 1. The worry is justified — but the corpus is broader than the MVP made it look

The MVP walkthrough leaned on Ang 2023 because that is where the dark matter physically concentrates, not
because the corpus is Ang-centric. The actual distribution:

- **13 papers, 694 records, spanning 4 phenotype systems**: eye colour (5 papers), blond hair (3), red hair
  (1), skin (2), albinism/hypopig skin (1), syndromic Waardenburg (1). Ang 2023 (53 records) is only the
  **fourth-largest** paper — Meyer 2020 (211 records), Kastelic 2013 (105), and Morgan 2018 (63) are larger.
- **Dark matter concentrates in two papers**: Ang 2023 contributes 7 of the 15 dark-matter genes (ATRN, EMCN,
  KALRN, MANBA, SLC39A8, SYT6, TACR3); Morgan 2018 contributes 5 (LTO1, MSX2, PKHD1, SIK1, TSPAN10 — TSPAN10
  is also contributed by Abbatangelo 2026, so paper-level counts overlap). That is why the MVP felt Ang-heavy.
- **6 of 13 papers touch ≥1 dark-matter gene** (Abbatangelo, Ang, Crawford, Meyer, Morgan, Pospiech),
  carrying **418 of 694 records (60%)**. The dark-matter framing is therefore not an Ang artifact — it reaches
  a clear majority of the corpus.

## 2. Where each paper fits (nothing is orphaned)

The papers cluster by phenotype system into a coherent structure the dark-matter framing organizes:

| cluster | papers | role in the framing |
|---|---|---|
| **Eye-colour / forensic panel** | Abbatangelo 2026, Meyer 2020, Pospiech 2016, Kastelic 2013, Salvo 2023 | The natural home of the **nearest-gene≠causal** story: HERC2→OCA2 is *the* forensic prediction problem. IRF4, SLC24A4, TSPAN10 dark matter live here. |
| **Skin pigmentation (population)** | **Crawford 2017**, Yang 2016 | The **genuinely-novel dark matter** story: MFSD12 (cited expression mechanism, Crawford) + the SLC24A5/SLC45A2 gene-flow alleles. This is the strongest "correctly-labelled but missing from the network" cluster. |
| **Albinism / hypopigmentation** | Ang 2023 | The **LD-passenger / no-signal dark matter** story: the chr4 hitchhikers Ang itself excluded, plus the OCA2 D1/D2 anchor. |
| **Blond hair (TYRP1)** | Kenny 2012, Norton 2014, Norton 2016 | D2 **depth** on one in-network gene (TYRP1 R93C) — population-specific alternative route. Not dark matter; the "alternative-route D2" pillar. |
| **Red hair (MC1R)** | Morgan 2018 | D1 **penetrance-matrix** depth on an in-network gene (MC1R allele grading) AND a second dark-matter engine (LTO1/MSX2/PKHD1/SIK1). |
| **Syndromic** | Morell 1997 (Waardenburg PAX3) | The clean **D1** anchor on an in-network gene (incomplete penetrance). |

Two honest caveats to fix regardless of framing decision: **Kastelic 2013 extracted 0 gene symbols** (it is a
model/marker paper — 105 records but no gene column populated), and the three TYRP1 papers collapse to a single
gene. Neither breaks the framing, but the paper's Methods must not imply 13 independent gene contributions.

## 3. Is "dark-matter association" the right framing? Assessment

**Strengths (why it works as the paper's spine):**
- It is the project's own measured result (48% of case genes are dark matter), not a borrowed metaphor.
- It reaches 60% of records / 6 of 13 papers — broad enough to be the organizing axis.
- It gives every paper a role (§2) instead of privileging one.
- It embodies the design principle the MVP is built on (principled refusal to overclaim): we refuse to call
  a gene "unexplained biology" without checking whether it is a passenger, a mislabel, or genuinely novel.
- The honest 4-way decomposition (positional-pointer / redirect-to-other / passenger-or-no-signal /
  genuinely-novel) is a *finding*, and it is more defensible than the original "mislabeled pointers"
  hypothesis (which the data falsified).

**Risks (what to watch):**
- "Dark matter" is a metaphor borrowed from cosmology; some reviewers dislike it. Mitigation: define it once,
  operationally ("case genes absent from both the mechanistic network and the OMIM-backed disease-gene
  compendium"), and use it consistently.
- 14 of 15 dark-matter genes carry `both` (D1+D2) case direction — so the dark-matter axis and the
  bidirectional-discordance axis are **correlated, not independent**. The paper must be clear which is the
  headline (recommendation below) and how they relate, or a reviewer will read circularity.
- Zero of 15 dark-matter genes resolve to an in-network gene (the one positional-pointer-to-in-network case,
  HERC2→OCA2, is a D'Arcy-*recoverable* gene, not dark matter). If the paper leads with
  "mislabeling," it overclaims. It must lead with the *decomposition*, of which mislabeling is one small,
  cited class.

**Recommendation:** Adopt a **two-level framing**, not a single slogan.
- **Headline (unchanged):** bidirectional genotype→phenotype discordance (D1 + D2) on one signed network —
  this is the method and the payoff loci (TYR, OCA2) live here.
- **Second act (new spine):** "*What the network doesn't contain, and why*" — the dark-matter decomposition as
  the honest coverage audit that motivates the next stage. "Dark-matter association" becomes the framing for
  the **coverage/gap analysis**, sitting under the discordance headline, not replacing it.

This keeps the discordance result (which the whole network was built to test) as the lead, and uses
dark-matter association as the rigorously-decomposed coverage story that reaches the rest of the corpus.

## 4. IF adopted — what would need rewriting (evaluation only; not done yet)

Scoped so the PI can approve before any edit. In rough order of edit size:

1. **README.md** — the project's one-paragraph pitch currently leads with discordance only. Add the
   coverage/dark-matter second act; state the 4-way decomposition; correct any implication of 13 independent
   gene contributions (Kastelic=0 genes, TYRP1×3 = one gene).
2. **project_dashboard.md** — §2 (project framing) and §4/§5a (active plan) need the two-level framing recorded
   as a locked decision; the dark-matter decomposition table (6/3/2/4) added; the "mislabeled-pointers
   hypothesis FALSIFIED" result logged so nobody re-runs it.
3. **TODO.md** — under AGREED: "extend dark-matter ledger to all 15 genes with cited resolution class." Under
   NEEDS-PI-DISCUSSION: "adopt two-level framing?"; "add new GWAS associations (Crawford / GWAS Catalog ≥2×
   replicated) as dark_matter_association loci?" (your question below — flagged, not assumed).
4. **FINDINGS_darcy_coverage.md** — add the per-paper mapping (§2) so the finding is corpus-wide, not
   Ang-centric.
5. **internal/RESEARCH_SYNTHESIS_locus_resolution_mvp.md** — already carries the decomposition; add the
   per-paper cluster table.
6. **Notebook 04** — its framing prose is coverage-only already; add a short "where each paper fits" cell if
   the corpus-wide framing is adopted.

Docs NOT affected: the network build notebooks (01/02), NB3 case assembly, the D'Arcy spec — those are data
provenance and are framing-neutral.

## 5. On bringing in NEW associations (Crawford beyond what we have / GWAS Catalog ≥2× replicated)

You asked whether we want other GWAS associations, and you like the "dark_matter_association" edge type. These
fit naturally: the integration schema (Track C) already defines `dark_matter_association` as an edge_type for
"association exists, resolution does not." Adding GWAS Catalog hits replicated ≥2× as `dark_matter_association`
loci (under the nearest-gene-vs-causal discipline: rsID identity, positional label, cited) is the concrete way
to grow the coverage audit corpus-wide. BUT this is a scope expansion that needs your explicit sign-off — it is
listed under NEEDS-PI-DISCUSSION, not started. Recommended sequence: land the 2-example MVP first, then decide
whether to widen the net to GWAS Catalog. Crawford specifically: MFSD12 is already captured; its additional
value is the *mechanism* (expression modulation) as a worked "genuinely-novel" example — cheap to add, high
illustrative value.

## 6. Decision requested
- (a) Adopt the two-level framing (discordance headline + dark-matter-association coverage spine)? Or keep
  discordance-only and treat dark matter as a subsection?
- (b) If adopted, authorize the doc rewrites in §4 (I will route them through PROJECT_MANAGER + the review
  gates, not edit ad hoc).
- (c) Authorize widening to GWAS Catalog ≥2×-replicated associations as `dark_matter_association` loci — or
  hold until after the MVP?
