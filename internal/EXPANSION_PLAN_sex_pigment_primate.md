# Expansion plan — sex-hormone × pigmentation coupling, toward a comparative primate question

**Status: TENTATIVE — for-alignment draft, not yet agreed. Not a build authorization.**
**Date:** 2026-07-10.
**Scope of this document:** a forward expansion of the project beyond the current pigmentation network,
reconciled to the PI's stated goal — **hormonal modulation of pigmentation, and when it produces sexual
dichromatism across primates.** Placing this in `internal/` changes no build state, no notebook, and no data
file. It makes no git commit. It lays out the reconciled backbone decision, the staged design, and the
decisions the PI must make, so they can be answered directly in the Decision Log (§6).

**Supersedes / reconciles two prior research memos:**
- *sex_hormone_network_scoping.md* — scoping of whether a sex-hormone network analog to Raghunath exists.
- *sex_pigment_primate_integration_strategy.md* — integration/phylogeny strategy.
This plan resolves the backbone tension between them (§2) and is the actionable local document; the memos
remain the long-form background.

---

## 1. Current grounded state (as recorded in `project_dashboard.md` §3; re-derive from the source files, not memory)

| Fact | Value | Source |
|---|---|---|
| Raghunath backbone nodes / edges | 265 / 429 | NB1 network files |
| Edge signs (+ / − / 0) | 379 / 43 / 7 | NB1 edge file |
| Gene-level network nodes (NB2) | 168 | `gene_network_nodes.csv` |
| Gene-level network edge rows (NB2) | 309 | `gene_network_edges.csv` |
| Validation-case records | 694 | `EXTRACT_*_records.csv` |

The existing pigmentation network (NB1 reconstruction → NB2 gene resolution) is the substrate this expansion
attaches to. **No number above changes as a result of this plan** — it is forward scope, not a build edit,
and it edits no processed data file. Values should be re-confirmed against the current source files before
they are relied on.

---

## 2. Backbone decision — RECONCILED to hormonal modulation

**Prior position (scoping memo):** the cleanest *methodological* Raghunath analog is the **gonadal
sex-determination** logical model (Ríos et al. 2016, doi:10.1186/s12918-016-0282-3) — a curated directed
signed network.

**Reconciled position (this plan):** the PI's goal is *hormonal modulation of pigment*, and that coupling is
mechanistically carried by **steroid biosynthesis and steroid/receptor action on melanogenic genes**, not by
the gonadal fate decision. Therefore:

- **Mechanistic backbone = steroidogenesis + receptor layer.**
  - *Steroidogenesis:* KEGG pathway **hsa00140** *Steroid hormone biosynthesis — Homo sapiens* (accession and
    title verified via KEGG REST, `rest.kegg.jp/get/hsa00140`); Reactome as a cross-check. Edge type =
    enzyme-catalyzed metabolic conversion (directed, not signed) — kept as a distinct typed layer.
  - *Receptor→target layer:* AR (androgen receptor) and ESR1/ESR2 (estrogen receptors) acting on downstream
    genes. Edge type = signed regulatory. Highest provenance burden; assembled with per-edge citations.
- **Sex-determination (Ríos 2016) is demoted to UPSTREAM CONTEXT, not backbone.** It sets *which hormonal
  milieu* a body is in (which gonad → which steroid output), but it is not the layer that touches pigment. It
  may enter later as the switch that selects hormonal state; it is not built as the mechanistic core.

**Why this reconciliation strengthens, not weakens, the design:** the orthology hazard flagged in the
integration memo — lineage-specific duplication/loss in the **CYP and HSD** steroidogenic families — now sits
*on the backbone itself*. That is where a comparative-genomics signal for dichromatism is most plausible
(evolvable steroid-synthesis capacity), so putting it on the critical path is a feature. It does raise the
Stage-C orthology work from a formality to a central task (§4, Layer 2).

**The coupling interface (where the two networks meet) is small and concrete:**
1. **Steroid-response regulation of melanogenic enzymes** — steroid hormones modulate TYR / TRP-1 / TRP-2
   transcripts in human melanocytes (doi:10.1038/jid.1998.1); ER effects on melanocytes
   (doi:10.2147/ccid.s333663); AR signaling in the melanocyte lineage (doi:10.1084/jem.20201137).
2. **The melanocortin hub as the shared node** — MC1R / POMC / ASIP link coloration and endocrine/physiological
   state pleiotropically (Ducrest & Roulin, doi:10.1016/j.tree.2008.06.001).
These define an explicit **bridge-edge table** connecting the receptor layer to pigmentation nodes — three
typed layers (pigmentation / hormonal / coupling), not one merged graph.

---

## 3. Capability inventory (checked against the live skill catalog + connectors, 2026-07-10)

| Need | Status | Tool |
|---|---|---|
| Ortholog / homology across primates | **Available** | `mcp-genomes` (`ensembl_homology`) — Compara ortholog vs. paralog typing |
| Orthology at scale / constraint | **Available (data)** | TOGA (doi:10.1126/science.abn3107); primate constraint (doi:10.1126/science.abn8197); Zoonomia (doi:10.1126/science.abn3943) |
| Gene identity / ID mapping / UniProt / Reactome | **Available** | `mcp-genes-ontologies`, `mcp-biomart` |
| Coding-sequence retrieval per species | **Available** | `mcp-genomes` (`ensembl_sequence`) |
| Cross-species sequence scoring | **Available** | `evo2` (coding likelihoods), `borzoi` (regulatory) |
| GWAS layer (hormone levels, pigmentation) | **Available** | `mcp-human-genetics` |
| **Phylogenetic comparative methods** (PGLS, phylo-logistic, ancestral state) | **Not a curated skill** | Installable: R `ape` / `phytools` / `caper` / `geiger` |
| **dN/dS selection tests** | **Not a curated skill** | Installable: bioconda PAML / HyPhy; MAFFT for MSA |
| **MSA / tree building** | **Not a curated skill** | Installable: MAFFT, IQ-TREE (bioconda) |

