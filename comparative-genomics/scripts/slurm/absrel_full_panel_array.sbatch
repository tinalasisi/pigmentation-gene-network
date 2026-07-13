#!/bin/bash
# absrel_full_panel_array.sbatch — per-branch aBSREL over the FULL gene panel (one task per
# gene), for the network-painting view + RERconverge cross-check. Companion to absrel_array.sbatch
# (which runs only the 9 v3-certified genes). Uses the SAME stop-codon/non-triplet cleaning as
# absrel_array.sbatch: aBSREL asserts on in-frame stops and non-triplet lengths (RELAX does not),
# so stops -> '---', trim to multiple of 3, strip {Test} tags (aBSREL tests ALL branches).
# Needs aln/<gene>.codon.aln.fa + aln/<gene>.tagged.nwk from relax_array.sbatch — run AFTER those.
# Submit:  cd $WORK && WORK=$WORK sbatch --array=1-80 \
#            --dependency=afterok:<relax_array_jobid> absrel_full_panel_array.sbatch
#SBATCH --job-name=pgn-absrel-panel
#SBATCH --account=tlasisi0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G
#SBATCH --time=04:00:00
#SBATCH --output=%x-%A_%a.log
set -uo pipefail
export PATH=/scratch/tlasisi_root/tlasisi0/tlasisi/envs/align/bin:$PATH
: "${WORK:?set WORK}"
REPO="$HOME/pigmentation-gene-network/comparative-genomics"
PANEL="${PANEL:-$REPO/config/gene_panel.csv}"
cd "$WORK"
TID=${SLURM_ARRAY_TASK_ID}
GENE=$(sed -n "$((TID+1))p" "$PANEL" | cut -d, -f1)   # +1: skip header; TID 1..N -> data rows
[ -z "$GENE" ] && { echo "no gene at row $TID"; exit 0; }
mkdir -p absrel absrel_in
[ -s "aln/${GENE}.codon.aln.fa" ] || { echo "no alignment for $GENE — skip"; exit 0; }
echo "[$(date +%T)] task $TID -> aBSREL(full panel) $GENE"
python - "$GENE" <<'PY'
import sys
g=sys.argv[1]; STOP={"TAA","TAG","TGA"}
def load(fa):
    d={};c=None
    for l in open(fa):
        l=l.rstrip("\n")
        if l.startswith(">"): c=l[1:]; d[c]=""
        elif c is not None: d[c]+=l
    return d
d=load(f"aln/{g}.codon.aln.fa"); out={}
for k,s in d.items():
    s=s[:len(s)-(len(s)%3)]
    out[k]="".join("---" if s[i:i+3].upper() in STOP else s[i:i+3] for i in range(0,len(s),3))
open(f"absrel_in/{g}.clean.fa","w").write("".join(f">{k}\n{v}\n" for k,v in out.items()))
nwk=open(f"aln/{g}.tagged.nwk").read().replace("{Test}","")
open(f"absrel_in/{g}.tree.nwk","w").write(nwk)
print(f"cleaned {g}: {len(out)} seqs")
PY
hyphy CPU=${SLURM_CPUS_PER_TASK:-8} absrel \
  --alignment "absrel_in/${GENE}.clean.fa" --tree "absrel_in/${GENE}.tree.nwk" \
  --output "absrel/${GENE}.ABSREL.json" --code Universal > "absrel/${GENE}.absrel.log" 2>&1
echo "[$(date +%T)] task $TID $GENE done exit=$? json=$([ -s absrel/${GENE}.ABSREL.json ] && echo ok || echo MISSING)"
