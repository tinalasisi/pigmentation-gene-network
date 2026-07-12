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

## Follow-ups from the NB2 reproducibility fix (both RESOLVED 2026-07-12T01:44Z)

- ✅ **`PLC*` filter documented in `DATA_SOURCES.md` entry 6.** The member-filter line now records that HGNC
  group 832 returns 19 protein-coding members (5 are PLA2G4* contaminants) and requires a `PLC*` prefix filter
  to reach the committed 14, at parity with the documented PLA2G*/PRSS* filters; also recorded per-group in
  `hgnc_gene_groups.json` (`member_filter`). See `CHANGELOG.md` 2026-07-12T01:44Z item 2.
- ✅ **Figure-generating code added to NB2.** Cells 8/15/20/22/27 now build the 5 `notebooks/figures/step*.png`
  from the notebook's own in-memory data (`fig.savefig` + `display`), verified value-for-value on a fresh
  clone. The figures reproduce rather than being opaque committed binaries. See `CHANGELOG.md`
  2026-07-12T01:44Z item 1. (Regenerated notebook + PNGs pending commit through the compliance gate.)

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
| 5a | **NB8 (optional)** — population-conditionality section (SLC24A5 gene-flow, TYRP1/Oceania, OCA2/E-Asia, MFSD12/Africa; compensating loci + gating modifiers as testable hypotheses) | ⬜ not started | NB7 | Optional per the approved plan; deterministic computation kept separate from any LLM per-item synthesis. **PI design note (2026-07-12, captured mid-build):** for every node/edge carried in the harmonized substrate, attach the lead variant's ALLELE FREQUENCY across populations (gnomAD / 1000G superpopulations AFR/EUR/EAS/SAS/AMR) so the population axis can ask *which layers of the network shift in frequency across ancestries* — a network-layer view of population differentiation, not a one-locus-at-a-time view. Frequencies pulled per the frozen-db-notebook pattern (mcp-variants/mcp-human-genetics), snapshot committed in-repo. Consider a per-layer differentiation summary (e.g. mean |ΔAF| or Fst-like contrast per tier T0–T3). |
| 5b | **Review + compliance-gated commit** — route NB4–NB8 through DATA_SOURCE_AUDITOR, REPRODUCIBILITY_SPECIALIST (verify every frozen snapshot each notebook reads is committed — the NB2 lesson), SCICOMM_REVIEWER, VISUAL_DATA_REVIEWER; fold in fixes; run the tiered pre-commit compliance gate (Tier 2 — new data + notebooks) via `REPO_COMPLIANCE_GATE` before any commit | ⬜ not started | 1–5a complete | No commit happens outside this gate |

---

## Open — surfaced during NB5 (must be dealt with in NB6)

- ⬜ **STRING enzyme-class-token mapping artifact (BLOCKS edge attribution in NB6).** A few of Raghunath's
  enzyme-*class* tokens (PLC, PKC, TRYPSIN, PHOSPHODIESTERASE) were sent to STRING's symbol-mapping API and
  resolved to an unrelated best-match gene (e.g. `PLC → HSPG2`) instead of failing cleanly; PLA2 and PRSS1
  correctly returned unmapped. This does NOT affect NB5's literal-token node-level counts, but any STRING edge
  touching one of these tokens must NOT be attributed to a specific enzyme-class member gene until the class
  label is expanded to its member genes explicitly. **Resolve in NB6 before any STRING edge is merged**, and
  discuss the caveat in-notebook. Documented in NB5 too.
