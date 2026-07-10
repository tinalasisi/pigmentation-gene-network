# DATA_SOURCES.md — provenance manifest

Every external data source used to build the expanded pigmentation gene network, documented so the repo
rebuilds with **no undocumented assumptions**. Each source has a full spec in `docs/specs/`; this file is the
one-screen index plus the reproducibility contract.

**Payoff loci:** the albinism causal genes **TYR (OCA1)** and **OCA2** — also the clinical validation cases.
Association markers are not treated as causal: for the blue-eye signal, HERC2 is the nearest gene to
rs12913832, but causality routes through OCA2 (its long-range enhancer target). Sources below are checked for
their coverage of these loci.

**Acquisition-method note.** Where a source was fetched programmatically, the exact endpoint/DOI is given and
the fetch is reproducible. Where a publisher put the data behind an anti-bot challenge (Cloudflare /
reCAPTCHA), we did **not** circumvent it — the file was supplied by the project owner from their own download,
and we document the exact file, DOI, and license so a rebuilder can obtain the identical file. GWAS Catalog
data were also cross-checked through the human-genetics **MCP connector** as an independent path; that mixed
method is documented in the GWAS spec.

**Redistribution policy (what this repo commits vs. references).** This repository is intended to be
publicly shareable, so it commits **only openly-licensed material** and references everything else by DOI:
- **Committed:** the Raghunath 2015 MOESM1–5 supplements (CC BY 4.0; the article PDF is not stored here — open-access at the DOI if wanted); the Bajpai 2023
  Table S1 (the identical table is a supplementary file of the article's **CC BY 4.0** PMC deposit,
  PMC10901463 — see the license note below); the HIrisPlex-S Erasmus MC Webtool Manual v2 (freely usable);
  all processed tables, scripts, notebooks, and the GWAS Catalog pull (EMBL-EBI terms, attribution).
- **Staged, not yet committed:** the D'Arcy et al. 2023 supplementary Tables S1–S6
  (`data/raw/darcy2023/*.xlsx`; **CC BY 4.0**, PMC9854651 — the article PDF is not stored here, cited by
  DOI). Openly licensed and eligible for the same commit path as Raghunath/Bajpai above; on disk but not
  yet git-committed — any commit runs through REPO_COMPLIANCE_GATE separately.
- **NOT committed — cited by DOI instead:** the subscription/full-text articles for Bajpai (typeset
  *Science* PDF/text), Baxter (*PCMR*, Wiley), Chaitanya HIrisPlex-S (*FSI:G*, Elsevier), and Walsh 2017
  (*Hum Genet*, Springer); **and the Baxter 2018 Table S7 supplementary data file** — a Wiley
  Version-of-Record supplement with no open-license copy (PMC10413850 = not Open Access), withheld and
  re-obtained by DOI. Only its derived CSV in `data/processed/` is committed. These are listed in [`data/raw/papers/REFERENCES.md`](data/raw/papers/REFERENCES.md)
  with DOI, PMID, and license. Every transformation performed on those texts is specified in `docs/specs/`,
  so the derived tables in `data/processed/` reproduce from the publisher's copy without the text being
  present here.

---

## Source index

