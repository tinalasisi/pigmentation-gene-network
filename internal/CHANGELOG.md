# Changelog — Pigmentation gene-network build

Append-only history of build and decision events for this project. Each entry is dated and records what
changed and why; entries are never rewritten. This file is one of three tracking documents (with `TODO.md`
and `project_dashboard.md`); see `START_HERE.md` for the convention. All three live in `internal/`, which is
tracked (committed to the public repo) so their cross-references resolve on GitHub — the escape hatch
`internal/untracked/` holds anything deliberately kept private.

---

## Guidance for agents: writing notes to each other

_This is standing guidance, not a dated event — it sits here, ahead of the dated entries, because it
governs how this file itself must and must not be used. Keep it up to date in place if the convention it
describes ever changes; unlike the entries below, this section may be edited rather than only appended to._

**(a) Where agent-to-agent notes go.** Operational message traffic between agent sessions — handoff pings,
"about to touch file X", status questions, coordination chatter — does **not** get written into this file,
as free-text edits or otherwise. It goes to the dedicated channel at `internal/handoffs/notes/`. Full
rationale for why the two must stay separate is in `internal/handoffs/MERGE_SAFETY.md` §4; the short version
is that this file is curated prose for a human reconstructing project history, and mixing in
higher-frequency operational chatter would either bury that history in noise or force every coordination
ping to be hand-curated into changelog-quality prose, defeating the point of a low-friction channel.

**(b) Message file naming and format (summarized from `internal/handoffs/MERGE_SAFETY.md` §3; that document
is authoritative — read it before writing tooling against this convention).** Each note is its own file in
`internal/handoffs/notes/`, written once and never edited:

```
{UTC_TIMESTAMP}__{platform}__{agent_tag}__{rand6}.md
```

- `UTC_TIMESTAMP` — `YYYYMMDDTHHMMSSZ` (compact ISO-8601, UTC, second resolution); lexicographic filename
  sort equals chronological order.
- `platform` — `claude-science` or `claude-code` (lowercase, hyphenated).
- `agent_tag` — short filesystem-safe id for the writing agent/session (e.g. the first 8 hex characters of
  a Claude Science frame id, optionally prefixed with a role name).
- `rand6` — 6 random lowercase hex characters; the collision backstop.

Each file is YAML front matter (`from`, `to`, `date_utc`, `platform`, `subject`) followed by a blank line
and a free-text Markdown body. A correction or reply is a new file that references the original by
filename — never an edit to an existing note.

**(c) This changelog stays curated prose, appended to only in the existing dated-entry format.** Every
change to this file below this guidance section is a new `## YYYY-MM-DD — <title>` entry, added at the end,
in full sentences, describing what changed and why. Existing entries are never rewritten. **The rule that
keeps this changelog merge-safe:** `internal/CHANGELOG.md` carries a `.gitattributes` `merge=union`
directive as a defensive backstop for the common case of two branches each appending one dated entry at the
tail — it does not guarantee entry order across a merge (a rare ordering glitch is a five-minute manual fix
because entries are self-dated) and it does not resolve a conflict if two branches edit the same existing
line. That backstop is sufficient here specifically because this file is written to rarely and normally by
one agent at a time; it is not a substitute for the notes channel's stronger, unconditional per-message
guarantee, and agent-to-agent traffic must not be routed through this file to "make use of" that backstop.

---

## 2026-07-10 — Notebook/document-format decision (#10) corrected: Quarto → GitHub Pages re-adopted as a CI-only render layer

**What changed.** Locked decision #10 (notebook/document format and publishing) was briefly reversed earlier
2026-07-10 — the prior version had mandated `.qmd` as the sole source of truth for notebooks with a Quarto →
GitHub Pages build. That mandate was withdrawn the same day on the finding that `.qmd` registers in the
Claude Science artifact store as `application/octet-stream` with no in-app viewer (download-only), whereas
`.ipynb` and `.md` both render inline; the Quarto scaffolding (`_quarto.yml`, `index.qmd`, `_site/`) was
removed. Later the same day, a Quarto + GitHub Pages site was re-adopted in commit `c3f258b` — this time as a
CI-only render layer over unmodified `.ipynb`/`.md` sources (`execute: enabled: false`, no kernel, Quarto
never runs in the Claude Science sandbox) rather than a `.qmd` source-of-truth change. Notebooks stay
`.ipynb`; prose stays plain Markdown; there is no `.qmd` twin of any notebook.

