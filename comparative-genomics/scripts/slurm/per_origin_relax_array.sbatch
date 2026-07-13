#!/bin/bash
# per_origin_relax_array.sbatch — per-(gene x origin) RELAX (the heterogeneous-architecture test).
# Flattens the 2-D (gene, origin) grid to a 1-D array: task t -> gene = t // N_ORIGINS,
#   origin = t %% N_ORIGINS. Needs config/origin_assignments.csv from the phylo audit AND the
#   alignments from relax_array.sbatch (reused). Run AFTER both are present.
# Submit (example for 80 genes x N_ORIGINS origins):
#   N_ORIGINS=<n> cd $WORK && WORK=$WORK N_ORIGINS=$N_ORIGINS \
#     sbatch --array=0-$((80*N_ORIGINS-1)) per_origin_relax_array.sbatch
#SBATCH --job-name=pgn-perorigin-relax
#SBATCH --account=tlasisi0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=16
#SBATCH --mem=8G
#SBATCH --time=02:00:00
#SBATCH --output=%x-%A_%a.log
set -uo pipefail
export PATH=/scratch/tlasisi_root/tlasisi0/tlasisi/envs/align/bin:$PATH
: "${WORK:?set WORK}"
: "${N_ORIGINS:?set N_ORIGINS to the number of origin_ids in origin_assignments.csv}"
REPO="$HOME/pigmentation-gene-network/comparative-genomics"
PANEL="${PANEL:-$REPO/config/gene_panel.csv}"
ORIGINS_CSV="${ORIGINS_CSV:-$REPO/config/origin_assignments.csv}"
cd "$WORK"
TID=${SLURM_ARRAY_TASK_ID}
GENE_IDX=$(( TID / N_ORIGINS ))
ORIG_IDX=$(( TID % N_ORIGINS ))
GENE=$(sed -n "$((GENE_IDX+2))p" "$PANEL" | cut -d, -f1)         # +2: skip header, 0-based idx
ORIGIN=$(tail -n +2 "$ORIGINS_CSV" | cut -d, -f3 | tr -d '"' | sort -u | sed -n "$((ORIG_IDX+1))p")   # f3 = origin_id (cols: species,family,origin_id,...)
[ -z "$GENE" ] && { echo "no gene at idx $GENE_IDX"; exit 0; }
[ -z "$ORIGIN" ] && { echo "no origin at idx $ORIG_IDX"; exit 0; }
echo "[$(date +%T)] task $TID -> gene=$GENE origin=$ORIGIN"
python "$REPO/scripts/02c_per_origin_relax.py" --gene "$GENE" --origin "$ORIGIN" \
  --aln aln --out relax_per_origin --qc qc/per_origin \
  --panel "$PANEL" --tree "$REPO/config/primate_species_tree.nex" \
  --origins "$ORIGINS_CSV" --threads ${SLURM_CPUS_PER_TASK:-16}
echo "[$(date +%T)] task $TID done (gene=$GENE origin=$ORIGIN)"