| # | Source | What it contributes | Acquisition | Status | Spec |
|---|--------|--------------------|-------------|--------|------|
| 1 | **NHGRI-EBI GWAS Catalog** (pigmentation) | 1,072 hair/eye/skin lead SNPs by trait ontology | Live pull, download endpoint + child traits (`gwas_catalog.py`); MCP cross-check | ✅ acquired | [gwas_catalog.spec.md](docs/specs/gwas_catalog.spec.md) |
| 2 | **Bajpai et al. 2023** (*Science*) | 169-gene genome-wide CRISPR screen hits + direction | Author-supplied supplement; Table S1 @ q<0.10 (license note in spec) | ✅ acquired | [bajpai2023.spec.md](docs/specs/bajpai2023.spec.md) |
| 3 | **Baxter et al. 2018/2019** (*PCMR*) | 635 human curated cross-species pigmentation genes | Author-supplied supplement; Table S7 | ✅ acquired | [baxter2018.spec.md](docs/specs/baxter2018.spec.md) |
| 4 | **HIrisPlex-S** (Chaitanya 2018) | 36/41 prediction markers → 16 genes; MC1R+HERC2/OCA2 complete | Author-supplied PDF; markers parsed | ✅ markers; ⚠ coefficients follow-up | [hirisplexs2018.spec.md](docs/specs/hirisplexs2018.spec.md) |
| 5 | **Raghunath et al. 2015** (*BMC Res Notes*) | 265-node / 429-edge directed signed melanogenesis backbone | Prior work (this project) | ✅ pinned | (network base — see Notebooks 1–2 and `project_dashboard.md`) |
| 6 | **Annotation / identity databases** (UniProt, MyGene, PubChem, ChEBI, GO) | Gene-free node typing (Steps 1–2) + HGNC/Entrez/Ensembl/GRCh38 gene identity (Step 3) for the 183 pending nodes | Live MCP connectors (genes-ontologies, chemistry), queried once; verbatim JSON **frozen** to `data/external/db_responses/` | ✅ frozen (Notebook 2) | (see entry 6 below + meta.json) |
| 6b | **HGNC gene groups** | Full member genes of the 6 `enzyme_activity_class` nodes (115 member edges), Step 4 | `rest.genenames.org` `fetch/gene_group_id/<id>`, frozen `hgnc_gene_groups.json` | ✅ frozen (Notebook 2) | (see entry 6 below) |
| 6c | **OmniPath** (11 datasets) | Four-way backbone validation (NB2 Step 6); HIrisPlex edge attestation **staged for a proposed enrichment step** (not run in NB2; notebook placement pending PI agreement) | `omnipathdb.org/interactions`, frozen internal + HIrisPlex subsets | ✅ frozen (Notebook 2) | (see entry 6b below) |
| 6d | **KEGG hsa04916** (Melanogenesis) | Curated-pathway membership scope cross-check (NB2 Step 6) | `rest.kegg.jp`, frozen `kegg_hsa04916.json` | ✅ frozen (Notebook 2) | (see entry 6c below) |
| 7 | **D'Arcy et al. 2023** (*Bioengineering*) | Table S1: 243-gene OMIM disease-gene table; Tables S4/S5: 451-node/4668-edge STRING PPI (association, not mechanistic); Table S6: A375/FM55 mass-spec | Europe PMC `PMC9854651/supplementaryFiles` (CC BY 4.0); 6 tables staged on disk at `data/raw/darcy2023/*.xlsx` (not yet git-committed — pending REPO_COMPLIANCE_GATE) | ✅ staged; cross-check not yet run; NB4/NB5 consumption pending TODO #0 | (see entry 6 above for the full characterization) |

---

## Per-source uniform entries

### 1. NHGRI-EBI GWAS Catalog — pigmentation associations
- **Identity / endpoint:** `https://www.ebi.ac.uk/gwas/api/search/downloads`, `shortForm:"<root>"` +
  `includeChildTraits=true&efo=true&facet=association`, over 10 frozen EFO/OBA/MONDO roots.
- **Version key:** access timestamp **2026-07-08T01:15:41Z** (catalog is a live resource; archived copy
  frozen under `output/catalog/versions/`).
- **Access method:** `scripts/gwas_catalog.py v1.0` + `scripts/traits_pigmentation.json`. Independent
  per-variant cross-check via human-genetics MCP connector (`gwas_associations_for_variant`).
- **License:** EMBL-EBI terms; attribution to the catalog (Sollis 2023) + per-row study PubMed IDs.
- **Fields:** 22 columns (rsid, chr, pos_hg38, risk_allele, or_beta, pvalue[string], mapped_gene, pubmed,
  study_accession, ancestry, …). **Build: GRCh38/hg38.**
- **Normalizations:** no p-value filter at pull; p-values kept as **strings** (underflow-safe −log10);
  effect sizes left as-reported (harmonized separately, with `needs_sumstats` honesty flag).
- **Payoff loci:** MC1R 16 assoc · OCA2 67 · HERC2 65.

### 2. Bajpai et al. 2023 — genome-wide CRISPR screen
- **Identity:** DOI 10.1126/science.ade6289 · PMC10901463 · *Science* 381(6658):eade6289.
- **File:** Table S1 (`science.ade6289_table_s1.xlsx`, "Low SSC FACS enriched genes"), full 4,956-gene screen.
- **Access:** author-supplied publisher download (programmatic fetch blocked by Cloudflare/reCAPTCHA; not
  circumvented). Access date 2026-07-08.
