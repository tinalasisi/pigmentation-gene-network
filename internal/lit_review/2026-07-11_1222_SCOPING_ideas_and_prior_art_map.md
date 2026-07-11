# Lit-review scoping — the project's ideas, and the prior-art map I will search against

_Author: GENETICS_LIT_REVIEWER (Genetics Literature Reviewer specialist). Session 2026-07-11._
_Status: scoping only. **No literature has been retrieved yet.** This document reads the project's own
internal record and translates its ideas into the search framings I will run. Every DOI/PMID mentioned below
is transcribed from the project's own documents (where the project reports it as DOI-verified); I have **not**
independently retrieved any of them, and none should be treated as a lit-review result until I pull it through
a connector. The purpose here is to fix, before searching, (a) what the ideas actually are and (b) under which
field vocabularies each must be checked — so a reviewer cannot later say "this exists under name X and you
didn't look."_

Sources read to build this: `README.md`; `internal/project_dashboard.md` (esp. §1, §4 design rationale,
locked decisions); `internal/RESEARCH_SYNTHESIS_locus_resolution_mvp.md`; `docs/network_integration_and_MVP_spec.md`;
`internal/FRAMING_EVALUATION_dark_matter.md`; `internal/FINDINGS_darcy_coverage.md`;
`internal/EXPANSION_PLAN_sex_pigment_primate.md`; `internal/TODO.md`;
`internal/deconvolutor/2026-07-10_1901_DECONVOLUTOR_SUMMARY_both_tracks.md`.

---

## 1. The central idea, stated once, plainly

The project builds the published Raghunath et al. (2015) directed melanogenesis model as a **signed, directed,
gene-level network** (168 gene nodes / 309 edge rows) and uses the *structure of that graph* to explain why
the same genotype gives different phenotypes across people. Two directions, one graph:

- **D1 — genotype present, phenotype absent** (reduced penetrance): a present causal genotype fails to reach
  the pigment endpoint because the **states of signed modifier nodes along the path block it**. The network
  says *which* modifier nodes could do the blocking.
- **D2 — phenotype present, canonical genotype absent** (alternative route): the endpoint is reachable by
  **alternative directed paths through other genes**, so the phenotype appears without the usual variant.

Pigmentation is chosen as the instrument, not the subject: near-zero environmental variance + high
heritability mean discordance is almost purely a genetic-architecture phenomenon. **The stated target is
disease-risk prediction that fails by genomic background — i.e. polygenic-score portability failure.**
"Pigmentation is the model organism; disease-risk prediction is the target."

The load-bearing engineering discipline: **association is not causation, and nearest gene is not causal
gene.** A GWAS locus is a SNP, not a gene; only the *resolved causal gene* is connected, and only through
*mechanism* (OmniPath + curated literature) — association sources (STRING, GWAS proximity) never draw an edge.
Canonical example: rs12913832 is intronic in HERC2 but regulates OCA2; HERC2 is not added, OCA2 carries the
signal.

**The phrase the project uses for its own output — and the one most exposed to "this already exists" — is
"GWAS by node": a network-derived, ranked list of candidate modifier genes** that explains why prediction
succeeds for some people and fails for others (dashboard §1).

---

## 2. Explicit ideas (named in the docs) vs. implicit ideas (operating assumptions not named as claims)

### Explicit — stated as the project's own commitments
1. Bidirectional genotype→phenotype discordance (D1/D2) as **one signed directed graph** phenomenon
   (locked decision 1/11).
2. **Nearest-gene ≠ causal-gene**; connect only the resolved causal gene, only via mechanism (locked
   decision 5; `nearest-gene-vs-causal` skill).
3. **Two-level framing**: headline = bidirectional discordance (payoff loci TYR + OCA2); second act =
   **"dark-matter association"** coverage audit — case genes absent from *both* the mechanistic network and
   the D'Arcy OMIM-backed disease-gene compendium (locked decision 11; `FRAMING_EVALUATION_dark_matter.md`).
4. Dark matter **decomposes into cited classes**, not one "unexplained biology" bucket (positional-pointer /
   redirect-to-other-gene / LD-passenger-or-no-signal / genuinely-novel). A "mislabeled-pointers" hypothesis
   was tested and **falsified** (0/15 dark-matter genes resolve to an in-network gene).
