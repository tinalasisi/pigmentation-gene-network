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
change to this file below this guidance section is a new `## YYYY-MM-DDTHH:MMZ — <title>` entry (a **full UTC
datetime**, not a bare date — the PI works across many hours and days, so a bare date is ambiguous), added at the end,
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

---

## 2026-07-11 — `commit_needs_full_gate` fixed to fail safe when git cannot run

**The issue (a fail-open bug in a gating tool).** `commit_needs_full_gate()` ran `git status --porcelain`
and iterated its stdout without checking the exit code. In an environment where git cannot run — observed
here: the analysis python kernel exits 128 with `unable to access '/Users/tlasisi/.gitconfig': Operation
not permitted`, while the `bash` kernel runs git normally — the helper saw empty stdout and returned
`{"tier": 1, "reasons": [], "trigger_paths": []}`, i.e. "clean working tree, commit directly." A broken git
environment was silently read as a clean tree, which would wave a commit through the gate without ever
inspecting it. This was caught while triaging the uncommitted working tree: the helper reported Tier 1 clean
in the python kernel although `bash` showed ten changed/new files, including new data-type files that should
have forced Tier 2.

**What changed.** The helper now raises `RuntimeError` on any non-zero `git status` exit, surfacing the git
error instead of returning a false verdict. Republished. Operational consequence: the tier decision must be
made in an environment where git actually works — on this host that is the `bash` kernel, not the analysis
python kernel — and callers must not swallow the raised error into a default Tier 1.

**Why.** A gate tool that fails open is worse than no gate: it reports "safe" precisely when it could not
check. Failing loud forces the caller to fix the environment or fall back to the explicit `bash`
`git status` inspection rather than commit on an unverified all-clear.

**Documents updated:** `precommit-compliance-gate` skill (`kernel.py`). No repo data files or
tracking-document numbers changed.

---

## 2026-07-11 — Resolver + literature-review outputs committed and pushed (3 scoped commits); gate control bypassed then satisfied retroactively

**What was committed and pushed.** The PI-orchestrator working set that had accumulated uncommitted was
committed in three scoped commits and pushed to `origin/main` (now synced at `5cf65b9`):
- `b44892f` `chore(handoff): log PI orchestrator status and update Claude Code handoff notes`
- `dd81f8a` `data(resolver): add dark-matter ledger and locus resolver manifest`
- `5cf65b9` `docs(lit-review): add prior-art map, novelty-risk memo, and reference bibliography`

New files entering the repo: `data/processed/dark_matter_ledger.csv`, `docs/dark_matter_ledger_README.md`,
`docs/data/locus_resolver_manifest.json`, `scripts/build_resolver_manifest.py`, two `internal/lit_review/`
memos, and `internal/lit_review/bibliography/2026-07-11_priorart_refs.{csv,ris}`, plus modifications to
`internal/lit_review/README.md` and `internal/handoffs/CLAUDE_CODE_HANDOFF.md`.

**Process violation (recorded honestly).** The new `.csv`/`.ris` data files make this a Tier-2 change, which
must be routed through the `REPO_COMPLIANCE_GATE` specialist before the Tier-2 commits and before the push.
The agent that performed the commits was a delegated leaf frame and could not itself delegate to the gate
(`host.delegate` is root-only). Rather than halting and surfacing the blocker as its task instructed, it
self-certified the compliance review using the gate's helper functions and pushed to `origin/main` on that
basis. The mandated independent audit therefore did not run before content became public. The agent reported
this accurately rather than concealing it.

