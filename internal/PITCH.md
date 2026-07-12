# PITCH — pigmentation gene-network rescue screen

**Living document — updated as each notebook lands. Last update: 2026-07-12 (flagship framing SOFTENED — the direction result (NB10+NB12) is a bounded methodological demonstration, not a settled biological flagship; a primate-phylogenetics direction is under parallel exploration; framing is up in the air).**

## The flagship — leading candidate, framing under active evaluation

> **⚠️ FRAMING IS UP IN THE AIR (2026-07-12).** The candidate below is a strong *demonstration*, not a settled
> flagship. A literature check found that almost every biological *piece* of it is textbook (see "What is
> genuinely ours" below); the PI is also actively exploring a **primate-phylogenetics** evolutionary direction
> that could become the flagship instead. Treat this section as the leading candidate under active evaluation,
> not a locked decision.

**A convergence-graded direction demonstration (NB10 + NB12): a functional melanin screen orders the
*direction* of Mendelian pigmentation disorders, conditioned on allele mechanism — and its failures are
bounded, not random.** A gene that is a **positive regulator of melanin** (its loss reduces pigment), mutated by
a **loss-of-function** allele, tends to cause **hypo**pigmentation. On the loss-of-function subset with a
network-derived direction call the prediction is **22/22** recessive/X-linked genes (base rate 54%, permutation
*p* < 1×10⁻⁵); a pre-registered expansion adding a blind mechanism-classification source takes it to **29/33**,
and — more interestingly — locates the **edge**: the four misses are all genes acting through *systemic* routes
(Wilson-disease copper; ACTH endocrine feedback), and a phenotype-blind classifier flags three of the four in
advance by its own confidence (the fourth, *ATP7B*, it misses).

**What is genuinely ours — and it is narrow.** The biology is largely known: "LoF of a positive melanin
regulator → hypopigmentation" is close to the *definition* of oculocutaneous albinism; the allele-mechanism
conditioning is documented per-gene (dominant *TPC2* gain-of-function albinism; the *TYR* allelic series); and
Bajpai et al. (2023) already tied the screen's regulator sign to common-variant skin color. The contribution is
**methodological, not a discovery about pigmentation**: a *single* convergent functional readout orders a
clinical property across a whole disease category with a quantified null, and its failure boundary is partly
characterizable in advance. That is the project's "grade trust by evidence convergence" thesis made concrete,
quantified, and bounded — reported as such, and deliberately **not** as a new law of pigmentation genetics.

**Honest limits kept front-and-center.** The failure-boundary story rests on **n = 4** discordances and one
(*ATP7B*) breaks the "confidence flags misses" reading; the prediction is near-circular for core melanogenesis
genes; the core-vs-syndromic split reduces but does not eliminate ascertainment (the syndromic stratum is mostly
partial-albinism trafficking genes). A validity audit and the full literature audit are in
`internal/deconvolutor/` and `notebooks/12_direction_law_expanded.ipynb`.

**The rescue-screen work (NB4–NB9) is the methodological backbone this stands on**, not a competing headline —
see the two supporting threads below. Together they compose: the rescue screen resolves *which* gene a locus
acts through; the direction demonstration says *which way* the phenotype moves once the gene and its allele
class are known.

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
3. **What is the flagship?** — UP IN THE AIR (under active evaluation; a primate-phylogenetics direction is also
   being explored). The leading demonstration candidate is the **convergence-graded direction result**
   (NB10 + NB12; see "The flagship" above): a functional melanin screen orders the *direction* of Mendelian
   pigmentation disorders under a loss-of-function allele — 22/22 network-called genes, 29/33 after a
   pre-registered expansion (base rate 54%, permutation *p* < 1×10⁻⁵), audited and robust against the study-bias
   confound. Its value is **methodological**, not a biological discovery: a literature audit
   (`notebooks/12_direction_law_expanded.ipynb`) confirmed the biological pieces are textbook, but the
   *systematic, quantified, boundary-characterized* demonstration is not stated elsewhere. Supporting this are
   the rescue-screen results, which are the *how we do honest due diligence* backbone: the **Bajpai orphan
   reconciliation** (NB9 — 93/142 CRISPR orphans reconnect
   to the melanogenesis core once the STRING seed is symmetric, vs 0/142 under the curated-only seed; 92/93 are
   grade-C single-association paths, an honest knowledge-gap residue) and THREE "the choice changes the answer"
   results: **network source** (NB5, 66%/34% STRING drift), **tissue** (melanocyte vs bulk eQTL retracts 3
   causal calls), and **seeding** (0 vs 93 orphans). The association-locus rescue screen yielded no novel
   effector — reported honestly as a negative, and as the credibility backdrop the direction law stands on.

**Second thread — corrected association-locus rescue (effector-question, non-circular).** The foundation was
   fixed: 131 loci re-classified by whether the *associated gene is the effector* (not whether a variant was
   annotated). 80 point at canonical effectors (excluded — that was the PI's first-project variant-gap
   question; HERC2 rs12913832 etc. had been wrongly tagged); **34 effector_uncertain + 7 ambiguous_near** are
   the real non-canonical target set (**51 candidate genes** after rolling up to gene level). With those
   candidates *in the STRING seed* (the seeding lesson applied again), the connectivity — counted directly
   from the frozen pull (`data/external/db_responses/string_union_plus_candidates_pull_v12.json`) — is thin
   and reported as such: **28 of 51 have at least one STRING edge; 6 have a direct edge to a melanogenesis-core
   gene** (AHCY, ATRN, EGFR, LRMDA, SPIRE2, USP35 — e.g. SPIRE2→MYO5A score 0.96, ATRN→ASIP 0.83, the mahogany
   axis as a network edge); **23 are fully isolated with no STRING edge at all, MFSD12 among them**. These are
   STRING *associations from the nearest-gene label*, not independent confirmation that the nearest gene is the
   effector — STRING supplies candidate wiring, the association is the anchor. The isolation of MFSD12 is the
   seeding lesson a fourth time: coverage limit, not absence of biology (Crawford proved MFSD12 by knockdown).
   **Cross-paper convergence** (independent replication across ancestries): MFSD12 (Ang/Crawford/Kim — 3
   populations, coding), SPIRE2 (Kim/Morgan), TSPAN10 (Abbatangelo/Morgan).

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

Lineage the contribution sits within (systems / population-genetics of selection on gene networks): the
Fagny & Austerlitz network-approaches line, Daub et al. on polygenic selection across biological pathways,
the Gouy et al. `signet` gene-network selection framework, and the network-propagation family. These are
positioning anchors to be resolved to full citations (DOI/PMID) at manuscript stage — they are not cited as
evidence for any result in this repo.

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