- **License / redistribution:** the article is deposited in **PMC10901463 under CC BY 4.0**
  (`license_ref = ccbylicense`, creativecommons.org/licenses/by/4.0/ — commercial use and adaptation
  permitted with attribution), and `Table_S1.xlsx` is a **supplementary-material file of that CC BY
  deposit** (verified 2026-07-10 via the PMC OA service + Europe PMC full-text XML). The identical data
  table is therefore redistributable with attribution to Bajpai et al. 2023 — this is the basis for
  committing it, independent of any "facts are not copyrightable" argument. The publisher's typeset
  *Science* PDF/text (© 2023 The Authors, exclusive licensee AAAS) is **not** redistributed. Cite the
  paper + DOI.
- **Fields kept:** GeneID(Ensembl), Symbol, GeneInfo, Localization, Process, Function,
  Combined_casTLE_Effect/Score, min/max effect, p_value, q_value, direction_note.
- **Normalization / hit-call:** **q_value < 0.10** → 169 hits (reproduces paper). All positive casTLE effect
  → uniform direction *perturbation reduces pigmentation*.
- **Payoff loci:** OCA2 is a hit; MC1R/HERC2 are not screen hits (expected — screen finds melanogenesis
  effectors, not the eye/hair colour regulators per se).

### 3. Baxter et al. 2018/2019 — curated cross-species gene list
- **Identity:** DOI 10.1111/pcmr.12743 · PMID 30339321 · PMC10413850 · *Pigment Cell Melanoma Res*.
- **File:** Supporting Information Table S7 (`pcmr12743-sup-0007-tables7.xlsx`, "650 Pigmentation Genes").
- **Access:** author-supplied (main text via PMC; SI tables not in PMC OA subset). Access date 2026-07-08.
- **License / redistribution:** Wiley/PCMR **subscription** Version of Record. The Table S7 supplement is
  **NOT redistributed** — no open-license copy exists (PMC10413850 returns `idIsNotOpenAccess`; Crossref
  license = VOR terms only; SI tables not in the PMC OA subset), and a curated gene list can carry
  compilation copyright in its selection/arrangement, so "factual data" is not a redistribution grant. The
  file `data/raw/baxter2018/pcmr12743-sup-0007-tables7.xlsx` is git-ignored; re-obtain via DOI
  10.1111/pcmr.12743 and save under that exact name (Notebook 01b expects it). Cite Baxter + OMIM/MGI/ZFIN/GO.
  The **derived** `data/processed/baxter2018_650_pigmentation_genes.csv` IS committed.
- **Fields:** Ensembl ID, human/mouse/zebrafish symbols, ortholog flag, pigment phenotype location,
  GO/OMIM/MGI/ZFIN evidence flags, PubMed, species-with-phenotype.
- **Normalization:** the sheet has **656 gene rows** (rows carrying a Gene stable ID; pandas reads it as 659 rows with 3 trailing blanks); **take the 635 with a human gene symbol** (matches the project's
  "Baxter 635"). Membership list only — no direction, no effect size.
- **Payoff loci:** OCA2, MC1R present; **HERC2 absent** (consistent with Raghunath).

### 4. HIrisPlex-S — Chaitanya et al. 2018 (+ Walsh 2017 model)
- **Identity:** DOI 10.1016/j.fsigen.2018.04.004 · PII S1872497318302205 · *FSI:Genetics* 35:123–135. Skin
  model coefficients: Walsh 2017 (*Hum Genet* 136:847). Web tool: hirisplex.erasmusmc.nl.
- **File:** paper PDF (`1-s2.0-S1872497318302205-main.pdf`, markers p3–5) + mmc1–4 supplements.
- **Access:** author-supplied (programmatic fetch returned abstract only). Access date 2026-07-08.
- **License:** Elsevier (subscription); rsIDs factual, model free-to-use via Erasmus MC tool.
- **Fields extracted:** 36 gene→rsID pairs (16 genes) + `in_novel_17plex_skin` flag.
- **System structure:** 41 SNPs; IrisPlex eye (6 SNP), HIrisPlex hair (22 SNP), HIrisPlex-S skin (36 SNP),
  all multinomial logistic regression.
