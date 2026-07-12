#!/usr/bin/env python3
"""
05_polysel_geneset.py — gene-SET (pathway/network) enrichment of selection scores.

The paper's central claim is a SET-level question: does the PIGMENTATION network
as a whole carry more dichromatism-associated selection than the HORMONE network
as a whole? Per-gene RELAX/aBSREL answers this gene-by-gene and dies to multiple
testing (the PoC: nothing survived BH). SUMSTAT (Daub et al. 2013 MBE
doi:10.1093/molbev/mst080; primate application 2017 PMC5435107) instead SUMS a
per-gene selection score within a gene set and tests the set against a null built
by resampling genes — detecting a coordinated, diffuse (polygenic) shift even when
no single gene is individually significant. This is the pleiotropy-dilution-robust
test for the two-network contrast.

Per-gene score used (in priority order, whatever is available):
  1. RELAX:   -log10(p) signed by direction of K  (intensified +, relaxed -)
              -> tests DIRECTIONAL selection-intensity shift on dichromatic lineages
  2. aBSREL:  gene-level max branch LRT among dichromatic (foreground) branches
              (from report/branch_rates.csv), as -log10(corrected p)
  3. |log2 K| (unsigned magnitude) as a fallback score

SUMSTAT statistic per set = sum of per-gene scores. Null = resample same-size
random gene sets from the SCORED BACKGROUND. Because our panel is only 80 genes,
the honest background is the full pigmentation NETWORK (803 genes) if scores exist
for them; with only the 80-gene panel scored, we instead do a
pigmentation-vs-hormone LABEL PERMUTATION (shuffle set labels among scored genes)
— which is the correct within-panel test and is stated as such in the output.

INPUT:
  report/relax_results.csv   (gene,set,K,p_value,...)  from 03
  report/branch_rates.csv    (optional, from 02b)      for aBSREL scoring
  gene_panel.csv             (gene,set)
  --network_scores <csv>     (optional) gene,score for the full 803-gene network
OUTPUT:
  report/polysel_geneset.csv     per-set SUMSTAT, null mean/sd, empirical p, z
  report/polysel_pergene.csv     per-gene score used (audit trail)
  report/SUMSTAT_SUMMARY.md      one-paragraph verdict, paste-able
"""
import argparse, os, csv, math, random, json
random.seed(20260712)

def read_csv(path):
    with open(path) as f: return list(csv.DictReader(f))

def relax_score(r):
    try:
        K=float(r["K"]); p=float(r["p_value"])
    except (TypeError, ValueError, KeyError): return None
    if p<=0: p=1e-300
    mag=-math.log10(max(p,1e-300))
    return mag if K>=1 else -mag   # signed by intensified(+)/relaxed(-)

def load_scores(args):
    """Return {gene: score}, {gene: set}, method_label."""
    panel={r["gene"]:r["set"] for r in read_csv(args.panel)}
    # priority 1: RELAX signed -log10 p
    if os.path.exists(args.relax):
        rows=read_csv(args.relax); sc={}
        for r in rows:
            s=relax_score(r)
            if s is not None: sc[r["gene"]]=s
        if len(sc)>=6:
            return sc, panel, "RELAX signed -log10(p) [intensified +, relaxed -]"
    # priority 2: aBSREL foreground max branch -log10(corrected p)
    if os.path.exists(args.branch):
        rows=read_csv(args.branch); byg={}
        for r in rows:
            if r.get("tested")!="True": continue
            try: cp=float(r["absrel_corrected_p"])
            except (TypeError,ValueError): continue
            g=r["gene"]; byg.setdefault(g,[]).append(-math.log10(max(cp,1e-300)))
        sc={g:max(v) for g,v in byg.items() if v}
        if len(sc)>=6:
            return sc, panel, "aBSREL foreground max branch -log10(corrected p)"
    raise SystemExit("No usable per-gene scores found (need report/relax_results.csv or branch_rates.csv).")

