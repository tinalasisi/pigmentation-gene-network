#!/bin/bash
# extract_staged_array.sbatch — fast per-species CDS extraction for NEW genes using PRE-STAGED
# genomes (staging/<acc>/{genome.fna,genome.mpi,cds_from_genomic.fna}). Mirrors 01's method
# (annotated -> direct CDS; else miniprot vs pre-built index) so new genes match the existing 80.
# Launch after prestage completes, with REF pointing at the new genes' proteins.
#   REF=refs/reference_proteins_new.faa sbatch --array=1-117%60 extract_staged_array.sbatch
#SBATCH --job-name=pgn-extract-new
#SBATCH --account=tlasisi0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=16
#SBATCH --mem=16G
#SBATCH --time=00:20:00
#SBATCH --output=%x-%A_%a.log
set -uo pipefail
export PATH=/scratch/tlasisi_root/tlasisi0/tlasisi/envs/align/bin:$PATH
W=/scratch/tlasisi_root/tlasisi0/tlasisi/pgn_run117
REPO=$HOME/pigmentation-gene-network/comparative-genomics
REF="${REF:-$W/refs/reference_proteins_new.faa}"
ACC_CSV=$REPO/config/accessions_all_recoverable.csv
cd "$W"; mkdir -p cds annot
ln -sf "$REPO/scripts/extract_miniprot_cds.py" extract_miniprot_cds.py
TID=$SLURM_ARRAY_TASK_ID
LINE=$(sed -n "$((TID+1))p" "$ACC_CSV")
SP=$(echo "$LINE" | cut -d, -f1 | tr ' ' '_'); ACC=$(echo "$LINE" | cut -d, -f2)
[ -z "$ACC" ] && { echo "no accession row $TID"; exit 0; }
STAGE="staging/${ACC}"
GENES=$(grep '^>' "$REF" | sed 's/^>//; s/|.*//' | sort -u)
if [ -s "$STAGE/cds_from_genomic.fna" ]; then
  # annotated -> pull CDS directly (longest transcript per gene), same as 01
  for g in $GENES; do
    seqkit grep -nrp "\[gene=${g}\]" "$STAGE/cds_from_genomic.fna" 2>/dev/null \
      | seqkit sort -l -r 2>/dev/null | seqkit head -n 1 2>/dev/null > "cds/${g}.__tmp.fna" || true
    if [ -s "cds/${g}.__tmp.fna" ]; then
      mkdir -p "cds/${g}"; awk -v s=">$SP" 'NR==1{print s} NR>1{print}' "cds/${g}.__tmp.fna" > "cds/${g}/${SP}.cds.fna"
    fi
    rm -f "cds/${g}.__tmp.fna"
  done
  echo "[$SP] annotated: extracted new genes from staged CDS"
elif [ -s "$STAGE/genome.mpi" ] && [ -s "$STAGE/genome.fna" ]; then
  # unannotated -> miniprot vs PRE-BUILT index (fast), then extract CDS
  miniprot -t "${SLURM_CPUS_PER_TASK:-16}" --gff "$STAGE/genome.mpi" "$REF" > "annot/${SP}.new.miniprot.gff" 2>/dev/null \
    || { echo "[$SP] miniprot failed"; exit 0; }
  python extract_miniprot_cds.py --gff "annot/${SP}.new.miniprot.gff" --genome "$STAGE/genome.fna" \
    --species "$SP" --genes "$REF" --outdir cds 2>/dev/null || echo "[$SP] extract failed"
  echo "[$SP] unannotated: miniprot vs pre-built index done"
else
  echo "[$SP] NOT STAGED (staging/$ACC missing) — skip"
fi
