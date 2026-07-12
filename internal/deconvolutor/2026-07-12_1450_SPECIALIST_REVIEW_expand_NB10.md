# Specialist review — should we expand NB10? (verdict + full reports)

_Convened 2026-07-12. Three specialists, run in dependency order: prior-art gate → (beta scoping ∥ plan critique)._

## Headline

**Do NOT expand yet. Audit the existing n=22 result first; drop the GWAS option; keep any Mendelian expansion narrow and conditional.**
All three specialists independently converged on this. The prior-art gate says the finding is genuinely novel
(so it is worth protecting), but the plan critic's core point is that **the open question is validity, not
power** — expanding gene-list size optimizes the wrong variable, and the beta-scoping proved the GWAS axis
tops out at 2–3 clean genes.

---

## 1. Prior-art gate (GENETICS_LIT_REVIEWER) — verdict B: novel formalization

Searches across PubMed and OpenAlex (title/abstract/full-text, no year restriction) for every vocabulary translation given -- 'melanogenesis positive/negative regulator', genotype-to-hypo/hyperpigmentation direction, LoF-vs-GoF allele-conditioned phenotype direction, TYR allelic-series direction flips, signed-network/Boolean predictions of pigmentation direction, and CRISPR-melanin-screen-anchored disease-direction prediction -- turn up the building blocks of NB10's rule as separately established facts, but never the compound, quantified, allele-conditioned predictive law itself.

What IS established: (1) the general Mendelian-genetics principle that recessive loss-of-function phenotypes read out the gene's normal function (haploinsufficiency/dominance theory), articulated classically by Wilkie's 1994 review of dominance mechanisms (PMID 8182727) and echoed in Casanova's 2015 discussion of how gain-of-function vs loss-of-function alleles in the SAME gene produce opposite immunodeficiency phenotypes (PMID 25645939) -- but this is field-general (immunology, developmental genetics), not stated for pigmentation and not conditioned on an independent regulator-sign call. (2) The TYR allelic-series direction flip (LoF -> OCA1 albinism vs specific missense/promoter variants -> melanoma-risk or pigmentation-modifying alleles) is well documented piecemeal in melanoma-genetics and pigmentation-GWAS literature (e.g. the melanoma genetics reviews at doi 10.1101/gad.191999.112 and 10.1101/gad.1437206, and TYR/HLA-A vitiligo-risk work at doi 10.1038/jid.2012.37), but no paper states TYR as a worked example of a general allele-conditioned direction rule. (3) Melanogenesis 'positive vs negative regulator' terminology and MITF/SOX10/PAX3 GRN sign are standard descriptive vocabulary in pigment-cell biology reviews (Pavan & Sturm 2019, doi 10.1146/annurev-genom-083118-015230; the medaka/zebrafish Pax3/7-Sox10-Mitf GRN paper, doi 10.1242/dev.202114; Manga et al. 2025, doi 10.1111/ahg.70003) -- these establish the concept of regulator sign but never use it to predict a Mendelian disorder's direction. (4) The Bajpai et al. 2023 genome-wide CRISPR melanin-content screen (doi 10.1126/science.ade6289, PMID 37561850) is real and has 54 downstream citations as of this search; none of those citing works use its hit-direction sign to predict the direction of a human Mendelian pigmentation disorder, still less test that prediction against a permutation-derived base rate.

Critically, the closest existing OMIM-based curation of this exact gene set -- D'Arcy et al. 2023 (doi 10.3390/bioengineering10010013, PMID 36671585), which builds the 'pigmentation diseasome' by combining OMIM phenotype calls with the Baxter and Yamaguchi gene lists and OpenTargets, and classifies disorders into hyperpigmentation / hypopigmentation / mixed groups -- contains ZERO occurrences of 'loss-of-function', 'gain-of-function', 'recessive', or 'direction' in its full text, and only one incidental use of 'dominant'. It builds the same phenotype-direction labels NB10 uses but never conditions them on allele mechanism or tests them against an independently called regulator sign. No search (across the LoF-mirrors-function framing, the GRN/Boolean-model framing, the signed-network framing, or the CRISPR-anchored framing) returned a paper doing what NB10 does: independently calling regulator direction from a genome-wide functional screen plus a GRN sign plus a signed pathway model, restricting the disease-direction claim to LoF alleles only, and quantifying concordance against a permutation null over a >20-gene disease set.

