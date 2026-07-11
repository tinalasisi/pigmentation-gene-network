# Network-integration method and MVP build spec (Research Track C)

**Status:** design/spec deliverable — not yet built, not yet a locked decision. Grounded in
`internal/project_dashboard.md` locked decisions 1–10, `TODO.md`, the `nearest-gene-vs-causal` discipline,
and this session's pre-grounding artifacts (`grounding_locus_pattern.json`, `case_gene_coverage_master.csv`).
Nothing here overrides those documents; where this spec proposes something new, it says so.

**Discordance glossary (used throughout):**
- **D1 — "genotype-present, phenotype-absent" (reduced penetrance).** A person carries the usual causal
  variant/genotype for a pigmentation trait, but the expected phenotype does not appear, because the state
  of modifier nodes elsewhere in the signed network blocks the path from the causal genotype to the pigment
  endpoint. Anchor case: Kalinago OCA2 R305W (Ang 2023) — pathogenic by SIFT/PolyPhen/PANTHER, yet R305W
  homozygotes without the population-specific modifier background (NW273KV) are not albino.
- **D2 — "phenotype-present, genotype-absent" (alternative route).** A person shows the phenotype without
  the usual causal genotype, because a directed path to the same pigment endpoint exists through a different
  gene/route on the network. Anchor case: Kalinago albinism (Ang 2023) — the albino individuals do not carry
  the catalogued OCA2 albinism variants; their albinism traces to a population-specific novel variant
  (NW273KV) a standard panel would miss.

Both directions are properties of one signed, directed graph — D1 reads modifier-node states along an
existing path; D2 reads the existence of alternative paths to the same endpoint.

---

## 1. How a resolved locus enters the network honestly

### 1.1 The problem this section solves

A GWAS/marker locus (e.g. `rs12913832`, GWAS-Catalog/dbSNP-mapped to **HERC2**) is a SNP, not a gene. The
gene name attached to it is the **nearest gene by genomic position** — an annotation convention, not a
functional claim. The project's own worked example (already stated in `README.md` and the dashboard) is that
`rs12913832`'s regulatory signal routes through **OCA2**, a different, already-in-network gene, via a
long-range intronic enhancer. Locked decision 5 bars association-only sources (STRING, GWAS co-mapping) from
creating a mechanistic edge; a locus's nearest-gene label and any resolved functional target must therefore
enter the project's data model in a way that (a) never silently promotes the nearest-gene label to a
mechanistic claim, and (b) can never be visually or programmatically confused with a curated OmniPath/
literature mechanistic edge.

### 1.2 Node representation

A resolved locus enters as a **new node type, `locus`**, distinct from the existing `gene` node type in
`gene_network_nodes.csv` (`node_class` today: `cleavage_precursor_gene` / `enzyme_activity_class` /
`network_protein_gene`). It is **never** merged into or used to rename a `gene` row.