**Why.** The constraint that caused the reversal (an opaque, download-only source format) does not apply to
a design where no notebook is ever authored or reviewed as `.qmd` — Quarto only wraps already-committed,
already-rendered `.ipynb` outputs into HTML in CI.

**Process change adopted alongside this correction.** A standing rule was added: any future decision about
file format, artifact type, or publishing/rendering approach must be checked against how it behaves on the
Claude Science surface (via the `PLATFORM_LIMITS_ADVISOR` specialist) *before* it is locked, precisely because
this reversal happened when that check was skipped.

**Documents updated:** `TODO.md` (item #10), `project_dashboard.md` (locked decision #10, §5a item 11).

---

## 2026-07-11 — Plan pivot: NB5 edge-drawing abandoned; D'Arcy annotation-layer + case-gene coverage finding adopted (PI-agreed, 2-day deliverable)

**Context.** Both currently-unauthorized forward tracks — the sex-hormone × pigmentation expansion, and the
NB4–NB8 causality-gated downstream chain — were run through the plan deconvolutor against a PI-imposed hard
48-hour deadline. Full critiques: `deconvolutor/2026-07-10_1808_DECONVOLUTOR_REPORT_sex_pigment_primate.md`,
`deconvolutor/2026-07-10_1859_DECONVOLUTOR_REPORT_NB4-NB8_downstream_chain.md`; synthesis:
`deconvolutor/2026-07-10_1901_DECONVOLUTOR_SUMMARY_both_tracks.md`.

**Verdict.** Neither track produces a scientific result in 48 hours. The sex-hormone expansion is blocked by
scale (multi-week research problems the prior plan understated as lookups — a live OmniPath query across all
11 aggregated resources for AR/ESR1/ESR2 → a 14-gene melanogenic/melanocortin set returned 0 direct edges out
of 344 interactions pulled). The NB4–NB8 chain is blocked by a decision gap plus a dead edge source: no
causal-gene tie-break rule exists for when nearest-gene/L2G/ClinVar disagree, and — the root cause below —
OmniPath does not cover the genes the design depends on.

**Root cause confirmed by a live check this session.** NB5's premise (draw new mechanistic OmniPath edges
for the validation-case genes) is unworkable: HERC2's 145 OmniPath interactions are all DNA-damage/
ubiquitin-ligase edges, none touching MITF/TYR/OCA2/MC1R or any melanogenesis node; MFSD12 and TMEM138 return
zero OmniPath edges; none of the 9 NB5 candidate genes is already in the 168-gene network or connects
candidate-to-candidate.

**New agreed direction.** Abandon edge-drawing entirely. Build the finding from annotation layers already on
disk: add D'Arcy & Kiel (2023) Table S1 (243-gene OMIM-backed disease-gene table with hypo/hyper/mixed
pigmentation-direction labels; DOI 10.3390/bioengineering10010013, PMC9854651, CC BY 4.0) as an
**annotation layer only** — its Tables S4/S5 STRING-association edges stay barred from the mechanistic
backbone, locked decision 5 unchanged — then cross the 13-paper, 31-gene validation-case set against network
coverage plus D'Arcy disease-direction.

**The D'Arcy cross-check — previously plan-stated, never run — was run this session and reproduces:**
- 465 D'Arcy-union genes (S1 ∪ S5, 508 total) absent from the 168-gene backbone — matches the dashboard's
  prior stated figure exactly.
- 227 of those 465 are disease-flagged (have an S1 disease row) — the dashboard had stated 230; the 3-gene
  delta is a synonym-resolution difference (gene-symbol matching), not a computational discrepancy. The
  dashboard figure is corrected to 227 with this note.
- 118 of those 465 are hypopigmentation-class — matches the dashboard's prior stated figure exactly.

