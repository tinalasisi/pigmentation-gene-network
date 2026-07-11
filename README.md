# Pigmentation gene network — hackathon build

**Why DNA-based risk prediction fails for some people — studied in the one system where the failure is
visible.** Polygenic prediction of disease (cancer, diabetes, heart disease) works far better in some people
than others, and we usually can't say why a given prediction fails: a variant's effect depends on the rest
of the genome around it. Pigmentation is the cleanest model system for that problem — highly heritable,
visible and measurable in everyone, with a well-mapped molecular pathway, and the *same* prediction failure
in checkable form (forensic-grade color prediction that still misses for some carriers). The pigmentation
network also shares its signaling backbone with disease (~1 in 6 of its protein nodes are canonical cancer
genes — AKT/MAPK/PI3K/TP53/Wnt/KIT). **Pigmentation is the model organism; disease-risk prediction is the
target.**

This repo reconstructs the published Raghunath et al. (2015) directed melanogenesis model as a signed,
gene-level network, and uses it to make one discrete, reproducible finding: **genotype→phenotype
discordance has a network structure, in both directions.** Direction 1 (D1) — a person carries the usual
causal variant but not the phenotype — is read as signed modifier nodes that can block the causal path
(the mechanism of incomplete penetrance / epistasis). Direction 2 (D2) — a person has the phenotype
without the usual causal variant — is read as the many alternative genes with a directed path to the same
pigment endpoint (the many-locus structure that a single-variant test cannot capture). A **validation-case
set of 13 published discordance papers** (3 D1 / 5 D2 / 5 both) has been assembled to test the finding;
testing each case against the network — with its mechanism pre-registered from the paper before the network
is consulted — is a planned step.

A load-bearing discipline runs through the build: **associations are not assumed causal.** Every gene a
case invokes is resolved to its causal gene before any edge is drawn, and only the resolved causal gene is
connected — so, for example, HERC2 (the nearest gene to the blue-eye marker rs12913832) is *not* added;
the signal routes through OCA2, its true long-range target. The albinism causal genes **TYR (OCA1)** and
**OCA2** are the payoff loci, and are also the clinical validation cases.

## Project background

The scientific framing, the notebook build narrative, and the locked design decisions are
maintained in the project's internal control document, `internal/project_dashboard.md` (design-rationale
section). That dashboard is internal background — it changes only when the design changes — and is
not restated here; this README is the public-facing rebuild guide (pinned inputs, notebook order,
reproducibility contract).
Data provenance is recorded in `DATA_SOURCES.md`. Project file inventory and live open items are tracked
on the internal control surface, `internal/project_dashboard.md`.

### Reference papers — FILES withheld (copyright), science used freely

The PI supplied 13 pigmentation genotype→phenotype-discordance reference papers (tracked under
`data/raw/papers/`).
The copyrighted **files** are not redistributed: publisher PDFs, supplements (`.xlsx`/`.docx`/`.pdf`/`.zip`),
and verbatim article-text captures (`*_fulltext.md`, one `*_ABSTRACT-ONLY.md`), all excluded by the top-level
`.gitignore`. Per-paper citations, DOIs, license/access status, how to obtain each file, and the exact
expected filenames are in [`data/raw/papers/REFERENCES.md`](data/raw/papers/REFERENCES.md). Our own extracted records (`EXTRACT_*.md`,
`*_records.csv` — citation-only genetic facts) are committed.

**One supplementary data table is also withheld:** the **Baxter et al. 2018 Table S7**
(`data/raw/baxter2018/pcmr12743-sup-0007-tables7.xlsx`) is a Wiley Version-of-Record supplement with no
open-license copy (PMC record not Open Access), so it is git-ignored and re-obtained via DOI
10.1111/pcmr.12743 — see the withheld stanza in
[`data/raw/papers/REFERENCES.md`](data/raw/papers/REFERENCES.md). The **Bajpai et al. 2023 Table S1**
(`data/raw/bajpai2023/science.ade6289_table_s1.xlsx`) IS committed: the identical table is a supplementary
file of the article's CC BY 4.0 deposit in PMC (PMC10901463). The derived tables in `data/processed/` are
committed for both and reproduce from the publisher copies.

