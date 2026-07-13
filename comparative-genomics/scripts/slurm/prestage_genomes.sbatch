#!/bin/bash
# prestage_genomes.sbatch — GENE-AGNOSTIC prep: unzip each cached genome once + build a miniprot
# index, so run-time extraction skips unzip + on-the-fly indexing (the ~45-min pole). Idempotent.
#SBATCH --job-name=pgn-prestage
#SBATCH --account=tlasisi0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --time=00:40:00
#SBATCH --output=%x-%A_%a.log
set -uo pipefail
export PATH=/scratch/tlasisi_root/tlasisi0/tlasisi/envs/align/bin:$PATH
W=/scratch/tlasisi_root/tlasisi0/tlasisi/pgn_run117
ACC_CSV=$HOME/pigmentation-gene-network/comparative-genomics/config/accessions_all_recoverable.csv
cd "$W"; mkdir -p staging
TID=$SLURM_ARRAY_TASK_ID
ACC=$(sed -n "$((TID+1))p" "$ACC_CSV" | cut -d, -f2)   # +1 skip header; col2 = chosen_accession
[ -z "$ACC" ] && { echo "no accession at row $TID"; exit 0; }
Z="genomes/${ACC}.zip"
[ -f "$Z" ] || { echo "MISSING cached zip: $Z"; exit 0; }
OUT="staging/${ACC}"
if [ -s "$OUT/genome.mpi" ] && { [ -s "$OUT/genome.fna" ] || [ -s "$OUT/cds_from_genomic.fna" ]; }; then
  echo "already staged: $ACC"; exit 0
fi
mkdir -p "$OUT"; rm -rf "$OUT/_x"
unzip -oq "$Z" -d "$OUT/_x" 2>/dev/null || { echo "unzip failed $ACC"; exit 0; }
DD="$OUT/_x/ncbi_dataset/data/${ACC}"
G=$(ls "$DD"/*.fna 2>/dev/null | grep -v cds_from_genomic | head -1)
CDS=$(ls "$DD"/cds_from_genomic.fna 2>/dev/null | head -1)
[ -n "$CDS" ] && cp "$CDS" "$OUT/cds_from_genomic.fna"
if [ -n "$G" ]; then
  cp "$G" "$OUT/genome.fna"
  miniprot -t "${SLURM_CPUS_PER_TASK:-16}" -d "$OUT/genome.mpi" "$OUT/genome.fna" 2>/dev/null || echo "index build failed $ACC"
fi
rm -rf "$OUT/_x"
echo "staged $ACC:"; ls -lah "$OUT" | grep -E 'genome.fna|genome.mpi|cds_from' || echo "  (nothing staged)"