Ortholog + genome retrieval is supported out of the box; the phylogenetic-statistics / molecular-evolution
layer is standard, license-free software that must be stood up (routine conda/bioconda). That is the only new
tooling investment.

---

## 4. The three compounding assumption layers (resolve in order; each gates the next)

**Layer 1 — Coupling edges.** The scientific content of the expansion; each bridge edge cited individually,
same discipline as existing edges. Deliverable: the three-layer typed graph.

**Layer 2 — Orthology (now on the backbone → central, not a formality).** Per-gene classification across
primates: 1:1 ortholog / one-to-many (paralog) / absent. Pigmentation core (TYR, OCA2, MC1R, MITF) is largely
clean 1:1 — favorable. The **CYP / HSD steroidogenic families are the hazard** — lineage-specific duplication
means "the ortholog" may not be well-posed. **Pre-registered rule:** only 1:1 orthologs enter the primary
comparative test; one-to-many genes analyzed separately with duplication modeled, never silently collapsed;
no-ortholog genes flagged and reported, never imputed. Analogs excluded (they break the homology assumption).
Direct extension of the project's existing "resolve to the causal gene before drawing an edge" rule.

**Layer 3 — Phylogenetic non-independence.** Primate species are not independent; shared ancestry confounds
any genotype↔dichromatism correlation. The test must use PGLS / phylogenetic logistic regression on a dated
primate tree, with a consistently coded dichromatism phenotype. Anchor datasets exist (facial colour patterns,
doi:10.1098/rspb.2011.2326; Colobinae pelage phylogenetics, doi:10.1371/journal.pone.0061659) but a
standardized dichromatism score is its own curation task.

Total confidence is the **product** of the three layers, not the sum — hence the staging in §5.

---

## 5. Staged design (each stage independently valuable and publishable)

1. **Stage A — Coupling layer (human, in silico).** Build the hormonal backbone (steroidogenesis hsa00140 +
   AR/ER receptor layer) and the explicit bridge-edge table to pigmentation at the melanocortin/steroid-
   response interface. Deliverable: three-layer typed graph. Uses only currently-available methods.
2. **Stage B — Conditional prediction (human, in silico).** Formalize "under which sex-network states do we
   expect between-sex pigmentation differences" as signed-path / perturbation analysis on the coupled graph,
   with hormonal state as the conditioning input — the same modifier-node reasoning the pigmentation project
   already does. Deliverable: testable conditional predictions.
3. **Stage C — Orthology resolution (HARD GATE before any comparative test).** Classify every gene in both
   layers across primates; apply the §4-Layer-2 rule; emit the gene set that is genuinely comparable.
4. **Stage D — Phylogenetic test (the evolutionary question).** On the comparable set, test whether
   network-predicted dichromatism potential correlates with observed primate sexual dichromatism (PGLS /
   phylo-logistic on a dated tree, standardized dichromatism score). Optional: dN/dS on bridge-node genes to
   ask whether the coupling interface shows lineage-specific selection.

If Stage-D signal is weak, Stages A–B still stand as a mechanistic sex×pigment model.

---

## 6. Decision log — please answer directly in this file

### A. Backbone confirmation
Confirm the reconciled backbone (§2): steroidogenesis + AR/ER receptor layer as mechanistic core, sex-
determination as upstream context only. **[ PI answer: ______ ]**

### B. Dichromatism phenotype definition
Binary (dimorphic / not) · continuous (colour-distance score) · trait-partitioned (pelage / facial / skin)?
Determines Stage-D statistics and curation effort. **[ PI answer: ______ ]**

### C. Primate scope
All primates · catarrhines only · a phenotype-dense clade? Broader scope worsens ortholog-completeness
(§4 Layer 2). **[ PI answer: ______ ]**

### D. Coupling-edge sourcing
Literature-curated only (recommended, given how load-bearing bridge edges are) · also a signed-interaction
database? **[ PI answer: ______ ]**

### E. Molecular-evolution depth
Orthology + presence/absence only · full dN/dS on bridge genes (adds MSA/PAML tooling, §3)? **[ PI answer: ______ ]**

### F. Sequencing vs. the current build
Does this expansion start after the current NB4–NB8 pigmentation chain is settled, or run as a parallel
track? **[ PI answer: ______ ]**

---

## 7. What happens after this document is answered

Once §6 is answered, the plan is promoted from TENTATIVE to an agreed expansion track. Promotion is not the
plan file sitting in `internal/` — it is the track being **entered into the project changelog**. Tracking uses
three distinct documents, and this expansion is recorded across them the same way any other work is:

- **Changelog** — the singular, append-only history: one dated entry per meaningful build or decision event
  (including this expansion's promotion and each §6 answer). It is separate from the running TODO and is the
  record of *what changed and why*. This is the document whose existence gates whether the track is real.
- **Running TODO** — the forward ledger of open work items (e.g. the Stage A–D tasks in §5). It answers *what
  is left to do*, not what has happened.
- **Dashboard** — the snapshot/control surface: current grounded state and canonical pointers. It **references**
  the changelog and the TODO; it does not duplicate their content or double as a history.

No repository commit is made from this document; any commit goes through the compliance gate.
