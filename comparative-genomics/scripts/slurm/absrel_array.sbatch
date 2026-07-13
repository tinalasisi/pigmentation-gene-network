#!/bin/bash
# absrel_array.sbatch — per-branch aBSREL (episodic positive selection / "who") on the
# v3-certified genes, one SLURM array task per gene. Answers WHICH lineages carry the signal.
# Submit:  cd $WORK && WORK=... sbatch --array=1-9 absrel_array.sbatch
#SBATCH --job-name=pgn-absrel
#SBATCH --account=tlasisi0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=16
#SBATCH --mem=8G
#SBATCH --time=03:00:00
#SBATCH --output=%x-%A_%a.log
set -uo pipefail
export PATH=/scratch/tlasisi_root/tlasisi0/tlasisi/envs/align/bin:$PATH   # env FIRST
: "${WORK:?set WORK}"
cd "$WORK"
GENES=(TFAP2A KITLG EDN3 HSD17B1 HSD17B12 SRD5A1 CYP7B1 SHBG HSD17B7)
GENE=${GENES[$((SLURM_ARRAY_TASK_ID-1))]}
mkdir -p absrel absrel_in
echo "[$(date +%T)] aBSREL task $SLURM_ARRAY_TASK_ID -> $GENE"
# clean: strip stop codons -> '---', trim to multiple of 3 (aBSREL asserts on stops/non-triplet,
# unlike RELAX); strip {Test} tags from the tree (aBSREL default tests ALL branches).
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
hyphy CPU=${SLURM_CPUS_PER_TASK:-16} absrel \
  --alignment "absrel_in/${GENE}.clean.fa" --tree "absrel_in/${GENE}.tree.nwk" \
  --output "absrel/${GENE}.ABSREL.json" --code Universal > "absrel/${GENE}.absrel.log" 2>&1
echo "[$(date +%T)] $GENE done exit=$? json=$([ -s absrel/${GENE}.ABSREL.json ] && echo ok || echo MISSING)"
