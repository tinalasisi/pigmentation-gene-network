# Claude Code build handoff — Locus Resolver MVP

**Purpose.** Hand the *buildable, deterministic* parts of the Locus Resolver MVP to Claude Code
(local, with browser + `quarto` CLI + git), so they can be finished and delivered back to Claude
Science for scientific review and integration. This document is self-contained: a fresh Claude
Code session with only the repo checked out should be able to execute every task below without
further context.

**Repo.** `/Users/tlasisi/GitHub/pigmentation-gene-network` (you have it locally; all paths below
are repo-relative). Branch `main`. Do NOT commit until Claude Science's REPO_COMPLIANCE_GATE has
cleared the tree (see "Return contract" at the bottom) — build on a feature branch
`feature/locus-resolver` and leave it uncommitted-to-main / unpushed.

---

## 0. What this MVP is (one paragraph)

The project models **bidirectional genotype→phenotype discordance** on a signed, directed
pigmentation gene network. Two directions, glossed everywhere (the abbreviations D1/D2 are hard to
follow, so ALWAYS spell them out in UI text and captions):
- **D1 = "genotype-present, phenotype-absent"** — the canonical causal variant is present but the
  expected pigmentation phenotype is absent (reduced penetrance; modifier nodes block the path).
- **D2 = "phenotype-present, genotype-absent"** — the phenotype appears without the canonical
  variant (an alternative gene/route reaches the same endpoint).

The MVP is an **interactive, client-side "Locus Resolver"** page (no backend, no server, no kernel)
that walks two cited worked examples and shows, for each, the distinction between a SNP's
*nearest-gene label* and its *cited functional target*, plus the D1/D2 classification of the case.
It is hosted on the project's existing Quarto → GitHub Pages static site.

## 1. The hard rule this whole MVP exists to demonstrate (do not violate it in code)

A GWAS/marker locus is a **SNP, not a gene**. The gene name attached to it is the **nearest gene by
genomic position** — an annotation convention, NOT a causal claim. The functional target may be a
different gene (regulatory variants act at a distance). Therefore, in every data file and every UI
element you build:
1. Keep the locus's identity as its **rsID**, carrying the nearest-gene label as a tagged attribute.
2. Attach a functional target **only when it has its own citation** (a PMID/DOI/eQTL dataset id in
   the `evidence_citation` field). **A row with a blank `evidence_citation` is invalid.**
3. **Never silently relabel** a locus to its functional target. The UI shows both; a toggle *adds*
   the resolved target, it never *replaces* the nearest-gene label.

This is the point of the demo. If your code ever collapses nearest-gene and causal-gene into one
label, the MVP has failed on its own thesis.

## 2. Data contract — inputs that already exist (read-only for you)

All committed to the repo. Schemas verified 2026-07-11.

| file | schema (header) | notes |
|---|---|---|
| `data/processed/gene_network_nodes.csv` | `gene,entrez,ensembl,chr,node_class,citation,citation_source` | 168 gene nodes. `node_class` ∈ {network_protein_gene, enzyme_activity_class, cleavage_precursor_gene}. This is the mechanistic backbone node table. |
| `data/processed/gene_network_edges.csv` | `source,target,sign,edge_class,via,citation,citation_source` | 309 edges. `sign` ∈ {+,−,0}. `edge_class` is always `mechanistic_projection`. **This is the ONLY table any path/graph computation may read.** |
| `data/processed/case_gene_coverage_master.csv` | `gene,entrez,ensembl,in_nb2_network,in_darcy_union,in_darcy_S1,darcy_s1_phenotype_class,coverage_tier,case_papers,case_discordance_direction,...` | 31 case genes, coverage tier + case direction per gene. |
| `data/processed/discordance_case_classification.csv` | `paper,doi,phenotype_system,discordance_direction,anchor_genotypes,mechanism_summary,n_records_extracted,extract_artifact,...` | 13 papers, pre-registered D1/D2 direction per paper — **this is the D1/D2 ground truth** (see §4 risk). |
| `data/case_records/EXTRACT_Ang2023_eLife_Kalinago.csv` | record-level | Kalinago OCA2 case: R305W (rs1800401) and NW273KV (rs797044784) variants with verbatim evidence. |
| `internal/grounding_locus_pattern.json` | JSON | Frozen dbSNP/GWAS-Catalog/eQTL-Catalogue pull for rs12913832 + the 15-gene dark-matter GWAS scan. **This is the raw material for the locus tables; no live network call needed.** |
| `internal/network_integration_and_MVP_spec.md` | prose | The full integration schema + panel/interaction spec from Track C. READ THIS — it is the design source of truth. |
| `internal/RESEARCH_SYNTHESIS_locus_resolution_mvp.md` | prose | The finding + why this MVP. |

Provenance backup (Claude Science artifact version IDs, if a file is missing from your checkout):
- gene_network coverage master: `1398722c-f2c1-4264-bfaa-0e84332ea5cd`
- grounding_locus_pattern.json: `69896463-6152-4472-8094-5d449c9f8f36`
- locus_resolution_table.csv (Track A, 24 rows): `b6ba3948-057c-4d8a-98c4-ef5189e845d7`
- network_integration_and_MVP_spec.md: `21ca2613-06e2-4450-9496-6c8940e7b37d`

