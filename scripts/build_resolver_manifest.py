#!/usr/bin/env python3
"""Build docs/data/locus_resolver_manifest.json from the committed CSVs.
Run from repo root: python scripts/build_resolver_manifest.py
Deterministic; no network, no kernel. Regenerates the exact manifest the Locus Resolver page reads.
"""
import json, glob
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "data" / "processed"
CR = ROOT / "data" / "case_records"
OUT = ROOT / "docs" / "data" / "locus_resolver_manifest.json"

ln = pd.read_csv(P/"locus_nodes.csv", dtype=str, keep_default_na=False)
le = pd.read_csv(P/"locus_annotation_edges.csv", dtype=str, keep_default_na=False)
nodes = pd.read_csv(P/"gene_network_nodes.csv", dtype=str, keep_default_na=False)
edges = pd.read_csv(P/"gene_network_edges.csv", dtype=str, keep_default_na=False)
cls = pd.read_csv(P/"discordance_case_classification.csv")
cov = pd.read_csv(P/"case_gene_coverage_master.csv")

GLOSS = {
 "D1":"genotype-present, phenotype-absent (canonical causal variant present, phenotype absent - reduced penetrance; modifier nodes block the path)",
 "D2":"phenotype-present, genotype-absent (phenotype without the canonical variant - an alternative gene/route reaches the endpoint)",
 "both":"both D1 and D2 evidence catalogued for this gene",
 "mixed":"direction varies across the papers citing this gene",
}

def locus_obj(lid):
    r = ln[ln.locus_id==lid].iloc[0]
    return {c: r[c] for c in ln.columns}

def edges_for(lid):
    return le[le.locus_id==lid].to_dict("records")

def subgraph(gene):
    e = edges[(edges.source==gene)|(edges.target==gene)]
    gset = {gene} | set(e.source) | set(e.target)
    n = nodes[nodes.gene.isin(gset)]
    return {"nodes":[{"id":r.gene,"kind":"gene","node_class":r.node_class,"citation":r.citation} for r in n.itertuples()],
            "edges":[{"source":r.source,"target":r.target,"sign":r.sign,"edge_class":r.edge_class,"citation":r.citation} for r in e.itertuples()]}

def case_text(pattern, rsid=None, needles=()):
    f = glob.glob(str(CR/f"EXTRACT_{pattern}*.csv"))
    if not f: return {}
    d = pd.read_csv(f[0], dtype=str, keep_default_na=False)
    ec = [c for c in d.columns if "effect" in c.lower() or "assoc" in c.lower()][0]
    out = {}
    sub = d[d.get("rsid","")==rsid] if rsid else d
    for _, row in sub.iterrows():
        for key, nd in needles:
            if nd in row[ec]:
                out[key] = row[ec]
    return out

# NOTE: the two worked examples are curated (which loci, which case quotes). This builder reproduces the
# manifest for THOSE examples from the committed files; extending to more examples means adding entries here.
manifest = {
 "schema_version":"1.0",
 "generated_by":"scripts/build_resolver_manifest.py",
 "direction_gloss":GLOSS,
 "provenance":{
   "locus_nodes":"data/processed/locus_nodes.csv",
   "locus_annotation_edges":"data/processed/locus_annotation_edges.csv",
   "backbone_nodes":"data/processed/gene_network_nodes.csv",
   "backbone_edges":"data/processed/gene_network_edges.csv",
   "case_direction":"data/processed/discordance_case_classification.csv + case_gene_coverage_master.csv",
   "case_text":"data/case_records/EXTRACT_*.csv"},
 "caveats":[
   "OCA2 has a single backbone edge (MITF->OCA2); HERC2 is not a backbone node. D1/D2 are NOT computed by graph traversal - they are the pre-registered, cited case classification. The network panel DISPLAYS the subgraph as mechanistic context, it does not derive direction.",
   "rs12913832 and rs1800401 positions are in DIFFERENT genome builds (GRCh38 vs GRCh37); display the shared cytoband 15q13.1 rather than bare bp, or liftover first.",
   "rs12913832 was NOT genome-wide significant in the Ang2023 Kalinago cohort (P_adj=0.075); the HERC2->OCA2 enhancer mechanism is the cited external finding (PMID:22234890, Visser 2012), not a Kalinago result."],
 "examples":[]
}

