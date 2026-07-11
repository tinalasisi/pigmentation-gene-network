# Novelty-risk memo — the four most reviewer-exposed claims

_Author: GENETICS_LIT_REVIEWER. Session 2026-07-11. Reads against the prior-art map
(`2026-07-11_1308_PRIORART_MAP_cross_field.md`); every DOI/PMID here is connector-verified there._

**Purpose.** For each load-bearing novelty claim: the closest prior art found, the field and name it lives
under, and a candid verdict on whether the project's framing survives it — and if so, on exactly what
distinction. This is the document meant to pre-empt "you didn't read the literature; this exists under X."

The honest posture throughout: **the project's novelty is not the network-prioritization act, and not the
observation that background modifies penetrance. It is the specific combination — a signed, directed,
mechanism-only network, read bidirectionally (D1 blocking / D2 alternative-route), on a near-zero-environment
instrument (pigmentation), used to give a mechanistic account of prediction failure.** Each claim below is
strongest when it leans on that combination and weakest when stated in isolation.

---

## Claim 1 — "GWAS by node": a network-derived ranked list of candidate modifier genes
**Exposure: HIGHEST.**

**Closest prior art.** Lee et al. 2011, "Prioritizing candidate disease genes by network-based boosting of
genome-wide association data" (10.1101/gr.118992.110, PMID 21536720) — nearly a name match. Plus the whole
network-propagation / random-walk prioritization family (Li & Patra 2010, 10.1093/bioinformatics/btq108;
GeneMANIA, 10.1186/gb-2008-9-s1-s4). **Field name: network-based gene prioritization / network propagation.**
Field size ~10k–120k works.

**Verdict: does NOT survive as "a new kind of output."** A network-derived ranked candidate-gene list from
GWAS input is a 15-year-old, named, heavily-cited method. If the paper presents "GWAS by node" as a novel
object, a reviewer will name Lee 2011 immediately.

**What DOES survive, and how to state it.** Three distinctions, all defensible:
1. **Edges are signed and directed mechanism, not association.** Standard prioritization propagates over
   undirected association graphs (STRING/co-expression). The project forbids association edges and encodes
   activation/repression direction — so its ranking carries a *mechanistic why*, not a proximity score.
2. **Bidirectional read.** Prioritization methods rank "genes near the signal." The project additionally uses
   the graph to explain the *absence* of expected phenotype (D1) and the *presence* of unexpected phenotype
   (D2) — a use of network structure the prioritization literature does not make.
3. **Refusal to over-connect.** The nearest≠causal discipline (only resolved causal genes enter, only via
   mechanism) is a deliberate precision-over-recall stance that the boosting/propagation methods, which
   maximize coverage, do not take.
   **Recommendation:** retire "GWAS by node" as a headline novelty term; reframe as "a signed-mechanism
   network read of genetic architecture," and cite Lee 2011 + Li & Patra 2010 as the method lineage the work
   refines.

---

## Claim 2 — D1/D2 as a signed-network reachability formalism for discordance
**Exposure: HIGH.**

**Closest prior art.** Two distinct precedents. (a) *Concept of background-dependent penetrance*: Fahed et al.
2020, "Polygenic background modifies penetrance of monogenic variants" (10.1038/s41467-020-17374-3, PMID
32820175) — the flagship, plus Kingdom 2021 (10.1038/s41467-021-23556-4) and the 2023 kidney-disease paper
(10.1038/s41467-023-43878-9). (b) *Network framing of multi-locus architecture*: Hu et al. 2011, "Six Degrees
of Epistasis: Statistical Network Models for GWAS" (10.3389/fgene.2011.00109, PMID 22303403); Chandler 2013
(10.1371/journal.pgen.1003661) for the model-organism grounding that a mutation's effect depends on
background.

**Verdict: the phenomenon is well-established; the *signed-path formalism* appears genuinely under-occupied.**
"Genomic background changes whether a variant expresses" is mainstream (Claim survives NOT as a discovery).
But the field operationalizes background almost entirely as a **polygenic score** (a sum of small effects) or
as **statistical epistasis** (interaction terms). Reading D1 as *specific signed modifier nodes gating a
directed path*, and D2 as *alternative directed paths reaching the endpoint*, is a mechanistic-graph
formalism I did not find occupied for human discordance in the sweep.

**What survives, and the risk.** The mechanistic reading is the real novelty — but its exposure is to the
*Boolean/logical network* modeling tradition (CellNOpt, MaBoSS, SBML-qual), which formalizes exactly
"node-state gating of signaling paths." **This is the one framing where I would run a second, targeted search
before the paper claims novelty** (see gaps below): if a logical-model paper has cast penetrance as
path-blocking in a signed network, it is the closest competitor and did not surface under my
genetic-vocabulary queries. Recommend: state D1/D2 as "a signed-reachability reading of discordance," cite
Fahed 2020 (concept) and Hu 2011 (network-of-GWAS precedent), and explicitly position against polygenic-score
operationalization.