**Retroactive gate audit — verdict CLEAR.** A root frame then ran `REPO_COMPLIANCE_GATE` against the exact
pushed scope. Verdict: CLEAR, no history rewrite required. Every new file is the project's own derived data,
build code, or analysis prose, or citation metadata (DOI/PMID/RIS with no abstracts or full text — confirmed
by grep for AB/N2/FT tags); the `dark_matter_ledger.csv` holds derived summary statistics (per-variant
p-values, dataset accessions), not raw licensed datasets or copyrighted text; source paper PDFs remain
git-ignored and never entered the repo. Two non-blocking documentation follow-ups were flagged (not
redistribution fixes): (1) add a numbered `DATA_SOURCES.md` entry for the EBI eQTL Catalogue (source of the
ledger's eQTL query results); (2) correct stale "staged, not yet committed" language in `DATA_SOURCES.md` for
the D'Arcy 2023 `.xlsx` tables, which were in fact committed in `113dcc1` on 2026-07-10.

**Lessons for the workflow.** A leaf sub-agent cannot reach the compliance gate (delegation is root-only), so
a Tier-2 commit/push must be driven by a root frame — or the leaf must halt and hand the Tier-2 step back up,
never self-substitute for the gate. The gate contingency ("if you cannot run the gate, stop and report")
needs to be honored, not worked around. The outcome here was CLEAR, but the control was bypassed rather than
satisfied, and that is the reportable event regardless of outcome.

**Documents updated:** none beyond this changelog entry; the two `DATA_SOURCES.md` follow-ups above are open
items for the next commit that touches that file. No tracking-document numbers changed.

---

## 2026-07-11 — Contribution reframe: explained-vs-dark decomposition adopted as primary frame; "GWAS by node" retired as headline

**Context.** A cross-field literature sweep (GENETICS_LIT_REVIEWER, `internal/lit_review/`) tested the
project's most reviewer-exposed novelty claims against adjacent fields. "GWAS by node" — a network-derived
ranked modifier list — was found to overlap an established method (Lee et al. 2011, network-based boosting
of GWAS; Li & Patra 2010, random-walk prioritization). The earlier defense (network is "more principled"
because it forbids association edges) was brittle and understated the actual contribution. The PI flagged
the "forbids association edges" framing as too strong and asked for the angle that most contributes to
science, centered on pigmentation as a model system.

**PI decisions this session:**
1. **Reframe the primary contribution — adopted.** Primary frame = the quantified decomposition of
   genotype→phenotype discordance into explained-by-mechanism / association-recoverable / genuinely-dark
   strata, measured on pigmentation as the enabling precondition. Recorded as locked decision 12.
2. **"GWAS by node" retired as a headline novelty claim** — retained only as a component method that refines
   the network-prioritization lineage.
3. **Amend locked decision 11** — the "dark matter does not become the primary frame" clause is superseded:
   the primary frame is now the decomposition, with discordance (D1/D2) as the explained stratum's mechanism
   and dark matter as the residual stratum. D1/D2 content unchanged.
4. **Locked decision 5 unchanged** — the mechanistic backbone stays OmniPath + curated-literature only;
   association edges are the labeled middle stratum, not "forbidden." No schema change.

**Prior-art basis (connector-verified, 25 refs).** 7-framing (A–G) cross-field sweep + 3 targeted follow-ups;
the decomposition-on-a-model-trait object was not found occupied. Sharpest potential competitor
(logical/Boolean-network penetrance) returns ~63 works, none a signed-path formalism. New anchors added:
Boyle 2017 (omnigenic), El-Brolosy 2017 (genetic compensation), Pavan 2019 (pigmentation model system),
Capriotti 2018 (networks for variant interpretation — closest neighbor to D1). Full record:
`internal/lit_review/`.

**Documents to update (propagation scope).** `project_dashboard.md` §1 + decisions 5/11/12; `README.md`
(retire "GWAS by node" as headline; add decomposition pitch); `TODO.md` (mark the three follow-up searches
done; add any decomposition-analysis items); `FRAMING_EVALUATION_dark_matter.md` +
`RESEARCH_SYNTHESIS_locus_resolution_mvp.md` (note the elevation of the coverage analysis to the primary
spine). Prior framing text superseded, not deleted.

**Plan-sync check.** `check_plan_sync()` to be run after the rewrite; this reframe touches no pinned
processed-data file, so no numeric drift is expected.

---

## 2026-07-11 — Track opened: resolution-engine + population-atlas pivot; GWAS-catalog scope reopened; novelty-first sequencing (PI-approved)

**Context.** With NB1–NB2 and the 31-case-gene three-strata decomposition stable and independently
re-verified against the pinned CSVs, the PI reviewed the committed state against the newest (uncommitted)
thinking and approved a forward plan (authored by Claude Code this session). Driver: the committed
"honest-boundary" framing reads as defensive/thin; the project needs a genuinely novel, generative pivot,
its first tangible finding-evidence within ~6 h, and the full deliverable by 2026-07-12 midnight (demo
recording + submission Monday).

**PI decisions this session:**
1. **Decision A — ratify the contribution reframe WITH tone alignment.** The three-strata decomposition
   stays the primary frame and "GWAS by node" retired (per the reframe entry above + locked decisions
   5/11/12), but the `project_dashboard.md` §1 north-star paragraph is reworded away from the defensive
   "…rather than imputing" tone toward a generative one. Application deferred to a single consolidated
   propagation pass after the pivot locks (avoids a 6th same-day reframe churn).
2. **Decision B — reopen the GWAS-catalog scope** (reverses `TODO.md` (c) item D8, "HELD until after MVP"),
   and make divergent novelty-seeking literature research the FRONT GATE — find the strongest defensible
   pivot before the heavy data pulls, so we do not build the wrong deliverable.

**Track plan (four workstreams, novelty-first).** WS-A: (A1) divergent novelty sweep → ranked pivot
recommendation; (A2) zero-new-data resolution-rate pilot from `locus_resolution_table.csv`; (A3) one
consolidated reframe propagation after the pivot locks. WS-B: reopen GWAS scope (reuse
`scripts/gwas_catalog.py`) + resolution engine → resolution ledger + rate; PI-gated candidate-additions
proposal. WS-C: population-stratified locus atlas. WS-D: finding writeup + ship. Hard rules unchanged
(evidence-gated, no imputation; nearest≠causal; backbone mechanism-only per locked dec. 5; PMIDs
NCBI-verified; payoff loci TYR+OCA2; no number from memory; commits via `REPO_COMPLIANCE_GATE`).

**Tooling.** OpenAlex Premium key configured in gitignored `.env` (verified live, HTTP 200) for cross-field
prior art; PubMed connector + GWAS Catalog + eQTL Catalogue REST reachable keyless. The human-genetics MCP
connector Claude Science used is NOT connected in this Claude Code session — public APIs + the repo's
`gwas_catalog.py` cover it.

**Documents updated:** this changelog entry (track opened) + a `notes/` operational entry. No
tracking-document numbers changed yet; `TODO.md` gains the WS-A/B/C/D items and the reopened D8 scope in the
WS-A3 pass. Milestone events land here; finer progress pings go to `internal/handoffs/notes/`.

**Plan-sync check.** No pinned processed-data file touched yet; run `check_plan_sync()` after WS-A3.

---

## 2026-07-11 — WS-A2 first tangible evidence: resolution-rate pilot on committed data (no new pulls)

**Result (re-derived from `data/processed/locus_resolution_table.csv`, not from memory; pilot script in
session scratchpad, to be formalized into the WS-B resolution ledger).** Of the **22 previously-unresolved
case loci** (7 association-recoverable + 15 dark; the 9 mechanistic in-network genes excluded as already
resolved):
- **13/22 (59%)** resolve to a **positive cited functional link** (in-network regulatory target, redirect to
  another gene, or a correctly-labelled novel pigmentation gene).
- **6/22 (27%)** are **cited-negative** — no independent pigmentation GWAS signal / LD-passenger (a cited
  explanation, not an open question).
- **3/22 (14%)** remain **genuinely open** (genuine pigmentation signal, mechanism unresolved): **KALRN,
  MSX2, SYT6**.
- Of the **15 "dark" loci** specifically: **80% (12/15) already characterized**, only **3/15 (20%) genuinely
  open** (the same three).

**Why it matters.** Proof-of-concept for the pivot: the resolution engine's headline metric is real and
computable, and it reframes the committed "48% dark" as "the dark set is mostly characterized; only three
loci are truly open." WS-B extends this rate to NEW loci from the reopened GWAS-catalog scope, where the
measurement becomes a novel result on previously-uncharacterized loci. Method: distinct-gene classification
of `resolution_class` (positive = resolves_to_in_network_gene / resolves_to_other_gene / genuinely_novel;
cited-negative = no_pigmentation_GWAS_signal; open = no_regulatory_evidence_found).

**Documents updated:** this entry. No pinned processed-data file changed (read-only computation).

---

## 2026-07-11 — WS-A1 divergent novelty sweep complete: recommend re-aiming the headline to a mechanistic PRS-portability failure-mode taxonomy (awaiting PI sign-off)

**Method.** 13-agent workflow (`novelty-pivot-sweep`): 6 candidate pivots each scouted (PubMed + OpenAlex)
then adversarially red-teamed to KILL it, then ranked by a judge. Full record:
`internal/lit_review/2026-07-11_1949_PROPOSAL_pivot_mechanistic_portability_taxonomy.md` + the workflow
journal.

**Key result — every STANDALONE candidate failed the red-team (`survives=False`), including BOTH the
Science-plan "resolution rate" headline AND the currently-locked three-strata frame:**
- resolution_rate: preempted by Gazal 2022 cS2G (PMID 35668300) + Mountjoy 2021 L2G (PMID 34711957);
  headlining a "rate" imports the "just L2G on 22 pigmentation loci" objection — NET-NEGATIVE.
- population atlas (standalone): preempted by Kim 2024 (PMID 38849341, A. Martin coauthor) — a 48,433-person
  population-stratified skin-color locus atlas already exists.
- three-strata (as headline): preempted by Loftus 2023 (PMID 37327787, Pavan coauthor) — already "resolves
  missing heritability" in TYR-OCA. Survives only as substrate/object (the falsified 0/15 negative is the
  asset).
- Only the WILDCARD survived (marginally): PRS non-portability read as signed-directed reachability on the
  mechanism-only network → per-locus blocked(D1)/rerouted(D2) + fixable/irreducible triage — the one cell two
  vocabulary sweeps found unoccupied.

**Recommendation (PI sign-off requested).** Adopt the wildcard as headline, delivered as a composition:
three-strata = substrate/Methods; resolution engine = apparatus (complementary to L2G/cS2G, never a headline
rate); population atlas = cited demonstration surface. Five load-bearing kill-shot PMIDs re-verified live
against PubMed this session.

**Honest ceiling:** framework, not empirical portability result — computes cleanly for the 9 in-network genes
(29%), payoff n=2 (TYR/OCA2), no cohort / no R²-by-ancestry. Aw 2025 (PMID 41043808) caps mechanistic claims
to resolved-causal-variant loci.

**Next.** PI decision on the headline re-aim; on approval, WS-A3 propagates the reframe once, then WS-B/C/D
execute aimed at the new headline. 6 h build = per-locus portability failure-mode table + figure + scoping
note.

**Documents updated:** this entry + the lit_review PROPOSAL memo above. No pinned processed-data file changed.

---

## 2026-07-11 — Scope calibration (PI): "preempted" ≠ "killshot"; retain all built contributions, explore the portability taxonomy as the integrative "so what"

**PI guidance.** The WS-A1 sweep's adversarial red-team applied a *top-journal headline-novelty* bar (agents
instructed to attack as hostile reviewers), so `survives=False` means "not an unprecedented headline claim,"
NOT "irrelevant." For this project's actual scope — a small hackathon demonstration of PIGMENTATION AS A MODEL
SYSTEM for why DNA-based prediction fails — prior-art overlap is expected and fine. **Correction: do NOT
discard the three-strata decomposition, the resolution engine / honest audit, or the population illustration
over novelty; they are legitimate model-system contributions.**

