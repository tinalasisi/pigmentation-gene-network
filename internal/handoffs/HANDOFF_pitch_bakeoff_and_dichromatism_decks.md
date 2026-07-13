# HANDOFF — Hackathon pitch bake-off + dichromatism-flagship decks (artifact-store work)

_From: Claude Science (PI_ORCHESTRATOR, frame 83c784db), 2026-07-13T14:49Z._
_To: any Claude working the hackathon-pitch or comparative-genomics dichromatism track._
_Purpose: this work lives in the Claude Science **artifact store**, NOT in the repo, so a_
_repo-based Claude cannot see it. This doc is the pointer. Artifact IDs below are stable;_
_open them in the Claude Science UI or via `host.artifact_path(<version_id>)`._

---

## Why you can't see this in the repo
Pitch decks, shared packets, and staged figures were produced as **artifacts** (the platform's
default output channel), not committed files. That is expected behavior, not a mistake — but it
means the repo has no record of them. This handoff makes them discoverable. The **analysis**
track (below, "Live coordination") is different and DOES belong in the repo.

## What was produced (two bake-off rounds)

### Round 2 (current) — sexual dichromatism as the flagship
The PI's clearest-novel-finding is the primate sexual-dichromatism selection result. Ten
independent pitch teams built sober, researcher-track HTML decks (no marketing kitsch), each
foregrounding dichromatism and using v3-certified numbers only.

- **Chosen winner — `pitch_CoupledSystemHuman.html`** (version `06040083-f7e3-4ff2-94cd-093e6add4923`).
  Frames the whole project as ONE coupled pigment-hormone network read three ways: deep time
  (primate dichromatism selection), human disease (the disorder quadrant), pharmacology (Melanotan).
  Leads with ~15 independent phenotypic origins (4 genome-tested), ~9x loss-vs-gain lability,
  module-split certified selection, MC1R non-significant (p_BH=0.144). Purple=pigment, orange=hormone.
- Nine other decks saved as artifacts (BirdVsPrimate = strongest pure-flagship alternative;
  TwoModules, FirstCladeWideTest round out the top tier).
- **`DICHR_PACKET.md`** (version `f6dd0038-2ba9-4d37-88a5-98af9365b1eb`) — the v3-certified shared
  brief all teams built from. **Use this as the numbers source of truth for any dichromatism pitch.**
  Key corrections it encodes: certified pigment module is **TFAP2A-KITLG-EDN3 (NOT KIT** — KIT is
  ns in v3, K=1.50); POMC/TYR **fail alignment QC** (aln_ref_ratio 0.68/0.65); MC1R p_BH=0.144
  (non-significant, opposite the bird single-gene model); SHBG is the one significant RELAXATION.

### Round 1 (superseded as the lead) — human disorder-architecture flagship
Ten decks foregrounding the human "empty quadrant" (no melanocyte-autonomous gene raises pigment
whole-body; the only whole-body dial is the diffusible hormone signal into cAMP->CREB->MITF).
- **`SHARED_PACKET.md`** (version `31f86c3a-749d-4f1a-9b57-dac821031f56`) — the human-side brief
  (disorder quadrant counts, NB13 GPER1 sex-hormone arm, Melanotan, MC1R rank-4/753 LoF-tolerance).
  Kept because the winner's human-disease + pharmacology panels draw on it.

### Real analysis figures staged as artifacts (publication-grade PNGs from the pipeline)
- `fig_origins.png` `fcbf477b-a2b9-488e-8ebe-2d5e30d06cd4` (235-tip origins tree, hero figure)
- `fig_certified_selection.png` `6371aa54-72ac-4df8-916d-b77f8eb7ef2d`
- `fig_two_networks.png` `f37034e9-1947-43ea-ae7c-67f7cf4058d6`
- `fig_pooling.png` `bd4230dc-4794-41db-a3d6-3016729488a1`
- `fig_tfap2a_tree.png` `18d4ae52-4fa1-4699-b1c4-db943aa19dad`
These are copies of `comparative-genomics/results/figures/` and `analysis/figures/` as of the
Jul-12 cluster push — the repo copies are authoritative; these artifacts are for deck embedding.

## LIVE COORDINATION — read before touching comparative-genomics/analysis/
As of 2026-07-13T14:45Z an **untracked** directory `comparative-genomics/analysis/module_selection/`
was being actively written (files timestamped 10:44-10:45 EDT) by a concurrent Claude session. It
contains the Opie-analog phylogenetic results (`opie_analog_results.csv`: Pagel lambda, ASR,
transition rates gain 0.0273 / loss 0.248, ~9.1x loss:gain, ARD preferred dAIC 19.79) and the
per-lineage module-balance metric (`module_balance_results.csv`, `fig_module_balance.png`) across
11 origins. **Do not edit that directory or commit its files** — it belongs to that session.

This PI frame is taking the NON-OVERLAPPING lane (per user direction): independent double-check of
those numbers from the raw `perorigin_v1/` data, plus the pieces not in module_selection/ —
refreshed core figures on the 26-dichromatic-species base, the `phytools::fitPagel` correlated-
evolution test, frozen replicable notebook(s), and a methods/results memo. Coordinate here before
duplicating.

## Data baseline note
Latest phenotype coding is **238 species / 26 dichromatic** (10 complete + 16 partial),
`comparative-genomics/config/primate_dichromatism_coding.csv`. Earlier docs saying "24 dichromatic"
predate the Jul-12 recoding. Latest selection data: `comparative-genomics/results/perorigin_v1/`
(per_origin_K.csv, branch_rates.csv), commit 4c07317.
