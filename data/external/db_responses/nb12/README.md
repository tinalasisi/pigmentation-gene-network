# NB12 frozen MyGene.info + QuickGO responses

Verbatim responses captured to support Notebook 12 Step 3 (blind GO-based mechanism classification).
Query captured 2026-07-13T19:23:37Z. No live calls are made at notebook run time; the `REQUERY`/`REQUERY_QUICKGO`
guards in `notebooks/12_direction_law_expanded.ipynb` re-hit the live APIs when run outside the sandbox.

| File | Query | Endpoint |
|---|---|---|
| `mygene_uniprot_resolution.json` | symbol lookup for the 50 NB12 uncovered LoF genes (`data/processed/nb12_direction_law_expanded.csv`, `regulator_call` is NaN) | GET `mygene.info/v3/query?q=symbol:<SYM>&species=human&fields=symbol,entrezgene,uniprot` |
| `quickgo_bp_annotations.json` | GO biological-process annotations for each gene's resolved UniProt Swiss-Prot accession | GET `ebi.ac.uk/QuickGO/services/annotation/search?geneProductId=UniProtKB:<ACC>&aspect=biological_process&limit=100` |

All 50 genes resolved to a UniProt accession via MyGene.info. 49/50 accessions returned at least one
GO biological-process term via QuickGO; `DNAJC12` returned zero BP annotations (`numberOfHits: 0`),
matching the notebook's own count ("Of 50 uncovered genes, **49** had GO BP terms") and the single
`mech_call` NaN row in `data/processed/nb12_direction_law_expanded.csv`.

The rule-based classification (positive_regulator / negative_regulator / not_melanin_regulator, plus
per-gene confidence and one-clause reasoning) that consumes these frozen BP terms was applied upstream
of this fetch and is itself frozen in `data/processed/nb12_direction_law_expanded.csv`
(`mech_call`/`mech_conf`/`mech_reason` columns) — these two files are the raw evidence behind that
classification, not the classification itself.
