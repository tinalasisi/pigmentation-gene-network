#!/bin/bash
# report_diag.sbatch — merge per-gene QC, then SUMMARY + certification diagnostics.
# Submit with:  cd $WORK && WORK=... sbatch --dependency=afterany:<relax_jobid> report_diag.sbatch
#SBATCH --job-name=pgn-report
#SBATCH --account=tlasisi0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:20:00
#SBATCH --output=%x-%j.log
set -uo pipefail
export PATH=/scratch/tlasisi_root/tlasisi0/tlasisi/envs/align/bin:$PATH
: "${WORK:?set WORK}"
REPO="$HOME/pigmentation-gene-network/comparative-genomics"
cd "$WORK"
# merge per-gene qc/<gene>.csv -> qc/alignment_qc.csv
python - <<'PY'
import glob, csv, os
files=[f for f in sorted(glob.glob("qc/*.csv")) if os.path.basename(f)!="alignment_qc.csv"]
rows=[]; fields=None
for f in files:
    rr=list(csv.DictReader(open(f)))
    if rr:
        rows+=rr; fields=fields or list(rr[0].keys())
if fields:
    with open("qc/alignment_qc.csv","w",newline="") as o:
        w=csv.DictWriter(o,fieldnames=fields); w.writeheader(); w.writerows(rows)
print("merged", len(rows), "genes into qc/alignment_qc.csv")
PY
ln -sf "$REPO/config/gene_panel.csv" gene_panel.csv
python "$REPO/scripts/03_report_summary.py"
python "$REPO/scripts/03b_diagnostics.py" --workdir "$WORK" --repo "$REPO"
echo "REPORT+DIAG DONE"
