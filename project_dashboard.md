# Pigmentation Project — Dashboard

_Internal control surface. This is the single document to read for project state, design rationale, and open
work; it is the cold-start brief for a new session. Last reconciled 2026-07-10._

This dashboard is the one internal governance document the project maintains. It absorbs the design rationale
formerly held in the build plan, folds in the live task status, and points to `TODO.md` as the machine-readable
backing ledger. See **Document architecture** below for the full document model.

---

## 1. Cold-start brief (read this first)

**What the project is.** Pigmentation is a model system for the genotype→phenotype map; the target is
disease-risk prediction that fails by genomic background. A pigmentation phenotype is the output of a directed
molecular network, and whether a high-effect variant expresses depends on the state of the other nodes around
it. The project builds that network — the published Raghunath et al. (2015) directed melanogenesis model plus
the pigmentation genes discovered since — and uses it to produce a network-derived, ranked list of candidate
modifier genes ("GWAS by node") that explains why prediction succeeds for some people and fails for others.
Pigmentation is the instrument because its environmental variance is near-zero and its heritability is high, so
discordance is almost purely a genetic-architecture phenomenon (Zhu 2004; Morgan 2018; Pavan & Sturm 2019) —
unlike environment-confounded complex disease. What is being built here is a method — reading genotype→phenotype
discordance off the structure of a signed directed network — and that method is not specific to pigmentation;
pigmentation is where it can be validated cleanly. Whether it helps at a given disease locus is an empirical
question for the grant stage, not something this build asserts. Where population-genetic data enters (grant
stage), it is an analytical input to mechanism and conditionality — how variation distributes across the
network's control points.

**The finding.** A signed directed network that explains genotype→phenotype discordance in **both directions**
with the same machinery:

- **D1 — genotype without phenotype** (causal variant present, trait absent): modifier-node states block the
  path from a present causal genotype to the pigment endpoint. Anchor: Kalinago OCA2 R305W (Ang 2023) — scores
  pathogenic by SIFT/PolyPhen/PANTHER, yet R305W homozygotes without NW273KV are not albino.
- **D2 — phenotype without the usual genotype** (trait present, canonical variant absent): the endpoint is
  reachable by alternative routes — on the current 168-gene backbone, ~114 genes besides TYR/OCA2/TYRP1/MC1R
  have a directed path to a pigment endpoint (plan-stated figure, to be recomputed on the connected graph).
  Anchor: Kalinago albinism (Ang 2023) — the albino individuals do not carry the catalogued OCA2 albinism
  variants; their albinism traces to a population-specific novel variant (NW273KV) that a standard albinism
  panel would miss.

Payoff loci are the albinism causal genes **TYR (OCA1) and OCA2** — the same genes as the clinical validation
cases, so payoff and validation are the same disease. Both directions are computable on the NB1+NB2 backbone
alone; the expansion notebooks enrich the finding but are not required for a v1 figure.

**Authoritative documents for a new session:** this dashboard (state + design), `README.md` (public rebuild
guide), `DATA_SOURCES.md` (provenance manifest), `NB3_case_assembly_provenance.qmd` (case-set provenance),
`TODO.md` (backing task ledger). Treat these as the source of truth over memory.

---

## 2. Build progress

_Two notebooks are complete and agreed (NB1, NB2). The validation-case set is complete as a dataset. The
structure below the line is a **proposed** design — the notebook layout beyond NB2 is not yet agreed by the
PI and must not be treated as settled or drafted as notebooks. Task status is
folded in from `TODO.md`; edit open items there, then re-render this view._

**Agreed and complete:**

| # | Notebook | Status | Result |
| --- | --- | --- | --- |
| 1 | Reconstruct the published network | ✅ done | Raghunath backbone: 265 nodes / 429 signed edges |
| 2 | Resolve the network to genes | ✅ done | Gene-level network: 168 gene nodes / 309 edge rows |

