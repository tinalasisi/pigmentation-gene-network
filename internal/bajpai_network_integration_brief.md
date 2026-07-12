# Brief for Claude Science — integrate Bajpai 2023 into the candidate-network comparison

**From:** T. Lasisi (PI) · **Date:** 2026-07-11 · **Status:** PI sign-off given (see "Why it's missing")

## Goal
Bring the **Bajpai et al. 2023 genome-wide CRISPR screen** into the candidate-network comparison
(Notebook 05) as a **node layer**, so it sits alongside Raghunath, D'Arcy/STRING, KEGG hsa04916, OmniPath,
and Baxter in the comparison — not as a fabricated edge network.

## Why it's currently missing (diagnose, don't re-litigate)
Two reasons, both real:
1. **Format.** Bajpai is a **weighted, signed node table** (169 genes, an effect size, one phenotype
   direction) — *not* a gene–gene edge list like the other sources. It does not auto-slot into an
   edge-centric comparison, so it was skipped.
2. **Deferred by design.** `docs/specs/bajpai2023.spec.md` explicitly parks it: the direction is
   "usable as an edge-sign prior toward the melanin endpoints in a **proposed downstream connection step
   (notebook placement pending PI agreement)**." **The PI has now approved bringing it in** — this brief is
   that agreement.

## What Bajpai is (authoritative — do not re-derive)
- **File:** `data/processed/bajpai2023_crispr_hits.csv` — **169 hit genes** (threshold q < 0.10, reproduces
  the paper's 169). Spec: `docs/specs/bajpai2023.spec.md`.
- **Columns of interest:** `GeneID` (Ensembl), `Symbol`, `Combined_casTLE_Effect` (magnitude of pigmentation
  change on perturbation), `Combined_casTLE_Score`, `q_value`, `direction_note`.
- **Direction is uniform:** all 169 hits have **positive casTLE effect = knockout/knockdown REDUCES
  pigmentation** → they are positive effectors/regulators of melanin. This is the sign prior toward the
  melanin endpoint.
- **Identity joins directly** to the network gene layer (Ensembl + HGNC), no remapping needed.
- **Sanity anchors:** positive controls recovered = TYR, DCT, SLC45A2, OCA2, KLF6, COMMD3. OCA2 **is** a hit;
  MC1R / HERC2 are **not** (expected — the screen finds melanogenesis *effectors*, not eye/hair-colour
  regulators). Use these to sanity-check the join.
- **Provenance:** cite Bajpai et al. 2023 (*Science* 381:eade6289; DOI 10.1126/science.ade6289). Raw Table S1
  is pinned (`data/raw/bajpai2023/`), CC BY 4.0 via PMC10901463.

## The key modeling decision — how to represent a screen as a "network"
Bajpai has **no intrinsic gene–gene edges. Do not invent any.** Use these representations:

- **PRIMARY — node-attribute / node-set layer (do this):** treat Bajpai as (i) a **node set** (the 169 hits,
  for membership/overlap) and (ii) a **node weight** (`Combined_casTLE_Effect`) with a uniform **sign**
  ("reduces pigmentation"). This is the honest form and slots straight into
  `data/processed/nb5_gene_set_membership.csv`.
- **SECONDARY — bipartite melanin-endpoint anchor (optional, separate layer):** a directed, signed star
  linking each hit → a single `pigmentation/melanin` endpoint node; edge weight = casTLE effect, sign =
  reduces-pigmentation. This is the spec's "edge-sign prior toward the melanin endpoints." Use it to
  *connect effectors to the phenotype*, **not** for topology comparison. Label it clearly as a derived
  bipartite layer.
- **DERIVED — Bajpai-induced subnetwork (only if an edge set is explicitly wanted):** induce edges by
  projecting the 169 genes onto an **existing** edge source (STRING/OmniPath/Raghunath). Label it
  "Bajpai genes, edges from <source>." **Never** present borrowed edges as an independent Bajpai network.

## Deliverables / acceptance criteria
1. **Membership comparison:** add Bajpai as a column/layer in `nb5_gene_set_membership.csv` — for each
   candidate network, which and how many of its nodes are Bajpai hits; node-set overlap (Jaccard) with each
   network; enrichment (are Bajpai hits over-represented in network X vs. background?).
2. **Node-weight overlay:** attach `Combined_casTLE_Effect` (and the sign) as a node attribute on the
   candidate/merged networks, usable downstream.
3. **Reverse coverage:** of the 169 Bajpai hits, how many appear in each candidate network, and how many are
   **orphan hits** absent from all networks (candidate new effector nodes worth flagging).
4. **Optional:** the bipartite melanin-endpoint layer as a clearly-labeled separate artifact.
5. **Docs:** update `DATA_SOURCES.md`, `internal/project_dashboard.md`, and `internal/CHANGELOG.md` to record
   Bajpai's inclusion, the representation decision, and that PI sign-off was given. Preserve citation/license.

## Guardrails (do NOT)
- Do **not** fabricate gene–gene edges from the screen, or treat casTLE effect as regulatory-edge strength.
- Do **not** present Bajpai as topologically comparable to the edge networks — it has no intrinsic topology.
- Keep it as **node membership + weight + phenotype sign**. The screen answers "which genes causally matter
  for melanin," not "who regulates whom."

## Why this matters (one line)
Bajpai is an **unbiased, experimental causal-importance weight on the nodes** (no literature study-bias) —
the right layer for validating and weighting downstream population-differentiation analyses and for checking
whether the candidate networks' structure aligns with the genes that causally build melanin.