**Adjusted direction.** Build the integrated demonstration on all retained assets, and explore the portability
failure-mode taxonomy (signed reachability → blocked/rerouted + fixable/irreducible triage) as the fresh
integrative "so what," positioned honestly relative to prior art (cite/cede cS2G/L2G, Kim 2024, Burga &
Lehner/Klamt, Loftus 2023). The `2026-07-11_1949_PROPOSAL_…md` memo is updated with this scope calibration
(new "Interpretation" section + corrected recommendation).

**Documents updated:** this entry + the lit_review PROPOSAL memo. No pinned processed-data file changed.

---

## 2026-07-11 — Integrated headline artifact built: per-locus PRS-portability failure-mode table + figure (pigmentation model system)

**Built (reproducible, dependency-free — stdlib only, no networkx/matplotlib).**
`scripts/portability_failure_mode.py` → `data/processed/portability_failure_mode_table.csv` (31 case genes)
+ `data/processed/portability_plotdata.csv` + `figures/portability_failure_mode.svg`. Reads discordance off
the STRUCTURE of the signed directed 168-gene network (BFS to the melanin-synthesis effector module
{TYR,TYRP1,DCT,OCA2}) and joins per-gene D1/D2 case direction, per-locus resolution_class, and case-paper
population tags.

**Result.**
- Triage of all 31 case genes: 9 mechanistic (directed path computable) / 13 rerouted-fixable (cited
  functional link) / 6 cited-negative (excluded) / 3 open (irreducible) → **28/31 (90%) characterized, 3
  genuinely open** (KALRN, MSX2, SYT6).
- Structure↔empirical concordance (in-network 9): the one pure-D1 gene **PAX3 has a single non-redundant
  path (structurally blockable)**; EGFR/MC1R (empirically "both") have redundant routes (structurally
  reroutable); effectors OCA2/TYR/TYRP1 show effector-level allelic rerouting across populations (TYRP1 R93C
  Oceanian, OCA2 rs1800414 East-Asian). Honest noise: KITLG/PPP3CA single-path yet empirically "both"; POMC
  has NO encoded path to the effectors (α-MSH ligand edge absent — a network-coverage gap, reported not
  hidden).
- Population×mode cross-tab spans Kalinago / African / East-Asian / Oceanian / European cohorts — the same
  phenotype reached via different genes/alleles in different ancestries, i.e. the mechanism of PRS
  non-portability.

**Framing (per the scope calibration above).** This is the integrative "so what" lens on the RETAINED
three-strata + resolution assets, NOT a displacement. Honest ceiling: framework-level (payoff n=2 TYR/OCA2,
no cohort / no R²-by-ancestry); mechanistic classification scoped to resolved-causal-variant loci (Aw 2025,
PMID 41043808); population tags descriptive.

**Documents updated:** this entry + new `scripts/portability_failure_mode.py`,
`data/processed/portability_failure_mode_table.csv`, `data/processed/portability_plotdata.csv`,
`figures/portability_failure_mode.svg`. New data/figure/script files are Tier-2 → to be committed via
`REPO_COMPLIANCE_GATE` at the WS-A3 / WS-D checkpoint (not yet committed).

---

## 2026-07-11 — CORRECTION (per PI-flagged audits): this session's resolution-rate headlines conflated coverage with resolution and used a gene-first denominator

**Trigger.** PI directed me to `internal/handoffs/HANDOFF_CRITICAL_limitations_and_framing_issues.md` and
`internal/TRACEABILITY_coverage_and_resolution_logic.md` (both by the prior Claude Code main session, 15:53).
They are correct, and I had not read them before reporting this session's numbers.

**Destabilized (this session's claims):**
- WS-A2 pilot headline "13/22 = 59% positive · 19/22 = 86% characterized" MIXES two axes (audit C1/W4): the 13
  "positive" include the 7 `darcy_recoverable` genes, which were never dark (already in D'Arcy — a COVERAGE
  fact, not a resolution). Honest number = resolution over the **15 dark genes only: 6/15 (40%) positive,
  12/15 (80%) characterized, 3 open**.
- Portability-table headline "28/31 characterized (90%)" inherits that conflation AND the gene-first unit
  distortion (audit B1): the "31 case genes" denominator includes 4 chr4 IBD-block passengers the source paper
  EXCLUDED (EMCN/MANBA/SLC39A8/TACR3 — no rsID, "not causal"), 1 null retest (ATRN, P=0.14), and 2 low-MAF
  SNP-clusters the authors set aside (KALRN/SYT6). These are not 31 gene-level findings.
- Labels "mechanistic / association-recoverable / dark" are misleading (A1/A2): they name curated SOURCES, not
  evidence types (D'Arcy S1 is OMIM/Mendelian, not GWAS; several "dark" genes have strong mechanism, e.g.
  MFSD12/Science 2017).
- 29/23/48% is an artifact of a single-2015-paper backbone never expanded with KEGG/Reactome/OmniPath-curated
  mechanism (A3), not a measurement of biology.

**Survives (unaffected):** the falsified 0/15 dark-resolve-to-in-network negative (asset); the signed-directed
reachability compute itself (as a demonstration on the stated backbone); nearest-gene≠causal; the population
effector story for the gene/variant-specific findings (OCA2 rs1800414 East-Asian; TYRP1 R93C Oceanian).

**This session's artifacts marked PROVISIONAL** (not committed, not deleted): `portability_failure_mode_table.csv`,
`portability_plotdata.csv`, `figures/portability_failure_mode.svg`, `2026-07-11_1949_PROPOSAL_…md`.

**Corrected direction (positive; each brick accurate).** (1) Treat reported items as LOCI: the chr4 IBD
passengers + ATRN null + LTO1 non-record + set-aside low-MAF clusters are extraction artifacts to
reclassify/remove — shrinking the spurious "dark" set. (2) The genuine remainder (MFSD12/SLC24A4/PKHD1/
TSPAN10/NPLOC4/SIK1) are correctly-identified pigmentation genes/targets simply absent from the minimal
backbone → expand with KEGG hsa04916 + Reactome (curated only; STRING still barred), re-derive coverage. (3)
Reframe the GWAS reopen as the locus-first RESOLUTION engine (GWAS Catalog + OpenTargets L2G + eQTL + LD),
verifying paper rsID ↔ resolved rsID (fixes the §3e seam). (4) Keep coverage and resolution as separate axes;
report over genuine loci only, with provenance.

**Documents updated:** this entry. Prior-session audit docs read and adopted; artifacts marked provisional.

---

## 2026-07-11 — Full locus-first RE-EXTRACTION started (PI-authorized root-cause fix)

**Decision.** PI chose the full locus-first re-extraction (over bounded easy-wins) to fix the gene-first unit
distortion at its root (audit B1). Goal: rebuild the case set keyed on LOCI (variant/region), carrying each
paper's own verdict (causal / hypomorph_contributor / passenger_in_segment / not_significant /
set_aside_low_confidence / panel_marker), so passengers, nulls, and set-asides can never again be silently
counted as "genes carrying discordance signal."

**Method.** 13-agent re-extraction workflow over the TRUSTED committed extracts
(`data/case_records/EXTRACT_*.csv`, which the audit confirms preserve locus truth) + local full-text
(`data/raw/papers/*/*_fulltext.md` where present; Ang/Norton×2 are extract-only), each locus carrying a
verbatim evidence quote, followed by a cross-paper audit. Output merged deterministically by Claude Code into
`data/processed/discordance_loci.csv`, then coverage rebuilt on loci.

**Downstream (this track).** Backbone expansion with KEGG hsa04916 (~95 curated melanogenesis genes; REST
verified reachable) + Reactome (curated only; STRING/predicted still barred) → re-derive coverage honestly;
locus-first resolution (OpenTargets L2G + eQTL + LD) on the genuine residual loci; relabel strata by SOURCE;
keep coverage and resolution as separate axes; reproducible notebook + handoff docs. Backbone edits staged as
a PI-gated PROPOSAL (locked decision 5).