**Complete as a dataset (notebook placement tentative):**

| — | Assemble the validation-case set | ✅ data done | 13 papers, 694 records across committed CSVs, direction-classified (3 D1 / 5 D2 / 5 both). Provenance sign-off items open (§5) |
| --- | --- | --- | --- |

**Proposed downstream direction — NOT yet agreed (do not build or draft as notebooks):**

| Proposed step | Intent |
| --- | --- |
| Case-gene manifest + evidence layer + causal-gene resolution | Resolve each case gene from its association marker to its causal gene (Open Targets L2G + ClinVar/OMIM); tag evidence |
| Causality-gated connection of the validation-case genes | Connect only resolved causal genes, only through mechanism (OmniPath + curated literature) |
| Unify layers + recompute the load-bearing metrics | Signed paths (D1) and alternative-reachability (D2) on the connected graph, with a null model |
| Bidirectional discordance by node (the payoff figure) | Two panels per albinism locus (TYR, OCA2): D1 modifier states, D2 alternative routes |
| Case validation (machine-checkable, both directions) | Test each case with its mechanism pre-registered from the paper before the network is consulted |

**Deferred to grant stage:** four-axis functional annotation (localization / process / molecular-function /
phenotype per node); ancestry-stratified / allele-frequency verification (1000G / HGDP / gnomAD by population).

---

## 3. Key metrics

_All values recomputed 2026-07-10 from the pinned processed files via `compute_canonical_facts()` / direct CSV
row counts (pigmentation-plan-sync skill), not retyped from prose. Version IDs are the files these came from._

| Metric | Value | Source file (version) |
| --- | --- | --- |
| Raghunath backbone nodes | 265 | `raghunath_nodes_typed.csv` (`61b4b0fb`) |
| Raghunath backbone edges | 429 | `raghunath_edges_typed_signed.csv` (`274d2225`) |
| Edge signs (+ / − / 0) | 379 / 43 / 7 | `raghunath_edges_typed_signed.csv` (`274d2225`) |
| Node types (complex / environmental / pending_db_resolution) | 24 / 2 / 239 | `raghunath_nodes_typed.csv` (`61b4b0fb`) |
| Dual-compartment bases | 58 | `raghunath_nodes_typed.csv` (`61b4b0fb`) |
| Gene-level network nodes (NB2) | 168 | `gene_network_nodes.csv` (`eb0110fa`) |
| Gene-level network edge rows (NB2) | 309 | `gene_network_edges.csv` (`b7ccce5a`) |
| Bajpai 2023 CRISPR hits (q<0.10) | 169 | `bajpai2023_crispr_hits.csv` (`f016fc99`) |
| Baxter compendium (rows / gene-IDs / human symbols) | 659 / 656 / 635 | `baxter2018_650_pigmentation_genes.csv` (`056e62f9`) |
| HIrisPlex-S markers / genes | 36 / 16 | `hirisplexs2018_markers.csv` (`8caf2c0b`) |
| D2 alternative-reach genes (besides TYR/OCA2/TYRP1/MC1R) | ~114 | plan-stated backbone figure — **to be recomputed on the connected graph**, not a pinned-file value |
| Validation-case records (committed per-paper CSVs) | 694 | committed `EXTRACT_*_records.csv`; grain differs by paper. `n_records_extracted` in the pinned classification CSV equals the committed row counts and sums to 694 (earlier 511 headline retired — NB3 prov §6) |

---

## 4. Design rationale (absorbed from the build plan)

This section carries the design thinking that formerly lived in `hackathon_build_plan.md` (now archived). It
changes only when the design changes.

### The two directions

Both are failure modes of the one-gene→one-trait Punnett square, and both fall out of one directed signed
graph: **D1** = a modifier node state suppresses a present causal path; **D2** = an alternative node reaches the
endpoint without the usual gene. The nine Raghunath target processes are the path-tracing endpoints, with
eumelanin and pheomelanin the headline pigment endpoints.

