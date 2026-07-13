#!/usr/bin/env python3
"""Collector for the pig_expansion run.

Post-processes the rebuilt combined tables (report/per_origin_K.csv, report/branch_rates.csv)
to:
  1. add a `category` column (functional group) + ensure `module` (pigmentation/hormone),
     sourced from analysis/module_selection/data/nb14_panel_justification.csv (the notebook-
     authoritative mapping; 110/110 panel genes covered),
  2. write the annotated combined tables into results/perorigin_v1/ (unified 110-gene tables),
  3. emit per-gene incremental files results/pig_expansion/{gene}.per_origin_K.csv and
     {gene}.aBSREL.json for each NEW gene as it lands (Claude Science's per-gene spec).

Idempotent + partial-safe: run it repeatedly as genes finish; it annotates whatever is present.
Run AFTER rebuilding report/ (03_report_summary --per-origin ; robust aBSREL flatten).
"""
import csv, os, json, sys, glob, shutil

REPO = os.path.expanduser("~/pigmentation-gene-network/comparative-genomics")
W = "/scratch/tlasisi_root/tlasisi0/tlasisi/pgn_run117"
JUST = os.path.join(REPO, "analysis/module_selection/data/nb14_panel_justification.csv")
NEW_PANEL = os.path.join(REPO, "config/gene_panel_new.csv")
OUT_COMBINED = os.path.join(REPO, "results/perorigin_v1")
OUT_PERGENE = os.path.join(REPO, "results/pig_expansion")

def load_groups():
    m = {}
    for r in csv.DictReader(open(JUST)):
        m[r["gene"]] = (r.get("module", "?"), r.get("category", "?"))
    return m

def annotate(in_csv, groups, gene_col="gene"):
    """Read a report CSV, insert module+category after the gene column, return (header, rows)."""
    if not os.path.exists(in_csv):
        return None, None
    rows = list(csv.DictReader(open(in_csv)))
    if not rows:
        return [], []
    cols = list(rows[0].keys())
    for extra in ("module", "category"):
        if extra not in cols:
            cols.insert(cols.index(gene_col) + 1, extra)
    for r in rows:
        mod, cat = groups.get(r[gene_col], ("?", "?"))
        r["module"] = mod          # pigmentation / hormone
        r["category"] = cat        # functional group / layer
    return cols, rows

def write_csv(path, cols, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

def main():
    groups = load_groups()
    new_genes = {r["gene"] for r in csv.DictReader(open(NEW_PANEL))}
    os.makedirs(OUT_PERGENE, exist_ok=True)

    # 1+2. annotate the combined tables -> results/perorigin_v1/
    summary = {}
    for name, gcol in (("per_origin_K.csv", "gene"), ("branch_rates.csv", "gene")):
        cols, rows = annotate(os.path.join(W, "report", name), groups, gcol)
        if cols is None:
            print(f"  {name}: report not built yet — skip"); continue
        write_csv(os.path.join(OUT_COMBINED, name), cols, rows)
        genes = sorted({r["gene"] for r in rows})
        summary[name] = (len(rows), len(genes))
        print(f"  {name}: {len(rows)} rows, {len(genes)} genes (annotated w/ module+category) -> perorigin_v1/")
        # 3. per-gene incremental for NEW genes
        for g in sorted(new_genes & set(genes)):
            grows = [r for r in rows if r["gene"] == g]
            write_csv(os.path.join(OUT_PERGENE, f"{g}.{name}"), cols, grows)

    # 3b. per-gene aBSREL JSON copies for new genes that have landed
    n_json = 0
    for g in sorted(new_genes):
        src = os.path.join(W, "absrel", f"{g}.ABSREL.json")
        if os.path.exists(src) and os.path.getsize(src) > 1000:
            shutil.copy(src, os.path.join(OUT_PERGENE, f"{g}.aBSREL.json")); n_json += 1
    print(f"  per-gene aBSREL JSONs emitted: {n_json}/{len(new_genes)}")
    print("DONE ->", summary)

if __name__ == "__main__":
    main()
