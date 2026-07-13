#!/usr/bin/env python3
"""
02c_per_origin_relax.py — per-INDEPENDENT-ORIGIN RELAX.

Script 02 runs ONE pooled RELAX per gene: every dichromatic tip is {Test}, so it can only
detect a shift shared by ALL origins (it presupposes convergent architecture). This driver
instead runs RELAX once per gene PER ORIGIN, to ask whether each independent origin of
dichromatism shifts the SAME genes or DIFFERENT genes — the heterogeneous-architecture test.

Design (per origin i, per gene):
  * Test      = origin i's dichromatic tips        -> tagged {Test}
  * Reference = monochromatic tips                 -> default (untagged)
  * Other origins' dichromatic tips are DROPPED from the tree, so the reference is purely
    monochromatic and origin i's signal is not contaminated by other origins' dichromatism.
  * A gene/origin is only fit if the pruned tree keeps >=4 tips and origin i has >=2 tips
    present in that gene's alignment (single-tip foregrounds are unidentifiable; flagged).

Reuses codon_align + prune_tag_tree from 02_align_and_relax.py so alignment/QC logic is
IDENTICAL to the pooled run. Alignments are reused if aln/<gene>.codon.aln.fa already exists
(produced by script 02); otherwise they are built once here.

Reads:
  aln/<gene>.codon.aln.fa            (reused if present; else built from cds/)
  <panel>  (gene,set)                default gene_panel.csv
  <tree>   primate species tree      default primate_species_tree.nex
  <origins> origin_assignments.csv   columns: species, origin_id  (from the phylo audit)

Writes:
  relax_per_origin/<origin_id>/<gene>.RELAX.json
  relax_per_origin/<origin_id>/<gene>.tagged.nwk
  qc/per_origin/<origin_id>__<gene>.csv          per (origin,gene) QC row (array-merge source)
  report/per_origin_relax.csv                    combined (full sequential run only)

Tools: mafft, hyphy, python(biopython,dendropy) on PATH — same env as script 02.

Usage:
  # single (origin,gene) for a 2-D SLURM array:
  python 02c_per_origin_relax.py --gene TFAP2A --origin origin_2 \
     --panel config/gene_panel.csv --tree config/primate_species_tree.nex \
     --origins config/origin_assignments.csv
  # all origins for one gene:
  python 02c_per_origin_relax.py --gene TFAP2A --origins config/origin_assignments.csv
  # everything (sequential, slow):
  python 02c_per_origin_relax.py --origins config/origin_assignments.csv
"""
import argparse, os, glob, csv, subprocess, importlib.util

# --- import codon_align + prune_tag_tree from the sibling pooled driver ---
_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("_relax02", os.path.join(_here, "02_align_and_relax.py"))
_relax02 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_relax02)
codon_align, prune_tag_tree = _relax02.codon_align, _relax02.prune_tag_tree

def sh(cmd, **kw): return subprocess.run(cmd, check=True, **kw)

def load_origins(path):
    """origin_id -> set(species) ; also all dichromatic species across origins."""
    origins = {}
    for r in csv.DictReader(open(path)):
        oid = r["origin_id"].strip()
        sp = r["species"].strip().replace(" ", "_")
        if not oid or oid.lower() in ("na", "none", ""):
            continue
        origins.setdefault(oid, set()).add(sp)
    all_dich = set().union(*origins.values()) if origins else set()
    return origins, all_dich

def ensure_alignment(gene, cds_dir, aln_dir, gap_col_thresh, outlier_k, threads=1):
    """Reuse aln/<gene>.codon.aln.fa if present (from script 02); else build it."""
    nuc = os.path.join(aln_dir, f"{gene}.codon.aln.fa")
    if os.path.exists(nuc):
        tips = [rec.split()[0][1:] for rec in open(nuc) if rec.startswith(">")]
        return nuc, tips
    built, info = codon_align(gene, cds_dir, aln_dir,
                              gap_col_thresh=gap_col_thresh, outlier_k=outlier_k, threads=threads)
    return built, (info.get("tips") if built else None)