- **Documented gaps:** (a) 36/41 markers captured — full 41 need Table 1 transcription; MC1R+HERC2/OCA2
  complete. (b) **Model coefficients not in this paper** — pull from Walsh 2017 + web tool when quantifying
  prediction confidence. One OCR fix (`rs228479`→`rs2228479`), one dup dropped.
- **Payoff loci:** MC1R full red-hair set (rs1805007/8/6, rs11547464, rs885479, rs2228479, rs1110400,
  rs3212355); blue-eye HERC2 rs12913832 + OCA2 rs1800407.

### 5. Raghunath et al. 2015 — directed melanogenesis backbone
- **Identity:** *BMC Res Notes* 2015; Additional Files 1–5. Cleaned to 265 nodes / 429 signed directed edges.
- **Access:** prior work in this project (`raghunath_edges_clean.csv`, `raghunath_nodes_typed.csv`).
- **Role:** the mechanistic directed/signed backbone; all other sources annotate or expand it.
- **Payoff loci:** OCA2 present (2 edges: MITF_melan→OCA2→Melanosome_biogenesis); **HERC2 absent**; MC1R
  present in both keratinocyte and melanocyte compartments.

### 6. Identity / type / enrichment / validation databases — Notebook 2 gene network
Notebook 2 uses each database for a distinct, documented role, on a strict **annotate-then-enrich**
ordering — annotation authorities first (decide *what a node is*, gene-free), then enrichment and
validation authorities (attach gene identity and relationships, then check them):
- **Annotation (Steps 1–2) — "what is this node?":** **UniProt** (reviewed Swiss-Prot, human) decides
  *is this a protein* via a **case-exact** gene-symbol match — the protein authority, used gene-free.
  **PubChem + ChEBI** give small-molecule / peptide-hormone identity (citable CID / ChEBI ID). **Gene
  Ontology via OLS** types biological-process nodes (citable GO ID). No gene database is used to annotate.
- **Enrichment (Steps 3–4) — gene identity + relationships:** **MyGene.info** (symbol → HGNC/Entrez/
  Ensembl/GRCh38) attaches gene identity to protein nodes — enrichment only, never a type decision.
  **HGNC gene groups** (`rest.genenames.org`, `fetch/gene_group_id/<id>`) give the **full membership** of
  each of the 6 `enzyme_activity_class` nodes (no single representative), each cited by its HGNC group ID.
  (The post-2015 pigmentation genes — HIrisPlex-S, and possibly wider GWAS hits — are **not** added here;
  they are held out of NB2 and staged for a proposed enrichment step, notebook placement pending PI
  agreement. See entry 4.)
- **Backbone validation (Step 6) — OmniPath, KEGG:** see entries 6b and 6c below. (OmniPath *also* supplies
  the frozen HIrisPlex-edge subset staged for the proposed enrichment step; it is not consumed in NB2.)
- Annotation/identity databases are reached through the **genes-ontologies** and **chemistry** MCP
  connectors; HGNC gene groups and OmniPath via direct REST (network-access-granted, frozen).
- **Access:** queried once from the `repl` connectors on **2026-07-08** (`queried_utc` stamped in
  `node_resolution.csv.meta.json`), then **frozen** to `data/processed/node_resolution.csv` (183 base
  symbols) + `complex_members.csv` (58 member rows). Notebook 2 is offline/deterministic over the frozen
  tables and makes no live calls — the meta.json lists every connector, method, and the resolution cascade
  so the freeze can be regenerated.
- **Role:** turns the `pending_db_resolution` nodes into typed, HGNC-identified gene nodes. Each node stores
  its `type_source` (which authority decided it) and `type_evidence_id` (the accession — Entrez / ChEBI /
  GO / PubChem CID). **No hand-typed classification list exists.**