### Notebook map (what each produces, and why)

> **Scope of this map:** items 1 and 2 are the agreed, completed notebooks. Item 3 (case assembly) is complete
> as a dataset. Everything numbered 4 and beyond is a **proposed** structure — the PI has not agreed the
> notebook layout past NB2 (see §2 above). The descriptions below elaborate the proposal
> so it can be evaluated; they do not settle it, and these notebooks must not be built or drafted until agreed.

1. **Reconstruct the published network** ✅ — A faithful, offline, deterministic reconstruction of the Raghunath
   model: 265 nodes, 429 directed edges, every edge signed from an explicit verb→sign dictionary over the 24
   verbs the file uses. Node typing is limited to the two cases the published file fixes deterministically
   (`complex` by colon syntax; `environmental` for UVA/UVB); all other nodes are left `pending_db_resolution`
   for NB2. Produces the mechanistic backbone every later step transforms.
2. **Resolve the network to genes** ✅ — Turns protein / metabolite / process nodes into a gene-level network by
   an annotate-then-enrich discipline: each node is typed by its own-type authority (UniProt for proteins,
   ChEBI/PubChem for compounds, GO for processes), then gene identity (MyGene) and gene-family membership (HGNC
   groups) are attached. Produces the 168-gene / 309-edge-row network, validated against OmniPath as a four-way
   verdict, behind a release-blocking citation gate (every node and edge carries a resolvable citation). MITF
   and NFKB1 recompute as the top hubs.
3. **Assemble the validation-case set** ✅ — Ingests the PI's 13 pigmentation genotype→phenotype-discordance
   papers, extracted from the authoritative publisher PDFs (694 records across committed per-paper CSVs; grain
   differs by paper), each classified by discordance direction (3 D1 / 5 D2 / 5 both) with verbatim page/table
   evidence. Produces `discordance_case_classification.csv` + per-paper `EXTRACT_*` records — the empirical base
   the finding is validated against. Provenance is recorded in `NB3_case_assembly_provenance.qmd`; several
   sign-off items remain open (see §5).
4. **Case-gene manifest + evidence layer + causal-gene resolution** ⬜ — Derives the resolution targets from the
   cases themselves: enumerates every (case, gene, anchor-genotype), joins to the 168-gene network, and tags
   each gene `core-connected` / `present-isolated` / `absent` — producing the 9-connected / 10-absent split as a
   computed checkpoint. Adds per-gene evidence tags from all discovery sources (HIrisPlex target flag, Bajpai
   CRISPR effect, GWAS replication count, Baxter human-relevant) and a standalone causal-gene resolution table
   (nearest gene vs Open Targets L2G vs ClinVar/OMIM, with tie-break rule). The causal call gates NB5 — no gene
   enters the graph on association alone.
5. **Causality-gated connection of the validation-case genes** ⬜ — Connects the 10 absent case-genes, but only
   the resolved causal gene and only through mechanism (OmniPath directed/signed + curated literature). Three
   outcomes per gene: association marker whose causal gene is already in-network → not added (HERC2 routes
   through OCA2); genuinely causal + connectable → mechanistic signed edges (SLC45A2, SLC24A5, SLC24A4, IRF4,
   ASIP); causal + no pathway mechanism → reported unconnectable (MFSD12, DDB1, TMEM138). Produces
   `nb5_causal_edges.csv` and `nb5_unconnectable.csv`, each edge tracing to its NB4 causal call.
6. **Unify layers + recompute the load-bearing metrics** ⬜ — Builds the single canonical graph and computes,
   per pigment endpoint, the two objects the figure consumes: signed distance / path enumeration from each
   causal gene (D1 — the on-path modifier nodes and their signs) and the set of all genes with a directed path
   to the endpoint (D2 — the alternative-causal pool, recomputed here on the NB5-connected graph). Adds a
   degree-preserving null model for the D2 reachability count and applies the D1 path-block check to the D2
   genes. A boundary note records that signed-graph reachability locates where epistasis would act but does not
   establish non-additivity (dynamics deferred to grant). Backbone-betweenness-vs-published kept only as a
   collapse QC.