def run_one(gene, oid, origins, all_dich, args):
    nuc, tips = ensure_alignment(gene, args.cds, args.aln, args.gap_col_thresh, args.outlier_k,
                                 threads=int(getattr(args, "threads", 1)))
    row = {"origin_id": oid, "gene": gene}
    if not nuc or not tips:
        row["status"] = "no_alignment"; return row
    tips = set(tips)
    fg = origins[oid] & tips                       # this origin's tips present in the gene
    other = (all_dich - origins[oid]) & tips       # other origins' dichromatic tips -> drop
    keep = [t for t in tips if t not in other]     # monochromatic + this origin only
    row["n_fg"] = len(fg); row["n_tips_kept"] = len(keep); row["n_other_dropped"] = len(other)
    if len(fg) < args.min_fg:
        row["status"] = f"underpowered_fg{len(fg)}"; return row
    if len(keep) < 4:
        row["status"] = "too_few_tips_after_drop"; return row
    odir = os.path.join(args.out, oid); os.makedirs(odir, exist_ok=True)
    treef = os.path.join(odir, f"{gene}.tagged.nwk")
    tf, n_fg = prune_tag_tree(args.tree, keep, fg, treef)
    row["n_foreground_tagged"] = n_fg
    if not tf or n_fg < args.min_fg:
        row["status"] = "tag_failed"; return row
    # prune the alignment to the kept tips so it matches the pruned tree (HyPhy needs identical taxa)
    keepset = set(keep); pruned = os.path.join(odir, f"{gene}.pruned.aln.fa"); _w = False
    with open(nuc) as _fh, open(pruned, "w") as _o:
        for _ln in _fh:
            if _ln.startswith(">"): _w = _ln[1:].strip() in keepset
            if _w: _o.write(_ln)
    outj = os.path.join(odir, f"{gene}.RELAX.json")
    try:
        sh(["hyphy", "CPU=" + str(args.threads), "relax", "--alignment", pruned, "--tree", tf,
            "--test", "Test", "--output", outj, "--code", "Universal"],
           stdout=open(os.path.join(odir, f"{gene}.log"), "w"), stderr=subprocess.STDOUT)
        row["status"] = "ok"; row["relax_json"] = outj
    except subprocess.CalledProcessError:
        row["status"] = "hyphy_failed"
    return row

QC_FIELDS = ["origin_id", "gene", "n_fg", "n_tips_kept", "n_other_dropped",
             "n_foreground_tagged", "status"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cds", default="cds"); ap.add_argument("--aln", default="aln")
    ap.add_argument("--out", default="relax_per_origin"); ap.add_argument("--qc", default="qc/per_origin")
    ap.add_argument("--panel", default="gene_panel.csv")
    ap.add_argument("--tree", default="primate_species_tree.nex")
    ap.add_argument("--origins", default="origin_assignments.csv",
                    help="CSV with columns species,origin_id (from the phylo audit)")
    ap.add_argument("--gene", default=None, help="run only this gene")
    ap.add_argument("--origin", default=None, help="run only this origin_id")
    ap.add_argument("--min-fg", dest="min_fg", type=int, default=2,
                    help="minimum origin tips in a gene to attempt a fit (single-tip fg is unidentifiable)")
    ap.add_argument("--threads", default="4")
    ap.add_argument("--gap-col-thresh", dest="gap_col_thresh", type=float, default=0.3)
    ap.add_argument("--outlier-k", dest="outlier_k", type=float, default=4.0)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True); os.makedirs(a.qc, exist_ok=True); os.makedirs("report", exist_ok=True)

    panel = {r["gene"]: (r.get("set") or r.get("group") or r.get("category") or "?") for r in csv.DictReader(open(a.panel))}
    if a.gene: panel = {g: s for g, s in panel.items() if g == a.gene}
    origins, all_dich = load_origins(a.origins)
    if a.origin: origins = {a.origin: origins[a.origin]}
    print(f"origins: {', '.join(f'{k}(n={len(v)})' for k,v in origins.items())}")

    rows = []
    for gene in panel:
        for oid in origins:
            r = run_one(gene, oid, origins, all_dich, a)
            r["set"] = panel[gene]; rows.append(r)
            with open(os.path.join(a.qc, f"{oid}__{gene}.csv"), "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=QC_FIELDS, extrasaction="ignore")
                w.writeheader(); w.writerow(r)
            print(f"{oid:10s} {gene:10s} fg={r.get('n_fg')} kept={r.get('n_tips_kept')} -> {r.get('status')}")
    if not (a.gene or a.origin):
        with open("report/per_origin_relax.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=QC_FIELDS + ["set"], extrasaction="ignore")
            w.writeheader(); w.writerows(rows)
    print("DONE -> extract K per (origin,gene) with 03_report_summary.py --per-origin")

if __name__ == "__main__": main()
