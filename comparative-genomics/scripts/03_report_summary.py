#!/usr/bin/env python3
"""
03_report_summary.py — collapse the run into a SMALL text report to paste back.

Reads relax/*.RELAX.json + qc/alignment_qc.csv and emits:
  report/SUMMARY.md        human-readable, paste this into the chat
  report/relax_results.csv small table (also safe to paste)
  report/summary.json      machine-readable (attach or paste)

NOTHING here needs the raw genomes/alignments — it reads only fit outputs and QC.
The three files together are a few KB: they carry every number needed to iterate
without transferring data. Paste SUMMARY.md (or attach summary.json) back.
"""
import json, glob, os, csv, math, argparse
os.makedirs("report",exist_ok=True)

def bh(pvals):
    idx=sorted(range(len(pvals)),key=lambda i:pvals[i]); n=len(pvals); out=[None]*n; prev=1.0
    for rank,i in enumerate(reversed(idx),start=1):
        k=n-rank+1; adj=min(prev, pvals[i]*n/k); out[i]=adj; prev=adj
    return out

def extract_K(path):
    """Pull (K, p, LRT, n_seqs, n_sites) from one RELAX JSON."""
    j=json.load(open(path)); tr=j.get("test results",{}); inp=j.get("input",{})
    return {"K":tr.get("relaxation or intensification parameter"),
            "p_value":tr.get("p-value"),"LRT":tr.get("LRT"),
            "n_seqs":inp.get("number of sequences"),"n_sites":inp.get("number of sites")}

def per_origin_summary(relax_dir, qc_dir, panel_path):
    """Walk relax_per_origin/<origin>/<gene>.RELAX.json, join per-(origin,gene) QC,
    BH-correct WITHIN each origin, write report/per_origin_K.csv."""
    panel={r["gene"]:r["set"] for r in csv.DictReader(open(panel_path))}
    qc={}
    for f in glob.glob(os.path.join(qc_dir,"*.csv")):
        for r in csv.DictReader(open(f)):
            qc[(r.get("origin_id"),r.get("gene"))]=r
    rows=[]
    for oj in sorted(glob.glob(os.path.join(relax_dir,"*","*.RELAX.json"))):
        origin=os.path.basename(os.path.dirname(oj)); gene=os.path.basename(oj).split(".")[0]
        try: k=extract_K(oj)
        except Exception: continue
        q=qc.get((origin,gene),{})
        rows.append({"origin_id":origin,"gene":gene,"set":panel.get(gene,"?"),**k,
                     "n_fg":q.get("n_fg"),"n_tips_kept":q.get("n_tips_kept"),"status":q.get("status","ok")})
    # BH within each origin separately
    by_origin={}
    for r in rows: by_origin.setdefault(r["origin_id"],[]).append(r)
    for oid,rs in by_origin.items():
        have=[r for r in rs if isinstance(r["p_value"],(int,float))]
        for r,pa in zip(have, bh([r["p_value"] for r in have])): r["p_BH"]=round(pa,4)
    cols=["origin_id","gene","set","K","p_value","p_BH","LRT","n_fg","n_tips_kept","n_sites","status"]
    with open("report/per_origin_K.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore"); w.writeheader()
        for r in sorted(rows,key=lambda x:(x["origin_id"],x["set"],x.get("p_value") or 1)):
            w.writerow(r)
    n_sig=sum(1 for r in rows if isinstance(r.get("p_BH"),(int,float)) and r["p_BH"]<0.05)
    print(f"wrote report/per_origin_K.csv ({len(rows)} (origin,gene) fits, {len(by_origin)} origins, BH<0.05: {n_sig})")

_ap=argparse.ArgumentParser()
_ap.add_argument("--per-origin",dest="per_origin",action="store_true",
                 help="summarize relax_per_origin/ instead of pooled relax/")
_ap.add_argument("--relax-dir",dest="relax_dir",default="relax_per_origin")
_ap.add_argument("--qc-dir",dest="qc_dir",default="qc/per_origin")
_ap.add_argument("--panel",default="gene_panel.csv")
_args=_ap.parse_args()
if _args.per_origin:
    per_origin_summary(_args.relax_dir,_args.qc_dir,_args.panel)
    raise SystemExit(0)