**Computed finding basis (verified this session, from the 13-paper case-record extracts and the pinned NB2
network):**
- 31 distinct case genes across the validation-case set.
- 9 of 31 (29%) are already in the NB2 168-gene network: EGFR, KITLG, MC1R, OCA2, PAX3, POMC, PPP3CA, TYR,
  TYRP1.
- Adding D'Arcy S1 disease-direction recovers 7 more that are absent from the network but present in D'Arcy:
  BNC2, HERC2, IRF4, LRMDA, RALY, SLC24A5, SLC45A2 — bringing coverage to 16/31 (52%).
- 15 case genes are absent from **both** the network and D'Arcy — the "dark-matter" gap that instantiates the
  project's thesis (prediction failing by genomic background): ATRN, EMCN, KALRN, MANBA, MFSD12, MSX2,
  NPLOC4, ORAOV1, PKHD1, SIK1, SLC24A4, SLC39A8, SYT6, TACR3, TSPAN10.

**Plan approved.** A 3-phase, 9-step, specialist-gated plan (Phase 1: parse D'Arcy S1 + reproduce the
cross-check + attach S1 direction as annotation-only, in parallel with case-gene ID resolution and NB3
formalization; Phase 2, gated: master coverage table + discordance-direction-vs-disease-direction cross;
Phase 3, gated: coverage-and-direction figure + findings memo, in parallel) is recorded as artifact
`e3d52bf4-4876-41f1-89c4-fb544c3677d1`, approved version `c1d3bf0a-ee55-45fb-8616-4ce3dceb9888`.

**Deferred, not abandoned.** The NB4–NB8 downstream chain and the sex-hormone × pigmentation expansion remain
on record as critiqued and not pursued for this 2-day deliverable — not deleted, not ruled out permanently.
Whether either is ever revisited post-deadline is unsettled; see `TODO.md` "Needs PI discussion" section.

**Documents updated:** `project_dashboard.md` (§2, §4, §5a, locked decision 2), `TODO.md` (AGREED vs
needs-discussion split).

## 2026-07-11 — Platform-handoff documents consolidated under `internal/handoffs/`; agent-notes guidance added to this file

**What changed.** Created `internal/handoffs/` as the canonical, documented home for platform-to-platform
handoff documents, building on top of the merge-safe agent-to-agent notes channel the
`REPRODUCIBILITY_SPECIALIST` had just designed at `internal/handoffs/notes/` (design and rationale in
`internal/handoffs/MERGE_SAFETY.md`; that mechanism was adopted as-is, not redesigned). Added
`internal/handoffs/README.md`, explaining what a handoff document is, when to write one, the
`HANDOFF_<FROM-PLATFORM>_TO_<TO-PLATFORM>_<topic>.md` naming convention for new ones, and pointing to
`MERGE_SAFETY.md` for the notes channel. Moved the two existing, previously untracked handoff documents —
`internal/CLAUDE_CODE_HANDOFF.md` and `internal/CLAUDE_SCIENCE_RETAINED.md` — into `internal/handoffs/`
under their original names (they predate the naming convention; renaming them would break the
cross-references already embedded in their own prose, so the README documents them as a named exception).
Fixed the one stale in-repo path reference this move broke (`CLAUDE_SCIENCE_RETAINED.md`'s pointer to the
build handoff). Added the "Guidance for agents: writing notes to each other" standing section to the top of
this file (above), and added short pointers to `internal/handoffs/` in `project_dashboard.md` §6 and
`TODO.md`'s housekeeping table, plus a new AGREED todo item to maintain handoff docs there going forward.

**Why.** The project had two ad hoc, untracked handoff documents at `internal/` root with no folder-level
documentation of what a handoff document is or how a new one should be named, and no written guidance
telling agents where operational notes to each other belong versus the human-facing changelog — both gaps
this session's `REPRODUCIBILITY_SPECIALIST` work on the notes channel made newly relevant to close.

**Plan-sync check.** Ran `check_plan_sync()` against `project_dashboard.md`: 0 drifted (3 numbers ok, 2 not
mentioned in the plan text, 0 missing source files). No numeric drift from this reorganization — it touched
no pinned data file.