---

## Claim 3 — "Dark-matter association" coverage audit as a finding
**Exposure: MODERATE–HIGH.**

**Closest prior art.** Renaux et al. 2023, "A knowledge graph approach to predict and interpret disease-causing
gene interactions" (10.1186/s12859-023-05451-5, PMID 37644440); the oligogenic-prediction lineage
(Papadimitriou 2019, 10.1073/pnas.1815601116); and biomedical-KG guilt-by-association (Gema 2023,
10.1038/s41467-023-39301-y). **Field name: knowledge-graph completion / link prediction over gene–disease
graphs.**

**Verdict: survives, because the project's move is the opposite of the ML default.** The "which case genes are
absent from the network" question, stated as a task, IS knowledge-graph incompleteness — and a reviewer from
ML will say so. But the KG-completion literature *predicts the missing edges* (imputes plausible gene–disease
links). The project deliberately **refuses to impute** — it audits coverage, classifies the gaps into cited
mechanistic classes (positional-pointer / redirect / LD-passenger / genuinely-novel), and reports what is
*not* explainable rather than guessing it. That refusal, plus the falsified mislabeled-pointers test (a
negative result honestly reported), is a defensible contribution *against* the completion framing, not a
weaker version of it.
   **Recommendation:** frame the audit explicitly as "coverage accounting, not link prediction," and cite
Renaux 2023 as the contrasting KG-completion approach. The negative result (0/15 resolve) is an asset — lead
with it.

---

## Claim 4 — nearest-gene ≠ causal-gene as a discipline
**Exposure: LOW (risk is over-claiming, not being scooped).**

**Closest prior art.** Watanabe et al. 2017, FUMA (10.1038/s41467-017-01261-5, PMID 29184056, 4513c) and the
entire post-GWAS L2G subfield (Open Targets L2G, fine-mapping, eQTL colocalization, gene-based tests).

**Verdict: this is standard practice, not a contribution — and the paper should say so.** Going beyond the
nearest gene to the functionally-implicated gene is exactly what FUMA/L2G/colocalization do routinely. The
risk here is the *inverse* of the others: if the paper presents nearest≠causal as its own methodological
insight, a reviewer will point to a decade of L2G work.
   **Recommendation:** present it as an applied discipline the project *adheres to* (with the HERC2→OCA2
worked example as illustration), citing FUMA/L2G as the established practice — not as a novel principle. This
strengthens credibility rather than weakening the paper.

---

## Bottom line for the PI

| Claim | Survives as novel? | On what distinction |
|---|---|---|
| 1. "GWAS by node" ranked list | **No** (as an output type) | Survives only as *signed-mechanism, bidirectional, precision-first* refinement of a named method (Lee 2011). Retire the term. |
| 2. D1/D2 signed-path formalism | **Partially / likely yes** | Phenomenon is mainstream (Fahed 2020); the *mechanistic signed-reachability reading* is under-occupied vs polygenic-score operationalization. **Verify against logical-modeling literature first.** |
| 3. Dark-matter coverage audit | **Yes** | Survives *because* it refuses the KG-completion default (Renaux 2023); audit + honest negative result is the contribution. |
| 4. nearest≠causal | **No — and shouldn't claim to** | Standard L2G practice (FUMA 2017); present as applied discipline, not insight. |

**The strongest honest framing of the whole paper:** not "a new method to rank genes," but "a signed,
mechanism-only network of a clean-instrument trait (pigmentation), read bidirectionally to give a *mechanistic*
account of the discordance that the polygenic-background and PRS-portability literatures observe *statistically*
— with an explicit, honestly-audited boundary (dark matter) where mechanism runs out." That framing sits in
open ground; the component claims, stated alone, do not.

## Gaps I recommend closing before submission (cheap)
1. **Logical/Boolean-network penetrance search** (Claim 2's real competitor) — query CellNOpt/MaBoSS/SBML-qual
   + penetrance/expressivity directly. ~1 connector pass.
2. **Targeted Open Targets L2G pull** (Claim 4) — confirm the exact standard-practice citation the paper
   should adopt.
3. **Loose-term pigmentation network-model search** (Claim/framing F) — confirm no pigmentation-specific
   discordance-network competitor exists under non-obvious vocabulary.

## Provenance
All identifiers connector-verified via `openalex_get_work` (see prior-art map). No full text retrieved; DOI/PMID
citation only. Landscape scan, not systematic review — absence of a competitor is weaker evidence than
presence, hence the three follow-up searches above.
