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
- **Commits follow the tiered pre-commit gate** (`precommit-compliance-gate` skill). Prose docs here
  (`.md`) are **Tier 1** — a fast local self-check, commit directly. Adding a **new** data-type file to
  `bibliography/` (`.csv`, `.ris`, `.bib`) is **Tier 2** — route that commit through `REPO_COMPLIANCE_GATE`.
  All references are DOI/PMID metadata only (no article full text), so redistribution risk is nil either way.

## Current contents

- `2026-07-11_1222_SCOPING_ideas_and_prior_art_map.md` — scoping of the project's ideas and the prior-art
  framings (A–H) to search; framing H (sex-hormone × primate expansion) is deferred per `TODO.md` (c) D4.
- `2026-07-11_1308_PRIORART_MAP_cross_field.md` — the cross-field prior-art map: 17 connector-verified close
  works across framings A–G, each tagged Overlaps / Adjacent / Background against the project's claim.
- `2026-07-11_1308_NOVELTY_RISK_top_claims.md` — novelty-risk memo on the top-4 exposed claims (does each
  survive its closest prior art, and on what distinction).
- `bibliography/2026-07-11_priorart_refs.csv` / `.ris` — the 17 verified references, machine-readable.