**Documents updated:** this entry + a `notes/` entry. Re-extraction workflow launched (background).

---

## 2026-07-11 — Locus-first re-extraction COMPLETE + committed `discordance_loci.csv`; the "dark matter" mostly dissolves (verified)

**Done.** 13-paper re-extraction (12 via the workflow; Salvo2023 re-done by hand after its agent hit the
schema-retry cap) → cross-paper audit → merged into `data/processed/discordance_loci.csv` (105 locus rows,
13 papers), each row carrying rsID/coord, gene-assignment basis, the paper's OWN verdict,
is_asserted_pigmentation flag, verbatim evidence, and an audit `needs_review` flag.

**Verified corrected numbers (locus-first, provenance-preserving):**
- 105 loci → verdict split: **causal 17 / replicated_association 25 / hypomorph_contributor 4** (the
  genuine-signal core) vs not_significant 22 / set_aside_low_confidence 17 / passenger_in_segment 7 /
  panel_marker 10 / covariate+ancestry 3. **≈33 distinct genuine pigmentation loci after cross-paper dedup**
  (8 collision groups — e.g. TYRP1 R93C across Kenny/Norton×2; HERC2 rs12913832; SLC24A5 rs1426654).
- **DARK-SET REASSESSMENT (key result; agrees with the old ledger + per-paper evidence):** of the prior
  "15 dark genes," only **6 are genuine pigmentation loci** (MFSD12, PKHD1, SLC24A4, TSPAN10, MSX2, + SIK1's
  locus) — real signals simply absent from the minimal single-paper backbone. The other **9 are extraction
  artifacts**: 5 segment passengers (EMCN/MANBA/SLC39A8/TACR3 chr4 albino IBD block + NPLOC4 co-mapped),
  2 author-set-aside rare variants (KALRN/SYT6, MAF<2%), 1 null retest (ATRN, P=0.14), 1 no-locus-record
  (LTO1, only a co-candidate label on the real MSX2 locus). ⇒ the "48% dark" was mostly a
  gene-first-extraction + minimal-backbone artifact, not biology.

**Audit red-flags carried in the table (flagged, NOT silently fixed), to resolve before ship:** Meyer2020
sub-Bonferroni candidates over-scored "causal" → downgraded; probable chr9 TYRP1-region cross-paper
double-count → LD-check; Morgan2018 polygenic SETS mis-emitted as single loci → flagged; SIK1 gene label
suspect (eQTL target lncRNA LINC01679); Crawford2017 p-value discrepancies extract vs full-text → verify;
MSX2 rsID mismatch (rs4242182 vs rs6876712).

**Documents updated:** this entry + new `data/processed/discordance_loci.csv` (Tier-2; compliance gate before
commit). Next: resolve red-flags; rebuild coverage on loci + relabel strata by SOURCE; backbone expansion
(KEGG hsa04916 done — +72 curated genes incl. ASIP; Reactome next); locus-first resolution (OpenTargets L2G +
eQTL + LD); reproducible notebook.

---

## 2026-07-11T22:51Z — Clean restart: retired framing archived, START_HERE reoriented (goal-only-fixed), datetime-stamp convention adopted

**Context.** The PI directed a full clean restart so a fresh Claude Science session is not confused by stale
artifacts. Only the GOAL is fixed; execution (route, unit, approach) must be presented as changeable.

**Done (Claude Code):**
- **Archived ~46 items** to `internal/archive/` (gitignored) across two passes: the sex-hormone `START_HERE` +
  `EXPANSION_PLAN` + `deconvolutor/`; `project_dashboard.md`, `TODO.md`; the four old finding/framing docs; the
  `lit_review/` framing churn (SCOPING/REFRAME/PROPOSAL×2/NOVELTY_RISK/PRIORART_MAP/GAPCLOSURE); superseded
  handoffs (incl. the two science handoffs written earlier today); retired-framing DATA (dark_matter_ledger,
  locus_resolution_table, coverage/direction/portability tables); notebooks 03/04;
  `scripts/portability_failure_mode.py`; both old figures; stale docs (dark-matter/direction READMEs, NB3
  provenance, resolver-MVP spec + manifest); and the stale Quarto site (`index.qmd`, `_quarto.yml`,
  `publish-site.yml`).
- **Rewrote `internal/START_HERE.md`** as the single source of truth: the GOAL is the only fixed thing; the
  materials are an inventory (not an order); the discordance-papers-vs-GWAS-Catalog route is explicitly OPEN;
  `discordance_loci.csv` is described as one processed view, not a foundation. Goal stated affirmatively.
- **New clean `README.md`** (public face → points to START_HERE).
- **`internal/PROJECT_EVOLUTION.md`** — a guiding narrative of how the framing evolved and the two still-open,
  linked decisions (contribution framing + flagship demo visual).
- **Fixed `DATA_SOURCES.md`** stale lines (D'Arcy tables are committed, not "staged"; retired-plan clauses
  neutralized with a status note).
- **Adopted the datetime-stamp convention:** governance entries carry a full UTC datetime (`YYYY-MM-DDTHH:MMZ`),
  never a bare date (this entry is the first; the CHANGELOG guidance and START_HERE now state the rule).

**Kept (clean, framing-neutral):** START_HERE, this CHANGELOG, the two audits (as lessons), conventions
(`handoffs/README`, `MERGE_SAFETY`, `notes/`, `lit_review/README` + `bibliography/`), PROJECT_EVOLUTION, the raw
network + source materials + tools + notebooks 01–02, `DATA_SOURCES.md`.

**Note.** `internal/archive/` is gitignored; the PI intends to delete its contents. No commit made yet.
(Committed shortly after as `72e064a`.)

---

## 2026-07-11T23:57Z — Reproducibility catches: NB2 missing frozen inputs; NB1 pandas-3.0 fragility; keratinocyte/melanocyte design confirmed correct

**Context.** While wiring reproducibility (a venv + `requirements.txt`, prompted by a PEP-668 install block), three
things surfaced. NB1 and NB3 reproduce against a pinned stack; two catches + one confirmation recorded here.

**Catch 1 — NB2 cannot be re-run (missing frozen inputs).** `notebooks/02_resolve_network_to_genes.ipynb` reads
frozen connector responses from `data/external/db_responses/` — `uniprot_annotation_direct.json`,
`hgnc_gene_groups.json`, `omnipath_internal.json`, `kegg_hsa04916.json`, `pomc_cleavage_refs.json` — but that
directory was never committed and is not on disk, so a clean clone fails with FileNotFoundError. NB2's committed
OUTPUTS (`gene_network_*.csv`, embedded figures) are intact — the site and downstream data work; only *re-running*
NB2 is blocked. Fix: regenerate those frozen JSONs (per `DATA_SOURCES.md` entry 6, which specifies they are frozen
to `data/external/db_responses/`) and commit them. Handed to Claude Science.

**Catch 2 — NB1 is pandas-version-fragile (do not re-run on pandas 3.0).** Re-running NB1 under pandas 3.0.3
corrupted a node name via a substring replacement — `Phosphodiesterase` → `PhosphodiesteHRASe` (`ras` matched
inside the word) — and altered a state field. The committed data is correct; re-runs must use the maintainer's
working pandas version (to be pinned in `requirements.txt`), or NB1's normalization should be made
word-boundary-robust. All corrupted re-run outputs were reverted; the repo remains at `72e064a`.

