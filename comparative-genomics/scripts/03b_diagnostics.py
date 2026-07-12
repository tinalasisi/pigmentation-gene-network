#!/usr/bin/env python3
"""
03b_diagnostics.py — certification diagnostics over staged pipeline outputs.

Reads (run workdir): aln/<gene>.codon.aln.fa, relax/<gene>.RELAX.json,
  annot/<species>.miniprot.gff, qc/alignment_qc.csv
Reads (repo): refs/reference_proteins.faa, config/species_states.csv,
  config/<accessions>.csv (for extraction method direct/miniprot)
Writes (report/): tip_roster.csv, extraction_qc.csv, fit_health.csv

All outputs are small text; no raw sequence leaves. Purpose: tell whether the
foreground is real and whether a hit is a fit/alignment artifact — the checks
that can't be done from SUMMARY.md alone.
"""
import argparse, os, glob, json, csv, re, sys

def read_states(path):
    st = {}
    for r in csv.DictReader(open(path)):
        st[r["species"].replace(" ", "_")] = r.get("dichromatism", "")
    return st

def read_methods(accessions_globs):
    """species -> 'direct' | 'miniprot' from the accessions CSV(s) annotated flag."""
    m = {}
    for g in accessions_globs:
        for path in glob.glob(g):
            if not os.path.exists(path): continue
            for r in csv.DictReader(open(path)):
                sp = r.get("species", r.get("chosen_accession", "")).replace(" ", "_")
                ann = str(r.get("annotated", "")).strip().lower()
                m[sp] = "direct" if ann == "true" else "miniprot"
    return m

def ref_lengths(faa):
    """longest reference protein per gene -> approx CDS nt length (aa*3)."""
    best = {}
    cur, curlen = None, 0
    def flush(g, l):
        if g and l > best.get(g, 0): best[g] = l
    for line in open(faa):
        if line.startswith(">"):
            flush(cur, curlen)
            cur = line[1:].split("|")[0].strip(); curlen = 0
        else:
            curlen += len(line.strip())
    flush(cur, curlen)
    return {g: l * 3 for g, l in best.items()}

def aln_info(aln_path):
    """return (tips list, alignment length in nt)."""
    tips, seqs, cur = [], {}, None
    for line in open(aln_path):
        line = line.rstrip("\n")
        if line.startswith(">"):
            cur = line[1:].strip(); tips.append(cur); seqs[cur] = ""
        elif cur is not None:
            seqs[cur] += line
    L = len(next(iter(seqs.values()))) if seqs else 0
    return tips, L

def parse_miniprot_identity(gff_path):
    """gene -> best-hit %identity (from the max-score mRNA for that gene)."""
    best = {}  # gene -> (score, identity)
    if not os.path.exists(gff_path): return best
    for line in open(gff_path):
        if line.startswith("#") or "\tmRNA\t" not in line: continue
        f = line.rstrip("\n").split("\t")
        if len(f) < 9: continue
        try: score = float(f[5])
        except: score = 0.0
        attrs = f[8]
        mident = re.search(r"Identity=([0-9.]+)", attrs)
        mtgt = re.search(r"Target=([^\s;]+)", attrs)
        if not mtgt: continue
        gene = mtgt.group(1).split("|")[0]
        ident = float(mident.group(1)) if mident else None
        if gene not in best or score > best[gene][0]:
            best[gene] = (score, ident)
    return {g: v[1] for g, v in best.items()}

LENGTH_KEYS = ["RELAX alternative", "MG94xREV with separate rates for branch sets",
               "Global MG94xREV", "unconstrained", "Nucleotide GTR"]

def branch_len(attrs):
    for k in LENGTH_KEYS:
        if k in attrs:
            try: return float(attrs[k])
            except: pass
    for v in attrs.values():
        if isinstance(v, (int, float)): return float(v)
    return 0.0

