# START HERE — cold-start brief for the sex-hormone × pigmentation expansion

**If you are a new session picking this project up, read this file first, then stop and confirm with the PI
before building anything.** This is an orientation document, not a build authorization.

---

## What this project is

There is an existing, completed pigmentation gene-network build in this repository (the Raghunath-backbone
network reconstructed in NB1, resolved to genes in NB2, with a downstream notebook chain). That work is the
substrate. It is not what you are here to change.

The **new** work is a forward expansion: coupling the pigmentation network to a sex-hormone (steroidogenesis +
androgen/estrogen receptor) layer, to ask when hormonal modulation produces **sexual dichromatism across
primates**. The full design for that expansion lives in one file:

- **`internal/EXPANSION_PLAN_sex_pigment_primate.md`** — the single live planning document. Read it in full.

## Where things stand — and what you must NOT assume

- The expansion plan is **TENTATIVE**. Its §6 Decision Log has six questions (A–F) that are **still
  unanswered** by the PI. Until those are answered, there is no agreed scope and no build authorization.
- **This is a fresh start. No artifact IDs, version hashes, or store references carry over.** Earlier drafts
  of these documents cited specific artifact/version identifiers; those have been removed on purpose because
  they will not resolve in a new project. Any number quoted from the prior build (node/edge counts, etc.) is
  provenance context only — **re-derive it from the actual source files before relying on it**, never trust a
  quoted figure as current.
- Two long-form background memos are referenced by name (`sex_hormone_network_scoping.md`,
  `sex_pigment_primate_integration_strategy.md`). They are background, not required reading to orient — and they
  are not in this folder. Do not go hunting for them or block on them; the expansion plan is self-contained.

## The document convention this project uses

All governance documents live in **`internal/`**, which is tracked and committed to the public repo (so their
cross-references resolve on GitHub). Project state is tracked in **three distinct documents** — keep them
distinct, do not let one absorb another:

- **`internal/CHANGELOG.md`** — singular, append-only history: one dated entry per meaningful build or
  decision event. This is the record of *what changed and why*. Entering a track into the changelog is what
  makes it real — not the plan file existing.
- **`internal/TODO.md`** — the forward ledger of open work items. Answers *what is left to do*.
- **`internal/project_dashboard.md`** — the snapshot / control surface: current grounded state and canonical
  pointers. It **references** the changelog and the TODO; it does not duplicate them or double as a history.

### Folder layout under `internal/`

- **`internal/` (root)** — the three governance documents above, plus this `START_HERE.md`. Tracked/public.
- **`internal/deconvolutor/`** — plan-critique reports, one per critiqued track. Tracked/public. Filenames
  are datetime-prefixed `{YYYY-MM-DD}_{HHMM}_{NAME}.md` so the folder sorts chronologically; see its README.
- **`internal/untracked/`** — gitignored escape hatch. Move a file here to drop it from the public repo
  (declutter) without deleting it.
- **`internal/archive/`** — gitignored. Retired working docs, renamed with a `z_archived_` prefix.

Only `internal/untracked/` and `internal/archive/` are private; everything else under `internal/` is public.

## What to do first (do not skip)

Before writing any code, building any network layer, or acquiring any data, **confirm with the PI**:

1. **The §6 decisions.** Walk the PI through Decision Log items A–F in the expansion plan and get them answered
   in that file. Nothing downstream is well-posed until they are.
2. **The tracking setup.** Confirm which of the three documents (changelog / TODO / dashboard) already exist for
   this fresh project and which you should create, and where they live.
3. **Sequencing.** Confirm whether this expansion starts now or waits on other work (this is §6 item F).

Only after the PI has confirmed scope does the plan promote from TENTATIVE to an agreed track, recorded in the
changelog. No repository commit is made from planning documents; any commit goes through the compliance gate.
