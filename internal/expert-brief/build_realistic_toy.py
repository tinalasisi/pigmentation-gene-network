#!/usr/bin/env python3
"""Build a PRODUCTION-SCALE masked toy dataset for the software dev.

The v1 toy (55 entities) was too small to reveal the real design problems
(dense single-layer field, thick thread column, occlusion at scale). This masks
our ACTUAL substrate (app/data/dataset.json) — so the toy is structurally
IDENTICAL to production (same ~803 entities, ~7,800 edges, heavy-tailed layer
membership, one broad layer, the sign-conflict edge, the stance pattern) — while
scrubbing every domain-revealing string (entity names, channel names, findings,
summaries, references). Fictional cold-case skin; real skeleton.

Out:  internal/expert-brief/toy_v2/dataset.json   (inspectable)
      internal/expert-brief/toy_v2/dataset.js     (window.__DATASET__ = …, drop-in)

Regenerate:  python3.11 internal/expert-brief/build_realistic_toy.py
"""
import json, os

DS = json.load(open("app/data/dataset.json"))
OUT = "internal/expert-brief/toy_v2"
os.makedirs(OUT, exist_ok=True)

# ---- real channels -> cold-case channels, preserving coverage order + roles ----
cov = {c["key"]: 0 for c in DS["channels"]}
for e in DS["entities"]:
    for c in e["channels"]:
        cov[c] += 1
by_cov = sorted(DS["channels"], key=lambda c: -cov[c["key"]])   # broad..selective
COLD = ["surveillance", "forensics", "records", "witnesses", "financial", "informants"]
CH_MAP = {c["key"]: COLD[i] for i, c in enumerate(by_cov)}
IMPLICATING_REAL = {"mechanistic", "regulon", "validation"}
STANCE = {CH_MAP[k]: ("implicates" if k in IMPLICATING_REAL else "notes") for k in CH_MAP}
ROLE = lambda n, tot: "broad" if n > .4*tot else ("mid" if n > .1*tot else "selective")
channels = [{"key": CH_MAP[c["key"]], "label": CH_MAP[c["key"]].title(),
             "role": ROLE(cov[c["key"]], len(DS["entities"]))} for c in by_cov]

FIND = {"surveillance": "Placed at two linked locations on the timeline.",
        "forensics":    "Trace evidence consistent with direct involvement.",
        "records":      "Appears in the cross-referenced records set.",
        "witnesses":    "Independently named by a corroborating account.",
        "financial":    "Fund-flow pattern matches the payout structure.",
        "informants":   "Named by a registered informant as in scope."}
TIER_SUM = {
    "implicated_multichannel": "Several independent channels implicate, with a watchlist anchor. The confident call.",
    "implicated_anchored":     "On the watchlist with an anchor; corroboration present but thinner.",
    "circumstantial":          "Some implicating channels place it in scope; no watchlist anchor.",
    "cleared":                 "Present only through notes-channels — nothing implicates. Cleared.",
    "decoy_cleared":           "Looks active but no channel implicates — presence without a case, correctly cleared."}

# ---- codenames (deterministic, unique) ----
STARS = ("Vega Rigel Altair Lyra Orion Draco Cygnus Mira Antares Polaris Sirius Capella Deneb Aldeb "
         "Spica Pollux Castor Bellatrix Regulus Arcturus Nashira Alphard Merak Dubhe Phecda Megrez Alioth "
         "Mizar Alkaid Thuban Elnath Alnilam Alnitak Saiph Mintaka Hadar Acrux Gacrux Atria Peacock Tarazed "
         "Sheliak Sadr Albireo Vindem Izar Cebalrai Sabik Unukalhai Menkar Diphda Hamal Sheratan Almach Mirach "
         "Enif Markab Scheat Algenib Kaus Nunki Ascella Kraz Algorab Gienah Zosma Chertan Adhafera Rasalas "
         "Subra Alterf Wasat Wezen Adhara Furud Aludra Muliphein Naos Turais Avior Miaplac Aspidiske Suhail "
         "Alphecca Nusakan Kornephoros Marfik Yed Sabik Cebalrai Rasalgethi Sarin Maasym Kuma Grumium "
         "Altais Aldhibah Edasich Athebyne Alrakis Tyl Batentaber Alsciaukat Muscida Talitha Alkaphrah "
         "Tania Alula Intercrus Chalawan Fafnir Chara Cor Asterion Merga").split()