## Directory layout
```
pigmentation-gene-network/
├── README.md                      # this file (the public entry point)
├── DATA_SOURCES.md                # provenance manifest (the reproducibility contract)
├── LICENSE                        # MIT (Tina Lasisi)
├── docs/
│   ├── specs/                     # one structured spec per data source
│   │   ├── gwas_catalog.spec.md
│   │   ├── bajpai2023.spec.md
│   │   ├── baxter2018.spec.md
│   │   └── hirisplexs2018.spec.md
│   └── NB3_case_assembly_provenance.md    # how the 13-paper validation-case set was acquired & extracted
├── notebooks/                     # every processed table is derived here from committed raw
│   ├── 01_reconstruct_published_network.ipynb  # Raghunath MOESM1-2 → 265/429 typed signed network
│   ├── 02_resolve_network_to_genes.ipynb       # annotate → gene network (168 nodes) + OmniPath validation (Raghunath-only)
│   ├── 01a_extract_bajpai_crispr.ipynb         # Table S1 → 169 hits (q<0.10)
│   ├── 01b_extract_baxter_genes.ipynb          # Table S7 → 635 human symbols
│   ├── 01c_extract_hirisplex_markers.ipynb     # transcribed raw table → 36 markers / 16 genes
│   └── 01d_reproduce_gwas_catalog.ipynb        # runs scripts/gwas_catalog.py, asserts anchors
├── scripts/                       # the pull/harmonize engine (provenance-grade, config-driven)
│   ├── gwas_catalog.py            # live GWAS Catalog pull by trait ontology
│   ├── traits_pigmentation.json   # frozen EFO/OBA/MONDO roots (the audit point)
│   ├── harmonize.py               # the one shared cross-source schema
│   └── vizhelpers.py              # underflow-safe -log10(p), trait categories, Manhattan layout
├── data/
│   ├── raw/                       # sources exactly as obtained — OPEN-licensed material committed
│   │   ├── raghunath2015/         #   MOESM1-5 supplements (BMC, CC BY)
│   │   ├── bajpai2023/            #   Table S1 .xlsx (CC BY via PMC10901463) — committed; paper NOT committed
│   │   ├── baxter2018/            #   Table S7 .xlsx WITHHELD (Wiley, no open copy); re-obtain by DOI
│   │   ├── hirisplexs2018/        #   Erasmus MC webtool manual + transcribed marker CSV; paper NOT committed
│   │   └── papers/                #   REFERENCES.md only — full texts cited by DOI, NOT redistributed
│   ├── processed/                 # tables DERIVED by the notebooks above (not hand-placed)
│   │   ├── raghunath_edges_typed_signed.csv   # ← 01  : 429 signed edges
│   │   ├── raghunath_nodes_typed.csv          # ← 01  : 265 typed nodes
│   │   ├── node_resolution.csv (+ .meta.json) # ← 02  : frozen DB type+identity resolution
│   │   ├── complex_members.csv                # ← 02  : HGNC-resolved complex membership
│   │   ├── chem_resolution_evidence.csv       # ← 02  : per-abbreviation DB synonym lookup + rulings
│   │   ├── gene_network_nodes.csv             # ← 02  : the gene network — 168 gene nodes (Raghunath-only)
│   │   ├── gene_network_edges.csv             # ← 02  : 309 edge rows (mechanistic projection)
│   │   ├── gene_graph_nodes.csv               # ← 02  : retained molecular topology — 248 canonical nodes
│   │   ├── gene_graph_edges_topology.csv      # ← 02  : topology edges (backbone + member_of)
│   │   ├── gene_graph_edges_projection.csv    # ← 02  : 309 gene–gene edges (relays contracted)
│   │   ├── nb2_omnipath_validation.csv        # ← 02  : four-way OmniPath verdict + KEGG membership
│   │   ├── bajpai2023_crispr_hits.csv         # ← 01a : 169 hits
│   │   ├── baxter2018_650_pigmentation_genes.csv  # ← 01b : full Table S7
│   │   ├── hirisplexs2018_markers.csv         # ← 01c : 36 markers
│   │   ├── hirisplexs2018_population_provenance.json
│   │   ├── discordance_case_classification.csv        # 13-paper case set, D1/D2/both (+ README)
│   │   └── discordance_case_classification_README.md  # column data dictionary
│   └── case_records/              # per-paper extracted genotype records (13 papers; PDF-sourced)
│       └── EXTRACT_<Author><Year>_..._records.csv     # one CSV per validation paper
└── tools/hooks/                   # pre-commit compliance hooks (redistribution gate)
```

