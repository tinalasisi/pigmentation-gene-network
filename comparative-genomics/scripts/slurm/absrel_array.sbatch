#!/bin/bash
# absrel_array.sbatch — one SLURM array task per gene: per-BRANCH dN/dS (HyPhy aBSREL).
# Needs the alignments + tagged trees from relax_array.sbatch (script 02) — run AFTER those.
# Does NOT need the origin map, so it can run in Round 1 immediately.
# Submit with:
#   cd $WORK && WORK=$WORK sbatch --array=1-80 \
#     --dependency=afterok:<relax_array_jobid> absrel_array.sbatch
#SBATCH --job-name=pgn-absrel-arr
#SBATCH --account=tlasisi0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=03:00:00
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
echo "[$(date +%T)] task $TID -> aBSREL $GENE"
python "$REPO/scripts/02b_branch_rates.py" --one "$GENE" --aln aln --out absrel --panel "$PANEL"
echo "[$(date +%T)] task $TID done ($GENE)"