def fit_health(json_path):
    try: j = json.load(open(json_path))
    except Exception: return None
    tr = j.get("test results", {})
    ba = j.get("branch attributes", {}).get("0", {})
    tested = j.get("tested", {}).get("0", {})
    fg = sum(branch_len(ba[b]) for b in ba if tested.get(b, "").lower() == "test")
    tot = sum(branch_len(ba[b]) for b in ba)
    K = tr.get("relaxation or intensification parameter")
    p = tr.get("p-value")
    lrt = tr.get("LRT")
    # converged proxy: finite p + LRT present + non-degenerate fg branch length
    degenerate = (fg < 1e-3) or (isinstance(K, (int, float)) and (K < 1e-4 or K > 100))
    return dict(K=K, p=p, LRT=lrt, fg_branch_len=round(fg, 5),
                tree_len=round(tot, 5), degenerate=degenerate)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", default=".")
    ap.add_argument("--repo", default=os.path.expanduser("~/pigmentation-gene-network/comparative-genomics"))
    a = ap.parse_args()
    W, R = a.workdir, a.repo
    os.makedirs(os.path.join(W, "report"), exist_ok=True)

    states = read_states(os.path.join(R, "config", "species_states.csv"))
    methods = read_methods([os.path.join(R, "config", "accessions_gibbon_flagship.csv"),
                            os.path.join(R, "config", "accessions_all_recoverable.csv")])
    reflen = ref_lengths(os.path.join(R, "refs", "reference_proteins.faa"))
    # per-species miniprot identity tables
    ident = {}  # species -> {gene: identity}
    for gff in glob.glob(os.path.join(W, "annot", "*.miniprot.gff")):
        sp = os.path.basename(gff).replace(".miniprot.gff", "")
        ident[sp] = parse_miniprot_identity(gff)

    # tip_roster + extraction_qc
    tr_rows, eq_rows = [], []
    for aln in sorted(glob.glob(os.path.join(W, "aln", "*.codon.aln.fa"))):
        gene = os.path.basename(aln).replace(".codon.aln.fa", "")
        tips, L = aln_info(aln)
        rl = reflen.get(gene, "")
        ratio = round(L / rl, 3) if rl else ""
        for sp in tips:
            tr_rows.append(dict(gene=gene, species=sp, state=states.get(sp, "?")))
            meth = methods.get(sp, "?")
            pid = ident.get(sp, {}).get(gene, "") if meth == "miniprot" else ""
            eq_rows.append(dict(gene=gene, species=sp, state=states.get(sp, "?"),
                                method=meth, pct_identity=pid, aln_len=L,
                                ref_len=rl, aln_ref_ratio=ratio,
                                ratio_flag=("HIGH" if (ratio != "" and ratio > 1.2) else "")))

    # fit_health (join RELAX + qc gaps)
    qc = {}
    qc_path = os.path.join(W, "qc", "alignment_qc.csv")
    if os.path.exists(qc_path):
        qc = {r["gene"]: r for r in csv.DictReader(open(qc_path))}
    fh_rows = []
    for jf in sorted(glob.glob(os.path.join(W, "relax", "*.RELAX.json"))):
        gene = os.path.basename(jf).split(".")[0]
        fh = fit_health(jf)
        if fh is None: continue
        q = qc.get(gene, {})
        aln = os.path.join(W, "aln", f"{gene}.codon.aln.fa")
        L = aln_info(aln)[1] if os.path.exists(aln) else ""
        rl = reflen.get(gene, "")
        ratio = round(L / rl, 3) if (rl and L) else ""
        flags = []
        K = fh["K"]
        if isinstance(K, (int, float)) and (K < 1e-4 or K > 100): flags.append("K_boundary")
        if fh["fg_branch_len"] < 0.01: flags.append("near_zero_fg")
        if fh["tree_len"] > 5: flags.append("branch_len_blowup")
        try:
            if int(float(q.get("n_foreground", 0))) < 3: flags.append("low_power")
        except: pass
        if ratio != "" and ratio > 1.2: flags.append("aln_gt_1.2x_ref")
        try:
            if float(q.get("pct_gaps", 0)) > 20: flags.append("gaps_gt_20pct")
        except: pass
        fh_rows.append(dict(gene=gene, set=q.get("set", ""), K=fh["K"], p=fh["p"],
                            n_tips=q.get("n_tips", ""), n_fg=q.get("n_foreground", ""),
                            fg_branch_len=fh["fg_branch_len"], tree_len=fh["tree_len"],
                            pct_gaps=q.get("pct_gaps", ""), aln_ref_ratio=ratio,
                            flags="|".join(flags) if flags else "clean"))

    def dump(path, rows, cols):
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
            for r in rows: w.writerow({c: r.get(c, "") for c in cols})

    dump(os.path.join(W, "report", "tip_roster.csv"), tr_rows, ["gene", "species", "state"])
    dump(os.path.join(W, "report", "extraction_qc.csv"), eq_rows,
         ["gene", "species", "state", "method", "pct_identity", "aln_len", "ref_len", "aln_ref_ratio", "ratio_flag"])
    dump(os.path.join(W, "report", "fit_health.csv"), fh_rows,
         ["gene", "set", "K", "p", "n_tips", "n_fg", "fg_branch_len", "tree_len", "pct_gaps", "aln_ref_ratio", "flags"])

    # brief console certification of the BH-significant / flagged genes
    print(f"tip_roster: {len(tr_rows)} rows | extraction_qc: {len(eq_rows)} rows | fit_health: {len(fh_rows)} genes")
    print("\nfit_health flags (non-clean):")
    for r in sorted(fh_rows, key=lambda x: (x["flags"] == "clean", x["gene"])):
        if r["flags"] != "clean":
            print(f"  {r['gene']:9s} K={r['K']} fg_bl={r['fg_branch_len']} gaps={r['pct_gaps']} ratio={r['aln_ref_ratio']} -> {r['flags']}")

if __name__ == "__main__":
    main()
