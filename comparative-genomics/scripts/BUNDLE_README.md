# HPC job bundle — primate dichromatism × pigmentation/hormone selection scan

Self-contained bundle for running the comparative selection analysis on an HPC
where **the agent has no data access**. Your Claude Code (or you) runs these on
the cluster; the only thing that comes back to the chat is a few-KB summary
(`report/SUMMARY.md` + `report/summary.json`) that we iterate over by paste.

## The paste-back contract (why this works without data access)
The agent never sees genomes, alignments, or trees. It only needs the contents
of **`report/SUMMARY.md`** (or `report/summary.json`) after each run — per-gene
K, p, BH-adjusted p, tip counts, foreground counts, and alignment gap%. That is
enough to decide: which genes to re-run, whether the foreground is powered,
which QC-flagged genes to drop, and what the pigmentation-vs-hormone contrast
looks like. Paste that file back; the agent replies with the next step.

If the agent asks for something not in SUMMARY.md, it will tell you the exact
one-liner to run (e.g. `seqkit stats aln/AR.codon.aln.fa`) and what to paste.

## Run order
```
bash 00_setup_env.sh                      # once: conda env with all tools
conda activate primate-selection
# --- FLAGSHIP FIRST (9 gibbon genomes, fast) ---
bash 01_fetch_and_extract.sh accessions_gibbon_flagship.csv
python 02_align_and_relax.py --states species_states.csv
python 03_report_summary.py
#   -> paste report/SUMMARY.md back into the chat
# --- FULL PANEL (117 genomes) once the flagship looks right ---
bash 01_fetch_and_extract.sh accessions_all_recoverable.csv
python 02_align_and_relax.py --states species_states.csv
python 03_report_summary.py
```
For SLURM, wrap 01/02 in an sbatch script (they are the heavy steps); 03 is trivial.

## Files
| file | role |
|---|---|
| `00_setup_env.sh` | conda/mamba toolchain (datasets, miniprot, gffread, seqkit, mafft, hyphy, biopython, dendropy) |
| `01_fetch_and_extract.sh` | download genomes from NCBI; extract per-gene CDS (direct for annotated, miniprot for unannotated) |
| `extract_miniprot_cds.py` | best-hit CDS extraction from miniprot GFF (stdlib only) |
| `02_align_and_relax.py` | codon-align (MAFFT) + QC + prune/tag tree + HyPhy RELAX per gene |
| `03_report_summary.py` | collapse fits+QC into the small paste-back report |
| `refs/reference_proteins.faa` | **query proteins** — 80 genes × up to 3 reference species (human, macaque, colobine). NOT the study species; only used to find genes. Prebuilt so the HPC needs no network for gene identity. |
| `gene_panel.csv` | 80 genes: 27 pigmentation-core + 53 hormone, with `set` label |
| `accessions_gibbon_flagship.csv` | 9 gibbon target genomes (5 dichromatic / 4 monochromatic) |
| `accessions_all_recoverable.csv` | 117 target genomes across 4 families |
| `species_states.csv` | species → dichromatic/monochromatic (RELAX foreground = dichromatic) |
| `primate_species_tree.nex` | primate species tree (primate phylogeny source); pruned per gene to available tips |

## Key parameters you may want to change
- **Foreground definition** (`species_states.csv`): RELAX tags every `dichromatic`
  species as a `{Test}` branch and tests for a *shared* selection-intensity shift
  across them vs the monochromatic background. To test a single clade, subset this
  file to that clade's species.
- **QC thresholds** (`02_align_and_relax.py`): min 4 tips/gene, min 30 codons,
  ≤1 internal stop, trailing partial codon trimmed. Genes with >40% gaps are
  flagged in the report (candidate drops).

## Known caveats (confirm on the cluster)
1. **Accession freshness**: `accessions_*.csv` is an NCBI snapshot (see
   TARGET_PANEL_MANIFEST). Re-run a `datasets summary genome taxon` check if it's
   been a while; accessions occasionally get superseded.
2. **miniprot CDS need frame QC**: handled (internal-stop / frame checks in 02),
   but genes with high gap% in the report are the ones to eyeball or drop.
3. **CDS `[gene=...]` matching** for annotated assemblies assumes NCBI's
   `cds_from_genomic.fna` gene tokens match our symbols; a few genes may need an
   alias (report will show them as missing tips).
4. **AR reference transcript** was short in Ensembl; miniprot uses the protein so
   this is mitigated, but check AR's aln length in the report.