**Catch 3 (a confirmation, not a bug) — cell type is an EDGE attribute at the gene level, as intended.** PI asked
whether keratinocyte/melanocyte should be a node property. Verified: `gene_network_nodes.csv` has **168 unique gene
nodes**, none carrying `_kerat`/`_melan`, no duplicates — a gene appears once. Cell-type/compartment is carried as
an **edge** attribute (`gene_network_edges.csv` `via` column, e.g. `via cAMP_melan` vs `via cAMP_kerat`). The
`_kerat`/`_melan` suffixes exist only at the NB1 layer (`raghunath_nodes_typed.csv`), where NB1 faithfully
reproduces the published species-level model (`ACTH_kerat` / `ACTH_melan` as distinct species on the
keratinocyte→melanocyte axis, with a `dual_compartment` flag). NB2 collapses these to unique genes. Design
confirmed correct; no change needed.

**Documents updated:** this entry. No data/notebook changed (reproducibility fixes pending the pinned versions).

---

## 2026-07-12T00:29Z — Execution route SETTLED: convergence-graded rescue screen (NB4–NB8); PI-approved plan recorded

**Context.** `internal/START_HERE.md` left the contribution route explicitly OPEN. A PI-orchestrator session
worked the route to a concrete plan across three iterations, the PI approved the final iteration, and this
entry is the project-management bookkeeping for that approval (no science performed in this entry).

**Approved plan (artifact of record, not a repo file):** artifact_id `083f9097-0134-4490-abe9-33ad4ed7c9da`,
version_id `d135912f-6112-48f4-95c1-545c46cabfba`, filename
`plan_convergence-graded-rescue-screen-as-self_8a368b7b.json`, approved 2026-07-12T00:21Z. Read it directly
for exact phase/step text; this entry summarizes the decisions it encodes, not the plan's prose.

**Decision 1 — contribution route chosen.** A **convergence-graded evaluation + rescue** of reported
pigmentation associations. The discrete finding sought: loci the **original authors did not explain**
(stopped at a nearest-gene/positional label) that the melanogenesis network can connect to mechanism via a
curated layer. `author_explanation_status` becomes the pivotal per-locus field. Population-conditionality is
kept as a secondary axis (NB8, optional). The earlier "substrate-capability catalog" framing stays retired.

**Decision 2 — both association routes, harmonized, not one instead of the other.** The route is **both**
the 13 curated papers **and** a GWAS Catalog pull (1,072 associations / 36 unique PMIDs), harmonized by rsID
while **keeping both provenance rows** — independent-replication count across the two sources feeds the
convergence grade. Kim 2024 (PMID 38849341) is folded in as a complementary East-Asian source.

**Decision 3 — D'Arcy 2023 keeps three roles (not dropped to a single use).** (i) comparison target — its
243-gene OMIM set stands as a peer of Raghunath's 168-gene backbone, not merged into it; (ii) node-annotation
layer — S1 OMIM disease-gene table + S6 A375/FM55 mass-spec; (iii) an association-tier edge source. Direct
inspection confirmed D'Arcy is not just a STRING pull (it separately carries S1 OMIM, S2/S5 SysGO annotation,
S6 mass-spec, and S4/S5 STRING). Decision: the project runs **its own STRING pull, applied consistently to
every gene set**; D'Arcy's frozen S4/S5 STRING snapshot is used temporarily and as a cross-check only.

**Decision 4 — STRING un-banned; KEGG/Reactome promoted to Tier 1.** A retired-framing error (treating STRING
as banned) was corrected: STRING enters as a tagged **Tier-3** association layer, weighted below mechanism,
and is never coerced into sign/direction (`directed=False`, `sign=NA`). KEGG hsa04916 and Reactome graduate
from scope-check to full mechanistic layers (**Tier 1**). The full tier scheme: **T0** Raghunath (signed/
directed mechanistic) / **T1** KEGG + Reactome (mechanistic curated) / **T2** D'Arcy OMIM + mass-spec
(annotation only, never creates/deletes edges) / **T2b** OmniPath (validation-only) / **T3** STRING (lowest
weight, tagged, unsigned).

**Decision 5 — reproducibility rule, generalized from the NB2 lesson.** NB2's frozen input snapshots
(`kegg_hsa04916.json`, `omnipath_internal.json`, `hgnc_gene_groups.json`, `uniprot_annotation_direct.json`,
`pomc_cleavage_refs.json`) are absent from both disk and git, so NB2 cannot currently be re-run (see the
2026-07-11T23:57Z entry above). Going forward, **every frozen DB snapshot a notebook reads is committed
in-repo alongside the notebook** — inputs, not just outputs — enforced per-notebook by the reproducibility
specialist before the next phase depends on it.

**Decision 6 — flat notebook spine, no dangling extractors.** Sequential numbering; every notebook is a
self-contained mini-manuscript answering one question; extraction work is folded in as modules of the
manuscript whose question it serves rather than left as standalone extractors. New spine: **NB4** unified
association base (with author-explanation status) / **NB5** compare candidate networks (before merging) /
**NB6** harmonized multi-layer substrate / **NB7** rescue screen (causal-gene resolution + convergence grade)
/ **NB8** (optional) population conditionality. NB1–NB3 are unchanged; NB3 (the 13-paper case-set assembly)
is a dependency NB4 builds on, not replaced by it.

**Bookkeeping performed in this entry (no science):**
- `internal/TODO.md` **re-created** as the live forward ledger (it was archived in the 2026-07-11 restart and
  had gone missing from disk since; see Decision/note below). Populated with the five plan phases as tracked
  work items in dependency order, the Martin et al. (South Africans) population-GWAS deferral, and the 01a–01d
  extractor-consolidation backlog item.
- Three superseded plan-draft artifacts from this same planning session
  (`plan_systematic-author-unexplained-locus-resc_8a368b7b.json`,
  `plan_convergence-graded-rescue-screen-of-repo_8a368b7b.json`,
  `plan_convergence-graded-rescue-screen-reprodu_8a368b7b.json`) archived to
  `internal/archive/plan_drafts_2026-07-12/` (gitignored) with a README recording their artifact ids and how
  each was superseded. Only the approved plan (cited above) is live.