7. **Bidirectional discordance by node (the payoff figure)** ⬜ — Two panels per albinism causal locus
   (TYR→eumelanin; OCA2→melanosome): D1 shows the signed modifier states that could block a present causal
   genotype; D2 shows the alternative genes/paths that reach the same endpoint without the usual gene, with the
   null-model context. Annotates the nearest-vs-causal resolution at each locus (e.g. HERC2-nearest vs
   OCA2-causal for rs12913832) and the disease bridge where genuine (ClinVar/OMIM). Regenerable from the NB6
   metrics table alone.
8. **Case validation (machine-checkable, both directions)** ⬜ — Tests each case against the network with a
   mechanism (D1/D2) **pre-registered from the paper before the network is consulted**, so a case can fail by
   being explained by the wrong mechanism. D1: does the signed-suppressor set for the locus contain the
   case-reported modifier? D2: does the alternative pool reach the endpoint through the case's gene — split
   reachable vs unreachable (MFSD12/DDB1/TMEM138). Produces a per-case pass/fail/unreachable table; the case set
   stays open to PI additions under the same pre-registration rule.

### The causality-gated spine

`NB3 cases → NB4 manifest + causal resolution → NB5 causality-gated connection → NB6 metrics → NB7 figure →
NB8 validation`. Edge creation uses OmniPath + curated literature only; association-flavoured sources (STRING
co-expression, GWAS proximity) cannot manufacture a mechanistic edge. Every absent case-gene passes NB4 causal
resolution before any edge is drawn, and only the resolved causal gene is connected. **HERC2 stays out of the
graph and routes through OCA2** (rs12913832 is a long-range OCA2 enhancer; L2G HERC2 0.428 vs OCA2 0.203 causal).
**MFSD12 / DDB1 / TMEM138** are the reported unreachable limit — causal genes with no melanogenesis-pathway
mechanism.

### Conceptual grounding — penetrance and epistasis

- **Incomplete penetrance = D1.** A pathogenic genotype fails to produce its phenotype through modifier alleles,
  background, and epistasis (Cooper 2013; Kingdom & Wright 2022; Chen 2016, 589k genomes). The network computes
  which background states flip penetrance per locus.
- **Epistasis = the mechanism of both directions.** Human oligogenic architecture (Crawford 2017, multi-locus,
  *not* an epistasis claim) and animal-model epistasis (Demars 2022, rabbit) are kept explicitly distinct. A
  signed directed edge turns an epistatic hypothesis into a named, testable structure.
- **Omnigenic core-peripheral view = why D2 has many alternative genes** (Vuckovic 2020).
- **Clinical horizon = PRS portability failure across populations** (Martin 2019) — the disease-scale shadow of
  the pigmentation-visible mechanism, deferred to the grant.

### Locked decisions

1. **Finding:** bidirectional discordance (D1 modifier-block; D2 alternative-route reach) on one signed directed
   graph; payoff loci = TYR (OCA1) + OCA2 = the clinical validation cases; both directions computable on the
   NB1+NB2 backbone alone.
2. **Backbone provenance:** Raghunath 2015 directed signed edges = mechanistic backbone; D'Arcy/Kiel 2023 =
   parallel reconstruction / annotation + disease-direction layer, not backbone.
3. **NB1 offline/deterministic** (types only what the file fixes); all database-backed typing + gene resolution
   in NB2, each call cited.
4. **Recompute network metrics on the final graph;** published precomputed values are validation references only.
5. **Edge creation = OmniPath + curated literature only;** association sources excluded. Connect the causal gene,
   never the association marker.
