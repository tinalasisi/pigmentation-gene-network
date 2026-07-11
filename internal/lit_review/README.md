# `internal/lit_review/` — literature-review working area

Working area for the **Genetics Literature Reviewer** specialist: landscape surveys, prior-art maps, and
novelty-risk memos for the pigmentation gene-network project.

This folder is **tracked and public** (only `internal/untracked/` and `internal/archive/` are gitignored; see
`internal/project_dashboard.md` §6 and the top-level `.gitignore`). It is a working channel, **not** one of
the three living governance documents — it references `project_dashboard.md` / `TODO.md` / `CHANGELOG.md` and
is referenced by them, but never absorbs or duplicates them.

## Naming convention

Datetime-sortable prefix, matching `internal/deconvolutor/`:

```
{YYYY-MM-DD}_{HHMM}_{TYPE}_{descriptive_name}.md
```

Use the datetime the document was written (24-hour clock). Do not renumber or rewrite existing files; add a
new dated file.

## Document types

| TYPE | What it is |
|---|---|
| `SCOPING_` | Reads the project's own record and translates its ideas into the search framings to run. No retrieved literature — orientation only. |
| `PRIORART_MAP_` | The "how this idea appears across fields" table: one row per genuinely-close prior work, with a resolvable DOI/PMID, the field it comes from, and how close it sits to the project's claim. |
| `NOVELTY_RISK_` | Memo on a specific exposed claim: the closest prior art found, under which name, and whether the project's framing survives it and on what distinction. |

## `bibliography/`

Machine-readable reference exports (`.ris` / `.bib` / `.csv`) so citations are reusable downstream, not
locked in prose. Every entry carries a resolvable DOI or PMID.

## Standing rules for anything written here

- **Never cite a paper not retrieved through a connector.** Every reference carries a resolvable DOI/PMID from
  an actual connector result — not a recalled citation.
- **DOI/PMID only, no copyrighted full text.** This folder is public; do not paste article full text or
  withheld supplements. Cite by identifier, following the repo's redistribution policy (`DATA_SOURCES.md`).
- **Commits go through `REPO_COMPLIANCE_GATE`.** Files are written and organized here; the actual commit is
  gated separately (see the `precommit-compliance-gate` skill).

## Current contents

- `2026-07-11_1222_SCOPING_ideas_and_prior_art_map.md` — scoping of the project's ideas and the prior-art
  framings (A–H) to search; framing H (sex-hormone × primate expansion) is deferred per `TODO.md` (c) D4.