def codename(i): return STARS[i % len(STARS)] + ("" if i < len(STARS) else "-" + str(i // len(STARS) + 1))

ents = sorted(DS["entities"], key=lambda e: e["id"])
ID = {e["id"]: f"E{idx:04d}" for idx, e in enumerate(ents)}
NAME = {e["id"]: codename(idx) for idx, e in enumerate(ents)}

# ---- references -> fake ids (production refs are 100% public URLs; withheld here) ----
REF = {}
new_refs = {}
def ref(rid):
    if rid not in REF:
        REF[rid] = f"SRC-{1000+len(REF)}"
        new_refs[REF[rid]] = {"kind": "Case source", "citation": f"Case source {REF[rid]}",
                              "access": "public"}   # NB: prod resolves to a real public URL
    return REF[rid]

def mapch(k): return CH_MAP[k]

entities = []
for idx, e in enumerate(ents):
    chs = [mapch(c) for c in e["channels"]]
    strands = [{"channel": mapch(s["channel"]), "stance": STANCE[mapch(s["channel"])],
                "finding": FIND[mapch(s["channel"])], "source": ref(s["source"])}
               for s in e["verdict"]["strands"]]
    fl = e["flags"]
    entities.append({
        "id": ID[e["id"]], "codename": NAME[e["id"]], "channels": chs, "n_channels": e["n_channels"],
        "flags": {"on_watchlist": fl["on_watchlist"],
                  "watchlist_class": ("priority" if fl.get("watchlist_class") == "priority" else "secondary") if fl["on_watchlist"] else None,
                  "physical_evidence": fl["physical_evidence"], "field_flagged": fl["field_flagged"]},
        "provenance": [ref(r) for r in e["provenance"]],
        "verdict": {"tier": e["verdict"]["tier"], "summary": TIER_SUM.get(e["verdict"]["tier"], ""),
                    "strands": strands}})

edges = [{"a": ID[e["a"]], "b": ID[e["b"]], "type": e["type"], "directed": e["directed"],
          "sign": e["sign"], "sign_conflict": e["sign_conflict"],
          "channels": [mapch(c) for c in e["channels"]], "n_channels": e["n_channels"],
          "tier": e["tier"], "provenance": [ref(r) for r in e["provenance"]]}
         for e in DS["edges"] if e["a"] in ID and e["b"] in ID]

DATASET = {
    "meta": {"note": "PRODUCTION-SCALE masked toy — fictional cold-case skin, real structural skeleton "
                     "(masked from the production substrate). Same schema as v1. Refs are placeholders; "
                     "in production every ref resolves to a public URL (PubMed/DOI/etc.).",
             "n_entities": len(entities), "n_edges": len(edges), "channels": [c["key"] for c in channels]},
    "channels": channels, "entities": entities, "edges": edges,
    "references": new_refs,
    "contexts": {"contexts": [{"id": "reference", "label": "The reference case",
                               "anchor": "Single context; cross-context re-binding deferred."}], "cross": []},
    "sequence": {"id": "seq", "context": "reference", "label": "", "note": "", "steps": []},
    "benchmark": {"context": "reference", "totals": {}, "items": []},
}
json.dump(DATASET, open(f"{OUT}/dataset.json", "w"), indent=1)
with open(f"{OUT}/dataset.js", "w") as f:
    f.write("window.__DATASET__="); json.dump(DATASET, f, separators=(",", ":")); f.write(";\n")

# ---- parity report (confirm it matches production distributions) ----
import collections
mem = collections.Counter(len(e["channels"]) for e in entities)
per = collections.Counter(c for e in entities for c in e["channels"])
econv = collections.Counter(e["n_channels"] for e in edges)
single = sum(1 for e in edges if e["n_channels"] == 1)
conflict = sum(1 for e in edges if e["sign_conflict"])
print(f"entities={len(entities)} edges={len(edges)} refs={len(new_refs)} channels={len(channels)}")
print("entity->#layers:", dict(sorted(mem.items())))
print("per-channel coverage:", {k: per[k] for k in [c['key'] for c in channels]})
print(f"single-layer edges: {single}/{len(edges)}  ({100*single//len(edges)}%)  | sign-conflict edges: {conflict}")
print("verdict tiers:", dict(collections.Counter(e['verdict']['tier'] for e in entities)))
print("wrote", OUT + "/dataset.json + dataset.js")