**Documents updated:** `internal/handoffs/README.md` (new), `internal/handoffs/CLAUDE_CODE_HANDOFF.md`
(moved), `internal/handoffs/CLAUDE_SCIENCE_RETAINED.md` (moved, one path reference fixed),
`project_dashboard.md` (§6), `TODO.md` (housekeeping table, item 14).

## 2026-07-11 — Two-level paper framing adopted: discordance headline + dark-matter-association second act

**Context.** `FRAMING_EVALUATION_dark_matter.md` evaluated whether "dark-matter association" should become
the paper's framing, given the coverage finding that 15 of 31 validation-case genes are absent from both the
mechanistic network and the D'Arcy disease-gene compendium. The evaluation found the worry justified but the
corpus broader than the coverage-finding MVP made it look (6 of 13 papers touch at least one dark-matter
gene, carrying 60% of records), and recommended a two-level framing rather than a single slogan.

**PI decisions this session (three):**
1. **Adopt the two-level framing — yes.** Headline (unchanged): bidirectional genotype→phenotype discordance
   (D1 = genotype-present/phenotype-absent; D2 = phenotype-present/genotype-absent) on one signed directed
   network, payoff loci TYR + OCA2 only. Second act (new spine): "dark-matter association" as the organizing
   frame for the coverage/gap analysis beneath the headline. Dark matter does not replace or compete with
   the discordance headline. Recorded as locked decision 11 in `project_dashboard.md`.
2. **Rewrite the project's documents to the new framing — yes.** Scope per `FRAMING_EVALUATION_dark_matter.md`
   §4: `README.md`, `project_dashboard.md`, `TODO.md`, `FINDINGS_darcy_coverage.md`,
   `RESEARCH_SYNTHESIS_locus_resolution_mvp.md`, and notebook 04 (one added markdown cell, no code/output
   changes).
3. **Widen the corpus to GWAS Catalog ≥2×-replicated associations as `dark_matter_association` loci —
   HELD until after the MVP.** Not authorized now; recorded as a held item, not an open question, in
   `TODO.md`'s needs-discussion table (item D8).

**Two caveats folded into every corpus description as part of this rewrite:** Kastelic 2013 extracted 0 gene
symbols (105 records, no gene column — a model/marker paper, not 13 independent gene contributions); the
three TYRP1 blond-hair papers (Kenny 2012, Norton 2014, Norton 2016) all reduce to the single in-network gene
TYRP1 — D2 depth, not breadth.

**Mislabeled-pointers hypothesis result carried into the framing (already run, not re-run):** 0 of 15
dark-matter genes resolve to an in-network gene via GWAS Catalog + eQTL Catalogue evidence — the hypothesis
is falsified; the dark matter decomposes into four cited classes instead (see
`RESEARCH_SYNTHESIS_locus_resolution_mvp.md` §1, logged in `project_dashboard.md` §3 so it is not re-run).

**Documents updated:** `README.md` (pitch + 4-way decomposition + 13-independent-genes correction),
`project_dashboard.md` (locked decision 11; §3 decomposition table + falsified-hypothesis log), `TODO.md`
(AGREED item 15; needs-discussion item D8, held), `FINDINGS_darcy_coverage.md` (per-paper cluster mapping),
`RESEARCH_SYNTHESIS_locus_resolution_mvp.md` (per-paper cluster table), `notebooks/04_darcy_coverage_finding.ipynb`
(one added markdown cell, "Where each paper fits" — no code cells or stored outputs touched).

**Plan-sync check.** `check_plan_sync()` run against `project_dashboard.md` after this rewrite — see the
run's own report for drift status; this rewrite touched no pinned processed-data file, so no numeric drift
is expected from it.

---

## 2026-07-11 — D'Arcy coverage finding + Locus Resolver MVP substrate committed (`85e8092`); motivating-example reference removed

**What changed.** The coverage/discordance finding and the deterministic input substrate for the Locus
Resolver MVP were committed to `main` at `85e8092` (32 files: 27 new, 5 modified; 2800 insertions), after the
REPO_COMPLIANCE_GATE cleared the working tree. Not pushed — the commit stages the shared substrate on `main`
so a Claude Code session can branch `feature/locus-resolver` from it and build in parallel (handoff in
`internal/handoffs/CLAUDE_CODE_HANDOFF.md`); the return contract stays on Claude Science
(`CLAUDE_SCIENCE_RETAINED.md`).