# Example 1: HERC2/OCA2 eye colour
oca2_gene_dir = cov[cov.gene=="OCA2"]["case_discordance_direction"].iloc[0]
pos_txt = case_text("Pospiech2016", rsid=None, needles=[("association","OR 0.031"),("penetrance_gap","NOT blue-eyed")])
manifest["examples"].append({
 "id":"herc2_oca2_eye",
 "title":"rs12913832: HERC2-labelled, OCA2-regulating (eye colour)",
 "thesis":"The SNP's nearest-gene label (HERC2) is not its functional target (OCA2). A naive nearest-gene tool stops at HERC2; the cited regulatory evidence redirects to OCA2, which is in the mechanistic network.",
 "locus":locus_obj("rs12913832"),
 "annotation_edges":edges_for("rs12913832"),
 "subgraph":subgraph("OCA2"),
 "resolved_target_in_network":True,
 "nearest_gene_in_network":False,
 "direction":{"gene":"OCA2","label":oca2_gene_dir,"gloss":GLOSS.get(oca2_gene_dir,""),
   "detail":"D1 illustration in this locus: Pospiech2016 reports the CC (blue-associated) genotype is incompletely penetrant - a fraction of CC individuals are NOT blue-eyed (genotype-present, phenotype-absent).",
   "source":"discordance_case_classification.csv (OCA2 direction); Pospiech2016 IrisPlex extract",
   "citation":"Pospiech2016 Int J Legal Med (IrisPlex population); OCA2 direction from case classification"},
 "case_text":{**pos_txt,"source":"EXTRACT_Pospiech2016_IntJLegalMed_IrisPlex_population"}})

# Example 2: Kalinago OCA2 (paper-level 'both' vs gene-level 'mixed')
ang_dir = cls[cls.paper.str.contains("Ang2023")]["discordance_direction"].iloc[0]
kal = case_text("Ang2023", rsid="rs1800401", needles=[("R305W_D1","NOT causal")])
kal2 = case_text("Ang2023", rsid="rs797044784", needles=[("NW273KV_D2","CAUSAL")])
manifest["examples"].append({
 "id":"kalinago_oca2",
 "title":"Kalinago OCA2: R305W (D1) and NW273KV (D2) in one case (Ang 2023)",
 "thesis":"Both discordance directions appear at one in-network gene. R305W is correctly OCA2-labelled and predicted-pathogenic yet non-penetrant (D1). The albino individuals carry no catalogued OCA2 variant, only the novel NW273KV a standard panel would miss (D2).",
 "locus":locus_obj("rs1800401"),
 "locus_secondary":locus_obj("rs797044784"),
 "annotation_edges":edges_for("rs1800401")+edges_for("rs797044784"),
 "subgraph":subgraph("OCA2"),
 "resolved_target_in_network":True,
 "nearest_gene_in_network":True,
 "direction":{"gene":"OCA2","label":ang_dir,"label_scope":"paper-level (Ang2023)",
   "gloss":GLOSS.get(ang_dir,""),"gene_level_label":oca2_gene_dir,
   "gene_level_note":"OCA2's direction ACROSS ALL citing papers is 'mixed'; WITHIN Ang2023 specifically it is 'both' (D1 via R305W + D2 via NW273KV). Complementary, not contradictory.",
   "detail":"D1 = R305W predicted-pathogenic yet no effect once NW273KV controlled. D2 = albinism traces to the novel NW273KV, not any catalogued OCA2 variant.",
   "source":"Ang2023 paper-level (discordance_case_classification.csv); OCA2 gene-level (case_gene_coverage_master.csv)",
   "citation":"Ang2023 eLife 10.7554/eLife.77514"},
 "case_text":{**kal,**kal2,"source":"EXTRACT_Ang2023_eLife_Kalinago (Main Table 1, Table 2, Appendix 1-table 5)"}})

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(manifest, indent=2))
print(f"wrote {OUT} ({OUT.stat().st_size} bytes); {len(manifest['examples'])} examples")