- ⬜ **Reactome REFRAMED as a discovery / rescue-connection layer (not a redundant KEGG co-tier).** PI
  decision (2026-07-12): KEGG hsa04916 (101 genes — full MC1R/cAMP + WNT + KIT/MAPK + calcium cascade +
  terminal enzymes) is the mechanistic CORE. Reactome's broader layer is a **manually curated
  UNION of 4 verified accessions** — Melanin biosynthesis (R-HSA-5662702), MITF-M-regulated melanocyte
  development (R-HSA-9730414), Melanocortin receptors (R-HSA-388601), Defective SLC24A5/OCA6 (R-HSA-5619036),
  156 genes total — broader and noisier, and that breadth is the asset: it is the substrate for testing.
  **ACCESSION CORRECTION (2026-07-12):** an earlier orchestrator claim that R-HSA-5619507 is the Reactome
  "Pigmentation" parent was WRONG — R-HSA-5619507 is "Activation of HOX genes during differentiation," an
  unrelated pathway. Reactome has no single "Pigmentation" pathway (melanin biosynthesis and MITF-regulation
  branches are hierarchically disjoint). The curated 4-accession union above replaces it. Do NOT reintroduce
  R-HSA-5619507. This breadth is the asset: it is the substrate for testing
  whether GWAS/paper loci that genetics found by association but could NOT mechanistically place fall into
  curated pigmentation reaction-space the mechanism-first core missed. Concretely:
    - NB5 isolates the **Reactome-only connection set** = genes in Reactome's parent hierarchy NOT in
      Raghunath-168 AND NOT in KEGG-101; characterizes it by sub-pathway (melanosome biogenesis, vesicle
      trafficking, MC1R/cAMP signalling, ion transport) and reports its size. This is the discovery surface.
    - Reactome snapshot MUST preserve reaction/edge structure + per-gene sub-pathway membership (not a flat
      gene list) so NB7 can cite the SPECIFIC reaction a rescued locus connects through.
    - NB7 gains a resolution class **`mediating-via-Reactome-reaction`**: an author-unexplained locus whose
      resolved causal gene lands in the Reactome-only connection set is a candidate rescue, connecting a
      "missing" association gene into curated pigmentation biology via a reaction the original authors did not
      name. This is a core project contribution ("query missing pigmentation genes found by association").
    Parent snapshot committed in-repo (frozen-db pattern); R-HSA-5662702 terminal snapshot kept as the precise
    terminal-enzyme reference.

## Closed — NB5 finalization fixes (2026-07-12, folded into the Bajpai re-render)

- ✅ **NB5 figure left-panel title said "4-way" but showed 5 bars** (Reactome added a 5th source, then
  Bajpai a 6th bar). Fixed: `nb5_candidate_network_comparison.png` left-panel title now reads "5-way"
  (4 curated/pathway networks + Bajpai's node-set), re-rendered alongside the Bajpai node-layer addition.
- ✅ **Bajpai 2023 CRISPR screen added as a NODE layer** to NB5, per PI sign-off
  (`internal/bajpai_network_integration_brief.md`): node-set flag + `Combined_casTLE_Effect` weight +
  uniform reduces-pigmentation sign in `nb5_gene_set_membership.csv` (169/169 hits joined; sanity check
  TYR/DCT/SLC45A2/OCA2 present, MC1R/HERC2 absent — passed); reverse coverage + enrichment vs. the screen's
  own assayed background (`nb5_bajpai_network_enrichment.csv`); 142/169 orphan hits flagged; optional
  labeled bipartite hit→melanin_content layer (`nb5_bajpai_bipartite_melanin_endpoint.csv`), never pooled
  with the edge networks; NO gene-gene edges fabricated. Networks-typology table added
  (`nb5_networks_typology.csv`, 9 sources).

## Data-fitness sign-off (2026-07-12) — binding conditions for the expanded plan

Both DATA_SOURCE_AUDITOR and GENETICS_LIT_REVIEWER signed off on the expanded data plan (GRN + Bajpai +
Reactome-discovery + L2G/eQTL/LD). Verdicts and the CONDITIONS that must be written into the build steps:

- ⬜ **GRN (new NB6): primary layer = CURATED REGULONS, not ChIP-seq peaks.** Both specialists independently:
  ChIP-seq TFBS (UniBind/ENCODE) → directed TF→target edges is a CATEGORY ERROR (binding near ≠ regulation of;
  same nearest-gene-vs-causal trap the project disciplines for SNPs). ENCODE has ~no melanocyte MITF/SOX10
  coverage (2 MITF expts, both K562); PAX3 has ZERO melanocyte ChIP-seq anywhere. **Use DoRothEA/CollecTRI
  curated regulons — ALREADY in-repo** (`omnipath_internal.json`: MITF 34 signed targets incl TYR/TYRP1/DCT/
  MLANA/OCA2/MC1R/KIT, SOX10 5, PAX3 18), directed+signed+confidence-tiered. Promote from NB2-validation-only
  to a first-class GRN layer. Conditions: (1) melanocyte-lineage-only if UniBind binding-evidence is added at
  all, tagged `binding-evidence`, undirected, NEVER labeled regulatory; (2) PAX3 = literature-curated candidate
  edges (PAX3→MITF/MET/RET), flagged low-confidence, NOT ChIP-seq-grade; (3) carry DoRothEA A–E confidence tier
  per edge; (4) a figure/table titled "GRN" means the regulon layer only. Route via MCP + frozen snapshot
  (replicable, more transparent than the omnipath package). NO fabricated edges — every edge cited.
- ⬜ **Reactome-only 121-set (NB8 rescue): GATE ON SUB-PATHWAY TAG, not set membership.** Only 29/121 are
  pigmentation-tagged; 92 are MITF's broader program (apoptosis/EMT/cell-cycle — BRCA1, CDKN2A, HDAC1, AGO1–4,
  vacuolar-ATPase subunits). Report "N of 29 pigmentation-tagged rescued" SEPARATELY from the 92; never a single
  "N of 121" headline (repeats the coverage-vs-resolution axis-conflation the traceability audit already fixed).