**What was committed.**
- Finding: `notebooks/04_darcy_coverage_finding.ipynb` (with stored cell outputs, CI renders no-execute),
  `internal/FINDINGS_darcy_coverage.md`, `internal/RESEARCH_SYNTHESIS_locus_resolution_mvp.md`,
  `internal/FRAMING_EVALUATION_dark_matter.md`, `figures/case_coverage_direction_map.png`.
- MVP substrate: `data/processed/locus_nodes.csv`, `locus_annotation_edges.csv` (pass
  `scripts/validate_locus_tables.py`), `case_gene_coverage_master.csv`, `case_gene_id_resolution.csv`,
  `direction_concordance{,_matrix}.csv`, `darcy_S1_direction_on_backbone.csv`, `darcy_backbone_crosscheck.csv`;
  `docs/network_integration_and_MVP_spec.md`, `docs/specs/darcy2023_S1.spec.md`,
  `docs/direction_concordance_README.md`.
- Governance/handoff: `internal/handoffs/` tree, `internal/lit_review/` tree, and the modified
  `README.md` / `CHANGELOG.md` / `TODO.md` / `project_dashboard.md` / `.gitattributes`.

**Motivating-example reference removed.** A motivating-example URL and tool name (the project's initial
framing prompt, never a project data source or citation) were removed from four untracked working-tree files —
`internal/RESEARCH_SYNTHESIS_locus_resolution_mvp.md`, `docs/network_integration_and_MVP_spec.md`,
`internal/FRAMING_EVALUATION_dark_matter.md`, and
`internal/lit_review/2026-07-11_1222_SCOPING_ideas_and_prior_art_map.md`. All four were untracked (never
previously committed), so the reference never reached GitHub. The surrounding "competitor / bar to beat"
prose was rewritten to stand on the project's own design principle (principled refusal to overclaim; the
nearest-gene-vs-causal discipline) with no invented claims, and the inspected tool was dropped from the
RESEARCH_SYNTHESIS Sources line (it was an inspected tool, not a citation). A full-tree re-scan confirmed
zero remaining mentions.

**Compliance.** REPO_COMPLIANCE_GATE verdict CLEAR: withheld publisher content (Baxter Table S7 + the
Baxter/HIrisPlex/Walsh article PDFs) remains `.gitignore`-blocked; the committed D'Arcy/Bajpai supplements
are open-license (CC BY); READMEs document what is withheld and how to obtain it by DOI. Removing the
reference only deleted text from untracked markdown (added no withheld material), so the CLEAR verdict was
unaffected.

---

## 2026-07-11 — `pigmentation-plan-sync` checker rewritten source-agnostic; `PROJECT_MANAGER` gains a standing staleness duty

**The issue.** The `pigmentation-plan-sync` skill's `check_plan_sync()` was over-fitted to a frozen snapshot
of the project. It hardcoded five specific processed filenames (`raghunath_nodes_typed.csv`,
`raghunath_edges_typed_signed.csv`, `bajpai2023_crispr_hits.csv`, `baxter2018_650_pigmentation_genes.csv`,
`hirisplexs2018_markers.csv`), hardcoded the column names it read from them, and matched plan numbers with a
`CLAIM_PATTERNS` dict of fragile per-source free-text regexes — including a Bajpai-specific pattern that had
been patched to avoid capturing the "2023" publication year as a hit count. Consequences: the checker was
structurally blind to every processed CSV added after that snapshot (`gene_network_nodes.csv`,
`gene_network_edges.csv`, `gene_graph_*`, `locus_*`, `complex_members.csv`, `darcy_*`, and others), a renamed
file silently degraded to `no_file`, and a new data source was never checked at all. It reported on the
specifics of a fixed source list rather than reconciling the plan broadly against the repo's actual state.

**What changed in the skill.** `kernel.py` and `SKILL.md` were rewritten to be source-agnostic and
table-driven, and republished (personal skill, overwrite):