**New table: `data/processed/locus_nodes.csv`** (kept separate from `gene_network_nodes.csv` — a locus is
not a gene-network node and must not be countable as one in NB2's 168-gene figure):

| column | required | meaning |
|---|---|---|
| `locus_id` | yes | rsID (dbSNP), e.g. `rs12913832` |
| `chrom` / `position` / `region` | yes | from dbSNP/GWAS Catalog, e.g. `15` / `28120472` / `15q13.1` |
| `nearest_gene_label` | yes | the gene symbol conventionally attached to this locus, e.g. `HERC2` |
| `gene_label_basis` | yes | controlled vocabulary: `nearest_gene_by_position` \| `GWAS_catalog_mapped_gene` \| `panel_convention` — never blank |
| `traits` | yes | semicolon-list of associated traits (from GWAS Catalog), e.g. `eye color;hair color;skin pigmentation` |
| `source_citation` | yes | dbSNP/GWAS Catalog accession or API query used, with retrieval date |

The node's **identity stays the locus/rsID**, carrying the nearest-gene label as a tagged attribute — exactly
the discipline in the `nearest-gene-vs-causal` skill: "Never silently reassign the node to the functional
target. Keep the positional label as the node identity and the functional target as a cited annotation."

### 1.3 Edge representation — a separate table, a separate vocabulary, never the mechanistic backbone

All relationships a locus participates in are **annotation edges**, kept in a table that is structurally
walled off from `data/processed/gene_network_edges.csv` (the OmniPath + curated-literature mechanistic
backbone, `edge_class = mechanistic_projection`, the only table D1/D2 path/reachability computations may
read).

**New table: `data/processed/locus_annotation_edges.csv`**:

| column | required | meaning |
|---|---|---|
| `locus_id` | yes | rsID, FK to `locus_nodes.csv` |
| `gene` | yes | the gene symbol this annotation edge points at (may be the nearest-gene label or a different resolved target) |
| `edge_type` | yes | controlled vocabulary — see §1.4 |
| `evidence_type` | yes | `positional` \| `statistical` \| `functional` — what kind of evidence backs this row |
| `evidence_citation` | **yes, no exception** | PMID/DOI/database accession that establishes this specific row. A `nearest_gene_link` cites the mapping source (GWAS Catalog/dbSNP accession); every other `edge_type` cites a paper or dataset with its own mechanism/statistic, never inherited from the `nearest_gene_link` row. **A row with a blank `evidence_citation` is invalid and must be rejected at load time** — this is the direct implementation of the skill's rule "No citation → no target annotation." |
| `directionality` | yes | always `locus -> gene` (loci are not signed regulators in this table; sign/mechanism belongs only in the mechanistic backbone once/if a target gene's own edges carry it) |
| `notes` | no | free text, e.g. tissue for an eQTL row |

### 1.4 The `edge_type` controlled vocabulary

| `edge_type` | meaning | example |
|---|---|---|
| `nearest_gene_link` | Positional annotation only: this locus's conventionally-assigned nearest gene. Carries **no functional claim**. | `rs12913832 --nearest_gene_link--> HERC2` (cite: GWAS Catalog mapped_gene field / dbSNP) |
| `regulatory_target` | A *cited* functional/mechanistic target distinct from the nearest-gene label — an enhancer, promoter, or chromatin-loop study names this gene as the locus's regulatory target. | `rs12913832 --regulatory_target--> OCA2` (cite: the enhancer paper establishing the HERC2-intron/OCA2-promoter loop) |
| `eQTL_target` | A statistical (not yet mechanistically resolved) association between the locus and a gene's expression level, from a named eQTL dataset/tissue. | `rs12913832 --eQTL_target--> OCA2` (cite: eQTL Catalogue dataset accession, e.g. `QTD000316`, skin tissue) |
| `in_LD_with` | This locus is a proxy/tag SNP in linkage disequilibrium with a separate variant that carries the functional evidence; the causal signal may sit at the LD partner, not this SNP. | `rs12913832 --in_LD_with--> rs1129038` (cite: LD reference panel + r²) |
| `dark_matter_association` | The locus/gene has a recorded GWAS/association signal but **no** pigmentation-relevant trait and **no** mechanistic or regulatory citation resolving it — an explicit "association exists, resolution does not," used for the 15 dark-matter case genes rather than silently omitting them. | `ATRN --dark_matter_association--> (no resolved target)` (cite: GWAS Catalog API pull, api_total=50, 0 pigmentation traits) |

Every value above carries an implicit `annotation_only = TRUE` — none of them is a `mechanistic_projection`
row and none may be copied, joined, or unioned into `gene_network_edges.csv`. The only way a locus's target
gene enters the mechanistic backbone is through the **existing, unrelated** NB2 gene-resolution pipeline for
that gene itself (e.g., OCA2 is already a `gene` node with `mechanistic_projection` edges from Raghunath/
OmniPath — that fact is independent of, and unaffected by, any locus annotation pointing at it).

### 1.5 Enforcing the separation so a reader (or a script) cannot confuse the two layers

1. **Separate files.** `locus_nodes.csv` / `locus_annotation_edges.csv` vs. `gene_network_nodes.csv` /
   `gene_network_edges.csv`. No shared primary key space (`locus_id` is always an rsID; `gene` is always a
   HGNC symbol).
2. **A load-time assertion**, run wherever both tables are read together (the resolver app, any notebook):
   `assert set(locus_annotation_edges.edge_type) <= {the five values in §1.4}` and
   `assert locus_annotation_edges.evidence_citation.notna().all()`. This is the same discipline the project
   already uses for the mechanistic backbone's citation gate (locked decision 6/8) applied to the new table.
3. **Visual separation everywhere the two layers are rendered together** (figures, the MVP resolver in §2):
   mechanistic edges are solid, signed (+/−/0), colored by sign; locus annotation edges are **dashed, gray,
   unsigned**, and locus nodes render as a **diamond glyph**, distinct from the gene circle. A legend entry
   reads: *"Dashed gray = locus annotation (positional or statistical), not a curated mechanistic edge."*
4. **No `edge_class` collision.** `gene_network_edges.csv`'s only current `edge_class` value is
   `mechanistic_projection`; `locus_annotation_edges.csv` never writes to that column name or that table, so a
   `pd.concat` mistake is a schema error, not a silent merge.
5. **A locus is never counted in the 168-gene NB2 figure or in any D1/D2 path/reachability computation** —
   those algorithms read `gene_network_edges.csv` only. A locus can be *displayed alongside* the graph it
   annotates; it is never a graph node those algorithms traverse.

This schema is a **strict superset of the current locked decisions**: it adds a new, clearly-labelled
annotation layer without touching the OmniPath + curated-literature backbone rule, without turning D'Arcy S1
(already an annotation layer, locked decision 2/4) into an edge source, and without reopening the deferred
NB4–NB8 causal-gene-resolution chain — a locus's `regulatory_target`/`eQTL_target` rows are *evidence for* a
future causal call, not a causal call themselves, and none of them draws a new edge into the backbone.

---

## 2. MVP deliverable: the Locus Resolver — an interactive, cited discordance walkthrough

### 2.1 The bar the MVP sets for itself

The design standard is principled curated-mechanism reasoning with worked examples, presented
interactively. Meeting it on substance rather than production values means: (a) show, not just assert, that
"nearest gene" and "causal gene" are different objects — most tools silently pick one; (b) make every
displayed claim click-through-cited; (c) compute the D1/D2 classification from the project's own signed
graph rather than asserting it in prose; and (d) do this for the project's own finding — bidirectional
genotype→phenotype discordance.

### 2.2 Decision: build the interactive discordance resolver (option a), not a static figure or a notebook

| Option | 48h buildable? | Meets the bar (§2.1)? |
|---|---|---|
| (a) Interactive discordance resolver | Yes — client-side only, no backend, data already exists | Yes — interactive, and adds the mislabeling-vs-modifier-block distinction |
| (b) Static locus-resolution map figure | Yes, faster | No — a static image cannot walk a case; loses on format alone |
| (c) Small notebook demo | Yes | Partial — `.ipynb` renders on the Quarto site per locked decision 10, but a notebook is a slower, more technical read than a guided walkthrough; weaker as the headline artifact |

**Recommendation: (a).** It is buildable within 48h specifically *because* the project's existing Quarto →
GitHub Pages setup already renders static, no-kernel content (locked decision 10) — a client-side HTML/JS
page fits that constraint exactly, needs no server, and reuses data already computed (§2.4). A static figure
is the fallback if time runs out; a notebook is not competitive as the primary deliverable.

### 2.3 The two worked examples

Chosen because together they cover **both** discordance directions **and** both locus-integration failure
modes named in the task brief — nearest-gene mislabeling vs. modifier-driven penetrance failure — which is
itself the differentiating claim against a single-mechanism demo.

1. **`rs12913832` / HERC2 / OCA2 — eye colour (D1+D2, "mixed" per `case_gene_coverage_master.csv`).**
   Walks: SNP (`rs12913832`, chr15:28,120,472, intron_variant) → nearest-gene label (**HERC2**, cited to
   GWAS Catalog/dbSNP mapping, `mapped_genes: ["HERC2"]`) → resolved functional target (**OCA2**, cited to
   the enhancer mechanism paper — to be pinned in Phase 1, §3) → OCA2's existing mechanistic backbone path to
   the eumelanin endpoint → D1/D2 classification (mixed: catalogued in both directions per the coverage
   table). This is the project's own flagship illustration (`README.md` lines 26, 192–193) made interactive
   and cited rather than asserted in prose.
2. **Kalinago OCA2, R305W / NW273KV (Ang 2023) — the D1 anchor and its D2 counterpart in one case.**
   Walks the *other* discordance path: R305W is a **correctly** OCA2-assigned, catalogued pathogenic variant
   (SIFT/PolyPhen/PANTHER) already in-network — no nearest-gene problem here — yet R305W homozygotes without
   a population-specific modifier background are not albino (**D1**: network path exists, modifier state
   blocks it). The Kalinago albino individuals, conversely, carry no catalogued OCA2 variant at all — their
   phenotype traces to the novel variant NW273KV (**D2**: phenotype without the usual genotype). Pairing this
   with example 1 shows the tool handles both failure modes — locus-mislabeling and modifier-state blocking —
   with the same graph, not two different hand-built demos.

### 2.4 Inputs (what already exists vs. what this reads)

- `data/processed/gene_network_nodes.csv` / `gene_network_edges.csv` — the 168-gene mechanistic backbone
  (existing).
- `data/processed/discordance_case_classification.csv` + `data/case_records/EXTRACT_Ang2023_eLife_Kalinago.csv`
  — the pre-registered D1/D2 case evidence with page/table citations (existing).
- `case_gene_coverage_master.csv` (this session's artifact) — coverage tier and case-direction per gene
  (existing).
- `grounding_locus_pattern.json` (this session's artifact) — the frozen dbSNP/GWAS-Catalog/eQTL-Catalogue
  response for `rs12913832` (variant record, trait list, `skin_eqtl_datasets: [QTD000316, QTD000544]`) plus
  the per-dark-matter-gene GWAS association pull (existing — this *is* the raw material for `locus_nodes.csv`
  / `locus_annotation_edges.csv`, not yet reshaped into that schema).
- **New, to build:** `locus_nodes.csv` and `locus_annotation_edges.csv` (§1), populated for the two worked
  examples only for the MVP (full 15-gene dark-matter population is a stretch goal, §3); a small JSON export
  bundling the subgraph, citations, and case text each panel needs, generated once and frozen (per the
  `frozen-db-notebook` discipline already surfaced this session — no live network call at render time on
  GitHub Pages).

### 2.5 Panels and interactions

- **Locus card (left panel).** rsID, chromosome/position, trait list. A toggle — *"Show nearest-gene label
  only"* vs. *"Show resolved target"* — that visually removes/adds the `regulatory_target` edge, so a viewer
  sees exactly what a nearest-gene-only tool would show and what is missed.
- **Network view (center panel).** The mechanistic backbone subgraph relevant to the example, rendered
  client-side (a lightweight JS graph library loaded from a CDN, e.g. Cytoscape.js or vis-network — no
  build step). Locus nodes are diamonds; gene nodes are circles; mechanistic edges are solid/signed/colored;
  locus annotation edges are dashed/gray, per §1.5's visual rule. Clicking any node or edge opens its
  citation in the evidence panel.
- **Evidence panel (right panel).** For whatever is selected: the exact citation (PMID/DOI/accession), the
  evidence type (`positional`/`statistical`/`functional` for a locus edge; the OmniPath resource or paper for
  a mechanistic edge), and for the case itself, the verbatim quote + page/table location already captured in
  the `EXTRACT_*` records (locked decision 8 — mechanism pre-registered from the paper).
- **D1/D2 classification readout.** A short computed statement, not asserted prose: for D1, whether a
  directed path from the causal gene to the pigment endpoint exists and which node's state would need to
  change to block it; for D2, whether an alternative directed path to the same endpoint exists bypassing the
  causal gene. Both are read directly off `gene_network_edges.csv` at build time, not hand-written.
- **Case selector.** A two-item switch between the worked examples (extensible to more genes later using the
  same `locus_nodes.csv`/`locus_annotation_edges.csv` schema, including the 15 dark-matter genes rendered
  with `dark_matter_association` edges and no resolved target — an honest "not yet resolvable" state that is
  itself a finding, not a rendering gap).

### 2.6 What makes it principled, concretely (not a design-doc claim)

- Every citation shown is a field in `evidence_citation`/`source_citation`, never inline prose — if a claim
  has no citation field, it cannot render.
- The nearest-gene label is never suppressed when the resolved target is shown — the toggle in §2.5 adds a
  second thing to look at, it never replaces the first, directly implementing the skill's "never silently
  reassign" rule inside the UI itself rather than only in the underlying data.
- The D1/D2 readout is a graph query result against the pinned mechanistic backbone, reproducible by re-
  running the export script — not a caption someone wrote once.
- The schema in §1 physically prevents the one failure mode this whole exercise exists to avoid: an
  association-only edge silently entering the mechanistic backbone. That prevention is checkable (§1.5, item 2)
  rather than a promise.

---

## 3. 48-hour build breakdown

**Already done (reusable as-is):**
- 168-gene / 309-edge mechanistic backbone, citation-gated (NB1 + NB2).
- 13-paper, 694-record validation-case set with pre-registered D1/D2 direction and verbatim evidence
  (`discordance_case_classification.csv`, `EXTRACT_*` records).
- Case-gene coverage master table (this session).
- Frozen `rs12913832` dbSNP/GWAS-Catalog/eQTL-Catalogue pull + the 15-gene dark-matter GWAS pull
  (`grounding_locus_pattern.json`, this session).
- A working Quarto → GitHub Pages static site (no kernel, `execute: enabled: false`) that already renders
  committed `.ipynb`/`.md` — the exact hosting model the MVP page needs (locked decision 10).
- The nearest-gene-≠-causal discipline and the HERC2/OCA2 worked example already written into `README.md`
  and the dashboard — this MVP operationalizes an argument the project has already committed to in prose.

**To build, by phase:**

| Phase | Hours | Task | Executor |
|---|---|---|---|
| 1 | 0–8 | Pin the `regulatory_target` citation for HERC2→OCA2 (the specific enhancer/chromatin-loop paper) and the `eQTL_target` rows from `grounding_locus_pattern.json`; draft `locus_nodes.csv` + `locus_annotation_edges.csv` for the two worked examples per §1's schema | GENETICS_DATA_EXTRACTOR (citation pull) |
| 1 | 0–8 | Verify every populated row has a non-blank `evidence_citation` and the right `edge_type`; confirm no row leaks into `gene_network_edges.csv` | REPRODUCIBILITY_SPECIALIST + DATA_SOURCE_AUDITOR (joint, mirroring the existing S1-annotation gate) |
| 2 | 8–24 | Write the frozen export script: subgraph + citations + case text → one JSON manifest per worked example, following the `frozen-db-notebook` discipline (no live call at render time) | build |
| 2 | 8–24 | Build the static HTML/JS resolver page (panels in §2.5, CDN-loaded graph library, no backend) | build |
| 2 | 20–28 | Wire the page into `_quarto.yml`/`index.qmd` navigation | RESEARCH_SITE_PUBLISHER |
| 3 | 24–36 | Colorblind-safe palette and legend check for the solid/dashed, circle/diamond visual separation; alt-text for the interactive figure | VISUAL_DATA_REVIEWER |
| 3 | 24–36 | Read-through for a non-specialist visitor: does the D1/D2 gloss appear on first use in each panel; is nearest≠causal surfaced, not buried | SCICOMM_REVIEWER |
| 3 | 30–38 | Confirm the client-side page renders under the GitHub Pages/Quarto no-kernel constraint with no unsupported runtime dependency | PLATFORM_LIMITS_ADVISOR |
| 4 | 36–44 | Independent recheck that the rendered D1/D2 classification and citations match the pinned CSVs/JSON (not hand-typed into the JS) | REPRODUCIBILITY_SPECIALIST |
| 4 | 40–44 | Reconcile `TODO.md`/dashboard with this new deliverable; log the decision and its provenance | PROJECT_MANAGER |
| 5 | 44–48 | Final click-through test of both worked examples; hand off the artifact for the pitch narrative | HACKATHON_DOCUMENTARIAN |

**Stretch, if time remains:** extend `locus_nodes.csv`/`locus_annotation_edges.csv` to the remaining
dark-matter genes in `grounding_locus_pattern.json` (`dark_matter_association` rows, no resolved target),
adding a third selector state that shows the honest "not yet resolvable" case rather than only successes.

**Explicitly out of scope for the 48h MVP** (per the dashboard's deferral of NB4–NB8): this spec does not
resolve a causal-gene tie-break rule for loci beyond the two worked examples, does not draw any new
mechanistic edge, and does not reopen Open Targets L2G / ClinVar-OMIM causal resolution. The Locus Resolver
demonstrates the *representation* discipline (§1) on cases already resolved in the literature; it is not a
general-purpose causal-gene resolver.

---

## 4. Summary

- **Integration method (§1):** loci enter as a distinct `locus` node type with a `gene_label_basis`-tagged
  positional label; any functional/statistical claim about their target is a separate, mandatorily-cited
  annotation edge in a table structurally and visually walled off from the OmniPath + curated-literature
  mechanistic backbone. Five `edge_type` values (`nearest_gene_link`, `regulatory_target`, `eQTL_target`,
  `in_LD_with`, `dark_matter_association`) cover every case the current data touches, and none of them can
  enter `gene_network_edges.csv`.
- **MVP (§2):** an interactive, client-side "Locus Resolver" page — no backend, hosted on the existing
  Quarto/GitHub Pages setup — walking two worked examples (`rs12913832`/HERC2/OCA2 nearest-gene mislabeling;
  Kalinago OCA2 R305W/NW273KV modifier-driven D1/D2) with every claim click-through-cited and the D1/D2 call
  computed from the pinned network, not asserted.
- **Build plan (§3):** a 5-phase, specialist-gated 48h schedule reusing all completed NB1/NB2/case-set/
  coverage-table work, adding only the two-example locus-annotation data, the frozen export, the static page,
  and its review passes.