6. **Every node/edge type traces to a recorded source;** no hand-typed classification lists.
7. **HIrisPlex / accuracy numbers cited only with population provenance;** no population / allele-frequency data
   in hackathon scope (deferred to grant).
8. **Case validation pre-registers each case's mechanism from the paper** before the network is consulted.
9. **License:** MIT (Tina Lasisi). MCP acquisition documented.
10. **Notebook format & site publishing:** `.qmd` is the sole committed source of truth (`.ipynb` converted
    once, removed, never a hand-maintained twin). No-kernel rendering only (`enabled: false` or
    `freeze: auto` + committed `_freeze/`). Publish via GitHub Pages + Actions, `_site/` git-ignored.
    Enforced by RESEARCH_SITE_PUBLISHER + the quarto-github-pages skill.

### Writing rules

_(Absorbed 2026-07-10 from the retired `CANONICAL_STATE.md`, which this dashboard now supersedes as the single
grounded source of truth.)_

- **State the work plainly and in general terms.** Describe the aims, methods, and scope directly. Don't frame
  the project by what it is not, and don't add caveats about topics the work doesn't address.
- **Ground every population reference in a cited source.** Report what a published study examined and found;
  keep claims to what the project's own data support.
- **No number from memory.** Canonical counts are recomputed from pinned artifacts; cite the artifact.

---

## 5. Open items

_Live view of the backing ledger, `TODO.md`. Edit open items there, then re-render this table._

| # | Item | Notebook | Owner | Blocking? |
| --- | --- | --- | --- | --- |
| 1 | Reconcile `DATA_SOURCES.md` to the current design (association-marker→causal-gene resolution via L2G/ClinVar, full-Bajpai-screen choice, bidirectional source roles). | manifest / provenance | PM | No — traceability debt, not build-blocking |
| 2 | Stage D'Arcy/Kiel (2023) paper + supplementary tables in the repo. | NB4 (Part C), NB5 shell | PM / build | Yes — blocks NB4 disease-direction class + NB5 shell PPI |
| 3 | Attach Complex Portal / CORUM connector (not attached). | NB5 | PM (connector) | Yes — blocks NB5 structural layer unless STRING+Reactome fallback is used |
| 4 | Pin ClinVar / OMIM as a versioned input in the manifest. | NB4 | PM / build | Yes — blocks NB4 causal-gene-resolution provenance |
| 5 | Supply additional validation case studies from the PI's own literature review, if wanted. | validation-case set | PI | Optional extension |

**NB3 case-set provenance sign-off items** (from `NB3_case_assembly_provenance.qmd` §7 — decisions for the PI,
not facts the PM can settle):

| # | Item | Status |
| --- | --- | --- |
| A | Notebook structure beyond NB2. | **Open — PI decision.** Only NB1/NB2 are agreed; the case set is complete as data but its notebook placement and the entire downstream layout are a proposal pending PI sign-off (§2). |
| B | Per-paper md→PDF re-extraction change-logs missing for 11 of 13 `EXTRACT_*.md`. | Open — decide whether to backfill. |
| C | Paper withholding path. | **Resolved** — papers live under `data/raw/papers/`; the on-disk `.gitignore` withholds `data/raw/papers/*` and keeps `REFERENCES.md`; README references point there. |
| D | Superseded duplicate record CSVs in the artifact store (two-wave extraction history). | Open — housekeeping. The canonical total (694) reproduces from the committed files; remaining task is to archive/remove the superseded duplicates so only the canonical CSV per paper is discoverable. |
| E | Superseded/duplicate per-paper record CSVs still live in the store. | Open — set a retention/retirement policy (one canonical file per paper). |

**Build status:** NB1 and NB2 complete and agreed; the validation-case dataset complete. The downstream
analysis is not started and its notebook structure is not yet agreed (open item A is the gate). Items #2–#4
concern inputs the proposed downstream work would need.

---

## 6. Document architecture

The project maintains a deliberately small living set. This is the standing rule, so the documentation does not
re-fragment.