**Novelty:** The novelty is in the formalization and the test, not in any single component. Every ingredient -- 'recessive LoF mirrors the gene's normal function', 'the same gene's GoF and LoF alleles can produce opposite phenotypes', 'melanogenesis has positive and negative regulators', 'TYR has an allelic series that flips direction' -- is independently known and cited above. What has not been done anywhere in the retrieved literature is: (i) calling regulator direction from THREE independent sources (a genome-wide CRISPR melanin screen, a GRN sign, and a signed/directed melanogenesis pathway model) rather than from qualitative pathway knowledge; (ii) explicitly restricting the direction claim to loss-of-function alleles (recessive/X-linked) and treating dominant genes with non-LoF mechanisms as expected non-applications rather than exceptions to explain away; (iii) quantifying concordance (22/22) against an empirical permutation-derived base rate (54% LoF->hypopigmentation base rate, p<1e-5) rather than asserting the rule qualitatively. This combination -- CRISPR-anchored, allele-conditioned, quantified against a null -- is the formalization that is genuinely unstated in the literature retrieved. Expanding to a larger disease-gene set tests a real, currently under-evidenced claim rather than re-deriving a textbook fact.

**Recommendation:** Expand. The individual mechanistic pieces (LoF mirrors function; allelic-series direction flips; melanogenesis has signed regulators) are established, but the specific CRISPR-anchored, allele-conditioned, quantified predictive law that NB10 proposes is not stated or tested anywhere in the retrieved literature -- this is verdict B, not A. A larger-n test is genuinely informative rather than re-deriving known biology. Two conditions should gate the expansion to keep the result honest: (1) build the larger gene set from OMIM phenotypic series or Orphanet with explicit per-gene inheritance-mode and LoF-mechanism annotation -- do not adopt the Baxter or D'Arcy lists wholesale, since both mix in genes without a confirmed human Mendelian LoF phenotype; (2) explicitly flag and, where feasible, sensitivity-test the ascertainment confound (curated pigmentation-gene lists preferentially include already-characterized regulators) -- e.g. by reporting concordance separately for core melanogenesis-pathway genes vs. syndromic/trafficking genes, so a reviewer cannot say the larger-n test just re-samples the same circularly-selected genes.

---

## 2. GWAS-beta scoping (GENETICS_DATA_EXTRACTOR) — viability: viable_core_genes_only

- Genes with an effect-allele-aligned pigmentation-GWAS beta: **12/35** (BNC2, CDKN2A, EDNRB, MC1R, MITF, OCA2, PAX3, PPP3CA, SLC24A5, SLC45A2, TYR, TYRP1)
- Clean (coding/missense) SNP→gene: **5** (SLC24A5, SLC45A2, OCA2, TYR, MC1R); the other 7 rest on nearest-gene — the retracted-finding failure mode.
- eQTL bridge that closes Bajpai↔eQTL↔GWAS: **1/35** (MC1R only, nominal significance, n=370).
- Proof of concept: **2–3 clean concordances (SLC24A5, SLC45A2, MC1R), 1 provisional (OCA2), 1 discordant (TYR)** — even the easy set is not uniformly clean.

