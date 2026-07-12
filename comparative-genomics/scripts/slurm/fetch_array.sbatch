#!/bin/bash
# fetch_array.sbatch — one SLURM array task per assembly row.
# Submit with:  cd $WORK && WORK=... ACC=<accessions.csv> sbatch --array=1-N%20 fetch_array.sbatch
# %20 caps concurrent NCBI downloads. Per-task processes row (TASK_ID) of ACC.
#SBATCH --job-name=pgn-fetch-arr
#SBATCH --account=tlasisi0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=00:25:00
#SBATCH --output=%x-%A_%a.log
set -uo pipefail
export PATH=/scratch/tlasisi_root/tlasisi0/tlasisi/envs/align/bin:$PATH   # env FIRST (no module/conda)
: "${WORK:?set WORK}" "${ACC:?set ACC to accessions csv}"
REPO="$HOME/pigmentation-gene-network/comparative-genomics"
cd "$WORK"
ln -sfn "$REPO/refs" refs
ln -sf "$REPO/scripts/extract_miniprot_cds.py" extract_miniprot_cds.py
TID=${SLURM_ARRAY_TASK_ID}
ROWCSV="row_${TID}.csv"
head -1 "$ACC" > "$ROWCSV"
sed -n "$((TID+1))p" "$ACC" >> "$ROWCSV"
SP=$(sed -n 2p "$ROWCSV" | cut -d, -f1)
echo "[$(date +%T)] task $TID -> $SP"
export THREADS=${SLURM_CPUS_PER_TASK:-4}
bash "$REPO/scripts/01_fetch_and_extract.sh" "$ROWCSV"
echo "[$(date +%T)] task $TID done ($SP)"