**Living — maintained going forward:**
- **[README.md]({{artifact:art_b122c8e6-7f48-4251-939e-f0bde8c66aa6}})** — the only public-facing document:
  rebuild instructions, pinned inputs, notebook order. (A science-communication pass is scheduled separately.)
- **project_dashboard.md** (this file) — the single internal control surface: state, design rationale, and open
  work. The one document the Project Manager maintains.
- **[TODO.md]({{artifact:art_5baeeb96-bf78-44f2-bd19-382b2169ed8c}})** — the machine-readable backing ledger for
  the Open-items table above.

**Data documentation — kept with the data, not planning docs:**
- **[DATA_SOURCES.md]({{artifact:art_ab9307c6-1b6b-4b4d-a7f9-302b0f65a4b5}})** — provenance manifest. **Lags the
  current architecture — see Open item #1.**
- **[NB3_case_assembly_provenance.qmd]({{artifact:art_1d09fb3e-2f62-4c25-bece-596b03839889}})** — case-set
  extraction provenance record.
- **[discordance_case_classification_README.md]({{artifact:art_5079f196-a5ce-4f4d-a79b-20217c472f1a}})** — case
  classification data dictionary.
- **[data/raw/papers/REFERENCES.md](data/raw/papers/REFERENCES.md)** — paper-withholding doc (per-paper
  citations, DOIs, license/access, how to obtain each file); lives with the (withheld) papers.

**Archive convention (standing rule, adopted 2026-07-10).** A retired document is renamed with a
**`z_archived_`** filename prefix and moved to `internal/archive/`. The prefix is load-bearing: it makes
retired files sort to the bottom, states plainly that they are not source-of-truth, and — combined with the
`z_archived_*` entry in `.gitignore` — guarantees an archived file is never committed to the public repo.
This exists because superseded copies under near-identical names (`project_dashboard.md` vs
`repo_project_dashboard.md`; `CANONICAL_STATE.md` as a second "source of truth") had drifted out of sight in
the artifact store; the prefix is how a future session tells current from retired at a glance.

**Single-source rule for the dashboard (standing rule, adopted 2026-07-10).** The dashboard has exactly one
name — **`project_dashboard.md`**, the git-tracked file at the repo root — and exactly one store artifact
(`artifact_id e4103019-a821-470d-893f-cebf33512291`). Every update edits that file in place and is saved as a
**new version of that one artifact** (`version_of`), never as a new artifact under a variant name. Do not create
`repo_project_dashboard.md`, `project_dashboard_v2.md`, `dashboard_final.md`, or any other alias: a second name
is a second source of truth, and the two silently diverge. If you find a divergent copy, the repo-tracked
`project_dashboard.md` wins; merge any newer content into it, then retire the alias by tombstone (below). The
earlier `repo_project_dashboard.md` artifact was exactly this failure — a mis-named parallel copy that recent
sessions edited while the repo file went stale; it was consolidated back into `project_dashboard.md` and
tombstoned on 2026-07-10.

**Archived — retired, recorded in `internal/archive/ARCHIVE_MANIFEST.md`.** The prior build plan, the redundant
dashboard views, the two handoff briefs, the per-notebook TODO, the FINDING/SOURCE_DECISION/PLAN working drafts,
and the process critiques were consolidated into this dashboard on 2026-07-10. **`CANONICAL_STATE.md` is
retired 2026-07-10** — its unique content (the AGREED/TENTATIVE split → §2; the canonical-numbers table → §3;
the writing rules → §4) is absorbed into this dashboard, which is now the single grounded source of truth.
Their content is either absorbed here or preserved as a dated archive record; nothing was deleted. See
`ARCHIVE_MANIFEST.md` for the per-document row (id, date retired, why, what supersedes it).

---

## 7. File custody — assembled repo (MVP)