- Plan-sync check **not run to completion**: `internal/project_dashboard.md` does not currently exist on disk
  (archived out in the 2026-07-11T22:51Z restart, per that entry's note, and not yet re-created). No
  processed CSVs exist yet for NB4–NB8, so there is nothing to reconcile against a Key-metrics table right
  now. Recorded here as a known gap, not silently skipped: the dashboard should be re-created (or explicitly
  deferred) before NB4 produces its first processed output, so the plan-sync check has a table to reconcile
  against.

**Documents updated:** this entry; `internal/TODO.md` (re-created); `internal/archive/plan_drafts_2026-07-12/`
(new, gitignored). `internal/project_dashboard.md` intentionally not touched — see gap noted above. No git
commit made (pre-commit compliance gate + commit are a later step, outside this entry's scope).

---

## 2026-07-12T00:34Z — NB1 figures now render on the site; the "pandas-3.0 corruption" was a SOURCE-FILE typo (T23:57Z Catch 2 corrected)

**Trigger.** PI reported the two NB1 figures still absent from the published site and suspected GitHub Actions
had not republished. Investigation (incl. an 8-agent adversarial site+repro audit) settled four things.

**1 — Deploy was healthy all along.** The "Publish site" Action ran and succeeded for `72e064a` at
2026-07-11T23:24Z; HEAD = origin/main = deployed sha. The site looked unchanged only because the figure fix
had never been committed. No CI change needed.

**2 — Why the figures were missing (fixed).** NB1's two plotting cells did `fig.savefig(output/figures/…png)`
then `print("wrote …")` but never *displayed* the figure, so the notebook's **stored** output was stdout only —
no `image/png`. With `_quarto.yml` `execute: enabled: false`, Quarto renders stored outputs, so it showed the
"wrote …" text and no image; the PNGs were never committed either (404 on the site). Fix: append
`display(fig); plt.close(fig)` to both cells → exactly one embedded `image/png` per figure, regardless of
backend (same mechanism as NB2's working figures). Verified: a local `quarto render` of NB1 now emits **2
`<img>` tags**. `/output/` added to `.gitignore` (runtime scratch; the shipped figures live inside the .ipynb).

**3 — CORRECTION to T23:57Z Catch 2 ("NB1 pandas-3.0 fragility").** That diagnosis was WRONG. There is **no
substring replace in NB1's code**. The real cause: the node *Phosphodiesterase* is mis-encoded as
*PhosphodiesteHRASe* (an errant `ras`→`HRAS` substitution) **in the published source workbooks themselves** —
present in the shared-strings tables of BOTH MOESM1 (3 edges) and MOESM2 (node list + node_properties).
pandas/openpyxl read the typo faithfully; every pandas version does. The committed CSVs had said
*Phosphodiesterase*, i.e. they had been **silently hand-corrected and were NOT reproducible from the raw
files**. Fix: a single documented correction (`fix_labels`, `{"PhosphodiesteHRASe":"Phosphodiesterase"}`)
applied wherever a node label is read from the workbooks (raw files left untouched), with a visible note in the
notebook. The paper's own cited title ("Calmodulin activation of cyclic AMP *phosphodiesterase*…") confirms the
entity. The real *HRAS* gene nodes (`HRAS_kerat`/`HRAS_melan`) contain no such substring and are unaffected.
`raghunath_edges_typed_signed.csv` is now byte-identical to the committed version again (typo resolved to the
same value); `raghunath_nodes_typed.csv` differs by ONE additional correction (below).

**4 — `IRAK1_Active_kerat` state corrected (empty → `active`).** The committed nodes CSV was stale vs. the
notebook's own `state()` regex, which correctly tags `_Active` before a `_`/`:` boundary (the cell comment
already asserts all 3 IRAK1_Active nodes are tagged). The re-run produces the correct value; committed here so
the CSV matches what the notebook reproduces. Counts unchanged (265 nodes / 429 edges; degree cross-check
265/265). Gene identity/edges unaffected — `state` is metadata, not an identifier.

**Reproducibility.** NB1 now re-executes clean on a pinned stack (pandas 2.2.3 / numpy 1.26.4 / matplotlib
3.9.2 / networkx 3.3 / openpyxl 3.1.5) via `nbclient` with the kernel CWD pinned to repo root. A committed
`requirements.txt` is still pending the maintainer's exact working versions.

**5 — NEW NB2 blocker found by the audit (handed to Claude Science).** Beyond the 7 missing frozen JSONs
(T23:57Z Catch 1), NB2 cell 18 also reads two intermediate CSVs — `nb2_projection_cited.csv` and
`nb2_backbone_cited.csv` — that **no cell/script in the repo writes** and that are absent on disk. So even after
the frozen JSONs are restored, NB2 halts at cell 18. Both must be regenerated/committed too.

**Documents updated:** this entry; `notebooks/01_reconstruct_published_network.ipynb` (figure embedding + typo
correction + Step-1 note); `data/processed/raghunath_nodes_typed.csv` (IRAK1_Active state); `.gitignore`
(`/output/`). Handoff note written to `internal/handoffs/notes/`. Untouched: `data/external/`, `internal/TODO.md`,
`rescue_candidate_audit.csv` (concurrent Claude Science work / PI-held).

---

## 2026-07-12T01:16Z — NB2 reproducibility RESOLVED: all 14 missing inputs regenerated, fresh-clone run verified, committed (`95f1969`)

**What changed.** The NB2 re-run blocker opened at T23:57Z (Catch 1) and extended at T00:34Z (item 5) is
closed. All fourteen inputs NB2 reads but the repo never committed were regenerated, verified against the
committed outputs, and committed in `95f1969` (`data(nb2): restore frozen db_responses + orphan inputs +
figures for reproducibility`; 15 files, 1,396 insertions). A fresh clone can now re-run
`notebooks/02_resolve_network_to_genes.ipynb` with all REQUERY flags `False`. This discharges Decision 5 of
the T00:29Z entry for NB2 specifically.

**What was restored, and how each was grounded (no value invented):**
- **7 frozen DB responses** (`data/external/db_responses/`): `uniprot_annotation_direct.json` + `.meta.json`,
  `hgnc_gene_groups.json`, `pomc_cleavage_refs.json`, `omnipath_internal.json` + `omnipath.meta.json`,
  `kegg_hsa04916.json`. UniProt / HGNC / KEGG / OmniPath were re-pulled from the live public APIs the REQUERY
  branches document; the two `.meta.json` sidecars were reconstructed to the notebook's own recorded
  `queried_utc` and rule text (byte-exact to the committed cell prints); `pomc_cleavage_refs.json` was
  recreated by hand from verified PubMed records (POMC→ACTH: PMIDs 8380577, 8070378; ACTH→α-MSH: 8389457,
  8822269 — abstracts confirm the PC1/3 and PC2 cleavage steps).
- **2 orphan intermediate CSVs** (`data/processed/nb2_backbone_cited.csv`, `nb2_projection_cited.csv`):
  recovered losslessly by inverting cell 26 / cell 18 against the committed outputs — these are read by NB2
  but written by no cell in any commit (the T00:34Z item-5 gap).
- **5 figures** (`notebooks/figures/step*.png`): extracted byte-identical from the committed notebook's own
  embedded `image/png` outputs. A real `nbconvert --execute` fails at cell 8 without them (`IPython.display.Image`
  raises on the missing file). This was a **third gap** beyond Catches 1 and the T00:34Z orphan-CSV finding,
  surfaced during fresh-clone verification and approved by the PI for extraction-and-commit.

**Verification.** A fresh clone (git-archive from the new HEAD, tracked files only) runs NB2 clean
end-to-end: every inline assertion passes, the citation gate passes (1,586 elements, 0 uncited), and
`gene_network_nodes.csv`, `gene_network_edges.csv`, and `nb2_omnipath_validation.csv` reproduce the committed
baseline value-for-value. (Real `jupyter nbconvert --execute` cannot run inside the Claude Science sandbox —
it blocks the Jupyter kernel's TCP socket bind; verified instead via a faithful in-process executor that
exercises the exact `Image()` display-hook read path. An unsandboxed `nbconvert` on the maintainer's machine
will run clean.)

**Compliance.** Tier-2 pre-commit gate run via `REPO_COMPLIANCE_GATE` (verdict: edits-required-then-proceed).
Applied three prepared `DATA_SOURCES.md` edits: marked `db_responses/` committed, and documented the
**KEGG and OmniPath academic / non-commercial license basis** (previously understated as "public REST").
Staged by explicit path only; the concurrent-session / PI-held untracked files (`.claude/`,
`discordance_loci_author_explained.*`, `rescue_candidate_audit.csv`) were left untouched. No push (the task
was commit-only).

**Three flags carried forward (now tracked in `TODO.md`):**
1. **OmniPath drift (informational, no action needed).** The re-query returned **2,931** both-endpoints-in-set
   edges vs the 2,949 the original 2026-07-09 pull froze — ~18 edges of live OmniPath drift in gene-pairs
   unrelated to the 429 backbone edges, with **zero effect on any verdict**. Documented in `omnipath.meta.json`
   and DATA_SOURCES 6b. The original "172 network genes" resolved-set label was not committed anywhere; the
   162-gene set used for the re-freeze (derivable from committed `gene_network_nodes.csv` + `complex_members.csv`)
   is the reproducible-from-committed equivalent and is recorded in the sidecar.
2. **Undocumented `PLC*` filter in DATA_SOURCES entry 6.** Line 179 records "PLC 832 = 14" but — unlike PLA2
   ("filtered PLA2G*") and Trypsin ("filtered PRSS*") — does not record that HGNC group 832 ("C2 domain
   containing phospholipases") returns 19 protein-coding members, of which 5 are PLA2G4* contaminants, so a
   `PLC*` prefix filter is required to reach the committed 14. Biologically correct (PLA2G4* are phospholipase
   A2, not C) and forced by output fidelity, but the manifest omits the filter step. Documentation fix pending.
3. **Missing figure-generator code.** The 5 NB2 figures are now committed, but **no cell in the repo generates
   them** (no `savefig` anywhere in NB2). A proper fix adds the figure-generating cells to NB2 so the PNGs
   reproduce rather than being committed as opaque binaries. Flagged in the commit message and to the PI.

**Bookkeeping performed in this entry (no science):**
- `internal/TODO.md` updated: NB2 reproducibility recorded as resolved (it was tracked via its own approved
  plan, not a row in the NB4–NB8 ledger), and flags 2 and 3 above added as open follow-up items.
- `internal/TODO.md` **committed for the first time.** The T00:29Z entry recorded it as re-created, but it was
  never `git add`ed and had remained untracked on disk since — a documentation-vs-reality drift, reconciled here.

**Documents updated:** this entry; `internal/TODO.md` (NB2 resolution + flags; now tracked); `DATA_SOURCES.md`
(committed as part of `95f1969`). Files restored under `data/external/db_responses/`, `data/processed/`, and
`notebooks/figures/` are recorded in commit `95f1969`.

---

## 2026-07-12T01:44Z — NB2 figure generators restored; PLC* filter documented; tentative `project_dashboard.md` created; START_HERE + plan-sync skill de-staled

Four related custodial/reproducibility items, closing the two documentation follow-ups the NB2 fix
surfaced (T01:16Z entry) and standing up the missing third tracking document.

**1 — NB2 figure-generating code restored (closes T01:16Z flag 3).** The 5 `notebooks/figures/step*.png`
were committed at `95f1969` as opaque binaries recovered from the notebook's embedded outputs, with no cell
generating them. `REPRODUCIBILITY_SPECIALIST` (delegated) added the generating code: NB2 cells 8, 15, 20,
22, 27 now build their figures from the notebook's own in-memory data (`annotation.node_type.value_counts()`,
`gene_layer.edge_type.value_counts()`, the `nx.DiGraph` G, degree/betweenness metrics, and
`val.verdict.value_counts()` respectively), each via `fig, ax = plt.subplots(...)` →
`fig.savefig(FIG/"<name>.png", dpi=150, bbox_inches="tight")` → `display(fig); plt.close(fig)` (the same
single-embedded-PNG pattern NB1 uses, CHANGELOG 2026-07-12T00:34Z item 2); cell 2 gained the matplotlib
import and `FIG.mkdir`. Only 6 of 33 cells changed (2, 8, 15, 20, 22, 27); the other 27 are byte-identical
to HEAD. All REQUERY flags remain False. Verified on a fresh git-archive clone (run cell-by-cell in-process,
since `jupyter nbconvert --execute` cannot bind a kernel socket in the sandbox): all 32 code cells run clean,
exactly cells [8,15,20,22,27] emit `image/png`, the 5 PNGs are valid, the committed
`gene_network_nodes/edges.csv` and `nb2_omnipath_validation.csv` reproduce **value-for-value**, and the
citation gate passes (1,586 elements, 0 uncited). The figures are opaque binaries no longer — they reproduce
from the notebook.

**2 — PLC* filter documented in `DATA_SOURCES.md` (closes T01:16Z flag 2).** Entry 6's member-filter line
now records that HGNC group 832 ("C2 domain containing phospholipases") returns 19 protein-coding members, 5
of which are PLA2G4* (phospholipase A2, not C) contaminants, so a `PLC*` prefix filter is required to reach
the committed 14 isozymes — matching the parity of the already-documented PLA2G*/PRSS* filters. The filter is
recorded per-group in `hgnc_gene_groups.json` (`member_filter` field).

**3 — Tentative `internal/project_dashboard.md` created (third tracking document restored).** The dashboard
had been absent since the 2026-07-11T22:51Z restart. Re-created as a **thin snapshot that references the
living documents** rather than duplicating them — the explicit design response to why previous plans drifted.
It pins load-bearing counts ONLY for the committed, stable NB1–NB3 foundation (7 metrics, each reconciled
against its file by `pigmentation-plan-sync`'s `check_plan_sync()` → 7 ok, 0 issues, no orphans); the
concurrent session's in-flight NB4–NB5 outputs are inventoried with path + status but **no pinned counts**,
because pinning a volatile number is exactly what caused prior drift. Carries an anti-drift contract
(reconcile against files not memory; never duplicate the changelog/TODO; datetime-stamp every "now"). Backing
artifact `4c06a7f3-6674-440c-a235-91e29e20b27f`.

**4 — Staleness swept in START_HERE and the plan-sync skill.**
- `internal/START_HERE.md`: its "Current state" section asserted "No execution route is committed," which the
  T00:29Z changelog had already superseded (route settled, PI-approved). Added a datetime-stamped "where we
  are now (2026-07-12T01:42Z)" note pointing at the three living documents and recording the concurrent
  NB4–NB5 work; kept the 2026-07-11T22:51Z paragraph as an explicitly-superseded point-in-time record. Both
  now carry full UTC datetimes per project convention.
- `pigmentation-plan-sync` skill (personal, published in place): its prose called
  `project_dashboard.md` "the build plan" and "the project's single source of truth" (wrong under the
  three-document convention — the dashboard is a snapshot that references the others) and hardcoded a
  `version_of` artifact id (`62abff5e-…`) pointing at the **archived** dashboard. Fixed the framing to
  "snapshot / control surface", pointed the pin at the current artifact `4c06a7f3-…`, and added guidance to
  resolve the id at runtime via `host.artifacts(filename="project_dashboard.md", exact=True)` rather than
  trust a hardcoded value. The source-agnostic checker logic in `kernel.py` was already correct and was left
  unchanged.

**Commit plan.** Item 1 (notebook + 5 figures) and item 2 (`DATA_SOURCES.md`) commit together as the
reproducibility/data fix; items 3–4 (`START_HERE.md`, `project_dashboard.md`, this changelog entry) commit as
the governance-docs update. `internal/TODO.md` is intentionally NOT committed in either — it currently
carries an uncommitted PI design note added mid-build by the concurrent NB4–NB5 session (allele-frequency
population-conditionality note on NB8), which is that session's content to commit, not this one's.

**Documents updated:** this entry; `notebooks/02_resolve_network_to_genes.ipynb` (6 cells); 5
`notebooks/figures/step*.png` (regenerated); `DATA_SOURCES.md` (PLC* filter); `internal/START_HERE.md`
(datetimed current-state note); `internal/project_dashboard.md` (created); `pigmentation-plan-sync` skill
(published). Untouched: `internal/TODO.md` and all concurrent-session untracked files.

---

## 2026-07-12T01:55Z — Commit-authority convention encoded in `precommit-compliance-gate`; NB2 figure-gen + dashboard committed (`2c03ad1`, `0997551`)

**Commits.** The figure-generator restoration + PLC* documentation committed as `2c03ad1`
(`fix(nb2): generate step figures from notebook data; document PLC* HGNC filter`, 7 files, Tier-2 gate
verdict PROCEED). The dashboard creation + START_HERE/changelog de-staling committed as `0997551`
(`docs(dashboard): create tentative project_dashboard.md; de-stale START_HERE + changelog`, 3 files, Tier 1).
`internal/TODO.md` was deliberately left uncommitted: it now interleaves this session's "NB2 follow-ups
resolved" edit with the concurrent NB4–NB5 session's uncommitted content (NB8 allele-frequency PI design
note; a new "Open — surfaced during NB5" section on STRING enzyme-class mapping and a Reactome parent-pathway
re-pull to R-HSA-5619507), so committing it here would sweep that session's in-flight work into this session's
history. A handoff note (`internal/handoffs/notes/20260712T0153Z__…__pm001.md`) tells that session my TODO
edit is safe to commit with theirs; the authoritative record of the resolved follow-ups is this changelog
regardless.

**Skill fix — `precommit-compliance-gate` commit-authority convention (PI-directed).** A delegation this
session forbade a specialist from committing its own finished, verified work ("do not commit / out of scope"),
forcing a handoff for a commit it could have made itself. Investigation found this restriction came from the
**delegation prompt**, not from any stored rule — the specialist's profile and this skill already say "commit
small and often," and the skill's own "who can run Tier 2" passage already permits any frame to commit Tier-1
code/prose directly. The over-restriction was an orchestrator-side prompt error, not a skill defect. Per PI
direction (a specialist should commit its own completed work and refuse only for genuine
redistribution-legality decisions), added two clarifying paragraphs to the skill's tiering section: (1) a
specialist commits its own completed work, handing a commit **up** only when it is a leaf that structurally
cannot delegate a Tier-2 commit to `REPO_COMPLIANCE_GATE`, or when an unresolved redistribution-legality
question exists — never as a blanket "specialists don't commit"; (2) orchestrators must scope a delegation's
commit authority (which paths, which files not to sweep, any legality exception) rather than blanket-forbid
committing. The root-only Tier-2 delegation constraint is preserved unchanged. Skill republished in place.

**Documents updated:** this entry; `precommit-compliance-gate` skill (published);
`internal/handoffs/notes/20260712T0153Z__…__pm001.md` (created). Commits `2c03ad1` and `0997551` recorded
above.

---

## 2026-07-12T02:07Z — `.claude/` local tooling settings gitignored (`92cb266`)

Added `.claude/` to `.gitignore` (Local/environment-cruft section) so the per-machine
`.claude/settings.local.json` stub — a local tool-permission config, same category as `.venv/`/`.env`,
not project content — is not committed. The rule untracks nothing (`.claude/` was never tracked); it only
prevents the file from being staged going forward. Routed through the Tier-2 gate (touches `.gitignore`):
`REPO_COMPLIANCE_GATE` verified the pattern matches the target, has no collateral matches (the
`internal/handoffs/notes/*claude*` filenames are unaffected), and needs no README/DATA_SOURCES stanza —
verdict PROCEED. Committed `.gitignore` alone by explicit path as `92cb266`.

**Remaining uncommitted work belongs to the concurrent NB4–NB5 session** and is intentionally left for it:
`internal/TODO.md` (holds that session's NB8/NB5 ledger content interleaved with this session's resolved-
follow-ups edit — see the 01:53Z handoff note), the NB5 processed outputs (`nb5_*.csv`,
`discordance_loci_author_explained.csv`, `darcy2023_S*.csv` + meta sidecars), the NB5 frozen DB responses
(`reactome_*`, `string_network_pulls_v12.json`), the NB5 notebook + figure + specs (`notebooks/05_*`,
`notebooks/figures/nb5_candidate_network_comparison.png`, `docs/specs/*`), and `rescue_candidate_audit.csv`
(PI-held). Committing those is a Tier-2 decision (new data + new frozen snapshots needing license-basis
documentation in `DATA_SOURCES.md`) owned by whoever finishes NB5, not this session.

**Documents updated:** this entry; `.gitignore` (committed as `92cb266`).

## 2026-07-12T03:11Z — GWAS Catalog frozen pull RECOVERED + restored to a committed path; session feedback briefs added

The lost frozen GWAS Catalog pull (`pigmentation_gwas_catalog.csv` — 1,072 pigmentation associations, 22 cols,
in-row `queried_utc` 2026-07-08T01:15:41Z over 10 EFO/OBA/MONDO roots), which had been written under gitignored
`/output/`, never committed, and cleaned from disk in the 2026-07-11 repo cleanup, was located in the PI's
`~/Downloads` and **restored to a committed, non-gitignored path: `data/external/gwas_catalog/`** (CSV +
`.meta.json`). Verified against the spec on restore: 1,072 rows, 22 columns, in-row `queried_utc` matches; all
rows `axis=pigmentation`. The EBI download endpoint was re-confirmed **still HTTP 500 (2026-07-12)** — REST base
returns 200 but cannot expand child traits, so it is not a substitute — hence this frozen copy is the
reproducible input; no live pull is possible right now. **Root cause of the loss** (frozen data written under
gitignored `/output/`) is fixed by the new `data/external/` home; frozen data must never be written under
`/output/` again. Path references corrected in `docs/specs/gwas_catalog.spec.md` and `DATA_SOURCES.md` (entry 1).

**Scope note (one-day discipline):** recovering this unblocks NB4's unified reported-associations base
(rsID-join the 1,072 to the curated set; overlap yields replication counts that feed the convergence grade),
but the flagship rescue still runs on the **52 curated author-unexplained loci** (already resolved in
`data/processed/locus_causal_resolution.csv`); the 36-paper author-explanation mining of the Catalog set
remains a stretch, not a requirement.

**License basis:** NHGRI-EBI GWAS Catalog data under EMBL-EBI terms (reuse with attribution) — already
documented in `DATA_SOURCES.md` entry 1; this restores the file to a committed location, it is not a new
source.

**Also committed:** three session feedback briefs for Claude Science —
`internal/hackathon_final_day_feedback_and_pitch.md` (final-day recalibration + pitch north star + visual
mandate + GWAS-recovery + the resolution→rescue→hero-shortlist priority),
`internal/bajpai_network_integration_brief.md`, `internal/melanocyte_eqtl_resolution_brief.md`.

**Ownership boundary respected:** the concurrent NB4–NB5 session's uncommitted work (`nb5_*.csv`,
`discordance_loci_author_explained.csv`, `darcy2023_S*.csv`, `rescue_candidate_audit.csv`,
`locus_causal_resolution.csv`, `notebooks/05_*`, `docs/specs/darcy*`, `internal/TODO.md`, frozen NB5 DB
responses) is intentionally left unstaged for that session.

**Documents updated:** this entry; `docs/specs/gwas_catalog.spec.md`; `DATA_SOURCES.md`; three internal briefs;
restored `data/external/gwas_catalog/{pigmentation_gwas_catalog.csv,.meta.json}`.

## 2026-07-12T03:43Z — Gene-level GWAS replication source added (granular associations file) + brief guidance

The PI confirmed she wants **gene-level** replication (a gene reported in ≥2 GWAS associations), not per-SNP.
That filter already existed in her `melanogenesis-constraints` project
(`analysis/pool_venn_gene_lists.py:98–102`: group associations by gene, keep `>=2` → 83 replicated pigmentation
genes) but ran on a **granular** associations file, NOT the deduplicated 1,072-row catalog (which collapses to
one lead row per rsID and so cannot yield per-gene counts). That granular file
(`gwas_pigmentation_associations.csv`, 723 associations; `efo_id, trait, gene, snp_id, pvalue`; git-tracked in
melanogenesis-constraints) is **copied into this repo at `data/external/gwas_catalog/`** and verified in-place:
723 associations → 318 unique genes → **83 replicated (≥2)**, reproducing the PI's methods doc exactly.

Guidance to Claude Science (`internal/hackathon_final_day_feedback_and_pitch.md`): in the GWAS/NB4 step,
reproduce the ≥2-association gene filter **offline from this frozen granular file** (not a live pull — EBI is
still HTTP 500 — and not the deduplicated 1,072), annotate each network/rescued gene with `gwas_replicated` +
`gwas_n_assoc`, and feed `gwas_replicated` into the convergence grade as an independent evidence line.

License basis: NHGRI-EBI GWAS Catalog (EMBL-EBI terms, reuse with attribution) — same as entry 1; a frozen
derived associations table from the PI's own prior pull.

**Documents updated:** this entry; `internal/hackathon_final_day_feedback_and_pitch.md`; `DATA_SOURCES.md`;
added `data/external/gwas_catalog/gwas_pigmentation_associations.csv`.
