#!/usr/bin/env python3
"""
02_align_and_relax.py  —  codon-align each gene, QC, prune tree, run HyPhy RELAX.

Reads:
  cds/<gene>/<species>.cds.fna    (from 01_fetch_and_extract.sh)
  gene_panel.csv                  (gene,set)
  leakey_primate_tree.nex         (primate species tree; superset of tips)
  --foreground dichromatic|<file> which tips are the RELAX {Test} branches
  species_states.csv              (species,dichromatism)  <- you provide/confirm

Writes:
  aln/<gene>.codon.aln.fa
  relax/<gene>.RELAX.json
  qc/alignment_qc.csv             per-gene QC (n_tips, len, %gaps, dropped_tips)
Tools: mafft, hyphy, python(biopython,dendropy) on PATH.

This is the COMPUTE step. It does NOT summarize — run 03_report_summary.py after.
"""
import argparse, os, glob, subprocess, json, re
from Bio.Seq import Seq
from Bio import SeqIO
import dendropy

def sh(cmd, **kw): return subprocess.run(cmd, check=True, **kw)

def codon_align(gene, cds_dir, aln_dir, min_tips=4, gap_col_thresh=0.5):
    files=glob.glob(os.path.join(cds_dir,gene,"*.cds.fna"))
    seqs={}
    for f in files:
        rec=next(SeqIO.parse(f,"fasta"))
        s=str(rec.seq).upper().replace("N","")
        # QC: must be near-multiple of 3; trim trailing partial codon
        s=s[:len(s)-(len(s)%3)]
        if len(s)<90: continue                      # <30 codons: skip
        aa=str(Seq(s).translate())
        # QC: reject if >1 internal stop (allow terminal)
        if aa[:-1].count("*")>1: continue
        seqs[rec.id]=s
    if len(seqs)<min_tips: return None,{"n_tips":len(seqs),"status":"too_few_tips"}
    os.makedirs(aln_dir,exist_ok=True)
    prot=os.path.join(aln_dir,f"{gene}.prot.fa")
    with open(prot,"w") as o:
        for sp,s in seqs.items(): o.write(f">{sp}\n{Seq(s).translate()}\n")
    aln_prot=os.path.join(aln_dir,f"{gene}.prot.aln.fa")
    with open(aln_prot,"w") as o: sh(["mafft","--quiet","--auto",prot],stdout=o)
    codon={}
    for rec in SeqIO.parse(aln_prot,"fasta"):
        aa=str(rec.seq); s=seqs[rec.id]; codons=[s[i:i+3] for i in range(0,len(s),3)]
        out=[]; ci=0
        for a in aa:
            if a=="-": out.append("---")
            else: out.append(codons[ci] if ci<len(codons) else "---"); ci+=1
        codon[rec.id]="".join(out)
    # codon-aware gap-column trim: drop codon columns that are majority-gap.
    # Reduces spurious-indel dN/dS inflation; frames preserved (we trim whole codons).
    n_cols_trimmed=0
    if codon and gap_col_thresh is not None:
        vals=list(codon.values()); n=len(vals); ncod=len(vals[0])//3
        keep=[c for c in range(ncod)
              if (sum(1 for x in vals if x[c*3:c*3+3]=="---")/n) <= gap_col_thresh]
        n_cols_trimmed=ncod-len(keep)
        codon={sp:"".join(x[c*3:c*3+3] for c in keep) for sp,x in codon.items()}
    if not codon or len(next(iter(codon.values())))<90:
        return None,{"n_tips":len(codon),"status":"too_short_after_trim"}
    nuc=os.path.join(aln_dir,f"{gene}.codon.aln.fa")
    with open(nuc,"w") as o:
        for sp,s in codon.items(): o.write(f">{sp}\n{s}\n")
    L=len(next(iter(codon.values())))
    gaps=sum(s.count("-") for s in codon.values())/(L*len(codon))
    return nuc,{"n_tips":len(codon),"aln_len":L,"pct_gaps":round(100*gaps,2),
                "n_cols_trimmed":n_cols_trimmed,"status":"ok","tips":sorted(codon.keys())}

