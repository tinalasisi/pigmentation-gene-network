# Project TODO ledger — Pigmentation gene-network build

**Scope:** the forward ledger of open work for the pigmentation genotype→phenotype network project. Answers
*what is left to do*; it does not duplicate `CHANGELOG.md` (history) or `project_dashboard.md` (snapshot/
control surface — see note below on its current absence). One of the three tracking documents described in
`START_HERE.md`.

**(Re)created:** 2026-07-12T00:29Z. The prior `TODO.md` was archived (gitignored, `internal/archive/`) in the
2026-07-11T22:51Z clean restart along with `project_dashboard.md`; unlike the dashboard, this ledger is
re-created now because the plan approved the same day needs a live place to track its five phases.
`project_dashboard.md` remains absent from disk — see the note in `internal/CHANGELOG.md`'s
2026-07-12T00:29Z entry; re-creating it is not in this ledger's scope to decide, only to flag.

**Source-of-truth documents:** `internal/CHANGELOG.md` (append-only decision history), this file (open work),
`internal/START_HERE.md` (goal + inventory), `DATA_SOURCES.md` (provenance manifest). The approved execution
plan itself is tracked as a Claude Science artifact, not a repo file — see the pointer in the tracked-work
table below.

---

## Recently resolved (not part of the NB4–NB8 plan)

- ✅ **NB2 reproducibility — RESOLVED and committed (`95f1969`), 2026-07-12T01:16Z.** All 14 inputs NB2 read
  but the repo never committed (7 frozen `db_responses/` JSONs + 2 orphan intermediate CSVs + 5 figures) were
  regenerated, verified to reproduce the committed outputs value-for-value on a fresh-clone run, and committed
  through the Tier-2 compliance gate. NB2 can now be re-run on a fresh clone (all REQUERY flags `False`). Full
  detail in `CHANGELOG.md` 2026-07-12T01:16Z. This closes the T23:57Z Catch 1 and T00:34Z item-5 blockers and
  discharges Decision 5 (T00:29Z) for NB2. Two documentation follow-ups it surfaced are logged below.

---

## Open follow-ups from the NB2 reproducibility fix (documentation only, non-blocking)

- ⬜ **Document the `PLC*` filter in `DATA_SOURCES.md` entry 6 (line ~179).** The manifest records "PLC 832 =
  14" without noting that HGNC group 832 returns 19 protein-coding members (5 are PLA2G4* contaminants), so a
  `PLC*` prefix filter is required to reach 14 — unlike PLA2 and Trypsin, whose filters ARE recorded. Add the
  filter step for parity. Biologically correct and already applied in the frozen `hgnc_gene_groups.json`; only
  the manifest prose is incomplete.
- ⬜ **Add figure-generating code to NB2.** The 5 `notebooks/figures/step*.png` are committed but no cell in
  the repo produces them (no `savefig` in NB2). They were recovered from the notebook's embedded outputs to
  unblock the re-run; a proper fix adds the plotting cells so the figures reproduce rather than being opaque
  committed binaries. Flag to PI — this is authoring work on NB2, not a bookkeeping fix.

---

## Tracked work — approved plan (convergence-graded rescue screen, NB4–NB8)

**Plan of record:** artifact_id `083f9097-0134-4490-abe9-33ad4ed7c9da`, version_id
`d135912f-6112-48f4-95c1-545c46cabfba`, filename `plan_convergence-graded-rescue-screen-as-self_8a368b7b.json`,
approved 2026-07-12T00:21Z. Read that artifact directly for the exact phase/step text; the rows below are a
tracking summary, not a substitute. Decisions 1–6 behind this plan are recorded in `CHANGELOG.md`'s
2026-07-12T00:29Z entry.

Dependency order — each phase consumes the prior phase's frozen output; do not start a phase out of order.

