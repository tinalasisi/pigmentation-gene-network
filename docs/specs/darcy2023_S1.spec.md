# darcy2023_S1_disease_genes.csv — spec / provenance

## Source

- **Publication**: D'Arcy, C.E. & Kiel, C. (2023). *Network Analysis and Protein-Protein
  Interaction Prediction of Skin Pigmentation Genes*. Bioengineering, 10(1), 13.
- **DOI**: 10.3390/bioengineering10010013
- **PMC**: PMC9854651
- **License**: CC BY 4.0
- **Table**: Supplementary Table S1, "Disease-gene network of skin pigmentation
  phenotypes."
- **Retrieval route**: Europe PMC `supplementaryFiles` endpoint (Table_S1_Bioengineering_FINAL.xlsx).
  The article PDF itself was not fetched or stored locally; it is cited above by DOI/PMCID
  for anyone who needs to consult the main text.
- **Sheet / header row**: `Sheet 1`, columns start at spreadsheet row index 2 (0-based) —
  i.e. `header=2` when read with `pandas.read_excel`. Rows 0–1 hold the table title and a
  blank spacer row.

## Extraction

Loaded with `pandas.read_excel(..., sheet_name=0, header=2)`. The raw sheet has 278 data
rows spanning **243 unique gene symbols** (some genes recur across multiple disease/OMIM
entries — e.g. `TYR` appears in 7 rows, `FANCA`/`KITLG`/`CDKN2A`/`KIT`/`IRF4` in 3 rows
each). This tidy CSV is **row-level** (one row per gene–disease association, matching the
source table), not deduplicated to one row per gene — downstream consumers that need a
gene-level table should group by `gene` and take the union of `phenotype_class` values (see
`darcy_S1_direction_on_backbone.csv`, which does exactly that for the 43-gene
backbone-overlap set).

## Column dictionary

| Column | Source column | Description |
|---|---|---|
| `gene` | `Gene name` | HGNC-style gene symbol, upper-cased and whitespace-stripped |
| `disease_name` | `Disease name` | Disease/phenotype label associated with the gene in this row |
| `inheritance` | `Inheritance/Acquired` | Mendelian inheritance pattern (AD/AR/XL/etc.) or `Acquired` |
| `phenotype_mim` | `Phenotype MIM number` | OMIM phenotype MIM number (blank for acquired/non-Mendelian entries) |
| `phenotype_class` | `Phenotype class` (normalized) | Controlled vocabulary, see dictionary below |
| `pigmentation_phenotype` | `Pigmentation phenotype` | Free-text clinical description of the pigmentation phenotype |
| `source` | `Source` | D'Arcy & Kiel's own citation of which upstream gene list(s)/OMIM contributed this row |

## `phenotype_class` value dictionary

The source column uses several free-text variants; this CSV normalizes them to four
controlled values by substring match (case-insensitive) — `mixed` → `Mixed` takes priority
over the hypo/hyper checks:

| Normalized value | Source strings mapped in | Row count |
|---|---|---|
| `Hypopigmentation` | "Hypopigmentation disorder" | 144 |
| `Hyperpigmentation` | "Hyperpigmentation disorder" | 81 |
| `Mixed` | "Mixed hypo- & hyperpigmentation disorder" | 47 |
| `Pigmentation phenotype` | "Pigmentation phenotype" (non-disease pigmentation trait, e.g. hair/eye colour variation without a discrete disorder) | 6 |

This is the **disease-direction axis** referenced by the D1/D2 finding in the pigmentation
gene-network project: it lets any gene (whether or not it sits in the 168-gene mechanistic
backbone) be annotated with the direction of pigmentation dysregulation reported in the
clinical/OMIM literature that D'Arcy & Kiel curated.

## Role in the project (annotation only)

This table is used strictly as an **annotation layer** — a lookup of `gene →
phenotype_class` — over the existing 168-gene mechanistic backbone network. Per locked
decision 5, it is never used to create, delete, or reweight a network edge, and it never
substitutes for or overwrites the backbone's own `node_class` field. See
`darcy_S1_direction_on_backbone.csv` for the resulting annotation join on the 43 genes
shared between the D'Arcy S1∪S5 gene sets and the 168-gene backbone, and
`darcy_backbone_crosscheck.csv`/`.json` for the reproduced count cross-check.