def prune_tag_tree(tree_path, tips, foreground, out_path):
    t=dendropy.Tree.get(path=tree_path, schema="nexus")
    def norm(x): return x.taxon.label.replace(" ","_")
    keep=[l.taxon for l in t.leaf_node_iter() if norm(l) in set(tips)]
    if len(keep)<4: return None,0
    t.retain_taxa(keep)
    # write newick, tag foreground tips with {Test}
    nwk=t.as_string(schema="newick", suppress_rooting=True, unquoted_underscores=True).strip()
    n_fg=0
    for sp in foreground:
        u=sp.replace(" ","_")
        if u in nwk and (u+"{Test}") not in nwk:
            nwk=re.sub(rf"\b{re.escape(u)}\b", u+"{{Test}}".format(), nwk, count=1); n_fg+=1
    open(out_path,"w").write(nwk)
    return out_path, n_fg

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--cds",default="cds"); ap.add_argument("--aln",default="aln")
    ap.add_argument("--relax",default="relax"); ap.add_argument("--qc",default="qc")
    ap.add_argument("--panel",default="gene_panel.csv")
    ap.add_argument("--tree",default="leakey_primate_tree.nex")
    ap.add_argument("--states",default="species_states.csv")
    ap.add_argument("--threads",default="8")
    ap.add_argument("--gene",default=None,help="run only this gene (for SLURM array jobs)")
    ap.add_argument("--gap-col-thresh",dest="gap_col_thresh",type=float,default=0.5,
                    help="drop codon columns with gap fraction above this (0-1); None disables")
    a=ap.parse_args()
    os.makedirs(a.relax,exist_ok=True); os.makedirs(a.qc,exist_ok=True)
    import csv
    panel={r["gene"]:r["set"] for r in csv.DictReader(open(a.panel))}
    if a.gene: panel={g:s for g,s in panel.items() if g==a.gene}
    states={r["species"].replace(" ","_"):r["dichromatism"] for r in csv.DictReader(open(a.states))}
    foreground=[sp for sp,st in states.items() if st.startswith("dichro")]
    QC_FIELDS=["gene","set","n_tips","aln_len","pct_gaps","n_cols_trimmed","status","n_foreground","relax_status"]
    def write_qc(path,rows):
        with open(path,"w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=QC_FIELDS,extrasaction="ignore")
            w.writeheader(); w.writerows(rows)
    qc_rows=[]
    for gene in panel:
        nuc,info=codon_align(gene,a.cds,a.aln,gap_col_thresh=a.gap_col_thresh)
        row={"gene":gene,"set":panel[gene],**{k:v for k,v in info.items() if k!="tips"}}
        if nuc:
            tips=info["tips"]
            treef=os.path.join(a.aln,f"{gene}.tagged.nwk")
            tf,n_fg=prune_tag_tree(a.tree,tips,foreground,treef)
            row["n_foreground"]=n_fg
            if tf and n_fg>=1:
                out=os.path.join(a.relax,f"{gene}.RELAX.json")
                try:
                    sh(["hyphy","relax","--alignment",nuc,"--tree",tf,"--test","Test",
                        "--output",out,"--code","Universal"],
                       stdout=open(os.path.join(a.relax,f"{gene}.log"),"w"),
                       stderr=subprocess.STDOUT)
                    row["relax_status"]="ok"
                except subprocess.CalledProcessError:
                    row["relax_status"]="hyphy_failed"
            else:
                row["relax_status"]="no_foreground_in_tree"
        qc_rows.append(row)
        write_qc(os.path.join(a.qc,f"{gene}.csv"),[row])        # per-gene (array merge source)
        print(f"{gene:10s} {row.get('status'):14s} tips={row.get('n_tips')} fg={row.get('n_foreground')} {row.get('relax_status','')}")
    if not a.gene:
        write_qc(os.path.join(a.qc,"alignment_qc.csv"),qc_rows)  # combined (full sequential run)
    print("DONE -> run 03_report_summary.py")

if __name__=="__main__": main()