- ⬜ **Bajpai: FIT as node layer.** Carry q<0.10 threshold-sensitivity (q<0.05→149, q<0.15→208) and the assay's
  melanocyte-mechanism bias — "not a Bajpai hit" is NOT evidence against a locus (asymmetric evidence).
- ⬜ **Locus resolution (NB8): resolve by rsID, not raw coordinate.** Loci are mixed-build (74 GRCh37 / 23
  no-build / 6 GRCh38 / 2 ambiguous). Tag every locus build in NB4; fail-loud on every zero-result liftover
  (liftover_variant returns empty, not error, on wrong source_build — assert n_results>0); the 25
  build-unresolvable rows need explicit disposition before entering the rescue denominator. **Use
  melanocyte-specific QTL (Zhang 2018 eQTL, Zhang 2021 meQTL), NOT bulk GTEx** — melanocytes are <5% of skin and
  their eQTLs differ from all 44 GTEx tissues.
- ✅ **Melanocyte eQTL NOW IN-REPO (2026-07-12, PI-supplied) — no GTEx needed.** Zhang 2018 (Genome Research
  gr.233304.117): `data/raw/papers/1621.pdf` (main) + `supp_gr.233304.117_Supplemental_Tables.xlsx` (20 tables).
  Key tables for the rescue test: **T-S6** = 379 curated pigmentation genes each with a **melanocyte eGene
  q-value** (join to our 52 resolved causal genes → a cell-type-APPROPRIATE convergence line); **T-S10** = eQTL
  at pigmentation GWAS SNPs (rs12203592→NEO1/PLA1A/TMEM140 via IRF4 trans); T-S5 = melanocyte(106) 4,997 eGenes
  vs bulk skin; T-S9 = cis/trans calls. This REPLACES the "documented limitation" — the connector (eQTL
  Catalogue) had zero melanocyte datasets and the resolution track fell back to bulk skin; GTEx is bulk skin =
  the WRONG tissue the reviewer warned against, never the fix. NB8: add `melanocyte_eGene_zhang2018` +
  `melanocyte_eGene_qvalue` as an additive convergence line (NOT a gate). Extract T-S6/T-S10 into a frozen
  processed CSV committed in-repo. **COMPLIANCE: the published supplement is open-access (commit OK); the dbGaP
  Data Use Certification `wga.pdf` and any controlled raw genotypes must stay gitignored** — flag to the
  compliance gate.
