# Project TODO ledger — Pigmentation gene-network build

**Scope:** project-wide task state for the pigmentation genotype→phenotype network
(hackathon → downstream grant). This is the backing ledger the internal dashboard references;
it is reconciled against the living documents, not memory.

**Last reconciled:** 2026-07-10, during the document-currency audit.

**Source-of-truth documents (the living set):**
- `README.md` — the public-facing rebuild guide.
- `project_dashboard.md` — the single internal control surface (status, design rationale, open items).
- `TODO.md` — this backing ledger.
- `project_dashboard.md` §2 — the AGREED vs TENTATIVE distinction (what is settled vs proposed).
- `DATA_SOURCES.md` — the provenance manifest.

**Retired (do NOT treat as source-of-truth):** `hackathon_build_plan.md`, `REPLAN_HANDOFF.md`,
`2026-07-07_claude-science_HANDOFF.md`, `project_dashboard_provenance.md`, `internal/NEXT_STEPS_PLAN.md`
(competing planning surface, absorbed into `project_dashboard.md` §5a), and all working drafts
(archived with a manifest).

---

## Canonical numbers (verified 2026-07-10 against pinned artifacts)

Recomputed directly from the pinned processed files, not from any plan text:

- **NB1:** 265 nodes / 429 edges; signs **379 + / 43 − / 7 ·0**
  (`raghunath_nodes_typed.csv` `61b4b0fb-…`, `raghunath_edges_typed_signed.csv` `274d2225-…`).
- **NB2:** 168 gene nodes / 309 edge rows
  (`gene_network_nodes.csv` `eb0110fa-…`, `gene_network_edges.csv` `b7ccce5a-…`).
- **Validation-case set:** 13 papers, 3 D1 / 5 D2 / 5 both, 694 records (grain differs by paper)
  (`discordance_case_classification.csv` `8fe42dc9-…`).

See `project_dashboard.md` §2 and §3 for the AGREED/TENTATIVE distinction and the canonical numbers.

---

## (a) DONE this session (2026-07-09) — design consolidation

- **Finding locked** — reframed to a **bidirectional genotype→phenotype discordance** model
  on a signed directed network:
  - **D1** (causal variant present, phenotype absent) → modifier-node states that block the path.
  - **D2** (phenotype present, usual variant absent) → 114 alternative genes reaching a pigment
    endpoint on the 168-gene backbone.
  - Payoff loci = albinism causal genes **TYR (OCA1) + OCA2** = the clinical validation cases.
  - Both directions computable on the existing **NB1 + NB2 backbone alone** (safety net;
    expansion enriches but is not required).
- **"Why pigmentation" argument locked** — near-zero environmental variance + high heritability
  ⇒ discordance is almost purely genetic-architecture, unlike environment-confounded complex
  disease. Anchored: Zhu/Evans/Duffy 2004 (twin), Morgan 2018 (UK Biobank), Pavan & Sturm 2019.
- **Penetrance/epistasis literature adopted as conceptual backbone** (all DOI-verified):
  incomplete penetrance = D1 (Cooper 2013; Kingdom & Wright 2022; Chen 2016, 589k genomes);
  epistasis mechanism (Crawford 2017 = human **multi-locus/oligogenic, NOT epistasis**;
  Demars 2022 = genuine epistasis but **RABBIT/animal-model analogue** — the two kept
  explicitly distinct); omnigenic (Vuckovic 2020); PRS-portability = grant horizon (Martin 2019).
- **Notebook structure beyond NB2 is TENTATIVE (not yet agreed by the PI).** Only NB1 and NB2 are
  agreed as notebooks. The case-assembly work is complete as a dataset, but its placement as a numbered
  notebook and the entire downstream chain (causal-gene resolution, causality-gated connection, metrics
  recompute, payoff figure, case validation) are a **proposed direction** to be settled with the PI, not
  a fixed plan. Do not draft those notebooks or their intros until agreed. See `project_dashboard.md` §2.
- **Deferred to grant (tentative):** four-axis functional annotation; ancestry / allele-frequency
  verification.
- **Six artifact annotations resolved** (folded into the design rationale, now in `project_dashboard.md`):
  1. Named populations removed from pitch (no allele-frequency data in scope).
  2. Case set noted **open** — PI supplies more from own literature review.
  3. Crawford / Demars corrected (oligogenic-human vs epistasis-rabbit, kept distinct).
  4. PRS-generalization added as explicit grant-direction bridge.
  5. **D'Arcy/Kiel 2023** (DOI 10.3390/bioengineering10010013, PMC9854651, PMID 36671585, CC BY 4.0)
     — 6 supplementary tables now staged under `data/raw/darcy2023/*.xlsx`: Table S1 (243-gene
     OMIM-backed disease-gene table) and Tables S4/S5 (451-node/4668-edge STRING PPI network,
     association not mechanistic), plus S2/S3/S6. Noted as a candidate source for the proposed
     downstream work; additive evidence-tag/PPI-shell candidate, not an NB4 input; cross-check
     computation not yet run. See `DATA_SOURCES.md` and `project_dashboard.md` locked decision 2.
  6. Activity-class origin explained (Raghunath's own node labels, expanded to gene families
     via HGNC).

---

