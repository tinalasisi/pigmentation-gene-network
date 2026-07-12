# PITCH — pigmentation gene-network rescue screen

**Living document — updated as each notebook lands. Last update: 2026-07-12 (NB10 mechanism→direction law promoted to PRIMARY flagship after a validity audit; rescue-screen threads repositioned as methodological support).**

## The flagship (one finding, layered evidence)

**A mechanism→direction law (NB10): a functional melanin screen predicts the *direction* of Mendelian
pigmentation disorders, conditioned on allele mechanism.** A gene that is a **positive regulator of melanin**
(its loss reduces pigment), mutated by a **loss-of-function** allele, causes **hypo**pigmentation; a negative
regulator causes hyperpigmentation. The rule is defined *only* under a loss-of-function allele — that condition
is the finding, not a caveat: it names exactly when a functional screen's sign transfers to a clinical
phenotype. On the loss-of-function subset the prediction is exact — **22/22** recessive/X-linked genes — against
a base rate of only 54% hypopigmentation (permutation *p* < 1×10⁻⁵). Every dominant "exception" breaks the
loss-of-function assumption in a documented way, and *TYR* flips direction *within one gene* across its allelic
series (recessive OCA1 albinism → hypo; dominant melanoma-susceptibility allele → hyper).

This is the project's convergence thesis made **directional and predictive** on its cleanest substrate. It is
robust against the study-bias confound that the project's own audits retracted a finding over: its strongest
evidence line is the **literature-independent Bajpai CRISPR screen** (which alone predicts 19/19), and the
signed network contributes **no** sign from STRING (the retracted-finding resource). A dedicated validity audit
(`internal/deconvolutor/`) confirmed the loss-of-function condition is assigned blind to direction, no gene was
silently excluded, and significance survives collapsing shared-complex genes to independent units
(*p* ≈ 3×10⁻⁶ at 15 units). Two honest framings the audit fixed: lead with the CRISPR line (the three "sources"
are really ~2.5, since two share MITF/SOX10/PAX3 logic), and state 22/22 as the predictive claim with the
dominant mechanisms as post-hoc interpretation.

**The rescue-screen work (NB4–NB9) is the methodological backbone that makes this credible**, not a competing
headline — see the two supporting threads below. Together they compose: the rescue screen resolves *which* gene
a locus acts through; the direction law says *which way* the phenotype moves once the gene and its allele class
are known.

## The three pitch answers (keep current)

1. **What did Claude Science help us do?** — curate author-explanation status of 105 loci from full PDFs;
   assemble a multi-layer substrate with per-edge provenance; resolve unexplained loci to causal genes in the
   right tissue; grade rescues by convergence — at weekend scale, fully reproducible.
2. **How are we closer to a finding?** — HONEST STATUS (2026-07-12, overnight): the network-rescue screen, run
   correctly on the effector-uncertain set with tissue-correct (melanocyte) eQTL, did NOT yield a novel
   network-discovered effector. What DID hold up is a **methodological finding**: melanocyte-vs-bulk eQTL
   correction retracts false bulk-skin causal-gene calls (TECRL, RAB11FIP2, CCND1) — *the tissue you resolve in
   changes the answer*, a sibling of NB5's "the network you choose changes the answer." Plus the foundation
   correction itself (the effector-question vs variant-gap distinction). The pure "rescue" thesis needs the
   careful per-paper re-extraction (internal/REEXTRACTION_PLAN.md) before it can be judged fairly.
3. **What is the flagship?** — the **mechanism→direction law** (NB10, primary; see "The flagship" above): a
   functional melanin screen predicts the *direction* of Mendelian pigmentation disorders under a
   loss-of-function allele — 22/22 recessive/X-linked genes, vs a 54% base rate (permutation *p* < 1×10⁻⁵),
   audited and robust against the study-bias confound. A prior-art review (`internal/deconvolutor/`) confirmed
   this compound, CRISPR-anchored, allele-conditioned predictive law is unstated in the literature — the pieces
   are known, the formalization is not. Supporting this are the rescue-screen results, which are the *how we do
   honest due diligence* backbone: the **Bajpai orphan reconciliation** (NB9 — 93/142 CRISPR orphans reconnect
   to the melanogenesis core once the STRING seed is symmetric, vs 0/142 under the curated-only seed; 92/93 are
   grade-C single-association paths, an honest knowledge-gap residue) and THREE "the choice changes the answer"
   results: **network source** (NB5, 66%/34% STRING drift), **tissue** (melanocyte vs bulk eQTL retracts 3
   causal calls), and **seeding** (0 vs 93 orphans). The association-locus rescue screen yielded no novel
   effector — reported honestly as a negative, and as the credibility backdrop the direction law stands on.