## Pinned input artifacts (version IDs)
Each acquired input is a versioned artifact. To load one in a notebook, use the version ID below.

### Processed data tables (the analysis-ready inputs)
| File | Rows | Version ID |
|------|------|-----------|
| `output/catalog/pigmentation_gwas_catalog.csv` | 1,072 SNPs | `9d04313b-e9c1-4d39-a0f8-8b368cc04c07` |
| `data/processed/bajpai2023_crispr_hits.csv` | 169 genes | `b9cfaf50-394a-4b02-8acc-c2c0ee9144f6` |
| `data/processed/baxter2018_650_pigmentation_genes.csv` | 656 gene rows (635 human) | `3fd8271a-2926-4494-908b-dea66a1b6195` |
| `data/processed/hirisplexs2018_markers.csv` | 36 markers | `1fd498f1-f470-418a-a59f-52f1efb7f218` |
| `data/processed/raghunath_edges_typed_signed.csv` | 429 signed edges | `b8eef726-9f8b-40a0-8eb3-4dd128e0167d` |
| `data/processed/raghunath_nodes_typed.csv` | 265 typed nodes | `db1ef45d-21c3-4eae-a291-b352e3ab794e` |

### Raw sources & engine (pinned for exact re-derivation)
| File | Version ID |
|------|-----------|
| `pigmentation_gwas_catalog.csv.meta.json` | `67689f76-6bda-4ab6-8fc9-cc4fe2b5461b` |
| `mcp_anchor_crosscheck.json` | `9e3ebc91-1fdf-4190-871b-e181601f8993` |
| `science.ade6289_table_s1.xlsx` (Bajpai full screen — committed, CC BY via PMC10901463) | `013e0476-ab1d-400e-a164-7eec96472e1b` |
| `pcmr12743-sup-0007-tables7.xlsx` (Baxter Table S7 — *NOT committed to repo; Wiley, obtain via DOI 10.1111/pcmr.12743*) | `61cac3f3-d3f8-4949-ac5f-6a38a9d00d36` |
| `gwas_catalog.py` | `0416e5cd-e337-44f5-adca-22a5fc00e590` |
| `traits_pigmentation.json` | `525ba2cc-998f-4ed7-b22b-c98d737eaf98` |
| `harmonize.py` | `34844b69-5fe5-4fad-8c07-03253fa3f750` |
| `vizhelpers.py` | `fc1c37a3-1426-40e7-a21f-e5b92bfbca54` |
| Bajpai full text *(reference only — NOT committed; obtain via DOI 10.1126/science.ade6289)* | `27a9ebc0-ca57-4e48-be32-6ae79d8d889c` |
| Baxter full text *(reference only — NOT committed; obtain via DOI 10.1111/pcmr.12743)* | `6801e2de-a320-4852-9f9f-af5171094132` |
| HIrisPlex-S abstract (XML) | `f151b7d7-593e-4483-b929-8a9f6d28769a` |

## Rebuild order

**Reproducibility contract:** every table in `data/processed/` is produced by a notebook in `notebooks/`
from committed raw material — none are hand-placed. Run these first; each is offline and deterministic
(except 01d, a documented live pull with a committed frozen snapshot), and each ends by asserting its
canonical count so drift fails loudly.

- **01** `01_reconstruct_published_network` — Raghunath MOESM1-2 → 265 nodes / 429 signed edges.
- **01a** `01a_extract_bajpai_crispr` — Bajpai Table S1 → 169 hits at q<0.10 (uniform direction).
- **01b** `01b_extract_baxter_genes` — Baxter Table S7 → 656 gene-IDs (635 human symbols), non-destructive.
- **01c** `01c_extract_hirisplex_markers` — transcribed marker table → 36 markers / 16 genes / 17 skin-panel.
- **01d** `01d_reproduce_gwas_catalog` — runs `scripts/gwas_catalog.py`; validates the frozen 1,072-SNP pull
  and asserts the SLC24A5/HERC2/MC1R anchors.

### Documentation

Prose documents are plain Markdown and notebooks are `.ipynb`; both render directly on GitHub with no build
step. `docs/NB3_case_assembly_provenance.md` is a frozen provenance record — the extractor code is shown for
provenance and is not executed as part of viewing it, so it needs neither a kernel nor the withheld source
PDFs. To re-run its extraction, obtain the papers (see the withheld-files note above) and execute the driver
code shown in that document.