| # | Phase | Status | Depends on | Notes |
|---|-------|--------|-----------|-------|
| 1 | **NB4** — unified association base with author-explanation status (curated-paper extraction from full PDFs/supplements + GWAS Catalog pull/refresh + text-mining author-explanation status for the 36 GWAS-Catalog PMIDs + harmonize by rsID, both provenance rows kept) | ⬜ not started | NB3 (case-set assembly, unchanged) | Correct gene labels `discordance_loci.csv` took at face value (esp. Morgan2018 PKHD1/ORAOV1/SIK1/MSX2); confirm Crawford2017 loci captured; verify ~1,072 associations / 36 PMIDs; add `REPORTED GENE(S)` back to `TIDY_COLS` |
| 2 | **NB5** — compare candidate networks before merging (D'Arcy + consistent-STRING extractor modules, then node/edge-level comparison of Raghunath 168 / D'Arcy 243 / KEGG ~101 / confirmed Reactome as peer gene sets) | ⬜ not started | NB4 | Confirm the Reactome melanogenesis accession live via `mcp-genes-ontologies` first (audit flagged R-HSA-5662702 as web-search-sourced, unconfirmed); re-derive the 465/230/118 D'Arcy-vs-Raghunath counts under an explicit harmonization rule |
| 3 | **NB6** — harmonized multi-layer substrate (T0 Raghunath / T1 KEGG+Reactome / T2 D'Arcy annotation / T2b OmniPath validation / T3 STRING, tiered per Decision 4) | ⬜ not started | NB5 (frozen outputs) | Every node/edge carries `supporting_layers` (+ `layer_evidence_type` on edges); STRING never coerced into sign/direction; citation-completeness gate is release-blocking; backbone edits staged as a PI-gated proposal |
| 4 | **NB7** — resolution and convergence-graded rescue screen (causal-gene resolution per locus via L2G/eQTL/LD, then rescue test + convergence grade + one confirming experiment per rescued locus) | ⬜ not started | NB6 | Filter to `author_explanation_status` in {stated_unknown, nearest_gene_only}; classify mechanistic / mediating-via-layer / LD-rescue / likely-population-specific / unexplained-and-unrescued; report the honest count, do not force a headline |
| 5a | **NB8 (optional)** — population-conditionality section (SLC24A5 gene-flow, TYRP1/Oceania, OCA2/E-Asia, MFSD12/Africa; compensating loci + gating modifiers as testable hypotheses) | ⬜ not started | NB7 | Optional per the approved plan; deterministic computation kept separate from any LLM per-item synthesis |
| 5b | **Review + compliance-gated commit** — route NB4–NB8 through DATA_SOURCE_AUDITOR, REPRODUCIBILITY_SPECIALIST (verify every frozen snapshot each notebook reads is committed — the NB2 lesson), SCICOMM_REVIEWER, VISUAL_DATA_REVIEWER; fold in fixes; run the tiered pre-commit compliance gate (Tier 2 — new data + notebooks) via `REPO_COMPLIANCE_GATE` before any commit | ⬜ not started | 1–5a complete | No commit happens outside this gate |

---

## Deferred — not in this build pass

- **Martin et al. population GWAS pull (South Africans).** Named explicitly in the approved plan's NB8 step
  as deferred to a **later population pass** — not built in this pass. Revisit only after NB8 (if built) or
  in a dedicated follow-up.
- **Consolidate the standalone extractors `notebooks/01a`–`01d`** (Bajpai CRISPR, Baxter genes, HIrisPlex
  markers, GWAS-Catalog reproduction) into their consuming mini-manuscripts, per the new flat-spine /
  no-dangling-extractor convention (Decision 6). These are the *older* pattern the convention corrects
  going forward — out of scope for the NB4–NB8 build; log as backlog only.

---

## Needs PI discussion — not authorized

- **`internal/project_dashboard.md` is absent from disk.** Archived out in the 2026-07-11T22:51Z restart and
  not yet re-created. It should exist before NB4 produces its first processed output (so `pigmentation-plan-sync`
  has a Key-metrics table to reconcile against), but re-creating it is a scope decision, not a bookkeeping
  one — flagging for the PI/next session rather than doing it here.

---

## Housekeeping

- This ledger reconciles against `CHANGELOG.md` and the plan artifact cited above, not against memory.
- Update a row's status marker (⬜ not started / 🔄 in progress / ✅ done / ⛔ blocked) the moment work state
  changes — do not let this ledger drift from reality.