**POC result:** POC table (nb11_gwas_beta_scoping_poc.csv, 5 rows) built for the 5 coding-variant candidates using gwas_associations_for_gene rows filtered to the 'Skin pigmentation'/'Skin color' trait family, cross-checked against eQTL Catalogue GTEx-skin and TwinsUK-skin (gene-level ge datasets QTD000311/QTD000316/QTD000544). Result: 3 of 5 are clean YES-concordant on GWAS allele sign alone (SLC24A5 rs1426654, SLC45A2 rs16891982, MC1R rs1805007) -- in each, the allele independently known in the literature as the reduced-function/LoF allele is also the GWAS-reported lighter-pigmentation allele, matching the positive-regulator prediction. MC1R additionally closes the full Bajpai-sign<->eQTL<->GWAS loop: rs1805007's T allele is the classic LoF 'red-hair' allele, is GWAS-associated with lighter skin (Fitzpatrick beta=-0.336, p=6e-14, GCST90255689), and shows a same-direction nominal skin eQTL (TwinsUK, beta=-0.243, p=0.022, n=370 -- NOT genome-wide significant, flagged accordingly). OCA2 rs1800414 is LIKELY concordant but the allele/strand correspondence to the literature-established functional allele was not independently re-verified in this scoping pass and is flagged rather than asserted. TYR rs1042602 is DISCORDANT/AMBIGUOUS in this pull: NB10's own annotation already marks law_applies=False for TYR, and the GWAS row used (GCST90255690, skin colour) has the A allele as darker, which conflicts with other literature calling A a mild-hypofunction (lighter-associated) allele -- this is a live illustration of the project's known sign-alignment failure mode, not a clean success case. Bottom line: the sign-aligned comparison works cleanly on 2-3 of the 5 'easy' genes (SLC24A5, SLC45A2, MC1R), is provisional on 1 (OCA2), and actively fails/is ambiguous on 1 (TYR) even among the best-case coding candidates -- so even the easy set is not uniformly clean.

**Confounds:** (1) Independent-literature functional-allele calls (which allele is 'LoF' for SLC24A5/SLC45A2/OCA2/MC1R) were drawn from established prior knowledge, NOT re-verified against a fresh, resolvable citation in this scoping pass -- a full extraction must pull an explicit functional-characterization citation (not GWAS Catalog) for each allele-to-function call, or the sign-alignment claim rests on an untraced assertion, which is the exact failure mode that produced the prior retraction. (2) Strand/allele-coding mismatches between GWAS Catalog's forward-strand allele and the coding-sequence allele used in functional papers are a known trap (ambiguous for A/T and C/G SNPs) and were not exhaustively checked here. (3) Multiple traits per gene (e.g. OCA2 has 168 clean pigmentation associations) require an explicit trait-selection rule for a real extraction -- this scoping pass picked one representative row per gene by a simple trait-name priority list, which is not sufficiently principled for a production table. (4) Population/ancestry heterogeneity: the clean-beta rows pulled are overwhelmingly European-ancestry UK Biobank studies; Crawford2017 African-ancestry skin loci are NOT present in this GWAS-Catalog gene-mapped pull at all, meaning any full build must source the African-ancestry comparison from the project's own curated tables (discordance_loci / locus_causal_resolution) rather than GWAS Catalog gene lookups, and keep it in a separate stratum. (5) eQTL bridge coverage is very thin (1/5 candidate genes, and that one hit is only nominally significant, n=370) -- absence of a self-gene eQTL hit for SLC24A5/SLC45A2/OCA2/TYR in this pass reflects the specific single-variant queries run, not a systematic sweep of the full eQTL Catalogue (other datasets/tissues, or a region-based rather than single-variant eQTL query, were not exhausted) -- true bridge availability is unresolved, not proven absent. (6) The TYRP1 case shows a locus-identity risk: the L2G-confirmed TYRP1 signal (Abbatangelo2026, eye-colour) and the beta-bearing TYRP1 signal used here (melanoma/phototype, rs2762461) are different variants that were not checked for LD/same-causal-signal -- silently treating them as interchangeable would repeat the nearest-gene-substitution error.

---

## 3. Plan critique (PLAN_DECONVOLUTOR) — partial kill

**Which option is better:** Neither is the right next move, and if forced to rank: Option 1 is the more
defensible use of any further effort, but only in a heavily descoped form, and Option 2 should be shelved, not
merely sequenced after Option 1.

Option 2's feasibility scoping has ALREADY returned an answer, and it is close to a "no" for a hackathon
timeline: 5 genes with clean SNP-to-gene assignment out of 35, 1 gene (MC1R, nominal significance only) that
actually closes the three-way sign-alignment loop the option is supposed to demonstrate, and TYR -- one of the
5 "clean" candidates -- already discordant. That is not a proof-of-concept to build out; it's a proof that this
axis tops out at n=2-3 clean genes, which is less powered than the n=22 result it's meant to strengthen, while
carrying strictly more directionality-error surface (allele/strand harmonization, LD/colocalization, trait-
polarity mismatch across ancestries) than the Mendelian axis. Pursuing it further spends hackathon time
recreating, in a new domain, the exact sign-error and nearest-gene failure modes this project has already been
burned by once.

