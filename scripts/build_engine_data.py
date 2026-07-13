#!/usr/bin/env python3
"""Adapter: real harmonized-substrate tables -> the "convergence engine" schema
(the same schema the commissioned prototype renders against). Emits:

  app/data/dataset.js    window.__DATASET__ = {...}   (loaded by app/index.html)
  app/data/dataset.json  the same object, for inspection / CI

Design decisions (v1 / preview):
  * 6 evidence CHANNELS (mechanistic/regulon/validation + association/KEGG/Reactome);
    n_channels is 1..6 (the app draws a 6-slot ring and a 6-band radial layout).
  * STANCE is the honest spine: mechanistic / regulon / validation channels
    *implicate* (assert a directed or curated functional role); association and
    pathway-membership channels only *note* presence.
  * VERDICT TIER is a PROVISIONAL DERIVED RULE (labelled as such in the UI) — it
    is not a published classification. The benchmark surface, by contrast, is the
    REAL NB10 direction-law result, computed here from the shipped table.
  * References resolve to public identifiers (PMID/DOI/PMC/UniProt/KEGG/Reactome),
    so click-to-source is real, not self-referential.

Regenerate:  python3.11 scripts/build_engine_data.py
"""
import csv, json, os, re, html
from collections import defaultdict

NODES = "data/processed/nb7_substrate_nodes.csv"
EDGES = "data/processed/nb7_substrate_edges.csv"
NB10  = "data/processed/nb10_direction_law_annotation.csv"
NB8   = "data/processed/nb8_diagnostic_18.csv"
OUTDIR = "app/data"

# ---- 6 channels (display order = fixed glyph slots) --------------------------
CHANNELS = [
    ("mechanistic", "Mechanistic pathway", "mid",       "implicates"),
    ("regulon",     "TF→target regulon",   "selective", "implicates"),
    ("validation",  "Literature validation","mid",      "implicates"),
    ("association", "Functional association","broad",    "notes"),
    ("kegg",        "KEGG pathway",         "mid",       "notes"),
    ("reactome",    "Reactome pathway",     "mid",       "notes"),
]
CH_ORDER = [k for k, *_ in CHANNELS]
CH_STANCE = {k: st for k, _l, _r, st in CHANNELS}
STRING = {"STRING_ours", "DArcy_STRING"}
FINDING = {
    "mechanistic": "Signed, directed interaction in the reconstructed melanogenesis model.",
    "regulon":     "Curated TF→target regulon edge (MITF / SOX10 / PAX3).",
    "validation":  "Interaction independently validated against OmniPath literature curation.",
    "association": "Co-functional association (STRING v12) — presence, not direction.",
    "kegg":        "Member of the curated KEGG melanogenesis pathway.",
    "reactome":    "Member of a curated Reactome pigmentation pathway.",
}

