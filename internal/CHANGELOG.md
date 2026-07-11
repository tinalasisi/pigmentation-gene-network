# Changelog — Pigmentation gene-network build

Append-only history of build and decision events for this project. Each entry is dated and records what
changed and why; entries are never rewritten. This file is one of three tracking documents (with `TODO.md`
and `project_dashboard.md`); see `START_HERE.md` for the convention. All three live in `internal/`, which is
tracked (committed to the public repo) so their cross-references resolve on GitHub — the escape hatch
`internal/untracked/` holds anything deliberately kept private.

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