- **Normalizations / rulings (all recorded, none silent):** protein type requires a **case-exact** gene
  symbol in a reviewed UniProt entry (guards the cAMP↔`CAMP` Entrez-820 collision → cAMP resolved to
  ChEBI:17489; also rejects ROS→`ROS1`, IL8/NFAT2 at Step 1); 3 alias→official updates surfaced in the
  Step-3 enrichment (IL8→CXCL8, NFAT2→NFATC1, IKBKA→CHUK), each UniProt-confirmed; the 6 one-to-many nodes
  are typed **`enzyme_activity_class`** (PLA2, PKC, PLC, MMPs, Trypsin, Phosphodiesterase) with **no gene
  at annotation** — their **full** member genes are attached in Step 4 from a citable HGNC gene-group call
  (PLA2 group 467 filtered PLA2G* = 20; MMPs 891 = 23; Trypsin 738 filtered PRSS* = 25; Phosphodiesterase
  681 = 24; PKC 3523 = 9; PLC 832 = 14; 115 member edges), **not** a single hand-picked representative.
  ACTH/α-MSH typed `peptide_ligand` by curated ChEBI peptide-hormone entries; the POMC→ACTH→α-MSH cleavage
  cascade is added as `cleaved_from` edges cited by PubMed PMIDs. All distinct protein symbols confirmed by
  a reviewed Swiss-Prot entry; 0 nodes unresolved.
- **Small-molecule / peptide typing — database synonym lookup, not a hand-authored dictionary:** each of the
  27 small-molecule/peptide network abbreviations is resolved by sending the **raw token** (underscores
  removed only) to the PubChem name/synonym index and accepting a hit **only when unambiguous** (one CID),
  with the formula cross-checked against ChEBI. **19/27** resolve this way — the database performs the
  abbreviation→entity step. The **8** it cannot resolve unambiguously (`Calcium_cyt`, `Cysteinyl_DOPA`,
  `Glutathionyl_DOPA`, `Indole_5_6_quinone`, `Indole_5_6_quinone_carboxylic_acid`, `DAG`, `ROS`, and
  `Singlet_oxygen` — where the DB returned the wrong entity, "oxidane") are flagged
  `manual_ruling_documented`, each with a written `ruling_rationale`. The per-node method, query string, and
  rationale live in `data/processed/node_resolution.csv` and `data/processed/chem_resolution_evidence.csv`.
- **Coordinate assembly:** GRCh38 (MyGene `genomic_pos`, default assembly).
- **D'Arcy/Kiel (2023) cross-check:** **STAGED** — the 6 supplementary tables are staged on disk under
  `data/raw/darcy2023/*.xlsx` (untracked in git as of this note; not yet committed — any commit goes
  through REPO_COMPLIANCE_GATE separately) (CC BY 4.0; the article PDF itself is not stored here, cited by
  DOI). The cross-check computation itself has not been run. D'Arcy et al. 2023 (*Bioengineering* 10(1):13, DOI
  10.3390/bioengineering10010013, PMC9854651, PMID 36671585, CC BY 4.0), retrieved from Europe PMC
  (`PMC9854651/supplementaryFiles`), contributes two components: (1) Table S1, a 243-gene OMIM-backed
  disease–gene table (phenotype MIM number + hyper-/hypo-/mixed-pigmentation phenotype class); (2) Tables
  S4/S5, a 451-node / 4668-edge STRING protein–protein interaction network (STRING `combined_score`,
  undirected/unsigned association, not directed/signed), expanded from the 243 disease genes and
  supplemented with A375/FM55 melanoma mass-spec expression (Table S6). Cross-check against the 168-gene
  Raghunath backbone shows 465 D'Arcy genes absent from the backbone (S1∪S5 union), 230 of them
  disease-flagged (118 hypopigmentation-class) — a candidate expansion pool for a proposed downstream
  annotation/PPI-shell step, not a source for the mechanistic backbone (see locked decision 2,
  `project_dashboard.md`/`TODO.md`). MyGene + UniProt remain the identity authority for NB2 gene typing;
  this cross-check is optional independent confirmation, not required for NB1/NB2, and NB4/NB5 consumption
  of the staged tables is pending TODO #0.
- **Citation completeness (release-blocking gate):** every node and every edge in Notebook 2 carries at
  least one **resolvable** citation — a PMID/DOI or a citable accession (UniProt, ChEBI, PubChem CID, GO,
  HGNC gene-group ID, OmniPath `source:PMID`, dbSNP rsID). The 429 backbone edges inherit Raghunath's own
  per-edge references (274 PMID via the MOESM1 reference legend, 138 NetProTM database, 16 reference-text,
  1 OmniPath:SIGNOR backfill). A closing assertion fails the run if any element is uncited (**passed:
  1,586 elements, 0 uncited** — gene-network nodes + gene-layer, backbone, projection, and validation
  tables; HIrisPlex tables moved to the enrichment notebook).