- The checker now discovers what to verify from the project's current state instead of a baked-in list. It
  parses every row of the dashboard's **Key metrics** table (each row already declares a value and its source
  CSV) and reconciles each against the cited file. No filename, source name, or number is hardcoded.
- Judgement is generic: a row whose label carries a whole-file count noun (nodes/edges/rows/records/hits/
  markers/entries) must match the cited file's row count (hard `DRIFT` on mismatch); any other stated integer
  must be reproducible from a simple column op on the cited file (soft `review` otherwise). Conditional facts
  such as the 58 dual-compartment bases reconcile via bounded group-wise distinct counts. The Bajpai count is
  now checked as a plain row count, so the publication-year special case was removed entirely.
- Added the coverage sweep the old checker lacked: `orphan_file` (a processed CSV on disk whose stem never
  appears in the plan — the un-inventoried-output staleness a per-number check cannot see) and `missing_file`
  (a cited pinned file gone from disk).
- Validated end-to-end against the live repo: 10 load-bearing counts reconcile `ok`, 0 drift, and the sweep
  surfaced 4 un-inventoried processed CSVs (`chem_resolution_evidence.csv`, `gene_graph_nodes.csv`,
  `gene_graph_edges_topology.csv`, `gene_graph_edges_projection.csv`) that the previous version could not see.
- A follow-up documentation fix: `SKILL.md` had described a glob file reference (`EXTRACT_*_records.csv`) as
  classified `external_ref`, but the parser's filename regex does not capture wildcard patterns, so such a
  row is skipped, not surfaced. The doc was corrected to state that glob/wildcard references are skipped and
  must be verified by hand.

**What changed in the specialists.** The `PROJECT_MANAGER` profile gained a standing **"Staleness is a
standing duty"** section (added ahead of the pre-commit compliance-gate section; profile otherwise unchanged,
still full-access). It makes drift-detection an unprompted responsibility on any task that touches the plan,
dashboard, inventory, or a build step, across three fronts: (a) numbers and file state reconciled against the
real files, never memory; (b) the project's own skills and checks, which go stale too — over-fitting to a
frozen snapshot (hardcoded filenames, per-source special cases, baked-in numbers) is to be fixed or flagged,
preferring source-agnostic checks that discover what to verify from current state; and (c) conflicting or
duplicate skills that claim authority over the same job, to be reconciled to a single source of truth with
the superseded one retired.

**Why.** A stale check reads as authoritative and is worse than no check; the over-fitted checker would have
silently passed a plan that omitted newer outputs. The skill fix removes the snapshot dependence, and the
profile change makes catching this class of drift — in data, in tooling, and in overlapping skills — a
standing part of the custodian role rather than something done only on request.

**Documents updated:** `pigmentation-plan-sync` skill (`SKILL.md`, `kernel.py`); `PROJECT_MANAGER` agent
profile (system prompt). No repo data files or tracking-document numbers changed.

---

## 2026-07-11 — Tiered pre-commit compliance gate propagated across all specialists and gate-referencing skills