### What is built and agreed

Two notebooks are complete and are the agreed build:

1. **Reconstruct the published network** ✅ → typed, signed 265/429 edge list from the Raghunath Additional
   Files. Offline and deterministic: every edge signed from an explicit verb→sign dictionary; node typing
   limited to the two cases the file fixes (`complex` by colon syntax, `environmental` for UVA/UVB).
2. **Resolve the network to genes** ✅ → the **168-gene / 309-edge-row** network (Raghunath-only), built by an
   **annotate-then-enrich** discipline with **every node and edge cited**. Each node is typed by its own-type
   authority (UniProt / ChEBI / PubChem / GO), then gene identity (MyGene) and gene-family membership (HGNC
   groups) are attached; the backbone is validated against OmniPath as a four-way verdict behind a
   release-blocking citation gate. MITF and NFKB1 recompute as the top hubs.

A third body of work is also complete as a **dataset** (its placement as a numbered notebook is not yet
settled — see below): the **validation-case set** — the PI's 13 genotype→phenotype-discordance papers,
extracted from the authoritative publisher PDFs (694 records across committed per-paper CSVs; grain differs by
paper), each classified by direction (3 D1 / 5 D2 / 5 both) with verbatim page/table evidence. Outputs:
`data/processed/discordance_case_classification.csv` + per-paper CSVs in `data/case_records/`; provenance in
`docs/NB3_case_assembly_provenance.md`.

### Proposed downstream direction (not yet agreed)

Everything beyond the two agreed notebooks is a **proposed design under discussion — the notebook structure is
not settled and awaits PI sign-off.** It is not a committed build order. The proposed direction, in outline:
resolve each validation-case gene from its association marker to its causal gene (Open Targets L2G +
ClinVar/OMIM); connect only the resolved causal genes, and only through mechanism (OmniPath + curated
literature — association sources never create an edge); recompute the load-bearing metrics on the connected
graph (signed paths for D1, alternative-reachability for D2, with a null model); and test each case against
the network with its mechanism pre-registered from the paper. A guiding principle already agreed: **HERC2 is
the nearest gene to the blue-eye marker rs12913832, not the causal gene — the signal routes through OCA2**, so
associations are never taken as causal. The specific per-gene connect/unconnectable assignments are candidate
outcomes of this proposal, not decided results.

## Which source feeds which notebook
- **Raghunath 2015** → Notebooks 1, 2 (the network backbone) — agreed.
- **13 discordance papers** (PI lit review) → the validation-case dataset — agreed as data.
- The remaining sources (**Open Targets L2G / ClinVar/OMIM** for causal resolution; **OmniPath + curated
  literature** for mechanistic edge creation; **Bajpai / Baxter / GWAS Catalog / HIrisPlex-S** as per-gene
  evidence tags only, never as a source of mechanistic edges) are intended to feed the *proposed* downstream
  work above, and their notebook assignments depend on a structure not yet agreed.

## Publishing the research website (one-time GitHub setup)

The site is built and deployed by `.github/workflows/publish-site.yml` on every push to
`main` (Quarto renders the committed notebook outputs — no kernel — and deploys via the
native Pages-from-Actions path). The workflow provisions the Pages site itself
(`configure-pages` runs with `enablement: true`), so no manual step is strictly required
before the first push. If the first run still fails at the `Get Pages site` step, a
repository admin does this once in the GitHub UI:

1. **Settings → Pages → Build and deployment → Source:** confirm it reads **GitHub
   Actions** (not "Deploy from a branch"). `enablement: true` creates a missing Pages site
   automatically, but it will not flip an existing *branch* source — a repo previously
   configured for "Deploy from a branch" must be switched here by hand once.
2. **Settings → Actions → General → Workflow permissions:** ensure Actions are allowed to
   run for the repository.
3. Push to `main` (or **Actions → Publish site → Run workflow**). On success the **deploy**
   job prints the live URL.
4. The site is served at `https://tinalasisi.github.io/pigmentation-gene-network/`. Confirm
   it loads and that no withheld file is reachable.

The *"Node 20 is being deprecated / running with Node 24 by default"* line the runner
prints is a warning, not an error; the pinned actions run on Node 24. If a run fails just
after it, read the next `Error:` line for the real cause. Preview locally with `quarto
preview` / `quarto render` on your own machine — Quarto does not run in the Claude Science
sandbox.
