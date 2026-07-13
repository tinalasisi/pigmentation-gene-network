#!/usr/bin/env python3
"""
02b_branch_rates.py — per-BRANCH dN/dS for every gene, for the network-painting view.

RELAX (script 02) gives one K per gene (a foreground-vs-background summary). To colour a
network node per lineage — "which module does THIS clade remodel?" — we need a value per
gene PER BRANCH. HyPhy aBSREL fits an adaptive branch model and reports, for every branch:
  * a baseline MG94xREV dN/dS (omega)  -> the value we paint with
  * an episodic-diversifying-selection test with a Holm-Bonferroni corrected p per branch
This runs aBSREL on all branches (no foreground tag needed) for each aligned gene, then
flattens the per-branch results into one tidy CSV.

Reads : aln/<gene>.codon.aln.fa  +  aln/<gene>.tagged.nwk (untagged is fine; aBSREL tests all)
Writes: absrel/<gene>.ABSREL.json
        report/branch_rates.csv   (gene, set, branch, is_tip, baseline_omega,
                                    absrel_p, absrel_corrected_p, selected_flag)
Tools : hyphy, python(biopython optional). Depends only on HyPhy JSON — no data transfer.

Run AFTER 02 (needs the alignments + trees it produced). Heavier than RELAX: aBSREL fits
per-branch, so budget ~2-5x the RELAX time per gene. On SLURM, array over genes.

Usage:
  python 02b_branch_rates.py                       # all genes with an alignment
  python 02b_branch_rates.py --genes MC1R,MITF,AR  # subset
  GENE=MC1R python 02b_branch_rates.py --one "$GENE"  # single (for array jobs)
"""
import argparse, os, glob, json, csv, subprocess

def run_absrel(aln, tree, out, logf):
    # aBSREL over ALL branches; no --branches restriction -> every branch gets a rate+test
    cpu = os.environ.get("SLURM_CPUS_PER_TASK", "16")  # honor the SLURM allocation (else hyphy auto-detects)
    subprocess.run(["hyphy","CPU="+cpu,"absrel","--alignment",aln,"--tree",tree,
                    "--output",out,"--code","Universal"],
                   check=True, stdout=open(logf,"w"), stderr=subprocess.STDOUT)

def parse_absrel(path):
    """Return list of per-branch dicts from an aBSREL JSON."""
    j=json.load(open(path))
    ba=j.get("branch attributes",{}).get("0",{})
    tested=j.get("tested",{}).get("0",{})
    rows=[]
    for br,attr in ba.items():
        # baseline omega key varies slightly across hyphy versions -> try known variants
        omega=None
        for k in ("Baseline MG94xREV omega ratio",
                  "Baseline MG94xREV omega ratio for *background*",
                  "baseline omega"):
            if k in attr: omega=attr[k]; break
        rows.append({
            "branch":br,
            "baseline_omega":omega,
            "absrel_p":attr.get("Uncorrected P-value"),
            "absrel_corrected_p":attr.get("Corrected P-value"),
            "n_rate_classes":attr.get("Rate classes"),
            "tested":tested.get(br)=="test",
        })
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--aln",default="aln"); ap.add_argument("--out",default="absrel")
    ap.add_argument("--panel",default="gene_panel.csv")
    ap.add_argument("--genes",default=None, help="comma list; default = all with an alignment")
    ap.add_argument("--one",default=None, help="single gene (array-job mode)")
    a=ap.parse_args()
    os.makedirs(a.out,exist_ok=True); os.makedirs("report",exist_ok=True)
    panel={r["gene"]:(r.get("set") or r.get("group") or r.get("category") or "?") for r in csv.DictReader(open(a.panel))}
    if a.one: genes=[a.one]
    elif a.genes: genes=a.genes.split(",")
    else: genes=[os.path.basename(f).split(".")[0]
                 for f in glob.glob(os.path.join(a.aln,"*.codon.aln.fa"))]
    all_rows=[]
    for g in genes:
        aln=os.path.join(a.aln,f"{g}.codon.aln.fa")
        tree=os.path.join(a.aln,f"{g}.tagged.nwk")
        if not (os.path.exists(aln) and os.path.exists(tree)):
            print(f"{g:10s} SKIP (no alignment/tree)"); continue
        outj=os.path.join(a.out,f"{g}.ABSREL.json")
        if not os.path.exists(outj):
            try: run_absrel(aln,tree,outj,os.path.join(a.out,f"{g}.log"))
            except subprocess.CalledProcessError:
                print(f"{g:10s} aBSREL FAILED"); continue
        try:
            rows=parse_absrel(outj)
            if not rows: raise ValueError("no branches")
        except Exception as e:
            print(f"{g:10s} SKIP (unreadable/empty aBSREL json: {type(e).__name__})"); continue
        n_sel=sum(1 for r in rows if r["absrel_corrected_p"] is not None and r["absrel_corrected_p"]<0.05)
        for r in rows:
            r["gene"]=g; r["set"]=panel.get(g,"?")
            r["is_tip"]="Node" not in r["branch"]  # heuristic; HyPhy names internal nodes NodeN
            r["selected_flag"]=(r["absrel_corrected_p"] is not None and r["absrel_corrected_p"]<0.05)
        all_rows+=rows
        print(f"{g:10s} branches={len(rows)}  episodic-selected={n_sel}")
    cols=["gene","set","branch","is_tip","baseline_omega","absrel_p",
          "absrel_corrected_p","n_rate_classes","tested","selected_flag"]
    with open("report/branch_rates.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
        for r in all_rows: w.writerow({c:r.get(c) for c in cols})
    print(f"DONE -> report/branch_rates.csv ({len(all_rows)} branch rows across {len(genes)} genes)")

if __name__=="__main__": main()