5. **Locus-integration schema**: loci enter as a separate `locus` node type (keyed by rsID) with annotation
   edges (`nearest_gene_link`, `regulatory_target`, `eQTL_target`, `in_LD_with`, `dark_matter_association`)
   structurally walled off from the mechanistic backbone (`network_integration_and_MVP_spec.md` §1).
6. **Conceptual grounding already cited in-repo** (project reports these DOI-verified; I have not re-pulled
   them): incomplete penetrance = D1 (Cooper 2013; Kingdom & Wright 2022; Chen 2016, 589k genomes); omnigenic
   architecture (Vuckovic 2020); PRS portability (Martin 2019); why-pigmentation (Zhu 2004; Morgan 2018;
   Pavan & Sturm 2019); human oligogenic vs animal epistasis kept distinct (Crawford 2017 oligogenic;
   Demars 2022 rabbit epistasis).
7. **Deferred expansion**: sex-hormone × pigmentation coupling (steroidogenesis + AR/ESR receptor layer) and
   **sexual dichromatism across primates** via phylogenetic comparative methods (`EXPANSION_PLAN...`).

### Implicit — the operating assumptions a reviewer will name, that the docs don't frame as prior-art risks
These are the framings the project *is* working in, whether or not it says so. Each is a place someone has
almost certainly published something adjacent under a different name. This list drives §3.

- **"GWAS by node" IS a network/graph reformulation of genetic architecture.** Ranking modifier genes by
  their position/paths in a curated network is, in other fields' words, *network-based gene prioritization*,
  *network propagation*, or *guilt-by-association* — mature subfields.
- **D1 = signed-path reachability with node-state gating** is the language of **Boolean / logical network
  models** and **signed-graph reachability / signaling-perturbation analysis** — a whole modeling tradition
  (CellNOpt, MaBoSS, SBML-qual, attractor analysis).
- **D2 = "how many genes have a directed path to the endpoint"** is a **reachability / connectivity** metric;
  the null model over it is a **network-permutation** problem (degree-preserving rewiring) with a known
  artifact literature.
- **The coverage/dark-matter audit is a "knowledge-graph completeness / missing-node"** problem — framed in
  ML terms it is *link prediction* and *knowledge-graph completion* over a gene–disease graph.