### 6b. OmniPath — backbone validation (NB2 Step 6); edge attestation staged for a proposed enrichment step
- **What:** OmniPath aggregates 11 signed/directed interaction resources (SIGNOR, SignaLink, DoRothEA,
  CollecTRI, KEGG-MEDICUS, and others). Queried at `omnipathdb.org/interactions` across all 11 datasets
  for the resolved gene set (172 network genes + 11 HIrisPlex genes staged for enrichment), `queried_utc`
  stamped in `omnipath.meta.json`.
- **Access:** direct REST (network-access granted); the full 49,316-edge pull is not committed — two frozen
  subsets are: `omnipath_internal.json` (2,949 edges, both endpoints in the resolved gene set — for NB2's
  backbone validation) and `omnipath_hirisplex_edges.json` (35 edges linking an HIrisPlex gene to a network
  gene — **staged for a proposed enrichment step**, not used in NB2). Re-runnable behind `REQUERY_OMNIPATH`.
- **Role — validation, NEVER silent addition.** In NB2, OmniPath assigns each backbone edge a **four-way
  verdict** (confirmed / not-in-OmniPath / sign-conflict / out-of-scope) in a separate joined table
  (`nb2_omnipath_validation.csv`);
  sign-conflicts are recorded as **"differs from cross-tissue consensus"**, not "wrong" (a tissue-specific
  signed edge can legitimately differ from OmniPath's pan-tissue aggregate). OmniPath edges are never
  merged into the mechanistic backbone. In the proposed enrichment step (pending PI agreement), the same
  OmniPath pull would gate added-gene edges: an HIrisPlex→network edge added **only** where OmniPath attests
  it (35 staged edges).
- **Why OmniPath:** it is the standard meta-resource for signed directed human interactions, so one query
  cross-checks the backbone against many curated resources at once; it also carries per-edge literature
  references, which supply resolvable citations for the attested added-gene edges.

### 6c. KEGG hsa04916 (Melanogenesis) — scope cross-check (NB2 Step 6)
- **What:** the curated KEGG melanogenesis pathway (101 genes). Pulled from `rest.kegg.jp`
  (`link/hsa/hsa04916`), frozen to `kegg_hsa04916.json`.
- **Role:** a membership column on the validation table (is each edge endpoint in the curated melanogenesis
  pathway) — a **scope reference, not an edge validator**. Used to see how much of the backbone lies inside
  the canonical pathway vs. its wider signalling context. SIGNOR (a causal-interaction resource) is already
  inside OmniPath's sources, so it is not queried separately.

---

## Available extensions — data in scope if the feasibility reassessment supports them
These are in-scope inputs; what is built now vs. deferred to the grant is a resourcing decision set in the
build order: population allele frequencies (HGDP, 1000 Genomes, gnomAD by population), GTEx tissue expression,
and ENCODE regulatory data. They support the conditional-phenotype / population-background question, as an
analytical input to mechanism and conditionality claims.

---

## Reproducibility contract
1. Acquired data are pinned as versioned artifacts (see `README.md` → pinned inputs table for version IDs).
2. Live pulls (GWAS Catalog) stamp a UTC timestamp and archive a frozen copy; the timestamp is the version.
3. Author-supplied files (blocked publisher supplements) are pinned verbatim with DOI + exact filename so an
   identical copy can be re-obtained.
4. Every normalization (hit thresholds, human-symbol filters, string p-values, OCR fixes) is stated in the
   per-source spec — none are applied silently.
5. Database-backed node typing + gene resolution (Notebook 2) is run once against the live MCP connectors and
   the **verbatim JSON responses are frozen**, UTC-stamped, to `data/external/db_responses/`. The notebook
   **replays the resolution cascade tier by tier over those frozen responses** (offline, no network calls) and
   asserts the replay reproduces `node_resolution.csv` (+ `.meta.json`) and `complex_members.csv` exactly — so
   every typing decision is shown and executed in-notebook, and the build is bit-for-bit reproducible. The
   meta.json records every connector/method/accession behind the freeze.
