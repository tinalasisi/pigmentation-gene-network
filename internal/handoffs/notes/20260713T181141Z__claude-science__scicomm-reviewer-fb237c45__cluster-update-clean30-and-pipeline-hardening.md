# Cluster update — what changed since the 43-gene pig_expansion runspec

**Created:** 20260713T181141Z
**Author:** scicomm-reviewer session (fb237c45)
**For:** Cluster Claude (Great Lakes HPC)
**Supersedes on two points:** `20260713T163427Z__…__pig-expansion-runspec.md` (still correct on
pipeline/output structure; the gene *list* and *scripts* below take precedence).

**TL;DR — before you launch pig_expansion, do two things:**
1. `git pull` origin/main (the alignment + SLURM scripts were hardened after the runspec was written).
2. Point the array at the **clean-30** config, not the 43-gene file.

---

## 1. Gene list: run the 30 orthology-clean genes, NOT 43

The earlier runspec listed all 43 candidates (Group A 21 + Group B 22). Since then the 43 were
put through an Ensembl Compara orthology screen (documented in NB14) and **13 were dropped** as
unsafe for a dN/dS scan. Run only the 30 that pass.

**Config to use:** `comparative-genomics/config/gene_panel_expansion_clean30.csv` (30 rows,
`ortholog_risk == clean`). Array should be `--array=1-30`.

**The 30 (16 melanosome biogenesis + 14 melanogenesis regulation):**
AP3B1, AP3D1, BLOC1S6, CDC42, CDH2, CTNNB1, CTNS, EGFR, EP300, GPR143, HGF, HPS1, HPS3, HPS4,
HPS5, HRAS, LYST, MAPK3, MYO5A, PPP3CA, RAB27A, RAB5C, RACK1, RAF1, SLC17A5, SLC1A2, SLC44A4,
SPTLC2, SRC, TRAF6

**The 13 excluded (do NOT run) and why:**
- HIGH_paralog (≥3 human paralogs → ortholog mis-mapping risk): FASLG, SLC29A3
- paralog_check (1–2 paralogs, also excluded): BCL2, EDN1, MAP2K1, MAP2K2, MLPH, PAK1, TP53
- low_ortholog_cov (<10/12 primates recover an ortholog): BLOC1S3, BLOC1S5, HPS6
- RAC1 fails both (paralog_check + low_ortholog_cov)

Keep the ortholog-recovery QC gate you already apply (drop any gene recovering <~60% of tips or
with aln_ref_ratio anomalies) — the screen used a 12-genome probe, your full 117-set run is the
real test.

## 2. Pipeline scripts were hardened AFTER the runspec — pull first

Two commits landed on origin/main after the 16:34Z runspec was written. Both make the pipeline
fail *loudly* instead of silently, which matters for the per-gene incremental output:

- **33e7efc** `fix(02)`: `codon_align()` now skips an empty/malformed CDS file (e.g. a miniprot
  no-hit for one species) with `try/except StopIteration` instead of crashing the whole gene.
  Previously one bad species FASTA killed the gene's alignment.
- **4be5686** `harden pipeline vs silent failures`: the SLURM sbatch wrappers
  (`absrel_array`, `relax_array`, `per_origin_relax_array`, `extract_staged_array`) now
  `exit 1` with a `TASK FAILED (gene=… rc=…)` line on any step failure, so a failed task shows
  up as a failed array element rather than an empty output file that looks "done". The panel
  loader also accepts `set`/`group`/`category` column names (clean30.csv uses `group`).

Net effect for you: a gene that fails now produces a **failed** array task (visible in sacct),
not a silent empty JSON. Please treat a missing per-gene output as "re-check", not "no signal".

## 3. Everything else this session was presentation-only (no rerun impact)

For completeness — the rest of my commits today do **not** change any input, gene set, tree, or
pipeline, so they need no action from you:
- NB13/NB14 gained explanatory + result figures; a broken markdown provenance table was fixed;
  NB14 was wired into the website nav; NB14's gene_panel.csv was reclassified as an *output* the
  notebook motivates (not a raw input). DATA_SOURCES entries 9 & 12 (Zhang PMID, hormone-panel
  KEGG provenance) were corrected. None of this touches `comparative-genomics/`.

## Output structure & prefix (unchanged from runspec)
Per-gene incremental files (`results/pig_expansion/{gene}.aBSREL.json`,
`{gene}.per_origin_K.csv`), fast/small genes first and MYO5A/LYST last, collector appends into
`branch_rates.csv` / `per_origin_K.csv` on each poll. Commit prefix `[hpc pig_expansion]`.
