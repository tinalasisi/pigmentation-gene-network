#!/usr/bin/env python3
"""Extract best-hit CDS per panel gene from a miniprot GFF.

miniprot emits mRNA features with a "Target=<GENE>|<refsp> ..." attribute and a
score. For each panel gene we keep the single highest-scoring mRNA, stitch its
CDS children in order, reverse-complement if on the minus strand, and write a
nucleotide CDS FASTA: cds/<gene>/<species>.cds.fna
Only depends on the Python stdlib + the genome FASTA (indexed with pyfaidx if
available, else a simple in-memory load).
"""
import argparse, os, re, sys
from collections import defaultdict

def load_genome(path):
    seqs={}; name=None; buf=[]
    op = open
    if path.endswith(".gz"):
        import gzip; op=gzip.open
    with op(path,"rt") as fh:
        for line in fh:
            if line.startswith(">"):
                if name: seqs[name]="".join(buf)
                name=line[1:].split()[0]; buf=[]
            else: buf.append(line.strip())
    if name: seqs[name]="".join(buf)
    return seqs

COMP=str.maketrans("ACGTNacgtn","TGCANtgcan")
def rc(s): return s.translate(COMP)[::-1]

def gene_of(attr):
    m=re.search(r"Target=([^|\s]+)\|", attr)
    return m.group(1) if m else None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--gff",required=True); ap.add_argument("--genome",required=True)
    ap.add_argument("--species",required=True); ap.add_argument("--genes",required=True)
    ap.add_argument("--outdir",default="cds")
    a=ap.parse_args()
    panel={l[1:].split("|")[0] for l in open(a.genes) if l.startswith(">")}
    # pass 1: pick best mRNA id per gene
    best={}  # gene -> (score, mrna_id)
    mrna_gene={}
    for line in open(a.gff):
        if line.startswith("#") or not line.strip(): continue
        f=line.rstrip("\n").split("\t")
        if len(f)<9: continue
        if f[2]=="mRNA":
            attr=f[8]; g=gene_of(attr)
            if g not in panel: continue
            mid=re.search(r"ID=([^;]+)",attr)
            mid=mid.group(1) if mid else None
            try: score=float(f[5])
            except: score=0.0
            mrna_gene[mid]=g
            if g not in best or score>best[g][0]:
                best[g]=(score,mid)
    keep={mid for _,mid in best.values()}
    # pass 2: collect CDS children of kept mRNAs
    cds=defaultdict(list)  # mrna_id -> list of (seqid,start,end,strand)
    for line in open(a.gff):
        if line.startswith("#") or not line.strip(): continue
        f=line.rstrip("\n").split("\t")
        if len(f)<9 or f[2]!="CDS": continue
        par=re.search(r"Parent=([^;]+)",f[8])
        par=par.group(1) if par else None
        if par in keep:
            cds[par].append((f[0],int(f[3]),int(f[4]),f[6]))
    genome=load_genome(a.genome)
    n=0
    for g,(score,mid) in best.items():
        parts=sorted(cds.get(mid,[]), key=lambda x:x[1])
        if not parts: continue
        strand=parts[0][3]; seqid=parts[0][0]
        if seqid not in genome: continue
        seq="".join(genome[seqid][s-1:e] for _,s,e,_ in parts)
        if strand=="-": seq=rc(seq)
        outd=os.path.join(a.outdir,g); os.makedirs(outd,exist_ok=True)
        with open(os.path.join(outd,f"{a.species}.cds.fna"),"w") as o:
            o.write(f">{a.species}\n{seq}\n")
        n+=1
    print(f"  [{a.species}] extracted {n} gene CDS (of {len(panel)} panel genes)")

if __name__=="__main__":
    main()