**Second thread — corrected association-locus rescue (effector-question, non-circular).** The foundation was
   fixed: 131 loci re-classified by whether the *associated gene is the effector* (not whether a variant was
   annotated). 80 point at canonical effectors (excluded — that was the PI's first-project variant-gap
   question; HERC2 rs12913832 etc. had been wrongly tagged); **34 effector_uncertain + 7 ambiguous_near** are
   the real non-canonical target set. With those candidates *in the STRING seed* (the seeding lesson applied
   again), **25 of 49 connect to the melanogenesis core** via high-confidence paths — e.g. SPIRE2→MYO5A,
   ATRN→ASIP (mahogany biology as a network edge), OPN4→FOS→MITF. **Cross-paper convergence** (independent
   replication across ancestries): MFSD12 (Ang/Crawford/Kim — 3 populations, coding), SPIRE2 (Kim/Morgan),
   TSPAN10 (Abbatangelo/Morgan). CAVEAT (the seeding lesson a fourth time): 21 candidates incl. **MFSD12**
   have NO high-confidence STRING edges at all — coverage limit, not absence of biology (Crawford proved
   MFSD12 by knockdown). These are association hypotheses; STRING supplies candidate wiring, the association
   is the anchor.

**Third thread — cross-ancestry population-conditional discoverability (NB11).** Some pigmentation genes are
   reported by different-ancestry GWAS through DIFFERENT, population-private variants — each common only where
   it was found, so a single-population study is blind to it. Quantified with Hudson Fst vs a 552-variant
   genome-wide 1000G baseline (mean 0.086; matches Bhatia 2013 continental ~0.10–0.12): 4 convergent genes
   (MFSD12, BNC2, SPIRE2, TSPAN10). **MFSD12 rs10424065 (African-discovery) Fst=0.26 = 96th percentile**; its
   mirror partner rs2240751 (EAS/Kalinago) peaks in the opposite populations; LD-independence CONFIRMED for the
   MFSD12 and BNC2 pairs (Ensembl pairwise LD empty across superpops). A systematic screen of 28 multi-ancestry
   catalog genes shows the mirror+Fst signal is strongest at canonical highly-differentiated loci (OCA2 Fst
   0.69, SLC24A5 0.51 — positive controls firing) and weaker at non-canonical ones. Martin 2017 KhoeSan adds a
   third population axis (SLC45A2 rs16891982 EUR 0.98 / San 0.14 / W.AFR 0.00). HONEST: MFSD12 is a KNOWN
   effector — this is cross-population PORTABILITY, not novel effector discovery; and Martin's non-canonical
   loci are mostly suggestive (high p), as that paper itself states. This is the project's original
   population-conditionality thesis, made quantitative. GWAS Catalog pull widened to recover REPORTED GENE(S)
   and split initial/replication ancestry (the merged version hid 21 discovered-in-one/replicated-in-another
   associations).