def sumstat_test(scores, panel, network_csv=None, n_perm=100000):
    sets={}
    for g,s in scores.items():
        st=panel.get(g,"?"); sets.setdefault(st,[]).append(s)
    scored_genes=list(scores)
    results=[]
    if network_csv and os.path.exists(network_csv):
        # true SUMSTAT: resample same-size sets from the network background
        bg={r["gene"]:float(r["score"]) for r in read_csv(network_csv) if r.get("score")}
        bg_vals=list(bg.values()); mode="network-background resampling"
        for st,vals in sets.items():
            obs=sum(vals); k=len(vals)
            null=[sum(random.sample(bg_vals,k)) for _ in range(n_perm)] if k<=len(bg_vals) else []
            results.append(_emp(st,obs,k,null,mode))
    else:
        # within-panel LABEL PERMUTATION between pigmentation & hormone
        mode="within-panel label permutation (pigmentation vs hormone)"
        allv=[scores[g] for g in scored_genes]
        for st,vals in sets.items():
            obs=sum(vals); k=len(vals)
            null=[sum(random.sample(allv,k)) for _ in range(n_perm)]
            results.append(_emp(st,obs,k,null,mode))
    return results, mode

def _emp(st,obs,k,null,mode):
    if null:
        mu=sum(null)/len(null)
        sd=(sum((x-mu)**2 for x in null)/len(null))**0.5 or 1e-9
        p_hi=(1+sum(1 for x in null if x>=obs))/(1+len(null))
        p_lo=(1+sum(1 for x in null if x<=obs))/(1+len(null))
        z=(obs-mu)/sd
    else:
        mu=sd=z=float("nan"); p_hi=p_lo=float("nan")
    return {"set":st,"n_genes":k,"sumstat":round(obs,4),"null_mean":round(mu,4),
            "null_sd":round(sd,4),"z":round(z,3),
            "p_enriched_high":round(p_hi,5),"p_enriched_low":round(p_lo,5),"null_mode":mode}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--relax",default="report/relax_results.csv")
    ap.add_argument("--branch",default="report/branch_rates.csv")
    ap.add_argument("--panel",default="gene_panel.csv")
    ap.add_argument("--network_scores",default=None)
    ap.add_argument("--n_perm",type=int,default=100000)
    a=ap.parse_args()
    os.makedirs("report",exist_ok=True)
    scores,panel,method=load_scores(a)
    with open("report/polysel_pergene.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(["gene","set","score"])
        for g,s in sorted(scores.items(),key=lambda x:-x[1]):
            w.writerow([g,panel.get(g,"?"),round(s,4)])
    results,mode=sumstat_test(scores,panel,a.network_scores,a.n_perm)
    cols=["set","n_genes","sumstat","null_mean","null_sd","z","p_enriched_high","p_enriched_low","null_mode"]
    with open("report/polysel_geneset.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(results)
    # verdict
    d={r["set"]:r for r in results}
    lines=["# SUMSTAT gene-set selection enrichment","",
           f"Per-gene score: **{method}**","",
           f"Null model: **{mode}**, {a.n_perm:,} permutations","",
           "| set | n | SUMSTAT | null mean | z | p(enriched, high) |",
           "|---|---|---|---|---|---|"]
    for r in results:
        lines.append(f"| {r['set']} | {r['n_genes']} | {r['sumstat']} | {r['null_mean']} | {r['z']} | {r['p_enriched_high']} |")
    if "pigmentation" in d and "hormone" in d:
        pz,hz=d["pigmentation"]["z"],d["hormone"]["z"]
        lines += ["", f"**Contrast:** pigmentation z={pz}, hormone z={hz}. "
                  + ("Pigmentation network carries the stronger directional selection signal."
                     if (isinstance(pz,float) and isinstance(hz,float) and pz>hz)
                     else "Hormone network carries the stronger directional selection signal."
                     if (isinstance(pz,float) and isinstance(hz,float)) else "Insufficient scores for a contrast.")]
    lines += ["","*Caveat:* within-panel permutation tests whether one set's summed score exceeds",
              "the other's given the pooled score distribution. A true genome/network background",
              "(--network_scores gene,score for all 803 pigmentation genes) makes this a full SUMSTAT",
              "test rather than a two-set contrast; supply it once network-wide scores exist."]
    open("report/SUMSTAT_SUMMARY.md","w").write("\n".join(lines))
    print("\n".join(lines))

if __name__=="__main__": main()
