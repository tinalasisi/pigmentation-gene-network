# Prior-art map — how "GWAS by node" and the discordance-network idea appear across fields

_Author: GENETICS_LIT_REVIEWER. Session 2026-07-11. Companion to the scoping doc
(`2026-07-11_1222_SCOPING_ideas_and_prior_art_map.md`) and the novelty-risk memo
(`2026-07-11_1308_NOVELTY_RISK_top_claims.md`)._

## What this is and how it was built

A landscape sweep to answer one question: **has the project's idea — reading genotype→phenotype discordance
off a signed directed gene network, and producing a network-ranked list of candidate modifier genes ("GWAS by
node") — already been done, possibly under a different name or in an adjacent field?**

**Method (fully reproducible).** Retrieval via the `literature` connector (OpenAlex, ~250M works; all
identifiers below are connector-returned, not recalled) and the `arxiv_search` connector for the ML framings.
Two passes: (1) a broad relevance+citation scan of 20 queries across framings A–G to size each field and find
its anchor works; (2) 8 sharp, relevance-sorted queries targeting the *specific* formulation, with abstracts,
to separate genuinely-close prior art from generic hub resources. Every work cited here was then re-fetched
individually by DOI (`openalex_get_work`) to confirm title/year/authors/identifiers; **17/17 verified, none
retracted.** Field sizes are OpenAlex `api_total` match counts (order-of-magnitude context, not exact).

**Reading guide.** "Distance to project" is my judgment of how close the prior work sits to the project's
specific claim: **Overlaps** (does essentially the same thing — novelty must be defended against it),
**Adjacent** (same tools/vocabulary, different target), **Background** (cited context, not a competitor).

---

## The map

### A — Network medicine / network-based gene prioritization  · field size ~10k–120k works
The most direct prior art. Ranking candidate genes by position/paths in a molecular network is a mature
subfield with named methods.

| Work | DOI / PMID | Distance | How close to the project's claim |
|---|---|---|---|
| Lee et al. 2011, *Genome Res* — "Prioritizing candidate disease genes by **network-based boosting of genome-wide association** data" | 10.1101/gr.118992.110 · PMID 21536720 · 715c | **Overlaps** | Almost a name-for-name match to "GWAS by node": takes GWAS signal and re-ranks/augments candidate genes using a functional gene network. The project's differentiator has to be the *signed, directed, mechanism-only, bidirectional-discordance* formulation — not the act of ranking genes by network position. |
| Li & Patra 2010, *Bioinformatics* — "Genome-wide inferring gene–phenotype relationship by **walking on the heterogeneous network**" | 10.1093/bioinformatics/btq108 · PMID 20215462 · 448c | **Overlaps** | Random-walk gene prioritization on a gene–phenotype network — the canonical "network propagation" method the project's ranking would be compared against. |
| Mostafavi et al. 2008, *Genome Biol* — GeneMANIA | 10.1186/gb-2008-9-s1-s4 · PMID 18613948 · 1127c | **Adjacent** | Standard guilt-by-association gene-function prediction; the baseline any network-prioritization claim is measured against. |

### B — Post-GWAS locus-to-gene (L2G) mapping  · field size ~1.5k–24k works
The nearest≠causal discipline lives here. This is where the project should say "we apply the established
practice," not "we introduce it."

| Work | DOI / PMID | Distance | How close |
|---|---|---|---|
| Watanabe et al. 2017, *Nat Commun* — FUMA (functional mapping & annotation of GWAS) | 10.1038/s41467-017-01261-5 · PMID 29184056 · 4513c | **Adjacent** | The standard toolset for going from GWAS locus to implicated gene (positional/eQTL/chromatin mapping + gene-based tests). Confirms that "don't stop at the nearest gene" is routine post-GWAS practice — relevant to whether the project's nearest≠causal framing is a *contribution* or a *convention it follows*. |

_(Open Targets L2G itself — the project's own named resource — was not returned as a top hit under these
generic queries; it is a known entity in the project docs. A targeted Open Targets pull is a cheap follow-up
if the PI wants the L2G comparison sharpened.)_

### C — Graph ML / knowledge-graph completion for gene–disease  · field size ~200–48k works
The coverage/"dark-matter" gap reframed in ML terms is *link prediction / KG completion*. Active and named.

| Work | DOI / PMID | Distance | How close |
|---|---|---|---|
| Renaux et al. 2023, *BMC Bioinformatics* — "A **knowledge graph approach to predict and interpret disease-causing gene interactions**" | 10.1186/s12859-023-05451-5 · PMID 37644440 · 26c | **Overlaps (for the coverage/gap claim)** | Predicts *gene–gene interaction* disease effects (oligogenic) via a KG — the closest analog to framing the missing-modifier / dark-matter question as a graph-completion task. The project's contrast: it *refuses* to predict a target without a citation, where KG-completion predicts by design. |
| Gema et al. 2023, *Nat Commun* — biomedical KG learning extending guilt-by-association to multiple layers | 10.1038/s41467-023-39301-y · PMID 37322032 · 109c | **Adjacent** | Shows guilt-by-association generalized on a multi-layer biomedical KG — the ML idiom the project's hand-curated ranking is the deliberate opposite of. |
| Zitnik et al. 2018, *Bioinformatics* — Decagon (polypharmacy via graph convolutional networks) | 10.1093/bioinformatics/bty294 · PMID 29949996 · 1398c | **Background** | The GNN-on-biological-graph method most likely to be raised as "why not learn the edges?" — useful to cite as the road not taken (the project uses curated signed edges by design). |

### D — Penetrance / modifier genetics  · field size ~230–3.2k works
The D1 claim (genotype present, phenotype absent, explained by modifiers) has a direct, high-profile
literature — but it is almost entirely *statistical/polygenic*, not *network-path*.

| Work | DOI / PMID | Distance | How close |
|---|---|---|---|
| Fahed et al. 2020, *Nat Commun* — "**Polygenic background modifies penetrance of monogenic variants**" | 10.1038/s41467-020-17374-3 · PMID 32820175 · 483c | **Overlaps (concept), differs (mechanism)** | The flagship statement of the D1 idea: whether a monogenic variant expresses depends on genomic background. But it operationalizes background as a *polygenic score*, not as *signed modifier-node states on a mechanistic network* — that mechanistic reading is the project's distinctive move. |
| Kingdom et al. 2021, *Nat Commun* — determinants of penetrance/expressivity in monogenic conditions | 10.1038/s41467-021-23556-4 · PMID 34108472 · 110c | **Adjacent** | Population-scale penetrance determinants; same phenomenon, statistical treatment. |
| 2023, *Nat Commun* — polygenic risk alters penetrance of monogenic kidney disease | 10.1038/s41467-023-43878-9 · PMID 38097619 · 66c | **Adjacent** | Same D1 pattern in a specific disease; confirms the polygenic-background framing is the field default. |
| Papadimitriou et al. 2019, *PNAS* — "Predicting disease-causing variant **combinations**" (VarCoPP/DIDA lineage) | 10.1073/pnas.1815601116 · PMID 31127050 · 112c | **Adjacent (D2/oligogenic)** | Predicts pathogenic variant *combinations* — the alternative-route/oligogenic idea (D2) in variant-combination form, not network-path form. |

### E — Boolean / logical & signed-network dynamics  · field size ~2.5k–63k works
The D1/D2 formalism (node-state gating of a path; alternative-path reachability) has deep roots here, but the
"signed directed graph reachability" query returns mostly unrelated network science — the on-target subset is
the genetic-interaction-network literature.

| Work | DOI / PMID | Distance | How close |
|---|---|---|---|
| Hu et al. 2011, *Front Genet* — "**Six Degrees of Epistasis: Statistical Network Models for GWAS**" | 10.3389/fgene.2011.00109 · PMID 22303403 · 65c | **Overlaps (framing name)** | Explicitly casts GWAS epistasis as a network-model problem — a direct precedent for "network structure explains multi-locus architecture." Statistical-interaction networks, not curated signed-mechanism graphs. |
| Boucher & Jenna 2013, *Front Genet* — genetic interaction networks: better understand to better predict | 10.3389/fgene.2013.00290 · PMID 24381582 · 121c | **Background** | Review of using genetic-interaction networks to predict phenotype — vocabulary and rationale overlap. |
| Chandler et al. 2013, *PLoS Genet* — "The Conditional Nature of Genetic Interactions: consequences of wild-type background" | 10.1371/journal.pgen.1003661 · PMID 23935530 · 87c | **Background (mechanistic anchor for D1)** | Model-organism demonstration that a mutation's effect depends on background — the biological grounding for D1, though not a network-prediction method. |

### F — Pigmentation / melanogenesis networks  · field size ~4k works
No direct competitor found: melanogenesis is modeled as *signaling pathways*, not as a signed graph built for
genotype→phenotype discordance. This supports the project's specific-instrument novelty.

| Work | DOI / PMID | Distance | How close |
|---|---|---|---|
| D'Orazio et al. 2016, *IJMS* — Signaling Pathways in Melanogenesis | 10.3390/ijms17071144 · PMID 27428965 · 1044c | **Background** | The standard pathway-level review of melanogenesis signaling; the substrate the project formalizes into a signed graph, not a competing discordance model. |

_No pigmentation-specific genotype→phenotype **network-prediction** model surfaced in the sweep. This is the
project's clearest open ground — but it is an instrument-level novelty (pigmentation as the clean test case),
not a method-level one; the method (A/C/D/E) has priors._

### G — PRS portability / genetic architecture  · field size ~500–630 works
The disease target (prediction fails by genomic background) is well-established — as the *motivation*, framed
statistically. The project's contribution is a *mechanistic explanation*, not a new observation of the failure.

| Work | DOI / PMID | Distance | How close |
|---|---|---|---|
| Liu et al. 2019, *Cell* — "Trans Effects on Gene Expression Can Drive **Omnigenic** Inheritance" | 10.1016/j.cell.2019.04.014 · PMID 31051098 · 607c | **Background** | The omnigenic/core-peripheral rationale for why D2 has many contributing genes — cited framing, already in the project docs. |
| Martin et al. 2017, *AJHG* — "Human Demographic History Impacts Genetic Risk Prediction across Diverse Populations" | 10.1016/j.ajhg.2017.03.004 · PMID 28366442 · 1568c | **Background** | The canonical PRS-portability-failure statement = the disease-scale target. The project explains a mechanism for such failures; it does not re-demonstrate them. |

---

## One-line synthesis per framing

- **A / C (network prioritization, KG completion): OVERLAP — highest novelty risk.** Ranking modifier genes
  by network position, and framing missing genes as graph-completion, both exist under established names.
- **B (L2G): CONVENTION, not contribution.** Nearest≠causal is standard post-GWAS practice; claim it as
  applied discipline.
- **D (penetrance modifiers): CONCEPT EXISTS, MECHANISM DIFFERS.** "Background modifies penetrance" is the
  Fahed-2020 flagship, but operationalized as polygenic score, not signed network paths.
- **E (logical/interaction networks): FRAMING PRECEDENT EXISTS** ("network models for GWAS epistasis").
- **F (pigmentation network): OPEN GROUND** at the instrument level — no pigmentation discordance-network
  competitor found.
- **G (PRS portability): the MOTIVATION, well-established** — the project supplies mechanism, not the
  observation.

See the novelty-risk memo for the defensible-distinction analysis on the top-4 exposed claims.

## Provenance & limitations
- All 17 cited works verified individually by DOI via `openalex_get_work` (title/year/authors/identifiers
  confirmed; none retracted). Field-size counts are OpenAlex `api_total`, retrieved 2026-07-11.
- This is a **landscape scan, not a systematic review**: relevance ranking is OpenAlex's; I did not screen
  every hit, and absence of a competitor in the sweep is weaker evidence than its presence. Two cheap
  follow-ups would harden specific corners: a targeted Open Targets/L2G pull (framing B) and a
  pigmentation-specific network-model search with looser terms (framing F).
- No paper full text was retrieved or reproduced; citation is by identifier only, per the repo's
  redistribution policy.
