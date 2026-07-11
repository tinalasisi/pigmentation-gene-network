# Project TODO ledger — Pigmentation gene-network build

**Scope:** project-wide task state for the pigmentation genotype→phenotype network
(hackathon → downstream grant). This is the backing ledger the internal dashboard references;
it is reconciled against the living documents, not memory.

**Last reconciled:** 2026-07-11, following the PI-agreed plan pivot (see `CHANGELOG.md`).

**This ledger distinguishes two kinds of item — do not treat them as equivalent:**
- **(b) AGREED** — the active, PI-approved plan (D'Arcy-annotation + case-gene-coverage finding). These are
  authorized work items with their gates and dependencies.
- **(c) NEEDS PI DISCUSSION — not authorized** — genuinely unsettled questions, including whether the
  deferred NB4–NB8 chain or the sex-hormone expansion are ever revisited. Nothing in that section is a todo
  to execute; it is a list of open questions for the PI.

**Source-of-truth documents (the living set):**
- `README.md` — the public-facing rebuild guide.
- `project_dashboard.md` — the single internal control surface (status, design rationale, open items).
- `TODO.md` — this backing ledger.
- `CHANGELOG.md` — the append-only, dated decision history.
- `project_dashboard.md` §2 — the AGREED vs deferred distinction (what is active vs critiqued-and-set-aside).
- `DATA_SOURCES.md` — the provenance manifest.

**Retired (do NOT treat as source-of-truth):** `hackathon_build_plan.md`, `REPLAN_HANDOFF.md`,
`2026-07-07_claude-science_HANDOFF.md`, `project_dashboard_provenance.md`, and all working drafts.

---

## Canonical numbers (verified 2026-07-10 against pinned artifacts)

Recomputed directly from the pinned processed files, not from any plan text:

- **NB1:** 265 nodes / 429 edges; signs **379 + / 43 − / 7 ·0**
  (`raghunath_nodes_typed.csv` `61b4b0fb-…`, `raghunath_edges_typed_signed.csv` `274d2225-…`).
- **NB2:** 168 gene nodes / 309 edge rows
  (`gene_network_nodes.csv` `eb0110fa-…`, `gene_network_edges.csv` `b7ccce5a-…`).
- **Validation-case set:** 13 papers, 3 D1 / 5 D2 / 5 both, 694 records (grain differs by paper)
  (`discordance_case_classification.csv` `8fe42dc9-…`), 31 distinct case genes.
- **D'Arcy backbone cross-check (run 2026-07-11):** 465 D'Arcy-union genes absent from the 168-gene backbone;
  227 of those disease-flagged (corrected from a prior plan-stated 230 — 3-gene synonym-resolution delta);
  118 hypopigmentation-class.
- **Case-gene coverage (computed 2026-07-11):** 9/31 (29%) already in the NB2 network; +7 recoverable via
  D'Arcy S1 disease-direction → 16/31 (52%); 15/31 absent from both ("dark matter").

See `project_dashboard.md` §2 and §3 for the AGREED/deferred distinction and the canonical numbers, and
`CHANGELOG.md` for the 2026-07-11 pivot that produced the D'Arcy and case-coverage figures above.

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

## (b) AGREED todos — active plan (PI-approved 2026-07-11)

**Item #0 (settle the notebook structure beyond NB2) is RESOLVED and retired — see the closed-items row
below.** The PI agreed the 3-phase, 9-step D'Arcy-annotation + case-gene-coverage plan (artifact
`e3d52bf4-4876-41f1-89c4-fb544c3677d1`, approved version `c1d3bf0a-ee55-45fb-8616-4ce3dceb9888`) in place of
the NB4–NB8 chain. Full rationale: `CHANGELOG.md` 2026-07-11 entry. The items below are the authorized work
from that plan; each carries its executor and cross-check gate from the approved plan artifact.

