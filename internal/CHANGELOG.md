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
