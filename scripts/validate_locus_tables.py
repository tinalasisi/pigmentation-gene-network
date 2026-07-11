#!/usr/bin/env python3
"""Acceptance test for the locus annotation tables (Locus Resolver MVP).
Run from repo root: python scripts/validate_locus_tables.py
Exits 0 on success, 1 on any failure. No network, no kernel needed.
"""
import sys, pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "data" / "processed"
VOCAB = {"nearest_gene_link","regulatory_target","eQTL_target","in_LD_with","dark_matter_association"}

def fail(msg):
    print("FAIL:", msg); sys.exit(1)

ns = pd.read_csv(P / "locus_nodes.csv", dtype=str, keep_default_na=False)
es = pd.read_csv(P / "locus_annotation_edges.csv", dtype=str, keep_default_na=False)

# controlled vocabulary
bad = set(es["edge_type"]) - VOCAB
if bad: fail(f"edge_type outside controlled vocab: {bad}")

# mandatory, non-blank citation on every annotation edge
if (es["evidence_citation"].str.strip() == "").any():
    fail("blank evidence_citation in locus_annotation_edges.csv")

# every node carries a gene_label_basis
if (ns["gene_label_basis"].str.strip() == "").any():
    fail("blank gene_label_basis in locus_nodes.csv")

# every position that is present must declare a genome_build
if "genome_build" in ns.columns:
    has_pos = ns["position"].str.strip() != ""
    if (has_pos & (ns["genome_build"].str.strip() == "")).any():
        fail("a locus has a position but no genome_build")

# referential integrity: every edge locus_id exists in nodes
missing = set(es["locus_id"]) - set(ns["locus_id"])
if missing: fail(f"edge references unknown locus_id: {missing}")

# the walled-off invariant: no locus row may leak into the mechanistic backbone
be = pd.read_csv(P / "gene_network_edges.csv", dtype=str, keep_default_na=False)
if "locus_id" in be.columns: fail("gene_network_edges.csv contaminated with a locus_id column")
leak = set(ns["locus_id"]) & (set(be["source"]) | set(be["target"]))
if leak: fail(f"rsID appears as a backbone node: {leak}")

print(f"OK: {len(ns)} loci, {len(es)} annotation edges; vocab clean; "
      f"citations present; builds declared; no backbone contamination.")
sys.exit(0)