- **The disease target (why does a variant's effect depend on the rest of the genome)** is, in statistical-
  genetics vocabulary, **genetic modifiers / genetic background effects / gene-by-genetic-background
  interaction / epistasis / variable expressivity** — and in clinical vocabulary, **PRS portability and
  transferability**.
- **Locus → causal gene** is the **post-GWAS gene-mapping / locus-to-gene (L2G)** subfield (Open Targets L2G,
  fine-mapping-to-gene, MAGMA/PASCAL gene-based tests).

---

## 3. The prior-art map — what I search, and under which field's words

This is the core deliverable of the scoping pass. For each framing I list the vocabulary I will query and the
**specific "closest prior art" question** the retrieval must answer. I will run these across the literature
connectors (PubMed / Europe PMC / bioRxiv / OpenAlex, plus Open Targets and human-genetics resources for the
gene-mapping framings) and report, per framing, what exists and how close it sits to the project's claim.

| # | Framing / field | Search vocabulary (the field's own terms) | The prior-art question to answer |
|---|---|---|---|
| A | **Network medicine / systems biology** | network medicine; disease module; network propagation; guilt-by-association; connectivity-based gene prioritization; DIAMOnD; random-walk-with-restart on interactome | Has "rank candidate modifier genes by network position for a heritable trait" already been done — and is "GWAS by node" just network-based gene prioritization under a new name? |
| B | **Post-GWAS gene mapping / L2G** | locus-to-gene; Open Targets L2G; fine-mapping to gene; nearest-gene fallacy; gene-based GWAS (MAGMA, PASCAL, VEGAS); TWAS; eQTL colocalization | Is the nearest≠causal → resolved-causal-gene discipline already the standard L2G pipeline? Where does the project's *mechanistic-edge* restriction differ from L2G's statistical approach? |
| C | **Graph ML / knowledge graphs for genomics** | graph neural network gene prioritization; node classification gene–disease; knowledge-graph completion; link prediction gene–disease; message passing biological network; PyKEEN / OpenBioLink / Hetionet | Has the coverage-gap ("dark matter") been framed as KG completion / link prediction — and does a GNN approach already rank modifier genes the way this network does by hand? |
| D | **Penetrance & modifier genetics** | incomplete penetrance modeling; modifier gene screen; genetic background effect; digenic/oligogenic disease (DIDA, OLIDA); background-dependent penetrance; variable expressivity | Has anyone modeled incomplete penetrance as *path-blocking in a signed network*, rather than statistically? Is D1 a known formalism? |
| E | **Boolean / logical & signed-network dynamics** | Boolean network model; logical model signaling; SBML-qual; attractor analysis; signed directed graph reachability; signaling network perturbation (CellNOpt, MaBoSS) | Is D1/D2 (node-state gating of a path; alternative-path reachability) a re-derivation of established logical-modeling reachability results? |
| F | **Melanogenesis / pigmentation networks specifically** | melanogenesis pathway model; pigmentation gene regulatory network; MITF network; Raghunath melanogenesis; pigmentation GWAS review | Has a pigmentation-specific network already been built for genotype→phenotype discordance? Direct prior-art check. |
| G | **PRS portability / genetic architecture** | polygenic score portability; PRS transferability across ancestries; missing heritability; omnigenic model; genetic interaction / epistasis architecture | Is the "prediction fails by genomic background, explained by network structure" claim already made in the PRS-portability literature by another mechanism? |
| H | **Comparative/evolutionary (expansion track)** | sexual dichromatism genetics primates; steroidogenesis melanogenesis coupling; androgen/estrogen receptor melanocyte; phylogenetic comparative method pigmentation; dN/dS pigmentation | For the deferred expansion: does a sex-hormone × pigmentation network coupling, or a network-predicted-dichromatism comparative test, already exist? |

---

## 4. The novelty claims most exposed — where I focus first

Ordered by how load-bearing the claim is to the paper **and** how likely an adjacent field has priority:

1. **"GWAS by node" as a novel object.** Highest exposure. Framings A + C + D. If network-based gene
   prioritization / network propagation already produces ranked modifier lists, the novelty is not the ranking
   but the *signed, mechanism-only, bidirectional-discordance* formulation — I must be able to state exactly
   what is new and cite what isn't.
2. **D1/D2 as a signed-network reachability formalism.** Framing E + D. Risk that logical-modeling or
   penetrance-modeling literature has an equivalent construct. Need the closest formal analog on record.
3. **"Dark-matter association" coverage audit as a finding.** Framing C + B. Risk it reads as knowledge-graph
   incompleteness / link-prediction, which is a named ML task. The project's defense (principled cited
   decomposition, refuse-to-overclaim) needs a prior-art contrast to stand on.
4. **The nearest≠causal discipline as a contribution.** Framing B. Lower exposure — this is likely *standard*
   L2G practice, so the honest posture is "we apply the established discipline," not "we introduce it." I
   should confirm that so the paper doesn't overclaim it.

---

## 5. What I deliberately will NOT do (scope boundary)

- I do **not** extract per-record datasets from papers — that is GENETICS_DATA_EXTRACTOR's job. I decide which
  papers matter and how the idea sits in the field; the Extractor mines the ones I flag.
- I do **not** decide scientific strategy or reopen locked decisions — that is the PI's call.
- I will **not** cite any paper I have not retrieved through a connector. The §2/§3 DOIs are the project's own
  transcribed citations, held here only as starting points to re-locate and verify, not as my findings.

---

## 6. Immediate next actions (pending PI go-ahead)

1. Run framings A–G against the literature connectors; produce a **"how this idea appears across fields" map**
   — one row per genuinely-close prior work, with resolvable DOI/PMID, the field it comes from, and a one-line
   statement of how close it sits to the project's claim.
2. Deliver a short **novelty-risk memo** for the top-4 claims in §4: for each, the closest prior art found,
   under which name, and whether the project's framing survives it (and if so, on what precise distinction).
3. Hold framing H (expansion) until the PI reactivates that track — it is deferred per `TODO.md` (c) D4.
