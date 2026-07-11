---
from: claude-science/pi-orchestrator-d80a52e7
to: all
date_utc: 2026-07-11T17:00:41Z
platform: claude-science
subject: Two-level framing landed + Locus Resolver substrate ready for Claude Code
---

Status from the Claude Science session, so a parallel/Claude Code session can pick up without collision.

## Committed this session (now on origin/main @ ecaa9ea)
- **Two-level paper framing adopted** (dashboard locked decision 11): bidirectional discordance (D1 =
  genotype-present/phenotype-absent; D2 = phenotype-present/genotype-absent) is the headline; "dark-matter
  association" is the coverage/gap spine beneath it. README, dashboard, FINDINGS, RESEARCH_SYNTHESIS, TODO all
  rewritten to it. GWAS-Catalog expansion is HELD until after the MVP (PI decision).
- **Mislabeled-pointers hypothesis FALSIFIED** (do not re-run): 0 of 15 dark-matter genes resolve to an
  in-network gene. HERC2->OCA2 is the one positional-pointer case and it is a D'Arcy-RECOVERABLE gene, not
  dark matter.
- **Locus Resolver MVP substrate** ready for Claude Code to build:
  - `internal/handoffs/CLAUDE_CODE_HANDOFF.md` — the full build spec (read this first).
  - `data/processed/locus_nodes.csv` + `data/processed/locus_annotation_edges.csv` — PRE-DRAFTED, pass
    `scripts/validate_locus_tables.py`. Claude Code should VALIDATE, not rebuild.
  - `internal/handoffs/LOCUS_TABLES_PREDRAFT_NOTE.md` — genome-build warning (rs12913832=GRCh38,
    rs1800401=GRCh37) + the honesty caveat (rs12913832 not significant in the Kalinago cohort; the
    HERC2->OCA2 enhancer mechanism is the cited external finding, PMID:22234890 Visser 2012, not a Kalinago
    result).
  - MATERIAL RISK for the build: OCA2 has exactly ONE backbone edge (MITF->OCA2), so D1/D2 CANNOT be computed
    by graph traversal — take direction from the cited case classification and DISPLAY the subgraph as
    context. See CLAUDE_CODE_HANDOFF.md section 4.

## Left untouched (not mine)
- `internal/CHANGELOG.md` has an uncommitted edit (pigmentation-plan-sync checker rewrite +
  PROJECT_MANAGER staleness-duty section) — that is the parallel session's work; Claude Science did not touch
  it.

## Coordination
Claude Science stays read-only on git per PI instruction (PI drives local commits). Deterministic build +
`quarto render` + browser test = Claude Code (the sandbox cannot render quarto or execute notebooks). Return
contract in `internal/handoffs/CLAUDE_SCIENCE_RETAINED.md`.


---
## Addendum 2026-07-11T17:30:16Z — resolver manifest + dark-matter ledger (both review-passed)

Two more Claude Science pieces are staged on disk (UNTRACKED — PI drives commits):

**Resolver manifest (built, deterministic, review-PASS):**
- `docs/data/locus_resolver_manifest.json` — the frozen export the Locus Resolver page reads. Both worked
  examples (herc2_oca2_eye, kalinago_oca2) fully populated with grounded/cited values + 3 caveats.
- `scripts/build_resolver_manifest.py` — regenerates it deterministically from the committed CSVs (verified
  byte-identical on all structural fields). Claude Code should READ the manifest and re-run the builder if
  CSVs change; do NOT hardcode values into the JS. CLAUDE_CODE_HANDOFF.md §3c updated to say so.
- Kalinago example direction is PAPER-LEVEL 'both' (Ang2023) with gene_level_label='mixed' carried alongside
  — complementary, not contradictory. Reproducibility gate: PASS. Source audit: annotation-only invariant HELD.

**Dark-matter ledger (built, review-PASS_WITH_NOTES → notes resolved):**
- `data/processed/dark_matter_ledger.csv` (15 genes) + `docs/dark_matter_ledger_README.md`. Four locked
  classes: genuinely_novel=4, redirects_to_other_gene=2, signal_no_eQTL_redirect=3,
  LD_passenger_or_no_signal=6 — matches project_dashboard.md §3 gene-for-gene. target_in_168_network=False
  for all 15 (the FALSIFIED 0/15 result).
- CITATION FIX applied (three misattributed PMIDs, verified against NCBI PubMed, corrected in BOTH the ledger
  AND the upstream Track A table `data/processed/locus_resolution_table.csv`): MFSD12 29489754→29025994
  (Crawford2017 Science); MSX2 30595370→30531825 (Morgan2018 Nat Commun); KALRN removed a fabricated
  "Chen et al." label from PMID:37294081 (which is Ang2023). If you regenerate the ledger, re-apply or fix at
  source — noted in the README.

All four checks this round: repro PASS (ledger+manifest), source-audit annotation-only HELD, PMID:22234890
verified, three ledger PMIDs corrected.


---
## Addendum 2026-07-11T18:24:58Z — decomposition finding sharpened; front-end PAUSED; residual lit gaps closed

PI decision: PAUSE the interactive Locus Resolver build; sharpen the decomposition FINDING first. Rationale
from the lit review (internal/lit_review/): nearest!=causal is the LOWEST-novelty claim (standard L2G
practice); the three-strata dark-matter decomposition is what SURVIVES as novel.

**Finding locked** — internal/DISCORDANCE_DECOMPOSITION_FINDING.md. Three strata over 31 case genes:
mechanistic (in-network) 9 = 29.0%; association-recoverable (D'Arcy) +7 -> 16/31 = 51.6%; dark 15 = 48.4%.
Dark decomposed 4/2/3/6 (genuinely_novel / redirects / signal-no-redirect / passenger-or-no-signal); 0/15
resolve to in-network (falsified mislabeled-pointers hypothesis = the asset).

**Two residual lit gaps CLOSED** (GENETICS_LIT_REVIEWER, internal/lit_review/2026-07-11_GAPCLOSURE_...md;
5 refs appended to bibliography):
- Gap A (Claim 4 citation): adopt Mountjoy 2021 Nat Genet (L2G methods, PMID 34711957) + Ghoussaini 2021 NAR
  (Open Targets Genetics portal, PMID 33045747), alongside FUMA — cite nearest!=causal as APPLIED PRACTICE,
  not novel insight. Both NCBI-verified.
- Gap B (framing F): a second, vocabulary-independent sweep (13 loose-term queries) again found NO
  pigmentation-specific discordance-network competitor. Open ground at the instrument level holds.
- All three cheap novelty-risk gaps now closed; none overturned the reframe.

**Front-end substrate remains staged and valid** (manifest, locus tables, dark-matter ledger) — repurposable
as a 'Discordance Decomposition Explorer' if/when the build resumes.
