# Brief for Claude Science — add melanocyte-specific eQTLs to the NB7 resolution/rescue layer

**From:** T. Lasisi (PI) · **Date:** 2026-07-11 · **Scope discipline:** this is an **upgrade to an existing
layer (NB7), NOT a new network.** Keep it lean.

## Goal
Add **melanocyte-specific cis-eQTLs (Zhang et al. 2018, *Genome Research*, Brown lab / NCI)** as a
**tissue-matched source in the eQTL resolution layer you already run** (NB7: L2G / eQTL / LD → causal-gene
resolution → rescue). This is *not* a gene–gene network and must not be built as one.

## Why (the payoff)
- Your current eQTL evidence comes from **bulk / wrong-tissue** datasets — the eQTL Catalogue queries on
  record are **GTEx skin sun-exposed (QTD000316)** and **TwinsUK (QTD000544)** (see
  `internal/TRACEABILITY_coverage_and_resolution_logic.md`). Bulk skin is keratinocyte-dominated; the
  melanocyte regulatory signal is diluted.
- **Zhang 2018 is purified primary melanocytes** — the correct cell type for pigmentation. It resolves
  pigmentation-associated SNPs to the gene they actually regulate *in melanocytes*, which is far more
  defensible for the rescue chain: **stranded SNP →(melanocyte cis-eQTL)→ eGene →(in melanogenesis
  network)→ endpoint.**
- It also helps fix a **known problem**: `internal/handoffs/HANDOFF_CRITICAL_limitations_and_framing_issues.md`
  (item **D2**) flags that "eQTL evidence is used inconsistently" (e.g. IRF4's top eQTL points to EXOC2). A
  canonical, cell-type-correct default source gives a principled tie-break.

## What it is (verify before citing)
- **SNP → gene cis-eQTL map** from ~**106** primary human melanocyte cultures (**confirm exact n, year, and
  PMID** — cited from memory as Zhang T. et al., *Genome Research* 2018, "Cell-type-specific eQTL of primary
  melanocytes…"). Use the **human-genetics MCP connector** to verify identity/version.
- It is **cis-heavy** → almost no trans power → **do not expect gene–gene edges.** It is a resolution layer.

## How (concrete, in order)
1. **First check the eQTL Catalogue** (the connector you already use, addressed by `QTD…` dataset IDs) for a
   **melanocyte** dataset. If present, adding it is just **one more dataset ID in the existing resolution
   query set**, alongside GTEx skin QTD000316 — near-zero new machinery.
2. **If it is NOT in the Catalogue** (melanocyte is niche — likely absent), ingest **Zhang 2018 supplementary
   tables** (significant eGene–SNP pairs) as a pinned source in `DATA_SOURCES.md` + a `docs/specs/` spec.
   Full summary stats from dbGaP only if genuinely needed (dbGaP access = heavier; avoid unless required).
3. It slots into the existing **`eQTL_target`** resolution basis (`scripts/validate_locus_tables.py` VOCAB)
   and the **NB7** rescue screen. No new representation.

## Deliverables / acceptance criteria
1. Melanocyte eQTL added as a resolution source with provenance (spec + `DATA_SOURCES.md` entry + citation).
2. Re-run locus→gene resolution on the rescue set; for each rescued locus, record the **eQTL basis** and the
   **source dataset** (melanocyte vs GTEx-skin vs TwinsUK).
3. **Flag any locus whose call CHANGES** with melanocyte vs bulk-skin eQTL — a locus that only resolves (or
   resolves *differently*) in melanocytes is itself a finding worth its own line.
4. Update the D2 note: state the eQTL basis + tissue per positive call; melanocyte is the preferred default
   where available.

## Guardrails (do NOT)
- Do **not** build a gene–gene network from it (cis-heavy — it has no topology).
- Do **not** use it to claim **population-differential** regulation. The melanocyte cultures are
  overwhelmingly **European ancestry** → it gives the **canonical reference** regulatory route, not
  cross-population variation. For the portability/discordance angle it is the *reference*, not the contrast.
- Keep it inside the resolution/rescue layer; it is not a peer to Raghunath / D'Arcy-STRING / KEGG / OmniPath.

## One-line framing
Melanocyte eQTLs make your rescue calls **cell-type-correct** — the right tissue for "which gene does this
pigmentation SNP act through" — without adding a new network or new scope.
