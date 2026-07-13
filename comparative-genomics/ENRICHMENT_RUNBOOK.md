# Gene-enrichment runbook — add N pigmentation genes to the existing 80

Purely additive: the 80 done genes are untouched; we extract + test only the new genes, then
re-run the reports over the accumulated result dirs (which now hold old + new).

## Done ahead of time (2026-07-13)
- **Genomes pre-staged**: `staging/<acc>/{genome.fna, genome.mpi, cds_from_genomic.fna}` via
  `prestage_genomes.sbatch` — unzip + miniprot-index once, so extraction skips the ~45-min pole.
- **Tools built + tested**: `fetch_ref_proteins.sh` (NCBI datasets → `>GENE|human`, longest isoform),
  `extract_staged_array.sbatch` (fast per-species extract vs pre-staged genomes; mirrors `01`).
- **relax_array.sbatch** bumped to 16 cores / 3h (no slowest-gene timeout).
- **02b_branch_rates.py** skips empty/unreadable JSON instead of crashing the flatten.

## When the gene list arrives (WORK=/scratch/tlasisi_root/tlasisi0/tlasisi/pgn_run117)
```
cd $WORK
# 1. genes -> reference proteins (login node; needs internet)
printf "GENE1\nGENE2\n..." > genes_new.txt
bash ~/fetch_ref_proteins.sh genes_new.txt          # -> refs/reference_proteins_new.faa
# 2. new-genes panel (set=pigmentation)
{ echo "gene,set"; grep '^>' refs/reference_proteins_new.faa | sed 's/^>//;s/|.*/,pigmentation/'; } \
    > $REPO/config/gene_panel_new.csv
N=$(( $(wc -l < $REPO/config/gene_panel_new.csv) - 1 ))
# 3. extract (fast; uses pre-staged genomes)
EJ=$(REF=$WORK/refs/reference_proteins_new.faa sbatch --parsable --array=1-117%60 $REPO/scripts/slurm/extract_staged_array.sbatch)
# 4. align + RELAX (16 cores; after extract)
RJ=$(WORK=$WORK PANEL=$REPO/config/gene_panel_new.csv sbatch --parsable --array=1-${N}%40 --dependency=afterok:$EJ $REPO/scripts/slurm/relax_array.sbatch)
# 5. per-origin RELAX (after relax; reuses alignments)
PJ=$(WORK=$WORK N_ORIGINS=14 PANEL=$REPO/config/gene_panel_new.csv sbatch --parsable --array=0-$((N*14-1))%96 --dependency=afterany:$RJ $REPO/scripts/slurm/per_origin_relax_array.sbatch)
# 6. MERGE (after per-origin): re-run reports over the ACCUMULATED dirs (old+new), on the login node.
#    python 03_report_summary.py --per-origin --relax-dir relax_per_origin --qc-dir qc/per_origin  -> report/per_origin_K.csv (all 110)
#    python 03_report_summary.py                                                                   -> report/relax_results.csv
#    then: cat -> Mac repo results/perorigin_v1/, commit + push FROM THE MAC (compute nodes have no internet).
```

## Measured timings (from tonight's run)
- extract (pre-staged): ~10 min · align+RELAX: ~2-3 h (bounded by slowest gene, 16 cores) ·
  per-origin: ~1 h · merge+push: ~10 min → **~3-4 h total**.
- Slowest-gene lever: predict slow genes by CDS length; they don't block delivery of the fast ones.
- **Do NOT run auto-git on the cluster.** Deliver by pulling CSVs to the Mac and pushing from there.
