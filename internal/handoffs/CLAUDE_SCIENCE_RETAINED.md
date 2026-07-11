# What stays on Claude Science — and the return contract

**Why a split at all.** The two platforms have non-overlapping strengths. This doc records what
Claude Science does that Claude Code cannot, and the exact hand-back sequence when Code's build
returns. Pass this to Claude Science (this agent, or a fresh session) alongside Code's deliverables.

## Capabilities only Claude Science has (do NOT delegate these to Claude Code)

1. **Genetics data connectors (MCP).** GWAS Catalog, eQTL Catalogue, FinnGen/BioBank-Japan PheWAS,
   via the `human-genetics` connector. Any new locus resolution, eQTL check, or trait lookup — e.g.
   extending the ledger to the 15 dark-matter genes, or pinning an `eQTL_target` citation — runs
   here. Claude Code has no access to these APIs.
2. **Citation verification.** `fetch_article_fulltext` (by DOI) + `web_search` to confirm a PMID/DOI
   is real and says what a row claims. (This is how PMID:22234890 was verified this session.) Any
   citation Code leaves blank or uncertain gets resolved here.
3. **The specialist review gates.** These are Claude Science sub-agents with curated rubrics:
   - `VISUAL_DATA_REVIEWER` — figure/interactive data-fidelity + colorblind-safety + alt-text.
   - `SCICOMM_REVIEWER` — no-overclaim, numbers-traceable, D1/D2 glossed on first use, prose clean.
   - `REPRODUCIBILITY_SPECIALIST` — every displayed value traces to a pinned file, not hand-typed.
   - `DATA_SOURCE_AUDITOR` — annotation-only invariant held; no association edge leaked into the
     mechanistic backbone; provenance documented.
   - `REPO_COMPLIANCE_GATE` — MANDATORY before any git commit/push/PR: confirms withheld data is
     gitignored and READMEs document what is withheld + how to obtain it.
   - `PROJECT_MANAGER` — updates CHANGELOG.md / project_dashboard.md / TODO.md, runs plan-sync,
     archives superseded plans.
4. **Scientific judgment calls.** Which resolution class a locus belongs to; whether a D1/D2 label is
   defensible; whether a network subgraph honestly represents the mechanism. These are the
   nearest-gene-vs-causal discipline decisions, not code.
5. **Reproducing/verifying network computations** against the pinned CSVs (the coverage chain, the
   465/227/118 cross-check, the tier counts 9/7/15).

## Return contract — when Claude Code hands back `feature/locus-resolver`

Run these in order. Nothing reaches GitHub until step 5 clears.

1. **Reproducibility check (REPRODUCIBILITY_SPECIALIST).** Independently re-run
   `scripts/validate_locus_tables.py`; confirm every value in `locus_resolver_manifest.json` traces
   to `locus_nodes.csv` / `locus_annotation_edges.csv` / the backbone / the case files — nothing
   hand-typed into the JS. Confirm the OCA2-is-a-near-leaf honesty (§4 of the Code handoff): the
   direction readout is *sourced from case classification*, not falsely presented as graph-computed.
2. **Citation verification (this agent + connectors/article-fetch).** For every row in
   `locus_annotation_edges.csv`, confirm the `evidence_citation` is real and supports the claim.
   Resolve any blank/uncertain citations Code flagged. Fill `eQTL_target` rows from the connector if
   the ledger is extended.
3. **Data-source audit (DATA_SOURCE_AUDITOR).** Confirm the walled-off invariant: no locus edge in
   `gene_network_edges.csv`; the two tables never concatenated; locus nodes not counted in the
   168-gene figure; annotation-only role stated correctly on the page.
4. **Presentation review (VISUAL_DATA_REVIEWER + SCICOMM_REVIEWER, parallel).** Figure fidelity +
   colorblind palette + alt-text; and D1/D2 glossed on first use in each panel, nearest≠causal
   surfaced not buried, no overclaim, every number traceable.
5. **Compliance gate (REPO_COMPLIANCE_GATE) — MANDATORY, blocks the commit.** Hand it the working
   tree. Only after it reports the tree clear may the branch be committed/merged/pushed.
6. **Project bookkeeping (PROJECT_MANAGER).** Log the MVP as a decision in CHANGELOG.md; update
   dashboard §4/§5a and TODO.md (move the MVP steps from "agreed" to "done"; note the dark-matter
   ledger extension as a stretch item still needing PI sign-off). Run plan-sync.

## The current agreed plan context (so a fresh Science session has it)
- Finding delivered: `notebooks/04_darcy_coverage_finding.ipynb` + `internal/FINDINGS_darcy_coverage.md`
  (coverage 9/31 in-network → 16/31 with D'Arcy annotation; 15 dark-matter; cross-check 465/227/118;
  payoff loci = TYR + OCA2 ONLY).
- Research done: `internal/RESEARCH_SYNTHESIS_locus_resolution_mvp.md` — the dark-matter
  "mislabeled-pointers" hypothesis was tested and FALSIFIED (0/15 resolve to in-network genes);
  decomposed into cited classes. HERC2→OCA2 is the one real positional-pointer case (and it is a
  D'Arcy-recoverable gene, not dark matter). PMID:22234890 verified.
- MVP approved by PI: interactive Locus Resolver, two worked examples. Build handoff:
  `internal/handoffs/CLAUDE_CODE_HANDOFF.md`.
- Standing constraints (locked): D'Arcy is annotation-only (S4/S5 STRING edges barred from backbone);
  edges are OmniPath + literature-curated only; notebooks single `.ipynb` (no `.qmd` twin), CI renders
  committed outputs with `execute: enabled: false`; always gloss D1/D2; primates sub-project is LAST,
  only after current-data options are exhausted.
- Primates: still deferred. The user has a primate phylogeny (sexual dichromatism resolved); the
  sub-project (sex-modulation × pigmentation in a closely-related clade) is on record but NOT to be
  started until the current MVP line is done.