Option 1 could, in principle, move the result from "striking at n=22" to "powered," but the two conditions the
prior-art gate itself attached (re-curate from OMIM/Orphanet with explicit annotation; split core-pathway vs
syndromic concordance) are the two things most likely to either dilute or break the headline -- and neither
addresses the deeper problem, which is validity, not power: whether the regulator-sign axis and the "3
independent sources" claim are actually independent of each other and of the clinical labels they're being
tested against. Spending effort on gene-list size when the open question is circularity is optimizing the wrong
variable.

The two are not usefully complementary as a "one-then-the-other" sequence in the order proposed. If anything is
done next, it should be neither option as scoped, but a cheap internal audit of the CURRENT n=22 result (see
endorsed plan below) -- because both options inherit that result's unaudited weak leg (Bajpai-sign
provenance, GRN/network non-independence, denominator framing), and any work built on top before that audit
may need to be redone or abandoned once it lands.

**Kill recommendation:** Partial kill, not full kill. The n=22 Mendelian result is genuinely the
project's strongest finding and doesn't need expansion to be reportable -- as a hackathon deliverable, "22/22
with an honestly-stated small n, a stated falsification rule, and a documented non-LoF exception mechanism for
every discordance" is already a complete, defensible, well-scoped result. Do not expand it purely to chase a
bigger n; that mostly adds confound surface (diluted single-source genes, non-portable null, complex-subunit
non-independence) without addressing the one thing that would actually strengthen it, which is a validity audit,
not a power increase.

Kill Option 2 outright for this hackathon. Its own feasibility scoping already came back essentially negative
(2-3 clean demonstration genes, one of which -- via TYR -- is discordant), and pursuing it further trades scarce
remaining time for a near-certain re-run of the project's own retracted nearest-gene / sign-error failure mode
in the GWAS domain.

If time remains after the cheap audit in the endorsed plan, spend it hardening the presentation of the existing
n=22 result (honest denominator framing, complex-collapsed significance, an explicit statement of what would
falsify the law) rather than on either expansion option.

**Endorsed cold plan:** Read cold, with no memory of how this got here, the simplest defensible plan is NOT
"pick Option 1 or Option 2 and build it out." It is a single, cheap step: audit the finding that already exists
before spending any further specialist-dispatch cycles scaling or extending it.

1. AUDIT THE CURRENT n=22 RESULT (half a day, no new data pull): (a) recompute the permutation p-value with
genes collapsed by shared protein complex (BLOC-1/2, HOPS/BLOC-3) rather than treated as 22 iid draws, to get an
honest effective-n; (b) check whether the signed-network (NB7) and GRN (NB6) edges were built independently of
the Mendelian phenotype labels they're being tested against, and whether they share build lineage with the
STRING resource behind the retracted degree finding; (c) report the true denominator (22/28 with exceptions
explained, not 22/22) and confirm the 6 exceptions' mechanisms were assigned blind to direction; (d) report
whether any gene was excluded for indeterminate sign, and how many.

2. ONLY IF (1) SURVIVES CLEAN: do a narrowly-scoped version of Option 1 -- not a full OMIM-phenotypic-series/
Orphanet re-curation, but pulling maybe 15-20 additional genes specifically chosen to test the core-pathway-
vs-syndromic split the gate demands, pre-registering the source-priority rule for sign conflicts before looking
at any new gene's direction call.

3. DROP OPTION 2 for this hackathon. The feasibility scoping already answered the question it was meant to
answer: 5/35 genes with unambiguous SNP-to-gene assignment, 1/35 closing the full sign-alignment loop (at
nominal significance only), and TYR already discordant among the "clean" candidates. That is a scoping verdict,
not an open question -- proceeding would spend remaining time re-encountering the project's own retracted-
finding failure mode (nearest-gene assignment, unverified allele/strand harmonization) in a new domain, for a
demonstration set too small to report as anything beyond an anecdote.

What I would NOT do: run a parallel data-extractor scoping pass and a parallel adversarial red-team on two
expansion options before auditing the thing both options are built on top of. That ordering spends effort
racing to scale a result whose internal validity hasn't been checked, and it is exactly backwards -- audit
first, because a negative audit result invalidates work already done on either expansion track, and a positive
one tells you Option 1's narrow version is worth a half-day, not a full re-curation.