rows=[]
for f in sorted(glob.glob("relax/*.RELAX.json")):
    gene=os.path.basename(f).split(".")[0]
    try: j=json.load(open(f))
    except Exception: continue
    tr=j.get("test results",{})
    fits=j.get("fits",{})
    # branch length / tree length if present
    inp=j.get("input",{})
    rows.append({"gene":gene,
                 "K":tr.get("relaxation or intensification parameter"),
                 "p_value":tr.get("p-value"),
                 "LRT":tr.get("LRT"),
                 "n_seqs":inp.get("number of sequences"),
                 "n_sites":inp.get("number of sites")})
# attach set + qc
panel={r["gene"]:r["set"] for r in csv.DictReader(open("gene_panel.csv"))}
qc={r["gene"]:r for r in csv.DictReader(open("qc/alignment_qc.csv"))} if os.path.exists("qc/alignment_qc.csv") else {}
for r in rows:
    r["set"]=panel.get(r["gene"],"?")
    q=qc.get(r["gene"],{})
    r["n_tips"]=q.get("n_tips"); r["n_foreground"]=q.get("n_foreground"); r["pct_gaps"]=q.get("pct_gaps")
# BH across all genes with a p-value
have=[r for r in rows if isinstance(r["p_value"],(int,float))]
padj=bh([r["p_value"] for r in have])
for r,pa in zip(have,padj): r["p_BH"]=round(pa,4)

# write csv
cols=["gene","set","K","p_value","p_BH","LRT","n_tips","n_foreground","n_sites","pct_gaps"]
with open("report/relax_results.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
    for r in sorted(rows,key=lambda x:(x["set"],x.get("p_value") or 1)):
        w.writerow({c:r.get(c) for c in cols})
json.dump(rows, open("report/summary.json","w"), indent=1)

# markdown
def fmt(x,n=3):
    try: return f"{float(x):.{n}g}"
    except: return str(x)
by_set={}
for r in rows:
    by_set.setdefault(r["set"],[]).append(r)
lines=["# RELAX run summary","",
       f"Genes with a RELAX fit: {len(rows)}  |  significant nominal p<0.05: "
       f"{sum(1 for r in rows if isinstance(r['p_value'],(int,float)) and r['p_value']<0.05)}  |  "
       f"significant BH<0.05: {sum(1 for r in have if r.get('p_BH',1)<0.05)}",""]
for s in sorted(by_set):
    lines.append(f"## {s}")
    lines.append("| gene | K | p | p_BH | tips | fg | %gap |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in sorted(by_set[s],key=lambda x:x.get("p_value") or 1):
        direc="relaxed" if (isinstance(r["K"],(int,float)) and r["K"]<1) else "intensified"
        star="*" if isinstance(r["p_value"],(int,float)) and r["p_value"]<0.05 else ""
        lines.append(f"| {r['gene']}{star} | {fmt(r['K'])} ({direc}) | {fmt(r['p_value'])} | "
                     f"{fmt(r.get('p_BH'))} | {r.get('n_tips')} | {r.get('n_foreground')} | {r.get('pct_gaps')} |")
    lines.append("")
# QC flags worth reporting back
flagged=[r for r in rows if (r.get("pct_gaps") and float(r["pct_gaps"])>40)
         or (r.get("n_foreground") in ("0",0,None))]
lines.append("## QC flags to report back")
if flagged:
    for r in flagged:
        lines.append(f"- {r['gene']}: gaps={r.get('pct_gaps')}%, foreground={r.get('n_foreground')}, tips={r.get('n_tips')}")
else:
    lines.append("- none")
lines += ["","### What to paste back to the chat",
          "Paste this whole file (or attach report/summary.json). It is a few KB and",
          "contains K, p, BH-adjusted p, tip counts, foreground counts, and gap% per gene —",
          "everything needed to decide next steps without transferring genomes or alignments."]
open("report/SUMMARY.md","w").write("\n".join(lines))
print("wrote report/SUMMARY.md, report/relax_results.csv, report/summary.json")