## 3. Data contract — outputs YOU create (deterministic, testable)

### 3a. `data/processed/locus_nodes.csv`
One row per locus (rsID). Columns (all required except `region`):
`locus_id,chrom,position,region,nearest_gene_label,gene_label_basis,traits,source_citation`
- `gene_label_basis` ∈ {`nearest_gene_by_position`, `GWAS_catalog_mapped_gene`, `panel_convention`} — never blank.
- Populate for the two worked-example loci for the MVP: `rs12913832` (HERC2) and the two Kalinago
  variants `rs1800401` (OCA2/R305W), `rs797044784` (OCA2/NW273KV). Values come from
  `grounding_locus_pattern.json` and the Ang2023 extract — do not invent positions.

### 3b. `data/processed/locus_annotation_edges.csv`
One row per (locus → gene) annotation. Columns (ALL required):
`locus_id,gene,edge_type,evidence_type,evidence_citation,directionality,notes`
- `edge_type` ∈ EXACTLY these five (controlled vocabulary):
  `nearest_gene_link` | `regulatory_target` | `eQTL_target` | `in_LD_with` | `dark_matter_association`
- `evidence_type` ∈ {`positional`, `statistical`, `functional`}.
- `evidence_citation` — **mandatory, never blank.** A `nearest_gene_link` row cites the mapping
  source (GWAS Catalog / dbSNP); every other edge_type cites its own paper/dataset.
- `directionality` is always `locus -> gene`.
- Required rows for the two examples (citations already verified by Claude Science):
  - `rs12913832 --nearest_gene_link--> HERC2` (cite: GWAS Catalog mapped_gene)
  - `rs12913832 --regulatory_target--> OCA2` (cite: **PMID:22234890** — Visser, Kayser & Palstra
    2012, Genome Res 22:446-455, doi:10.1101/gr.128652.111; melanocyte enhancer / chromatin loop.
    THIS PMID IS VERIFIED — use it verbatim.)
  - `rs1800401 --nearest_gene_link--> OCA2` (R305W is correctly OCA2-assigned; positional == functional here)
  - `rs797044784 --nearest_gene_link--> OCA2` (NW273KV, the Kalinago novel albinism variant)

**Acceptance test for 3a/3b** (write it as `scripts/validate_locus_tables.py`, must pass):
```python
import pandas as pd
ns = pd.read_csv("data/processed/locus_nodes.csv")
es = pd.read_csv("data/processed/locus_annotation_edges.csv")
VOCAB = {"nearest_gene_link","regulatory_target","eQTL_target","in_LD_with","dark_matter_association"}
assert set(es.edge_type) <= VOCAB, f"bad edge_type: {set(es.edge_type)-VOCAB}"
assert es.evidence_citation.notna().all() and (es.evidence_citation.str.strip()!="").all(), "blank citation"
assert ns.gene_label_basis.notna().all(), "blank gene_label_basis"
# the walled-off invariant: no locus row may leak into the mechanistic backbone
be = pd.read_csv("data/processed/gene_network_edges.csv")
assert "locus_id" not in be.columns, "backbone contaminated"
assert set(ns.locus_id) & set(be.source.astype(str)) == set(), "rsID appears as backbone source"
print("locus tables valid:", len(ns), "loci,", len(es), "annotation edges")
```

### 3c. `docs/data/locus_resolver_manifest.json` (the frozen export the page reads)
A single JSON the static page loads at runtime (no live calls). Generate it once with
`scripts/build_resolver_manifest.py` from the CSVs above + the backbone subgraph + the case text.
Structure (one object per worked example):
```json
{
  "examples": [
    {
      "id": "herc2_oca2_eye",
      "title": "rs12913832: HERC2-labelled, OCA2-regulating (eye colour)",
      "locus": { "...from locus_nodes.csv..." },
      "annotation_edges": [ "...from locus_annotation_edges.csv for this locus..." ],
      "subgraph": { "nodes": [...], "edges": [...] },   // OCA2 + its 1-hop backbone neighbourhood
      "direction": { "label": "mixed", "gloss": "D1 (genotype-present/phenotype-absent) AND D2 (phenotype-present/genotype-absent) both catalogued", "source": "case_gene_coverage_master.csv + discordance_case_classification.csv", "citation": "..." },
      "case_text": "verbatim evidence + page/table ref from EXTRACT/classification"
    },
    { "id": "kalinago_oca2", "...": "..." }
  ]
}
```

## 4. MATERIAL RISK — read before building the "D1/D2 computed from network" panel

**OCA2 is a near-leaf in the current network: it has exactly ONE edge, `MITF → OCA2 (+)`
(cited PMID:22234890). It has no outgoing edge to any pigment endpoint node.** Consequently:

- **You CANNOT compute D1/D2 by graph traversal (path-to-endpoint) for these two examples.** There
  is no downstream path from OCA2 to traverse, and the network has no explicit "pigment endpoint"
  sink node.