### Must-answer questions before committing to ANY expansion
1. Was the non-LoF-mechanism explanation for each of the 6 dominant discordances (TYR, CDKN2A, PSENEN, BNC2, KIT, FASLG) determined BLIND to the observed direction, or assigned post-hoc after seeing which genes broke the pattern? This determines whether '22/22' or '22/28-with-6-explained-exceptions' is the honest framing.
2. Were any candidate genes dropped from the n=22/28 set for having no usable/indeterminate sign call from any of the 3 sources, and if so, how many, and were they tabulated anywhere? Silent exclusion of indeterminate-sign genes is a survivorship-bias channel distinct from (and not fixed by) curation-depth ascertainment.
3. Does the 'signed-directed melanogenesis network' (NB7) share a database/build lineage with the STRING-based network implicated in the retracted degree finding? If signed edges for well-studied genes (OCA2/TYR/MC1R) are more complete or more confidently signed than for sparsely-annotated trafficking genes, that is the identical failure mode inside a layer currently being counted as an independent source.
4. Were any GRN-sign or signed-network edges curated or sanity-checked against known Mendelian mutant phenotypes during their original construction? If so, testing NB10 against those same phenotypes is partly definitional, not predictive, for the genes carrying only those two sign sources.
5. For the ~12 non-CRISPR-covered genes, is GRN sign architecturally independent of signed-network sign, or do both trace to the same MITF/SOX10/PAX3-centered logic? If the latter, the claimed 'agreement across 3 independent sources' should be reported as ~1.5 sources for that tier.
6. Could the Bajpai CRISPR 'positive regulator' call for any gene reflect a general fitness/viability effect (essential-gene knockouts reducing melanin readout for non-mechanistic reasons) rather than a true melanogenesis-regulation effect? This risk concentrates exactly in the ~12 genes with Bajpai-only sign support.
7. Is the true count of independent genetic units behind the LoF n=22 closer to 22, or closer to 8-10 once shared-complex genes (BLOC-1/2, HOPS/BLOC-3 subunits: the HPS and CHS genes) are collapsed to one test per complex? The reported p<1e-5 assumes iid draws that this may violate.
8. Given the GWAS-beta scoping has already returned (5/35 genes with clean SNP-gene assignment, 1/35 closing the eQTL loop, TYR discordant even among the clean set) -- is there still a case for treating Option 2 as open, or does this scoping result alone settle it as not worth further investment for a hackathon deliverable?
9. If any further work is done, what is the actual remaining hackathon time budget, and is there enough of it left to REACT to a negative result from the gate-mandated core-vs-syndromic sensitivity split (i.e., to soften/restructure the headline claim), or would all remaining time already be spent on the curation step that produces that split?

### Option 1 (larger Mendelian set) failure modes
OPTION 1 (larger Mendelian/OMIM set) has five distinct failure modes, in order of severity:

1. THE GATE'S OWN ESCAPE HATCH REINTRODUCES ITS BANNED CONFOUND. Condition (1) says build from OMIM phenotypic
series / Orphanet "with explicit per-gene inheritance + LoF-mechanism annotation." But that annotation exists
in curated, extractable form precisely for genes that are already well-studied -- the same ascertainment
channel that produced D'Arcy/Baxter. The confound isn't removed, it's moved one step upstream and made harder
to see.

2. THE REGULATOR-SIGN AXIS DOESN'T SCALE WITH THE DISEASE-GENE AXIS. Expanding the OMIM/Orphanet side to n=60-100
does nothing if direction-of-effect still bottlenecks through ~10 CRISPR-covered genes, a fixed 3-TF GRN
(MITF/SOX10/PAX3), and one signed network. New genes will disproportionately enter as single-source calls
(exactly today's pattern: HPS/CHS trafficking genes get their "positive regulator" label ONLY from
bajpai_effect, no independent confirmation) -- the denominator grows, evidentiary quality per gene shrinks, and
you dilute rather than power up.