**The issue.** The pre-commit compliance gate existed in two divergent versions across the specialist
profiles, a duplicate-authority drift. The `precommit-compliance-gate` skill and two profiles
(`PROJECT_MANAGER`, `RESEARCH_SITE_PUBLISHER`) carried the current **tiered** rule — Tier 1 (fast local
self-check, commit directly) for scoped commits that only modify already-tracked files or add the project's
own code/prose, Tier 2 (delegate to `REPO_COMPLIANCE_GATE`) only when a new document/data/archive file
appears or `.gitignore`/README/`DATA_SOURCES` change, and always at push/PR/tag/release. Nine other profiles
still carried an older non-tiered paragraph ("Before ANY action that publishes… you MUST first hand the
working tree to REPO_COMPLIANCE_GATE… This holds even for a quick or routine commit") that forced a delegated
gate round-trip on every commit. That is what caused small changes to be held up and to backlog into rare,
oversized commits.

**What changed.** The nine profiles still on the old rule were reconciled to the single canonical tiered
text (taken verbatim from the already-correct profiles so no new wording drift was introduced):
`DATA_SOURCE_AUDITOR`, `PLAN_DECONVOLUTOR`, `REPRODUCIBILITY_SPECIALIST`, `PI_ORCHESTRATOR`,
`SCICOMM_REVIEWER`, `VISUAL_DATA_REVIEWER`, `HACKATHON_DOCUMENTARIAN`, `PLATFORM_LIMITS_ADVISOR`,
`GENETICS_DATA_EXTRACTOR`. Only the compliance-gate paragraph was replaced; each profile's identity, other
instructions, skill list, and unrestricted access were left unchanged. The `quarto-github-pages` skill's one
gate sentence, which still implied gating every commit, was rewritten to defer to the tiered check
(`commit_needs_full_gate`) and republished. Left untouched: the `precommit-compliance-gate` skill (already
the tiered source of truth), `PROJECT_MANAGER` and `RESEARCH_SITE_PUBLISHER` (already tiered), and
`REPO_COMPLIANCE_GATE` (the gate itself, exempt).

**Verification.** After the edits, no profile retains the old non-tiered block, and every gate-referencing
profile except `REPO_COMPLIANCE_GATE` now carries the tiered rule.

**Why.** A specialist should be able to commit small, already-cleared changes (a source edit, a
tracking-document update, a prose fix) directly, and reserve the delegated gate for commits that actually
introduce redistribution risk or for the push/PR/release where content leaves the machine. Divergent copies
of the same rule are the same failure mode as a duplicate document under a variant name — they silently drift
— so the fix reconciles them all to one source of truth rather than leaving two live.

**Documents updated:** nine agent profiles (system prompts, compliance-gate section only);
`quarto-github-pages` skill (`SKILL.md`). No repo data files or tracking-document numbers changed.

---

## 2026-07-11 — Scoped-commit / clear-message hygiene added to the gate skill and all committing specialists

**The issue.** The tiered gate made small commits cheap, but nothing yet made scoped, well-messaged commits
the expected practice, and the working tree showed the symptom: several unrelated changes
(`internal/CHANGELOG.md`, a handoff doc, and a batch of new resolver outputs) were accumulating uncommitted,
headed for one large "document it all at once" commit. Recent history also mixed clear scoped subjects
(`docs:`, `ci:`) with vague ones (`moving things around.`, `Update project_dashboard.md`), which defeats
using `git log` as a rollback map of project progress.

**What changed.** A **Commit hygiene** section was added to the `precommit-compliance-gate` skill (the single
source of truth every committing specialist loads) and republished. It states: commit at the boundary of each
completed unit of work rather than at end of session; one concern per commit, staged by explicit path (not
`git add -A`); and a clear conventional-style message (`<type>(<scope>): <imperative summary>`, with a body
for the non-obvious *why*), with worked examples and an explicit list of vague subjects to avoid. It also
notes that committing more often does not change the tier — each scoped commit runs the same fast Tier-1
self-check.

A concise awareness clause pointing at that section was added to the shared compliance-gate paragraph carried
by all ten canonical-block specialists, and an equivalent clause to `RESEARCH_SITE_PUBLISHER`'s own gate
paragraph — eleven committing specialists in total. `REPO_COMPLIANCE_GATE` was left unchanged: it prepares
edits and reports a verdict but does not commit ("the human commits"), so commit hygiene does not apply to it.

**Demonstrated in practice.** The changelog entry above (tiered-gate propagation) was committed on its own as
a scoped Tier-1 commit (`docs(changelog): …`) staged by explicit path, rather than being bundled with the
unrelated untracked outputs in the working tree. Those other outputs are another session's products and were
flagged for their owner rather than swept into this commit.

**Why.** A history of small, self-contained, clearly-messaged commits documents project progress and gives
per-change rollback points; an end-of-session pile of mixed changes gives neither and forces after-the-fact
reconstruction of what happened.

**Documents updated:** `precommit-compliance-gate` skill (`SKILL.md`, new Commit-hygiene section); eleven
agent profiles (system prompts, compliance-gate clause only). No repo data files or tracking-document numbers
changed.