| # | Item | Phase | Executor | Cross-check gate | Depends on |
|---|------|-------|----------|-------------------|------------|
| 0 | **CLOSED 2026-07-11.** Settle the notebook structure beyond NB2 with the PI. Resolved by the plan pivot: NB3 formalized, NB4–NB8 deferred (not adopted). See `CHANGELOG.md` and `project_dashboard.md` §5a. | — | PM | — | — |
| 1 | Parse D'Arcy S1 into a clean annotation table (243-gene disease table → committed CSV + spec README). | 1 (parallel) | GENETICS_DATA_EXTRACTOR | REPRODUCIBILITY_SPECIALIST + DATA_SOURCE_AUDITOR | none |
| 2 | Reproduce the backbone cross-check as an independent second implementation (expect 465 / 227 / 118 — see Canonical numbers above). | 1 (parallel) | build | REPRODUCIBILITY_SPECIALIST (independent recompute, not a re-run) | item 1 |
| 3 | Attach S1 disease-direction to the 43 backbone-overlapping genes as a **new annotation column only** — hard integrity gate: no S4/S5 STRING edge may enter the backbone; no `node_class` may be mutated. | 1 (parallel) | build (annotate-then-enrich skill) | REPRODUCIBILITY_SPECIALIST + DATA_SOURCE_AUDITOR (joint) | item 1 |
| 4 | Resolve the 31 case-gene symbols via MyGene/HGNC (canonical IDs, not string match, per locked decision 6 — watch deprecated/synonym symbols e.g. LRMDA/C10orf11, ORAOV1). | 1 (parallel, independent of D'Arcy) | build | REPRODUCIBILITY_SPECIALIST | none |
| 5 | Formalize NB3 as a runnable document (§5a Option A); close the cheap provenance sign-offs (change-log backfill note, one-canonical-CSV-per-paper). | 1 (parallel, fully independent — does not gate Phase 2) | build | SCICOMM_REVIEWER + REPRODUCIBILITY_SPECIALIST | none |
| 6 | Build the master coverage table (9 in-network / 7 D'Arcy-recoverable / 15 dark-matter tiers) with evidence tags (HIrisPlex/Bajpai/Baxter). | 2 (gated on items 1–4, Gate A) | build | REPRODUCIBILITY_SPECIALIST (independent re-derivation of tier counts) | items 1, 2, 3, 4 |
| 7 | Cross discordance-direction (case D1/D2) against disease-direction (D'Arcy hypo/hyper/mixed) — the analytic core. | 2 (gated on item 6, Gate B) | build | REPRODUCIBILITY_SPECIALIST (join logic; missing labels reported not imputed) | item 6 |
| 8 | Draw the coverage-and-direction figure (coverage tier × disease direction × case direction; highlight albinism payoff loci + dark-matter gap). | 3 (gated on Gate B, parallel with item 9) | build (figure-composer/figure-style) | VISUAL_DATA_REVIEWER | item 7 |
| 9 | Write the findings memo (29%→52% coverage claim, 15-gene dark-matter gap, every number cited to a computed artifact). | 3 (gated on Gate B, parallel with item 8) | build | SCICOMM_REVIEWER + REPRODUCIBILITY_SPECIALIST | item 7 |

**Housekeeping items (not gated by the plan above — proceed independently):**

| # | Item | Belongs to | Owner | Blocking? |
|---|------|-----------|-------|-----------|
| 10 | **Reconcile `DATA_SOURCES.md` to the current design.** Reflect the D'Arcy annotation layer, the retirement of association-marker→causal-gene resolution (that step is deferred with NB4), the full-Bajpai-screen choice, bidirectional source roles. | manifest / provenance | PM | Correctness/traceability debt |
| 11 | **CLOSED — staging AND cross-check.** D'Arcy/Kiel (2023) 6 supplementary tables staged at `data/raw/darcy2023/*.xlsx` (CC BY 4.0; article PDF cited by DOI, not stored); untracked in git — any commit goes through REPO_COMPLIANCE_GATE separately. Cross-check run 2026-07-11 (item 2 above). | active-plan annotation layer | PM / build | No — closed |
| 12 | **Supply additional validation case studies** from PI's own literature review, if wanted. | validation-case set | PI | Optional extension |
| 13 | **Store hygiene — governance files saved under 3 parallel naming families** (`repo_*` current, `ondisk_*`/bare-name superseded duplicates). Re-save each canonical governance file as a new version of one artifact under its bare name; retire the `repo_*`/`ondisk_*` duplicates. | governance | PM | No — traceability/search-hygiene debt, not build-blocking |

**Build status:** Notebooks 1 and 2 complete and validated. The validation-case dataset (13 papers, 694
records, 31 case genes) is complete. Item #0 is resolved; items 1–9 above are the active, authorized work
(Phase 1 parallel tracks in progress; Phases 2–3 gated as shown).

---

## (c) NEEDS PI DISCUSSION — not authorized

_Nothing in this section is agreed work. These are open questions carried forward from the plan-deconvolutor
critique and the §5a decision log; they are not scheduled, not gated into the active plan, and must not be
treated as todos to execute. Bring these to the PI when there is a natural checkpoint (e.g. after the 2-day
deliverable lands)._

| # | Question | Origin |
|---|----------|--------|
| D1 | Should the NB4–NB8 causality-gated downstream chain ever be revisited post-deadline, and if so, on what timeline? It is deferred, not ruled out. | `CHANGELOG.md` 2026-07-11; `deconvolutor/2026-07-10_1859_DECONVOLUTOR_REPORT_NB4-NB8_downstream_chain.md` |
| D2 | If NB4–NB8 is revisited: what is the tie-break rule when nearest-gene, Open Targets L2G, and ClinVar/OMIM disagree on a locus's causal gene (the HERC2/OCA2 case is a real instance, not hypothetical)? | `project_dashboard.md` §5a gap 2 |
| D3 | If NB4–NB8 is revisited: what minimum evidentiary bar makes a "curated literature" edge admissible, given OmniPath itself barely covers the case genes? | `project_dashboard.md` §5a gap 3; live OmniPath check this session (HERC2 145/145 edges non-melanogenic; MFSD12/TMEM138 zero edges) |
| D4 | Should the sex-hormone × pigmentation expansion (steroidogenesis/AR/ESR coupling, cross-primate dichromatism) ever be pursued, and on what timeline, given the live OmniPath check found 0 direct AR/ESR1/ESR2→melanogenic edges? | `deconvolutor/2026-07-10_1808_DECONVOLUTOR_REPORT_sex_pigment_primate.md`; `internal/EXPANSION_PLAN_sex_pigment_primate.md` §6 (still-unanswered Decision Log A–F) |
| D5 | What is the eventual treatment of the 15 "dark-matter" case genes (absent from both the network and D'Arcy)? Candidates include: leave as an open finding (the point of the deliverable), pursue targeted literature curation per gene, or fold into a future NB4-style resolution if D1 is ever answered yes. | This session's coverage computation |
| D6 | Should Complex Portal/CORUM ever be attached as a connector? Only relevant if D1/D2 resolve toward reopening NB5's structural layer — not needed for the active plan. | Former TODO item (retired below) |
| D7 | Should ClinVar/OMIM be pinned as a versioned manifest input? Only relevant if D1 resolves toward reopening NB4's causal-gene resolution — not needed for the active plan (D'Arcy S1 disease-direction is an annotation, not a causal call). | Former TODO item (retired below) |

**Retired items (superseded by the 2026-07-11 pivot, kept here for traceability only):**
- Former item "Attach Complex Portal / CORUM connector" — was gated on old item #0; folded into D6 above.
- Former item "Pin ClinVar / OMIM as a versioned input" — was gated on old item #0; folded into D7 above.

---

## (d) Locked decisions — quick reference

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
   directed/signed) + S6 mass-spec expression. All 6 tables are staged under `data/raw/darcy2023/*.xlsx`;
   staging does not change the rule — D'Arcy's S4/S5 edges remain barred from the mechanistic backbone by
   locked decision 5, unchanged by the 2026-07-11 pivot. As of 2026-07-11, D'Arcy Table S1 is the **active
   plan's annotation layer** (§2 of `project_dashboard.md`) — consumed for disease-direction labels only,
   never as an input to a causal-gene resolution step (that step, part of the deferred NB4–NB8 chain, is not
   being built — see (b) AGREED todos above and `CHANGELOG.md`). The cross-check has been **run** (2026-07-11):
   465 D'Arcy genes absent from the 168-gene backbone; 227 disease-flagged (corrected from a prior
   plan-stated 230 — 3-gene synonym-resolution delta); 118 hypopigmentation-class. See `DATA_SOURCES.md` and
   `project_dashboard.md` §4 locked decision 2 for the full cross-check.
5. **NB1 offline/deterministic** (types only what the file fixes); all DB-backed typing +
   gene resolution in NB2, each call cited.
6. **Recompute network metrics on the final graph;** published precomputed values are validation
   references only.
7. **HIrisPlex / accuracy numbers cited only with population provenance;** no population /
   allele-frequency data in hackathon scope (deferred to grant).
8. **Every node/edge type traces to a recorded source;** no hand-typed classification lists.
9. **License:** MIT (Tina Lasisi). MCP acquisition fine if documented.
10. **Notebook/document format + publishing:** notebooks `.ipynb`, prose `.md`, no `.qmd` twin of any
    notebook. A Quarto → GitHub Pages setup (`_quarto.yml`, `index.qmd` as a prose landing page,
    `.github/workflows/publish-site.yml`; added in commit `c3f258b`) is **configured** to render committed
    `.ipynb` outputs with `execute: enabled: false` (no kernel, nothing withheld at render time); Quarto
    itself never runs in Claude Science. The config was verified this session; that the Actions run is green
    and the Pages URL serves is the PI's own report, not independently checked here. Briefly reversed
    2026-07-10 over a since-superseded `.qmd`-as-source-of-truth plan; see `project_dashboard.md` locked
    decision 10 for the full history and design rationale.