3. THE CORE-VS-SYNDROMIC SPLIT THE GATE MANDATES MAY SHATTER THE HEADLINE, AND THE PLAN HAS NO STATED REACTION
PLAN FOR THAT. If concordance is near-ceiling for multi-source core-pathway genes (OCA2/MC1R/TYRP1) but weaker
or noisier for single-source trafficking genes, that split is not "same law, two subpopulations" -- it is the
CRISPR screen's own hit-calling driving the appearance of a mechanistic law in exactly the genes it was used to
label. That is structurally identical in shape to the retracted network-degree finding: a variable (screen/
literature coverage) correlates with both "gets called a regulator" and "gets called concordant."

4. THE PERMUTATION NULL DOESN'T PORT, AND THE EFFECTIVE N IS SMALLER THAN IT LOOKS. The 54% base rate must be
re-derived from the expanded set's own inheritance mix, not reused. Separately, HPS1-HPS11/BLOC1S3-6 and
LYST/CHS1 are not 22 independent tests -- they largely encode shared trafficking complexes (BLOC-1/2,
HOPS/BLOC-3), so the permutation test's iid-Bernoulli assumption overstates the effective sample size for both
the current n=22 and any larger set built the same way.

5. THREE "INDEPENDENT" SOURCES MAY BE ONE. GRN sign and signed-network sign both plausibly encode the same
MITF/SOX10/PAX3-centered regulatory logic -- for the genes that carry only these two calls, the claimed
triangulation is closer to 1.5 independent sources than 3, and this is exactly the tier of genes an expansion
would add the most of.

### Option 2 (GWAS common-variant axis) failure modes
OPTION 2 (GWAS common-variant axis) has a feasibility problem that is worse than a
statistical risk -- the scoping run has ALREADY landed (GENETICS_DATA_EXTRACTOR, artifact
nb11_gwas_beta_scoping_poc.csv), and it is not a "pending" unknown, it is a verdict:

FEASIBILITY VERDICT ALREADY RETURNED: of the 35 NB10-annotated genes, only 12 have a GWAS pigmentation
association with both a reported effect and a resolved effect allele. Of those 12, only 5 have unambiguous
SNP->gene assignment via coding/missense consequence (SLC24A5, SLC45A2, OCA2, TYR, MC1R) -- the other 7 rely on
GWAS Catalog's positional nearest-gene pipeline, the EXACT mechanism that produced this project's already-
retracted finding. The eQTL bridge that would close Bajpai-sign <-> eQTL <-> GWAS into one non-circular loop
works for exactly ONE gene (MC1R), and only at nominal (not genome-wide) significance, n=370. Of the 5 clean
candidates, TYR is actively DISCORDANT in this pull -- which matches NB10's own law_applies=False flag for TYR,
but means the "closes the loop" demonstration set is really 2-3 genes, not 35 or even 12.

Additional risks on top of that ceiling:
1. DIRECTIONALITY IS NOT GUARANTEED EVEN UNDER A CORRECT MODEL. A common-variant eQTL that modestly lowers
expression of a positive regulator need not track a null allele's direction if the gene shows threshold/
non-linear dose-response near wild-type levels (plausible for developmental TFs).
2. ALLELE/STRAND HARMONIZATION ACROSS SOURCES (GWAS Catalog, Crawford 2017, eQTL panels) is a well-known silent
sign-flip risk, and the scoping data shows this happening already -- one TYR row in the pull disagrees with
another on which allele is "darker."
3. LD/COLOCALIZATION IS ASSUMED, NOT TESTED. Pigmentation loci (OCA2/HERC2 being the textbook case) are
LD-dense with multiple plausible causal genes; "same locus, same direction" without formal colocalization
(coloc/SuSiE) risks being an LD artifact, the same "correlated with something else, not biology" failure that
killed the degree finding.
4. TRAIT-POLARITY IS NOT PORTABLE ACROSS SOURCES. Crawford 2017 (African-ancestry skin pigmentation) is
confirmed NOT retrievable through the GWAS-Catalog gene-query route used for the scoping pass and must stay a
separate, unpooled stratum -- the "bridging Crawford 2017 + other project papers + GWAS Catalog" framing in the
option description overstates what one query pipeline can actually deliver.
5. NO NULL MODEL IS STATED for this axis at all (Option 1 at least has the 54% LoF base rate); without one, "the
directions mostly agree" is unfalsifiable in the same way the retracted finding was before anyone checked it.
