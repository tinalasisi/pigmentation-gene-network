#!/bin/bash
# relax_array.sbatch — one SLURM array task per gene (align + gap-trim + RELAX).
# Submit with:  cd $WORK && WORK=... sbatch --array=1-80 --dependency=afterany:<fetch_jobid> relax_array.sbatch
#SBATCH --job-name=pgn-relax-arr
#SBATCH --account=tlasisi0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=01:00:00
#SBATCH --output=%x-%A_%a.log
set -uo pipefail
export PATH=/scratch/tlasisi_root/tlasisi0/tlasisi/envs/align/bin:$PATH
: "${WORK:?set WORK}"
REPO="$HOME/pigmentation-gene-network/comparative-genomics"
PANEL="${PANEL:-$REPO/config/gene_panel.csv}"
cd "$WORK"
TID=${SLURM_ARRAY_TASK_ID}
GENE=$(sed -n "$((TID+1))p" "$PANEL" | cut -d, -f1)
[ -z "$GENE" ] && { echo "no gene at row $TID"; exit 0; }
echo "[$(date +%T)] task $TID -> gene $GENE"
python "$REPO/scripts/02_align_and_relax.py" --gene "$GENE" \
  --cds cds --aln aln --relax relax --qc qc \
  --panel "$PANEL" --tree "$REPO/config/primate_species_tree.nex" \
  --states "$REPO/config/species_states.csv" --threads ${SLURM_CPUS_PER_TASK:-4} \
  --gap-col-thresh "${GAP_COL_THRESH:-0.3}" --outlier-k "${OUTLIER_K:-4.0}"
echo "[$(date +%T)] task $TID done ($GENE)"