- **Do this instead:** take the D1/D2 label from `discordance_case_classification.csv` /
  `case_gene_coverage_master.csv` (the pre-registered, cited case direction) and present it as a
  *sourced* readout ("direction: mixed — source: case classification, papers X/Y"), NOT as a
  computed graph result. The network panel *displays* the OCA2 neighbourhood subgraph (MITF→OCA2 and
  MITF's own edges) as mechanistic context; it does not claim to have *derived* the direction.
- Label this honestly in the UI: the direction is *curated from the case literature*, and the
  subgraph is *the mechanistic context the network provides* — which for OCA2 is currently thin
  (one regulator). That thinness is itself an honest finding, not a bug to hide.

If you want a graph-*computed* element, the defensible one is: "is the resolved target present in the
168-gene backbone? yes/no, and what are its curated edges?" — a membership + neighbourhood query,
which IS computable and true. Do that; do not fake a path computation.

## 5. Front-end spec (the part Claude Code is best at)

Build a **single static HTML/JS page** at `locus_resolver.qmd` (Quarto passes raw HTML/JS through) or
a plain `docs/locus_resolver.html` embedded via an iframe — your call, whichever renders cleanly
under `execute: enabled: false`. No build step, no bundler; load the graph library from a CDN.

Three panels (full spec in `internal/network_integration_and_MVP_spec.md` §2.5):
1. **Locus card (left):** rsID, chrom:pos, trait list, and a toggle *"Show nearest-gene label only"*
   vs *"Show resolved target"* that adds/removes the `regulatory_target` edge in the graph.
2. **Network view (center):** the subgraph from the manifest, rendered with **Cytoscape.js** or
   **vis-network** (CDN). Visual separation is MANDATORY and is the thesis made visible:
   - gene nodes = **circles**; locus nodes = **diamonds**.
   - mechanistic edges = **solid, coloured by sign** (+ / − / 0); locus annotation edges = **dashed,
     gray, unsigned**.
   - Legend text: *"Dashed gray = locus annotation (positional or statistical), not a curated
     mechanistic edge."*
   - Click a node/edge → its citation opens in the evidence panel.
3. **Evidence panel (right):** for the selected element, the exact `evidence_citation` (as a
   clickable DOI/PubMed link), the `evidence_type`, and for the case, the verbatim quote + page/table
   ref from the manifest's `case_text`.

Plus a **case selector** (2-item switch between the two examples) and a **direction readout** that
shows the sourced D1/D2 label with its full gloss (per §4 — sourced, not computed).

**Palette:** colorblind-safe. Reuse the project's Okabe-Ito set already used in the coverage figure
(`#0072B2` blue, `#E69F00` orange, `#CC79A7` pink; sign colours: choose from Okabe-Ito, not red/green).
Provide alt-text for the graph.

**Do NOT hardcode any citation, position, direction, or gene name into the JS.** Every displayed
value must come from `locus_resolver_manifest.json`. This is checkable and is a review-gate criterion.

## 6. Site integration + the render/deploy step (the part the sandbox CANNOT do)

Claude Science's sandbox **cannot run `quarto render`** (it blocks the CPU-arch probe and socket
bind) and **cannot execute notebooks** (same socket-bind wall). This is precisely why the handoff
exists — **you run these locally:**
1. Add the new page to `_quarto.yml` `render:` list and the navbar (a new entry, e.g. text
   `"Locus Resolver"`). Keep `execute: enabled: false`.
2. `quarto render` locally and open `_site/locus_resolver.html` in a browser. Verify both examples
   render, the toggle works, clicks open citations, and the dashed/solid + diamond/circle separation
   is visible.
3. Confirm no unsupported runtime dependency (the page must work as static files served by GitHub
   Pages — test with `python -m http.server` over `_site/`).
4. Leave the result on branch `feature/locus-resolver`, **uncommitted to main / unpushed** — hand
   back to Claude Science for the compliance gate + review before anything reaches GitHub.

## 7. What NOT to do
- Do not invent or "improve" any citation. If a row needs a citation you don't have, leave it for
  Claude Science (it has the genetics connectors + article-fetch + web search). Blank-citation rows
  are invalid by §3b's test anyway.
- Do not add any locus edge to `gene_network_edges.csv`, and do not `pd.concat` the two edge tables.
- Do not relabel a locus node to its functional target.
- Do not extend to the 15 dark-matter genes for the MVP (stretch goal only; the two examples are the
  deliverable).
- Do not commit to `main` or push — Claude Science runs the compliance gate first.

## 8. Deliverables back to Claude Science
On the `feature/locus-resolver` branch, uncommitted-to-main:
- `data/processed/locus_nodes.csv`, `data/processed/locus_annotation_edges.csv`
- `scripts/validate_locus_tables.py` (passing), `scripts/build_resolver_manifest.py`
- `docs/data/locus_resolver_manifest.json`
- the page (`locus_resolver.qmd` or `docs/locus_resolver.html`) + any JS/CSS assets
- `_quarto.yml` + navbar edits
- a one-paragraph note of what you verified locally (render OK, toggle OK, http.server OK)