- ⬜ **Still-open lit-reviewer suggestions:** an MPRA/Hi-C functional layer (a reporter screen named target genes
  incl MFSD12/OCA2/MITF) as the per-locus "confirming experiment"; verify Simcoe 2021 eye-color GWAS is in the
  trait-root pull; Zhang 2021 meQTL if a supplement is later added.

## Commit hygiene corrected (2026-07-12)

- ✅ Phase-1 backlog cleared as 3 scoped commits (04e1b26 NB4, 3fc877f NB5, dcbb92a NB6) through the Tier-2
  compliance gate. ROOT-CAUSE: "batch the reviews at the end" was misread as "batch the commits" — commits
  should be scoped and frequent (one unit of work each, the moment it's done); only the scicomm/visual/
  reproducibility/data-source REVIEW pass is batched. Going forward: commit each notebook as it lands.
- ⬜ **Kim 2024 extraction (NEW — PI added the full PDF+supplement).** NB4 correctly documented Kim as a gap
  (no extracted data existed when it ran) and did NOT fabricate. Now `data/raw/papers/Kim2024_NatCommun_
  EastAsianSkinColor/` has the full PDF + Supplementary_Data.xlsx. Extract its lead loci (12 known + 11 novel,
  26 lead variants) via GENETICS_DATA_EXTRACTOR and fold into NB4's unified base as an additional curated
  source; re-render the funnel. data/raw/papers/ stays gitignored (PDFs withheld); only the extracted CSV commits.
- ⬜ **Snapshot licenses to live-verify before PUSH** (gate hit sandbox 403, relied on domain knowledge):
  Reactome CC0, Open Targets CC0, Ensembl no-restriction. KEGG already precedented (tracked, DATA_SOURCES §6c:
  academic non-commercial use). Confirm at the push-time full-tree compliance sweep.

## Deferred — not in this build pass

- **Martin et al. population GWAS pull (South Africans).** Named explicitly in the approved plan's NB8 step
  as deferred to a **later population pass** — not built in this pass. Revisit only after NB8 (if built) or
  in a dedicated follow-up.
- **Consolidate the standalone extractors `notebooks/01a`–`01d`** (Bajpai CRISPR, Baxter genes, HIrisPlex
  markers, GWAS-Catalog reproduction) into their consuming mini-manuscripts, per the new flat-spine /
  no-dangling-extractor convention (Decision 6). These are the *older* pattern the convention corrects
  going forward — out of scope for the NB4–NB8 build; log as backlog only.

---

## Flagship track — mechanism→direction law (NB10, primary; added 2026-07-12, independent session)

- ✅ **NB10 built, executed, audited.** Direction law formalized (22/22 LoF concordant, permutation *p*<1e-5),
  prior-art gated (verdict B: novel formalization), and validity-audited (survives weak-leg checks). Reports in
  `internal/deconvolutor/`. Notebook + backing CSVs + figures on disk.
- ✅ **NB12 — narrow pre-registered expansion (this session).** Expanded the LoF direction test to additional
  OMIM/Orphanet pigmentation-disorder genes, built with explicit per-gene inheritance + LoF-mechanism
  annotation (NOT the Baxter/D'Arcy lists wholesale), and report concordance SEPARATELY for
  core-melanogenesis-pathway vs syndromic/trafficking genes — the ascertainment-confound sensitivity test the
  prior-art gate mandated. Pre-register the source-priority rule for sign conflicts before looking at any new
  gene's direction call.
- ⬜ **Framing fixes surfaced by the audit (fold into NB10 write-up):** (a) lead with the CRISPR line, not "3
  independent sources" (they are ~2.5 — GRN and signed-net share MITF/SOX10/PAX3 logic); (b) state 22/22 as the
  predictive claim and the 6 dominant non-LoF mechanisms as post-hoc interpretation.
- ⛔ **GWAS common-variant axis — SHELVED for this hackathon.** Scoping returned 5/35 clean SNP→gene genes,
  1/35 closing the eQTL loop, TYR discordant even among the clean set (see the 2026-07-12 specialist review).
  Re-open only with a colocalization step and a stated null model.

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