**The flagship in detail — the mechanism→direction law (NB10; the one clean *positive* result).**
Independent of the rescue screen entirely, on the cleanest substrate the project has (high-penetrance Mendelian
disorders). A gene that is a **positive regulator of melanin** — read independently from the Bajpai CRISPR
screen, the NB6 GRN sign, and the NB7 signed network — causes **hypopigmentation** when mutated by a
**loss-of-function** allele. Result: **22 / 22** recessive/X-linked genes with a direction call are concordant,
against a loss-of-function base rate of only **54 %** hypopigmentation (permutation *p* < 1×10⁻⁵; Fisher
loss-of-function-vs-dominant *p* ≈ 1×10⁻³). All **6** dominant discordances have a documented
non-loss-of-function mechanism (*TYR* melanoma-susceptibility allele vs recessive OCA1 albinism — the rule
flips direction *within one gene* across its allelic series; *CDKN2A*/*KIT* proliferative; *PSENEN*
Notch/keratinocyte; *BNC2* developmental; *FASLG* acquired). **Why this is the strongest positive claim we
have:** unlike the other threads it is not a caution or a reconciliation — it *predicts which way the phenotype
goes* and names the exact condition (loss-of-function allele) under which the prediction is valid, plus its own
falsification rule (positive regulator + hyperpigmentation ⇒ look for a non-loss-of-function allele). It is
**robust against the STRING study-bias confound** — its strongest evidence line is the literature-independent
CRISPR screen — which is the bar that retracted the project's earlier degree-based finding. It composes with
the rescue screen: that screen says *which* gene a locus acts through; this law says *which direction* the
phenotype moves once the gene and its allele class are known. (Two probes run alongside — cancer-gene
pleiotropy and the layer-convergence prior itself — both came back honest negatives dominated by STRING study
bias; the convergence-prior probe shows the project's own "more layers = more real" assumption is largely
circular unless the layers are genuinely source-independent, as NB10's function-vs-clinic design is. Full
comparison in `FINDINGS_MEMO.md`.)

## Positioning

Within the systems-population-genetics lineage. This rescue/convergence contribution is **distinct** from the
R21's gene-property prediction — it is not "not novel."

> _Suggested anchor references (from the PI's final-day directive §9, NOT yet verified against the papers in
> this repo — confirm each citation before it goes in any public deliverable): Fagny & Austerlitz 2021;
> Daub 2013; signet / Gouy 2017; the network-propagation family._

## Progress (notebook by notebook)

| NB | Question | Key result | Status |
|----|----------|------------|--------|
| NB4 | Unified association base | 105 curated → **52 author-unexplained** → **27 also GWAS-Catalog-replicated** (replicated + off-canonical + author-unexplained = the rescue targets). `gwas_replicated` is an additive convergence annotation, never a gate. | ✅ |
| NB5 | Compare candidate networks | Bajpai CRISPR added as a node layer (142 orphan hits in no curated network); networks-typology table; **"the network you choose changes the answer"** — our STRING pull recovers 60% of Raghunath's edges, agrees only 66% with D'Arcy's frozen STRING (34% drift). | ✅ |
| NB6 | Gene regulatory network | **58 curated-regulon TF→target edges** (MITF 34, PAX3 19, SOX10 5), directed + signed, DoRothEA A–E tiered, every edge cited. MITF directly activates 8 core pigmentation genes. No ChIP-seq peaks (binding≠regulation). | ✅ |
| NB7 | Harmonized multi-layer substrate | Merge all layers into one tagged node/edge table, per-edge provenance + tier; resolve the STRING enzyme-class-token artifact. | 🔄 building |
| NB8-diag | **Rescue diagnostic (the honest pivot)** | Ran the rescue test on the corrected ~18 effector-uncertain loci. **VERDICT: no novel network-discovered effector.** 5 connect non-circularly but none is a discovery (LRMDA=OCA7 mislabeled; SIK1/ATRN=known MC1R-axis biology at weak loci; EGFR=GRN route at null locus; CCND1=bulk-only, retracted). 6 honest negatives. **The real result: melanocyte-vs-bulk eQTL correction retracts 3 false causal-gene calls — using the wrong tissue manufactures false effectors.** | ✅ diagnostic |
| NB8 | Hero shortlist | ON HOLD — no hero to surface until the foundation is fixed and a genuine connection exists. | ⏸ blocked |
| NB9 | Bajpai orphan reconciliation | Symmetric 714-gene STRING pull reconciles **93 of 142** CRISPR orphans to the melanogenesis core (≤4 hops, score≥700) vs **0/142** under the curated-only seed — the "seeding changes the answer" result; 49 stay orphan as the honest knowledge-gap residue (92/93 are grade-C single-association paths). | ✅ |
| NB10 | Mechanism→direction law | **Flagship candidate (the one clean positive result).** Positive melanin regulator + loss-of-function allele → hypopigmentation: **22/22** recessive/X-linked concordant vs 54% base rate (permutation *p*<1e-5; Fisher LoF-vs-dominant *p*≈1e-3); all 6 dominant discordances have documented non-LoF mechanisms (*TYR* flips within its allelic series). Three independent direction sources (CRISPR/GRN/signed-net) agree; robust against STRING study bias. | ✅ |

## Honest-count discipline

Report the count as measured; do not force a headline. The Reactome-reaction rescue class is gated on
sub-pathway tags: **29 pigmentation-tagged reported separately from the 92 MITF-program genes** — never one
inflated "N of 121." GWAS replication is an additive convergence line, never a candidate filter. Bajpai
corroboration is asymmetric — "not a hit" is not evidence against.