The project has been assembled into the git repository at `pigmentation-gene-network/` and committed
(2026-07-10, commit `74f472b`, 65 files, after clearing the REPO_COMPLIANCE_GATE; `internal/` and
`z_archived_*` excluded). Paths below are the real repo locations; the pinned version IDs
identify the artifact each file was written from. The full per-file inventory across all conversations is
regenerable via the `project-file-dashboard` skill.

**Notebooks (`notebooks/`):**
- [`01_reconstruct_published_network.ipynb`](notebooks/01_reconstruct_published_network.ipynb) — Raghunath → 265/429 typed signed network
- [`02_resolve_network_to_genes.ipynb`](notebooks/02_resolve_network_to_genes.ipynb) — → 168-gene network + OmniPath validation
- [`01a_extract_bajpai_crispr.ipynb`](notebooks/01a_extract_bajpai_crispr.ipynb) · [`01b_extract_baxter_genes.ipynb`](notebooks/01b_extract_baxter_genes.ipynb) · [`01c_extract_hirisplex_markers.ipynb`](notebooks/01c_extract_hirisplex_markers.ipynb) · [`01d_reproduce_gwas_catalog.ipynb`](notebooks/01d_reproduce_gwas_catalog.ipynb) — source extractors

**Scripts (`scripts/`):** `gwas_catalog.py` · `harmonize.py` · `vizhelpers.py` · `traits_pigmentation.json`

The minimal set to reconstruct the project, by role, with pinned version IDs:

**Notebook 1 — reconstruct published network (+ source extraction):**
`raghunath_nodes_typed.csv` `61b4b0fb-f462-4c7f-a9a1-dfae8b58aa52` ·
`raghunath_edges_typed_signed.csv` `274d2225-741f-4069-94ce-89241fb78c8c` ·
`bajpai2023_crispr_hits.csv` `f016fc99-a43f-45d9-a611-b020d1cc694d` ·
`baxter2018_650_pigmentation_genes.csv` `056e62f9-f9b1-4c02-ae91-1d7786ef76ce` ·
`hirisplexs2018_markers.csv` `8caf2c0b-102b-4bc0-b620-3de18b7f51e4` ·
`pigmentation_gwas_catalog.csv` `dd61e041-cae8-4bb8-a7e5-d134f51abcb7`

**Notebook 2 — resolve network to genes:**
`gene_network_nodes.csv` `eb0110fa-b1c6-42fe-9766-4dd8b285ad41` ·
`gene_network_edges.csv` `b7ccce5a-1765-44f4-9cb6-ded912c5b7ae` ·
`node_resolution.csv` `69623169-3877-4467-8467-136b49e3f4ec` ·
`complex_members.csv` `f5b25620-8161-4ae9-ad17-6eae148ae1ac` ·
`nb2_omnipath_validation.csv` `689c847d-29d3-4770-a3fb-d16507645ced`

**Notebook 3 — validation-case set:** the 13 per-paper record CSVs in
[`data/case_records/`](data/case_records/), the classification in
[`data/processed/discordance_case_classification.csv`](data/processed/discordance_case_classification.csv)
+ its README, and the provenance record in
[`docs/NB3_case_assembly_provenance.qmd`](docs/NB3_case_assembly_provenance.qmd). Paper files are withheld
by `.gitignore` (re-obtainable by DOI via `data/raw/papers/REFERENCES.md`); the extracted records are kept.

**Governance & provenance:** `README.md` (`4fb96bc9`) · `DATA_SOURCES.md` (`a1872729`) ·
`project_dashboard.md` (this file) · `TODO.md` · `NB3_case_assembly_provenance.qmd` (`c2f65092`) ·
`LICENSE` (`a9f5e5bf`) · `REFERENCES.md` (`236a08f6`).

---
_Reconciled 2026-07-10 during the governance-consolidation session. Canonical numbers recomputed from the pinned
files; notebook status folded from `TODO.md`; design rationale absorbed from the retired build plan._