## (b) OPEN todos

| # | Item | Belongs to | Owner | Blocking? |
|---|------|-----------|-------|-----------|
| 0 | **Settle the notebook structure beyond NB2 with the PI.** Everything downstream of NB2 is a proposed direction, not agreed. This decision gates all items below that name a specific downstream notebook. | plan | PI | Gates the downstream design |
| 1 | **Reconcile `DATA_SOURCES.md` to the current design.** Reflect: association-marker→causal-gene resolution (L2G anchored by ClinVar), the full-Bajpai-screen choice, bidirectional source roles. | manifest / provenance | PM | Correctness/traceability debt |
| 2 | **CLOSED — staging.** D'Arcy/Kiel (2023) 6 supplementary tables staged on disk at `data/raw/darcy2023/*.xlsx` (CC BY 4.0; article PDF cited by DOI, not stored). Untracked in git as of this note — not yet committed; any commit goes through REPO_COMPLIANCE_GATE separately. **Residual — open:** the cross-check computation has not been run, and NB4/NB5 consumption of the staged tables is pending TODO #0. Additive evidence-tag / PPI-shell candidate, not an input to NB4's causal-gene resolution (nearest-gene / L2G / ClinVar-OMIM); its STRING-association edges (S4/S5) cannot enter the mechanistic backbone regardless of staging. | tentative evidence-tag / PPI-shell candidate | PM / build | No — staging done; residual cross-check/consumption work is additive, not a blocker |
| 3 | **Attach Complex Portal / CORUM connector.** Not attached — a dependency for the proposed structural-gene layer. STRING + Reactome fallback is documented. | proposed downstream | PM (connector) | Gated by item #0 |
| 4 | **Pin ClinVar / OMIM as a versioned input** in the manifest, for causal-gene resolution provenance. | manifest → proposed downstream | PM / build | Gated by item #0 |
| 5 | **Supply additional validation case studies** from PI's own literature review, if wanted. | validation-case set | PI | Optional extension |
| 6 | **Doc consolidation: `internal/NEXT_STEPS_PLAN.md` archived** (2026-07-10) as a competing planning surface — its decision log/options absorbed into `project_dashboard.md` §5a. No action needed; recorded for the audit trail. | governance | PM | Done — recorded here for traceability |
| 7 | **Store hygiene — governance files saved under 3 parallel naming families** (`repo_*` current, `ondisk_*`/bare-name superseded duplicates) per `ARCHIVE_MANIFEST.md`'s "Store hygiene — OUTSTANDING" note. Re-save each canonical governance file as a new version of one artifact under its bare name; retire the `repo_*`/`ondisk_*` duplicates. | governance | PM | No — traceability/search-hygiene debt, not build-blocking |

**Build status:** Notebooks 1 and 2 are complete and validated. The validation-case dataset (13 papers,
694 records) is complete. The downstream analysis is **not started and its notebook structure is not yet
agreed** — item #0 is the gate.

---

## (c) Locked decisions — quick reference

1. **Finding:** bidirectional discordance (D1 modifier-block + D2 alternative-gene reach)
   on the signed directed network; payoff = TYR/OCA2. The D2 alternative-reach count is a figure to be
   recomputed on the connected graph, not a fixed number.
2. **Why pigmentation:** near-zero environmental variance + high heritability ⇒ discordance is
   genetic-architecture, not environment (Zhu 2004, Morgan 2018, Pavan & Sturm 2019).
3. **Conceptual backbone = penetrance/epistasis literature** (all DOI-verified);
   Crawford (oligogenic, human) and Demars (epistasis, rabbit) kept **explicitly distinct**.
4. **Backbone provenance:** Raghunath 2015 directed signed edges = mechanistic backbone. D'Arcy/Kiel 2023
   (DOI 10.3390/bioengineering10010013, PMC9854651, PMID 36671585, CC BY 4.0) is two components, neither
   backbone: (a) Table S1, a 243-gene OMIM-backed disease-gene table (annotation/disease-direction layer);
   (b) Tables S4/S5, a 451-node/4668-edge STRING PPI network (undirected/unsigned association, not
   directed/signed) + S6 mass-spec expression. All 6 tables are now staged under
   `data/raw/darcy2023/*.xlsx`; staging does not change the rule — D'Arcy is a **tentative, additive**
   evidence-tag/PPI-shell candidate, not an NB4 input, and its S4/S5 edges are barred from the mechanistic
   backbone by locked decision 5 regardless of staging. The cross-check computation itself has not been
   run. See `DATA_SOURCES.md` and `project_dashboard.md` §4 locked decision 2 for the full cross-check
   (465 D'Arcy genes absent from the 168-gene backbone, 230 disease-flagged, 118 hypopigmentation-class).
5. **NB1 offline/deterministic** (types only what the file fixes); all DB-backed typing +
   gene resolution in NB2, each call cited.
6. **Recompute network metrics on the final graph;** published precomputed values are validation
   references only.
7. **HIrisPlex / accuracy numbers cited only with population provenance;** no population /
   allele-frequency data in hackathon scope (deferred to grant).
8. **Every node/edge type traces to a recorded source;** no hand-typed classification lists.
9. **License:** MIT (Tina Lasisi). MCP acquisition fine if documented.
