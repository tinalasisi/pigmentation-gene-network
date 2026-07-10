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
guide), `DATA_SOURCES.md` (provenance manifest), `NB3_case_assembly_provenance.md` (case-set provenance),
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
> as a dataset. **Everything numbered 4 and beyond (NB4–NB8) is a tentative design sketch, not a spec** — the
> PI has not agreed the notebook layout past NB2 (see §2 above and TODO #0). The evidence-source lists,
> disease-bridge annotations, and per-gene outcomes named below are illustrative of the kind of design being
> considered, not fixed commitments: read every "lists X/Y/Z" as "a candidate set might include X, Y, Z" and
> every named outcome (e.g. a specific gene call) as an example the design would need to re-derive, not a
> result already computed. A builder should not treat any sentence below as settled spec. These notebooks
> must not be built or drafted until TODO #0 is resolved with the PI; see § Open decisions below for the
> options on the table.

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
   the finding is validated against. Provenance is recorded in `NB3_case_assembly_provenance.md`; several
   sign-off items remain open (see §5).
4. **Case-gene manifest + evidence layer + causal-gene resolution** ⬜ _(tentative design sketch, pending TODO #0)_ —
   The sketch: derive the resolution targets from the cases themselves — enumerate every (case, gene,
   anchor-genotype), join to the 168-gene network, and tag each gene `core-connected` / `present-isolated` /
   `absent`, which on today's case set would give something like a 9-connected / 10-absent split, to be
   recomputed if built. A candidate evidence-tag set might include a HIrisPlex target flag, a Bajpai CRISPR
   effect, a GWAS replication count, and a Baxter human-relevant flag, plus a standalone causal-gene
   resolution step (illustratively: nearest gene vs Open Targets L2G vs ClinVar/OMIM, with a tie-break rule
   still to be written — see NEXT_STEPS_PLAN gap #2 absorbed below). If built, the intent would be that the
   causal call gates NB5 and no gene enters the graph on association alone; none of this is implemented or
   agreed.
5. **Causality-gated connection of the validation-case genes** ⬜ _(tentative design sketch, pending TODO #0)_ —
   The sketch: connect the absent case-genes, but only the resolved causal gene and only through mechanism
   (OmniPath directed/signed + curated literature, with a minimum evidentiary bar for the literature half
   still to be written). Illustrative outcome categories a gene might fall into: an association marker whose
   causal gene is already in-network (e.g., a route-through case like HERC2→OCA2); a genuinely causal and
   connectable gene getting mechanistic signed edges (candidates discussed: SLC45A2, SLC24A5, SLC24A4, IRF4,
   ASIP); or a causal gene with no pathway mechanism, reported unconnectable (candidates discussed: MFSD12,
   DDB1, TMEM138 — noting MFSD12 in particular has an emerging melanosomal-transport mechanism in the
   literature not yet in curated pathway databases, so "unconnectable" there means "not yet in a curated
   edge source," not "no mechanism exists"). None of these gene-level outcomes are computed; they are
   examples of what the design would need to determine if built.
6. **Unify layers + recompute the load-bearing metrics** ⬜ _(tentative design sketch, pending TODO #0)_ —
   The sketch: build the single canonical graph and compute, per pigment endpoint, the two objects a figure
   would consume — signed distance/path enumeration from each causal gene (D1) and the set of genes with a
   directed path to the endpoint (D2 — the alternative-reach pool, recomputed on whatever graph NB5 would
   produce). A candidate design adds a degree-preserving null model for the D2 reachability count (with the
   sign/edge-type preservation and pre/post-D1-filter ordering questions still open — see NEXT_STEPS_PLAN gap
   #5 absorbed below) and applies the D1 path-block check to the D2 genes. Whether signed-graph reachability
   would need a boundary note distinguishing "locates where epistasis would act" from "establishes
   non-additivity" is a drafting question for if this notebook is built, not a settled claim now.
7. **Bidirectional discordance by node (the payoff figure)** ⬜ _(tentative design sketch, pending TODO #0)_ —
   The sketch: two panels per albinism causal locus (TYR→eumelanin; OCA2→melanosome) — D1 showing the signed
   modifier states that could block a present causal genotype, D2 showing the alternative genes/paths that
   reach the same endpoint without the usual gene, with null-model context if NB6 is built. It might annotate
   the nearest-vs-causal resolution at each locus (illustratively, HERC2-nearest vs OCA2-causal for
   rs12913832); any disease-bridge annotation would draw on ClinVar/OMIM sources and, additively, the now-staged
   D'Arcy Table S1 disease-gene table as a candidate evidence tag — this is not yet a checkable rule, and
   whether it stays a discretionary call or resolves to one is one of the open questions carried below.
   Whether this step is regenerable from an NB6 table alone, or should be merged with NB8, is likewise open.
8. **Case validation (machine-checkable, both directions)** ⬜ _(tentative design sketch, pending TODO #0)_ —
   The sketch: test each case against the network with a mechanism (D1/D2) pre-registered from the paper
   before the network is consulted, so a case could fail by being explained by the wrong mechanism —
   illustratively, does the signed-suppressor set for a locus contain the case-reported modifier (D1), or does
   the alternative pool reach the endpoint through the case's gene, split reachable vs unreachable (D2,
   candidates discussed: MFSD12/DDB1/TMEM138). A per-case pass/fail/unreachable table is one possible output
   shape; the case set would stay open to PI additions under the same pre-registration rule if this step is
   built. Whether genes whose only mechanistic edge derives from the same paper supplying their case should be
   scored, excluded, or flagged as non-independent is an open design question, not yet answered.

### The causality-gated spine _(tentative pipeline sketch, pending TODO #0 — not built)_

The candidate sequence being discussed: `NB3 cases → NB4 manifest + causal resolution → NB5 causality-gated
connection → NB6 metrics → NB7 figure → NB8 validation`. The one piece of this that IS a locked design
principle regardless of whether NB4-NB8 are ever built — locked decision 5 below — is that edge creation
uses OmniPath + curated literature only; association-flavoured sources (STRING co-expression, GWAS proximity,
and, per §3 above, D'Arcy's S4/S5 STRING-association edges) cannot manufacture a mechanistic edge. Everything
else in this section is illustrative of how that principle would apply if the sketch were built: every
absent case-gene would pass NB4 causal resolution before any edge is drawn, and only the resolved causal gene
would be connected. The HERC2/OCA2 example (rs12913832 is a long-range OCA2 enhancer; L2G HERC2 0.428 vs OCA2
0.203) and the MFSD12/DDB1/TMEM138 "unreachable" example are illustrations of the resolution logic, not
computed results — see NB5's entry above for the caveat on MFSD12 specifically.

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
2. **Backbone provenance:** Raghunath 2015 directed signed edges = mechanistic backbone. D'Arcy/Kiel 2023
   (DOI 10.3390/bioengineering10010013, PMC9854651, PMID 36671585, CC BY 4.0) is two components, neither of
   which is backbone: (a) Table S1, a 243-gene OMIM-backed disease-gene table (phenotype MIM + hyper/hypo/mixed
   pigmentation class) — an annotation/disease-direction source; (b) Tables S4/S5, a 451-node/4668-edge
   STRING PPI network (STRING `combined_score` — undirected, unsigned association, not directed/signed) +
   S6 A375/FM55 mass-spec expression. **All 6 supplementary tables are now staged** under
   `data/raw/darcy2023/*.xlsx` (retrieved from Europe PMC `PMC9854651/supplementaryFiles`, CC BY 4.0; the
   article PDF is cited by DOI, not stored). Staging does not change the backbone rule: the S4/S5
   STRING-association edges remain barred from the OmniPath + curated-literature mechanistic backbone by
   locked decision 5. D'Arcy is a **tentative, additive** evidence-tag / PPI-shell candidate for the proposed
   downstream design (§4, NB4/§5a Open decisions below) — it is not an input to NB4's causal-gene resolution
   (nearest-gene / Open Targets L2G / ClinVar-OMIM), and having it staged is not a build authorization for any
   proposed (NB4-NB8) step; the cross-check computation itself has not been run. See DATA_SOURCES.md for the
   465/230/118 backbone cross-check (S1∪S5 union; an earlier 173/76 figure was a narrower S5-only subset and
   is superseded).
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
10. **Notebook & document format:** notebooks are `.ipynb`; prose documents are plain Markdown (`.md`). Both
    render natively on GitHub with no build step, and — the deciding constraint — both preview in Claude
    Science, the surface this project is developed and reviewed in. No Quarto.
    _(Reversed 2026-07-10. The prior decision #10 mandated `.qmd` as the sole source of truth with a Quarto →
    GitHub Pages build. It was withdrawn on the empirical finding that `.qmd` registers in the artifact store
    as `application/octet-stream` and has no in-app viewer in Claude Science — it is download-only — whereas
    `.ipynb` (`application/x-ipynb+json`) and `.md` (`text/markdown`) both render inline. Committing to a
    format that is opaque in the working surface was the wrong call; the format decision now optimizes for the
    surface the work actually lives in. All Quarto scaffolding — `_quarto.yml`, `index.qmd`, `_site/`, and the
    `.qmd` form of the NB3 provenance record — was removed the same day, and the NB3 record was converted to
    `docs/NB3_case_assembly_provenance.md`. A static-HTML-linking-to-`.ipynb` publishing approach is under
    consideration as a lighter replacement — see open items — but is not adopted.)_

### Standing rule — surface-compatibility review before locking format/publishing decisions

_(Adopted 2026-07-10, prompted by the decision #10 reversal.)_ Any decision about **file format, artifact
type, or publishing/rendering approach** must be checked against how it behaves on the surface this project is
developed and reviewed in (Claude Science) **before** it is locked as a decision. Route such decisions through
the `PLATFORM_LIMITS_ADVISOR` specialist (backed by the `harness-limits-review` skill), which grounds every
limit in in-session introspection or a dated public source rather than memory. The decision #10 reversal —
committing to `.qmd`, which is download-only in Claude Science — is the failure this rule prevents: the
advisor already existed and was simply not consulted. This is a process rule, not a new capability.

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
| 2 | **CLOSED — staging.** D'Arcy/Kiel (2023) 6 supplementary tables (Table S1 disease-gene table; Tables S2/S3; Tables S4/S5 STRING PPI network; Table S6 mass-spec) staged on disk at `data/raw/darcy2023/*.xlsx` (CC BY 4.0; article PDF cited by DOI, not stored). Untracked in git as of this note — not yet committed; any commit goes through REPO_COMPLIANCE_GATE separately. **Residual — open:** the cross-check itself has not been run, and NB4/NB5 consumption of the staged tables is pending TODO #0. | tentative evidence-tag / PPI-shell candidate (design sketch pending TODO #0) | PM / build | No — staging done; residual cross-check/consumption work is additive, not a blocker; D'Arcy is not an input to NB4's causal-resolution calls (nearest-gene / L2G / ClinVar-OMIM) and its STRING-association edges cannot enter the OmniPath+curated-literature mechanistic backbone |
| 3 | Attach Complex Portal / CORUM connector (not attached). | NB5 | PM (connector) | Yes — blocks NB5 structural layer unless STRING+Reactome fallback is used |
| 4 | Pin ClinVar / OMIM as a versioned input in the manifest. | NB4 | PM / build | Yes — blocks NB4 causal-gene-resolution provenance |
| 5 | Supply additional validation case studies from the PI's own literature review, if wanted. | validation-case set | PI | Optional extension |
| 6 | Doc consolidation: `internal/NEXT_STEPS_PLAN.md` archived (2026-07-10) as a competing planning surface — its decision log/options absorbed into §5a above. | governance | PM | Done — recorded for the audit trail |
| 7 | Store hygiene — governance files saved under 3 parallel naming families (`repo_*` current, `ondisk_*`/bare-name superseded duplicates) per `ARCHIVE_MANIFEST.md`'s "Store hygiene — OUTSTANDING" note. Re-save each canonical governance file as a new version of one artifact under its bare name; retire the duplicates. | governance | PM | No — traceability/search-hygiene debt, not build-blocking |

**NB3 case-set provenance sign-off items** (from `NB3_case_assembly_provenance.md` §7 — decisions for the PI,
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

## 5a. Open decisions for TODO #0

_This section folds in the decision-log content from `internal/NEXT_STEPS_PLAN.md`, archived as a competing
planning surface (see §6 and `ARCHIVE_MANIFEST.md`). It records the options and open questions the PI needs
to answer to close TODO #0 — nothing here is settled; it is the input to that decision, not a decision._

**The three options weighed for what to build next** (none started; not mutually exclusive across time —
e.g. C now, then A or B later):
- **Option A — build the case-assembly step as a real, runnable document (an NB3 formalization).** Narrow
  scope: turns the already-complete case-assembly dataset into a regenerable document. Does not by itself
  commit to NB4–NB8.
- **Option B — settle the full NB4–NB8 structure now**, after closing the load-bearing gaps below. Commits
  to the causality-gated downstream chain in §4's notebook map as a designed plan, once the gaps are
  resolved. Converts today's "proposed direction" language into a committed plan in one step.
- **Option C — housekeeping-first: do the buildable-now items and defer the structure decision.** Proceeds
  with items not gated by TODO #0 (DATA_SOURCES.md reconciliation, NB3 provenance change-log backfill,
  duplicate-CSV retirement, optional additional cases) while #0 is decided separately.

**Load-bearing gaps that would need to close before Option B is approvable** (a plan-critic review; none of
these block Option A or C):
1. Circularity risk between NB4 and NB8 — a case's mechanistic edge (NB5) and its validation case (NB8) can
   derive from the same paper, so a "pass" may just confirm the extraction read the paper correctly rather
   than showing independent network explanatory power. No current tracking or exclusion rule.
2. No causal-gene tie-break rule when nearest-gene, Open Targets L2G, and ClinVar/OMIM disagree (the
   HERC2/OCA2 illustration is a real instance of this disagreement, not a hypothetical).
3. No stated minimum evidentiary bar (PMID count, evidence code, curation database) for a "curated
   literature" edge — the literature half of the edge-admission rule is otherwise unaudited.
4. OmniPath is heterogeneous — some of its components (e.g., text-mining/expression-inferred regulon calls
   in DoRothEA/CollecTRI) are not clearly more mechanistic than the STRING association signal the design
   excludes; naming OmniPath without a resource/evidence-tier filter doesn't guarantee the directed/signed
   bar is met edge-by-edge.
5. Null-model specification gap — unclear whether the degree-preserving null for D2 reachability also
   preserves edge sign and edge-type composition, and whether it is fit before or after the D1 path-block
   filter.
6. The D2 "alternative-causal pool" label implies causal resolution that only actually holds for newly
   NB5-gated genes; pre-existing NB2 backbone nodes were admitted under looser, association-permissive
   typing and would not be re-screened before being counted in D2.
7. NB7's "regenerable from NB6 alone" claim is in tension with a discretionary disease-bridge-genuineness
   judgment described in the same step.
8. NB7/NB8 duplication risk — both consume identical D1/D2 outputs and differ only in output format; kept as
   separate notebooks, the shared logic can drift out of sync between them.
9. Scope-disclosure mismatch — the granular design detail already written (named gene outcomes, specific
   tie-break requirements) outruns the "not yet agreed" framing that governs it; §4's notebook map has now
   been reworded (2026-07-10) to close this specific gap.
10. Evidence-tag combination rule is missing — no stated rule for how HIrisPlex/Bajpai/GWAS/Baxter evidence
    tags combine or resolve when they disagree on a gene.
11. Open Targets L2G may cross the anti-leakage boundary — L2G is itself network/functional-genomics-derived
    (eQTL, chromatin interaction, VEP features); if it resolves a case's causal gene before that gene's
    mechanism is pre-registered per locked decision 8, it is unclear whether L2G counts as "the network" for
    that boundary.

_Balancing note carried from the same review: the methodological core is not in question — the HERC2/OCA2
example is established biology, restricting mechanistic edges to OmniPath's signaling/TF-target/enzyme-
substrate resources while excluding STRING/GWAS-proximity is the standard causality-gating distinction, and
L2G+ClinVar/OMIM+nearest-gene triangulation is a legitimate resolution strategy. The gaps above are about
specification and audit trail, not the underlying scientific logic._

**Feasibility flags:** the MFSD12/DDB1/TMEM138 "unreachable" framing is uneven — MFSD12 has an emerging
melanosomal-transport mechanism in the literature not yet in curated pathway databases (so "not yet curated"
is the accurate claim there, not "no mechanism exists"); TMEM138 has essentially no established
melanogenesis mechanism and DDB1 is pleiotropic with only indirect links. At network scale (~168–200 nodes),
an empirical null from edge-swapping will be noisy, and naive swapping on a signed directed graph can
introduce sign-degree artifacts unless sign and direction are preserved deliberately.

**Decision-log questions for the PI** (grouped by area; answer directly against these, e.g. in a PI-annotated
copy of this section or in conversation with the PM):

*Scope:*
1. Authorize NB4–NB8 at today's level of written detail, or scope narrowly to "formalize the case-assembly
   step" with NB4–NB8 held as an unelaborated placeholder pending separate sign-off?
2. Given the grant horizon, is the full six-notebook apparatus (null model, structural-connector dependency,
   external-paper dependency) the right scope, or would a lighter NB4+NB8-only causal-check fit the timeline
   better?

*Causal-gene resolution and edge admissibility (blocks NB4/NB5 regardless of Q1–2):*
3. What is the tie-break rule when nearest-gene, L2G, and ClinVar/OMIM disagree on a locus's causal gene?
4. What minimum evidentiary bar makes a "curated literature" edge admissible for NB5?
5. Should the causal-gene resolver be built as a standalone, reusable module rather than embedded in a
   case-manifest document?

*Anti-leakage and independence of validation:*
6. For genes whose only mechanistic edge is sourced from the same paper as their case, should that case be
   scored separately, excluded, or flagged non-independent?
7. Does L2G count as "the network" for the anti-leakage boundary (locked decision 8)?

*Null model and metrics design:*
8. Should the D1 path-block filter apply before or after the D2 null model is fit, and should the null
   preserve edge sign and edge-type rather than degree alone?

*Payoff figure and case validation:*
9. Is "disease bridge, where genuine" meant to become a checkable rule, or stay discretionary — and if
   discretionary, should the "regenerable from NB6 alone" claim be dropped?
10. Should the payoff figure and case validation merge into one document sharing a single D1/D2 computation
    layer?

*Documentation publishing (tentative — replaces the withdrawn Quarto workstream; see reversal in decision #10):*
11. Adopt static HTML linking to the `.ipynb` notebooks (GitHub renders `.ipynb` natively; a plain `index.md`
    or small static `index.html` links to each), or rely on GitHub's native in-repo rendering with no site at
    all? No build step either way. This is a proposed direction, not adopted.

**What happens once these are answered:** the PM reconciles this dashboard and `TODO.md` against the
answers, closes TODO #0, and either formalizes the case-assembly step per the chosen scope or proceeds with
housekeeping only — in whatever combination the answers specify. No NB4–NB8 build action is taken until that
reconciliation happens.

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
- **[`docs/NB3_case_assembly_provenance.md`](docs/NB3_case_assembly_provenance.md)** — case-set
  extraction provenance record (plain Markdown; converted from `.qmd` on 2026-07-10, see decision #10).
- **[discordance_case_classification_README.md]({{artifact:art_5079f196-a5ce-4f4d-a79b-20217c472f1a}})** — case
  classification data dictionary.
- **[data/raw/papers/REFERENCES.md](data/raw/papers/REFERENCES.md)** — paper-withholding doc (per-paper
  citations, DOIs, license/access, how to obtain each file); lives with the (withheld) papers.

**Archived documents** are recorded in `internal/archive/ARCHIVE_MANIFEST.md` (retired build plan, superseded
dashboard views, handoff briefs, and working drafts) — see that manifest for the per-document row.

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
[`docs/NB3_case_assembly_provenance.md`](docs/NB3_case_assembly_provenance.md). Paper files are withheld
by `.gitignore` (re-obtainable by DOI via `data/raw/papers/REFERENCES.md`); the extracted records are kept.

**Governance & provenance:** `README.md` (`4fb96bc9`) · `DATA_SOURCES.md` (`a1872729`) ·
`project_dashboard.md` (this file) · `TODO.md` · `NB3_case_assembly_provenance.md` ·
`LICENSE` (`a9f5e5bf`) · `REFERENCES.md` (`236a08f6`).

---
_Reconciled 2026-07-10 during the governance-consolidation session. Canonical numbers recomputed from the pinned
files; notebook status folded from `TODO.md`; design rationale absorbed from the retired build plan._