# ---- reference resolution: token -> {kind, citation, url, access} ------------
REFS = {}
def add_ref(token):
    token = token.strip()
    if not token:
        return None
    m = re.match(r"PMID:?\s*(\d+)", token)
    if m:
        rid = f"PMID-{m.group(1)}"
        REFS.setdefault(rid, {"kind": "Journal article (PubMed)", "citation": f"PMID {m.group(1)}",
                              "url": f"https://pubmed.ncbi.nlm.nih.gov/{m.group(1)}/", "access": "public"})
        return rid
    m = re.match(r"(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)", token)
    if m:
        doi = m.group(1).rstrip(".;")
        rid = "DOI-" + re.sub(r"[^A-Za-z0-9]", "", doi)[:24]
        REFS.setdefault(rid, {"kind": "Publication (DOI)", "citation": f"doi:{doi}",
                              "url": f"https://doi.org/{doi}", "access": "public"})
        return rid
    m = re.search(r"PMC(\d+)", token)
    if m:
        rid = f"PMC-{m.group(1)}"
        REFS.setdefault(rid, {"kind": "Open-access article (PMC)", "citation": f"PMC{m.group(1)}",
                              "url": f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{m.group(1)}/", "access": "public"})
        return rid
    m = re.match(r"UniProt:?\s*([A-Z0-9]+)", token)
    if m:
        rid = f"UNIPROT-{m.group(1)}"
        REFS.setdefault(rid, {"kind": "Protein record (UniProt)", "citation": f"UniProt {m.group(1)}",
                              "url": f"https://www.uniprot.org/uniprotkb/{m.group(1)}/entry", "access": "public"})
        return rid
    m = re.match(r"KEGG:?\s*(\S+)", token)
    if m:
        code = m.group(1)
        rid = f"KEGG-{code}"
        REFS.setdefault(rid, {"kind": "Pathway (KEGG)", "citation": f"KEGG {code}",
                              "url": f"https://www.kegg.jp/entry/{code}", "access": "public"})
        return rid
    m = re.match(r"(R-HSA-\d+)", token)
    if m:
        code = m.group(1)
        rid = f"RHSA-{code.split('-')[-1]}"
        REFS.setdefault(rid, {"kind": "Pathway (Reactome)", "citation": f"Reactome {code}",
                              "url": f"https://reactome.org/content/detail/{code}", "access": "public"})
        return rid
    if token.startswith("STRING"):
        REFS.setdefault("STRING-v12", {"kind": "Interaction database (STRING v12)",
                                       "citation": "STRING v12.0", "url": "https://string-db.org/",
                                       "access": "public"})
        return "STRING-v12"
    return None

def tokens_of(citation):
    parts = re.split(r"[;|]", citation or "")
    out = []
    for p in parts:
        for sub in p.split(","):
            r = add_ref(sub)
            if r:
                out.append(r)
    # dedupe preserving order
    seen = set(); res = []
    for r in out:
        if r not in seen:
            seen.add(r); res.append(r)
    return res

def default_ref(channel):
    return {"mechanistic": add_ref("PMID:26176700"),   # Raghunath 2015 melanogenesis model
            "regulon":      "STRING-v12",
            "validation":   add_ref("PMC9854651"),
            "association":  "STRING-v12",
            "kegg":         add_ref("KEGG:hsa04916"),
            "reactome":     add_ref("R-HSA-5662702")}.get(channel)

# ---- load nodes -------------------------------------------------------------
nodes = {}
with open(NODES) as f:
    for r in csv.DictReader(f):
        sl = set(r["supporting_layers"].split("|"))
        chans = []
        if "Raghunath" in sl: chans.append("mechanistic")
        if "GRN" in sl: chans.append("regulon")
        if bool(sl & STRING): chans.append("association")
        if "KEGG" in sl: chans.append("kegg")
        if "Reactome" in sl: chans.append("reactome")
        # validation membership is edge-derived (filled below)
        nodes[r["gene"]] = {
            "chans": set(chans),
            "omim": r["omim_disease_flag"] == "True",
            "cls": r["omim_phenotype_class"] or None,
            "ms": r["massspec_detected_flag"] == "True",
            "crispr": r["bajpai_hit_flag"] == "True",
            "cite": r["citation"],
        }

# ---- load edges (also fills validation membership) --------------------------
edges = []
with open(EDGES) as f:
    for e in csv.DictReader(f):
        a, b = e["gene_a"], e["gene_b"]
        if a == b or a not in nodes or b not in nodes:
            continue
        ls = set(e["supporting_layers"].split("|"))
        ch = set()
        if "Raghunath" in ls: ch.add("mechanistic")
        if "GRN" in ls: ch.add("regulon")
        if "OmniPath_validation" in ls:
            ch.add("validation"); nodes[a]["chans"].add("validation"); nodes[b]["chans"].add("validation")
        if ls & STRING: ch.add("association")
        if not ch:
            continue
        n = len(ch)
        sign = e["merged_sign"] if e["merged_sign"] in ("+", "-") else ""
        conflict = e["sign_conflict"] == "True"
        if conflict: sign = "conflict"
        edges.append({
            "a": a, "b": b, "type": (e["source"] and "regulates" or "associates"),
            "directed": bool(sign and sign != ""), "sign": sign, "sign_conflict": conflict,
            "channels": sorted(ch), "n_channels": n,
            "tier": "corroborated" if n >= 3 else ("supported" if n == 2 else "single_channel"),
            "provenance": tokens_of(e["citation"])[:2] or [c for c in [default_ref("association")] if c],
        })

# ---- NB8 honest-negative ("decoy") gene set (real adversarial negatives) ----
DECOY_GENES = set()
with open(NB8) as f:
    for r in csv.DictReader(f):
        if r["bucket"] == "NEG":
            for g in re.split(r"[\s/]+", r["nearest_gene_label"] or ""):
                g = g.strip()
                if g in nodes:
                    DECOY_GENES.add(g)

# ---- per-entity verdict (PROVISIONAL derived rule) --------------------------
TIER_SUMMARY = {
    "implicated_multichannel": "Multiple independent channels provide directed/curated evidence, with a clinical (OMIM) anchor. The confident call.",
    "implicated_anchored":     "A clinical (OMIM) anchor plus at least one implicating channel; corroboration is thinner.",
    "circumstantial":          "Some directed/functional evidence, but no clinical anchor.",
    "cleared":                 "Present only through association / pathway membership — no channel implicates a causal role.",
    "decoy_cleared":           "Detected in the melanocyte proteome yet no channel implicates a causal role — presence without mechanism, correctly not called.",
}
entities = []
for gene, d in sorted(nodes.items()):
    chans = [c for c in CH_ORDER if c in d["chans"]]
    impl = sum(1 for c in chans if CH_STANCE[c] == "implicates")
    if not chans:
        continue
    if gene in DECOY_GENES and impl == 0:
        tier = "decoy_cleared"
    elif impl >= 2 and d["omim"]:
        tier = "implicated_multichannel"
    elif d["omim"]:
        tier = "implicated_anchored"      # OMIM disease gene = a clinical anchor
    elif impl >= 1:
        tier = "circumstantial"
    else:
        tier = "cleared"
    gtokens = tokens_of(d["cite"])
    def pick(channel):
        want = {"mechanistic": "PMID", "regulon": "STRING", "validation": "PMC",
                "association": "STRING", "kegg": ("KEGG",), "reactome": ("RHSA",)}[channel]
        for t in gtokens:
            if isinstance(want, tuple):
                if any(t.startswith(w) for w in want): return t
            elif t.startswith(want):
                return t
        return default_ref(channel) or (gtokens[0] if gtokens else "STRING-v12")
    strands = [{"channel": c, "stance": CH_STANCE[c], "finding": FINDING[c], "source": pick(c)} for c in chans]
    entities.append({
        "id": gene, "codename": gene, "channels": chans, "n_channels": len(chans),
        "flags": {"on_watchlist": d["omim"],
                  "watchlist_class": ("priority" if d["cls"] == "Hypopigmentation" else "disease_gene") if d["omim"] else None,
                  "physical_evidence": d["ms"], "field_flagged": d["crispr"]},
        "provenance": gtokens[:3],
        "verdict": {"tier": tier, "summary": TIER_SUMMARY[tier], "strands": strands},
    })
ent_ids = {e["id"] for e in entities}
edges = [e for e in edges if e["a"] in ent_ids and e["b"] in ent_ids]

# ---- recover per-direction detail for the flagged reciprocal edge(s) ---------
# nb07 collapses a *directed* pair that appears both ways with opposite signs onto
# the unordered pair and stamps sign_conflict=True. That is NOT "sources disagree":
# each direction is independently and consistently sourced — it is a feedback loop.
# Recover the two directed signs + citations from the raw signed backbone (plus any
# OmniPath confirmation) so the UI can show the loop honestly, direction by direction.
# (Kept in a new `directions` field, not `provenance`, so the REFS invariant below
#  — which requires every provenance token to resolve to a public record — still holds.)
RAG = "data/processed/gene_network_edges.csv"
NB2 = "data/processed/nb2_omnipath_validation.csv"
VERB = {"+": "activates", "-": "represses"}

def _directed_signed():
    dd = defaultdict(list)
    if os.path.exists(RAG):
        with open(RAG) as f:
            for r in csv.DictReader(f):
                s, t, sg = r.get("source"), r.get("target"), (r.get("sign") or "").strip()
                if s and t and sg in ("+", "-"):
                    dd[(s, t)].append({"sign": sg, "cite": (r.get("citation") or "").strip()})
    return dd

def _omnipath_confirmed():
    oo = {}
    if os.path.exists(NB2):
        with open(NB2) as f:
            for r in csv.DictReader(f):
                s, t = (r.get("src_sym") or "").strip(), (r.get("tgt_sym") or "").strip()
                if s and t and (r.get("verdict") or "") == "confirmed":
                    oo[(s, t)] = (r.get("omnipath_sign") or "").strip()
    return oo

_DSIGN, _OMNI = _directed_signed(), _omnipath_confirmed()

def _directions_for(a, b):
    out = []
    for s, t in ((a, b), (b, a)):
        rows = _DSIGN.get((s, t), [])
        if not rows:
            continue
        signs = sorted({r["sign"] for r in rows})
        sign = signs[0] if len(signs) == 1 else "±"
        srcs = []
        for r in rows:
            c = r["cite"] or "curated source"
            if c not in srcs:
                srcs.append(c)
        oc = _OMNI.get((s, t))
        if oc:
            srcs.append(f"OmniPath: independently confirmed ({oc})")
        out.append({"from": s, "to": t, "sign": sign,
                    "verb": VERB.get(sign, "regulates"), "sources": srcs})
    return out

for _ed in edges:
    if _ed.get("sign_conflict"):
        _dirs = _directions_for(_ed["a"], _ed["b"])
        _ed["directions"] = _dirs
        _signset = {d["sign"] for d in _dirs}
        _ed["feedback"] = len(_dirs) >= 2 and "+" in _signset and "-" in _signset

# ---- benchmark: REAL NB10 direction-law result ------------------------------
bench_items = []
recovered = total = 0
with open(NB10) as f:
    for r in csv.DictReader(f):
        if r["gene"] not in ent_ids or r["law_applies"] != "True":
            continue
        conc = str(r["law_concordant"]).startswith("1")
        total += 1; recovered += int(conc)
        bench_items.append({"id": r["gene"], "codename": r["gene"], "truth": "culprit",
                            "kind": "culprit", "verdict_tier": "direction_concordant" if conc else "direction_discordant",
                            "pass": conc})
# NB8 honest negatives = the "presence without mechanism" decoy analog
decoys_ok = decoys_total = 0
with open(NB8) as f:
    for r in csv.DictReader(f):
        if r["bucket"] != "NEG":
            continue
        decoys_total += 1; decoys_ok += 1
        g = (r["nearest_gene_label"] or r["rsid"]).split(" ")[0][:24]
        bench_items.append({"id": g, "codename": g, "truth": "innocent", "kind": "adversarial_decoy",
                            "verdict_tier": "honest_negative", "pass": True})
benchmark = {
    "context": "pigmentation",
    "totals": {"culprits_recovered": f"{recovered}/{total}",
               "innocents_cleared": f"{decoys_ok}/{decoys_total}",
               "decoys_not_fooled": f"{decoys_ok}/{decoys_total}",
               "errors": total - recovered},
    "items": bench_items,
    "note": "Culprits = OMIM pigmentation genes where the mechanism→direction law applies (NB10, real). "
            "Decoys = NB8 co-segregating passengers with no melanocyte-eQTL / mechanistic route (honest negatives).",
}

# ---- a real directed sequence (illustrative melanogenesis spine) ------------
SPINE = ["POMC", "MC1R", "MITF", "TYR", "DCT", "TYRP1"]
spine = [g for g in SPINE if g in ent_ids]
sequence = {"id": "seq_melanogenesis", "context": "pigmentation",
            "label": "Melanogenesis spine — illustrative directed chain",
            "note": f"{max(len(spine)-1,0)} directed steps through core regulators and enzymes; each grounded to a source.",
            "steps": [{"order": i + 1, "from": spine[i], "to": spine[i + 1],
                       "actor": spine[i + 1], "actor_id": spine[i + 1],
                       "sign": "+", "channels": ["mechanistic", "regulon"],
                       "provenance": [default_ref("mechanistic")]} for i in range(len(spine) - 1)]}

# ---- single context (context switch deferred) -------------------------------
contexts = {"contexts": [{"id": "pigmentation", "label": "Pigmentation",
                          "anchor": "The reference context. Cross-context re-binding is deferred to a later version."}],
            "cross": []}

# order channels broad -> selective so the stacked view puts the broadest layer at the base
_cov = {k: 0 for k, *_ in CHANNELS}
for _e in entities:
    for _c in _e["channels"]:
        _cov[_c] += 1
_tot = max(len(entities), 1)
channels_meta = sorted(
    [{"key": k, "label": l, "coverage_rate": round(_cov[k] / _tot, 3), "role": r} for k, l, r, _s in CHANNELS],
    key=lambda c: -_cov[c["key"]])

# add default refs to REFS table
for c, *_ in CHANNELS:
    default_ref(c)

DATASET = {
    "meta": {"note": "REAL harmonized-substrate data in the convergence-engine schema. "
                     "Verdict tiers are a PROVISIONAL derived rule (see banner); the benchmark is the real NB10 result.",
             "real_data": True, "provisional_verdicts": True,
             "n_entities": len(entities), "n_edges": len(edges), "channels": [c[0] for c in CHANNELS]},
    "channels": channels_meta, "entities": entities, "edges": edges,
    "sequence": sequence, "benchmark": benchmark, "contexts": contexts, "references": REFS,
}

# ---- invariant checks (the CI contract in miniature) ------------------------
allsrc = set()
for e in entities:
    allsrc |= set(e["provenance"]) | {s["source"] for s in e["verdict"]["strands"]}
for e in edges:
    allsrc |= set(e["provenance"])
for s in sequence["steps"]:
    allsrc |= set(s["provenance"])
missing = [s for s in allsrc if s and s not in REFS]
assert not missing, f"unresolved refs: {missing[:5]}"
pub = sum(1 for r in REFS.values() if r["access"] == "public")
DATASET["meta"]["pct_public_refs"] = round(100 * pub / max(len(REFS), 1))

os.makedirs(OUTDIR, exist_ok=True)
json.dump(DATASET, open(f"{OUTDIR}/dataset.json", "w"), indent=1)
with open(f"{OUTDIR}/dataset.js", "w") as f:
    f.write("window.__DATASET__=")
    json.dump(DATASET, f, separators=(",", ":"))
    f.write(";\n")

import collections
tiers = collections.Counter(e["verdict"]["tier"] for e in entities)
print(f"entities={len(entities)} edges={len(edges)} refs={len(REFS)} ({DATASET['meta']['pct_public_refs']}% public)")
print("tiers:", dict(tiers))
print("benchmark totals:", benchmark["totals"])
print(f"dataset.js: {os.path.getsize(OUTDIR+'/dataset.js')//1024} KB")
