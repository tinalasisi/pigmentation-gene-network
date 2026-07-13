#!/usr/bin/env python3
"""
02_align_and_relax.py  —  codon-align each gene, QC, prune tree, run HyPhy RELAX.

Reads:
  cds/<gene>/<species>.cds.fna    (from 01_fetch_and_extract.sh)
  gene_panel.csv                  (gene,set)
  primate_species_tree.nex         (primate species tree; superset of tips)
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

def drop_outlier_tips(codon, k=4.0, min_tips=4):
    """Drop misaligned/paralogous tips that inflate RELAX branch lengths, WITHOUT dropping
    genuinely-divergent-but-correct lineages (e.g. lemurs). Metric = NEAREST-NEIGHBOUR p-distance:
    a real divergent lineage is close to its relatives (small NN dist); a misaligned/paralogous
    sequence is far from everyone incl. its closest relative (large NN dist). Flag tips whose NN
    distance is a strong robust-z (MAD) outlier AND >1.5x median. Conservative; never below min_tips.
    numpy-vectorized (~instant for 100 tips)."""
    import numpy as np
    tips=list(codon.keys()); T=len(tips)
    if T<=min_tips: return codon, []
    L=len(next(iter(codon.values()))); ncod=L//3
    ids={}
    def row(s):
        r=np.empty(ncod, dtype=np.int32)
        for j in range(ncod):
            c=s[j*3:j*3+3]
            r[j]=0 if c=="---" else ids.setdefault(c, len(ids)+1)   # 0 == gap
        return r
    M=np.stack([row(codon[t]) for t in tips])                       # (T, ncod)
    nn=np.zeros(T)
    for i in range(T):
        both=(M[i]!=0) & (M!=0)                                     # (T, ncod) both non-gap
        n=both.sum(1); d=((M!=M[i]) & both).sum(1)
        pd=np.divide(d, n, out=np.ones(T), where=n>0)              # 1.0 where no overlap (suspicious)
        pd[i]=np.inf                                                # exclude self
        nn[i]=pd.min()                                             # distance to NEAREST neighbour
    med=float(np.median(nn)); mad=float(np.median(np.abs(nn-med))) or 1e-9
    z=(nn-med)/(1.4826*mad)
    outliers=[tips[i] for i in range(T) if z[i]>k and nn[i]>med*1.5]
    keep=[t for t in tips if t not in outliers]
    if len(keep)<min_tips: return codon, []                         # never break the gene
    return {t:codon[t] for t in keep}, outliers

def codon_align(gene, cds_dir, aln_dir, min_tips=4, gap_col_thresh=0.5, outlier_k=4.0, threads=1):
    files=glob.glob(os.path.join(cds_dir,gene,"*.cds.fna"))
    seqs={}
    for f in files:
        rec=next(SeqIO.parse(f,"fasta"))
        s=str(rec.seq).upper().replace("N","")
        # QC: must be near-multiple of 3; trim trailing partial codon
        s=s[:len(s)-(len(s)%3)]
        if len(s)<90: continue                      # <30 codons: skip
        aa=str(Seq(s).translate())
        # QC: reject ANY internal stop (HyPhy RELAX rejects stop codons; >1 was too lenient
        # and caused ~36 genes to fail on frameshifted miniprot extractions)
        if aa[:-1].count("*")>0: continue
        seqs[rec.id]=s
    if len(seqs)<min_tips: return None,{"n_tips":len(seqs),"status":"too_few_tips"}
    os.makedirs(aln_dir,exist_ok=True)
    prot=os.path.join(aln_dir,f"{gene}.prot.fa")
    with open(prot,"w") as o:
        for sp,s in seqs.items(): o.write(f">{sp}\n{Seq(s).translate()}\n")
    aln_prot=os.path.join(aln_dir,f"{gene}.prot.aln.fa")
    with open(aln_prot,"w") as o: sh(["mafft","--thread",str(threads),"--quiet","--auto",prot],stdout=o)
    codon={}
    for rec in SeqIO.parse(aln_prot,"fasta"):
        aa=str(rec.seq); s=seqs[rec.id]; codons=[s[i:i+3] for i in range(0,len(s),3)]
        out=[]; ci=0
        for a in aa:
            if a=="-": out.append("---")
            else: out.append(codons[ci] if ci<len(codons) else "---"); ci+=1
        codon[rec.id]="".join(out)
    # v3 per-sequence outlier removal: drop long-branch/misaligned/paralogous tips that
    # inflate RELAX branch lengths (the fix column-trimming can't do). Runs before column trim.
    n_outliers=0; outlier_tips=[]
    if codon and outlier_k:
        codon, outlier_tips = drop_outlier_tips(codon, k=outlier_k, min_tips=min_tips)
        n_outliers=len(outlier_tips)
    # codon-aware gap-column trim: drop codon columns that are majority-gap.
    # Reduces spurious-indel dN/dS inflation; frames preserved (we trim whole codons).
    n_cols_trimmed=0
    if codon and gap_col_thresh is not None:
        vals=list(codon.values()); n=len(vals); ncod=len(vals[0])//3
        keep=[c for c in range(ncod)
              if (sum(1 for x in vals if x[c*3:c*3+3]=="---")/n) <= gap_col_thresh]
        n_cols_trimmed=ncod-len(keep)
        codon={sp:"".join(x[c*3:c*3+3] for c in keep) for sp,x in codon.items()}
    if not codon or len(codon)<min_tips or len(next(iter(codon.values())))<90:
        return None,{"n_tips":len(codon),"n_outliers":n_outliers,"status":"too_few_or_short_after_qc"}
    nuc=os.path.join(aln_dir,f"{gene}.codon.aln.fa")
    with open(nuc,"w") as o:
        for sp,s in codon.items(): o.write(f">{sp}\n{s}\n")
    if outlier_tips:
        with open(os.path.join(aln_dir,f"{gene}.outliers.txt"),"w") as o: o.write("\n".join(outlier_tips)+"\n")
    L=len(next(iter(codon.values())))
    gaps=sum(s.count("-") for s in codon.values())/(L*len(codon))
    return nuc,{"n_tips":len(codon),"aln_len":L,"pct_gaps":round(100*gaps,2),
                "n_cols_trimmed":n_cols_trimmed,"n_outliers":n_outliers,
                "outlier_tips":";".join(outlier_tips),"status":"ok","tips":sorted(codon.keys())}

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
    ap.add_argument("--tree",default="primate_species_tree.nex")
    ap.add_argument("--states",default="species_states.csv")
    ap.add_argument("--threads",default="8")
    ap.add_argument("--gene",default=None,help="run only this gene (for SLURM array jobs)")
    ap.add_argument("--gap-col-thresh",dest="gap_col_thresh",type=float,default=0.5,
                    help="drop codon columns with gap fraction above this (0-1); None disables")
    ap.add_argument("--outlier-k",dest="outlier_k",type=float,default=4.0,
                    help="drop tips with robust-z divergence > k (v3 outlier removal); 0 disables")
    a=ap.parse_args()
    os.makedirs(a.relax,exist_ok=True); os.makedirs(a.qc,exist_ok=True)
    import csv
    panel={r["gene"]:r["set"] for r in csv.DictReader(open(a.panel))}
    if a.gene: panel={g:s for g,s in panel.items() if g==a.gene}
    states={r["species"].replace(" ","_"):r["dichromatism"] for r in csv.DictReader(open(a.states))}
    foreground=[sp for sp,st in states.items() if st.startswith("dichro")]
    QC_FIELDS=["gene","set","n_tips","aln_len","pct_gaps","n_cols_trimmed","n_outliers","status","n_foreground","relax_status"]
    def write_qc(path,rows):
        with open(path,"w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=QC_FIELDS,extrasaction="ignore")
            w.writeheader(); w.writerows(rows)
    qc_rows=[]
    for gene in panel:
        nuc,info=codon_align(gene,a.cds,a.aln,gap_col_thresh=a.gap_col_thresh,outlier_k=a.outlier_k,threads=int(a.threads))
        row={"gene":gene,"set":panel[gene],**{k:v for k,v in info.items() if k!="tips"}}
        if nuc:
            tips=info["tips"]
            treef=os.path.join(a.aln,f"{gene}.tagged.nwk")
            tf,n_fg=prune_tag_tree(a.tree,tips,foreground,treef)
            row["n_foreground"]=n_fg
            if tf and n_fg>=1:
                out=os.path.join(a.relax,f"{gene}.RELAX.json")
                try:
                    sh(["hyphy","CPU="+str(a.threads),"relax","--alignment",nuc,"--tree",tf,"--test","Test",
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
