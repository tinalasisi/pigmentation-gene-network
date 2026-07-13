#!/usr/bin/env python3
"""Generate a TOY dataset that mirrors the structure & distributions of our real
data, in a neutral fictional domain (a "convergence engine" for a set of cold-case
investigations). No real values are used; only the *shape* is preserved:

  - a set of ENTITIES, each with multi-label membership across several evidence
    CHANNELS (2 broad + 4 progressively selective), heavy-tailed so most entities
    sit in 1-2 channels and a tiny CORE sits in 5-6 (the "convergence");
  - typed, mostly-unsigned RELATIONSHIPS between entities, each backed by a subset
    of channels (heavy-tailed convergence), a signed minority, one rare conflict;
  - an ordered directed SEQUENCE (a reconstructed chain of events), each step
    grounded to sources;
  - a per-entity VERDICT (a classification into tiers + evidence strands);
  - a BENCHMARK (labelled ground truth incl. adversarial decoys) with pass/fail;
  - two selectable CONTEXTS that re-bind a subset of verdicts;
  - a PROVENANCE table (every claim carries source refs).

Deterministic (seeded). Regenerate:  python3 generate_toy.py
"""
import json, random, os

random.seed(11)
HERE = os.path.dirname(os.path.abspath(__file__))

# ---- fictional vocabulary (neutral, evocative, domain-free) -------------------
CODENAMES = [
    "Vega","Rigel","Altair","Lyra","Orion","Draco","Cygnus","Mira","Antares","Polaris",
    "Sirius","Capella","Deneb","Aldeb","Spica","Pollux","Castor","Bellatrix","Regulus","Arcturus",
    "Nashira","Alphard","Merak","Dubhe","Phecda","Megrez","Alioth","Mizar","Alkaid","Thuban",
    "Elnath","Alnilam","Alnitak","Saiph","Mintaka","Hadar","Acrux","Gacrux","Atria","Peacock",
    "Tarazed","Sheliak","Sadr","Albireo","Vindem","Izar","Cebalrai","Rasalgethi","Sabik","Unukalhai",
    "Menkar","Diphda","Hamal","Sheratan","Almach","Mirach","Enif","Markab","Scheat","Algenib",
]
CHANNELS = [  # (key, display, coverage rate)  — 2 broad, then progressively selective
    ("surveillance", "Surveillance",  0.82),
    ("comms",        "Comms records", 0.74),
    ("witnesses",    "Witnesses",     0.34),
    ("forensics",    "Forensics",     0.28),
    ("finance",      "Financial",     0.22),
    ("informants",   "Informants",    0.11),
]
CH_KEYS = [c[0] for c in CHANNELS]
EDGE_TYPES = ["coordinates_with", "handler_of", "pays", "shields", "rivals", "tipped_off"]
SIGNED_TYPES = {"handler_of", "shields", "rivals"}  # these assert a directed, signed link
TIERS = ["implicated_multichannel", "implicated_anchored", "circumstantial",
         "cleared", "decoy_cleared"]

N_ENTITIES = 55
N_EDGES = 170


def pick_channels_for_entity():
    ch = [k for k, _d, rate in CHANNELS if random.random() < rate]
    if not ch:
        ch = ["surveillance"]  # everyone shows up on at least one channel
    return ch


def ref(prefix, lo=10, hi=99):
    return f"{prefix}-{random.randint(lo, hi)}"


# ---- entities -----------------------------------------------------------------
random.shuffle(CODENAMES)
entities = []
for i in range(N_ENTITIES):
    name = CODENAMES[i]
    ch = pick_channels_for_entity()
    on_watch = (len(ch) >= 3 and random.random() < 0.7) or random.random() < 0.12
    entities.append({
        "id": f"S{i:02d}",
        "codename": name,
        "channels": ch,
        "n_channels": len(ch),
        "flags": {
            "on_watchlist": on_watch,
            "watchlist_class": random.choice(["priority", "person_of_interest"]) if on_watch else None,
            "physical_evidence": random.random() < 0.35,
            "field_flagged": random.random() < 0.12,   # a functional "field test" hit
        },
        "provenance": sorted({ref("CF", 1000, 1999) for _ in range(random.randint(1, 3))}),
    })

by_id = {e["id"]: e for e in entities}
# hubs = the highest-convergence entities (attract links, like a network hub)
hubs = sorted(entities, key=lambda e: -e["n_channels"])[:8]
hub_ids = [h["id"] for h in hubs]

# ---- verdicts (per-entity classification + evidence strands) ------------------
STRAND_FINDING = {
    "surveillance": "Placed at two linked locations on the timeline.",
    "comms":        "Contact pattern matches the coordinating cluster.",
    "witnesses":    "Independently named by a corroborating account.",
    "forensics":    "Trace evidence consistent with direct involvement.",
    "finance":      "Fund flow aligns with the payout structure.",
    "informants":   "Named by a registered informant as in-scope.",
}
decoy_ids = set(random.sample([e["id"] for e in entities if not e["flags"]["on_watchlist"]
                               and e["flags"]["physical_evidence"]], k=5))
for e in entities:
    n = e["n_channels"]; wl = e["flags"]["on_watchlist"]
    if e["id"] in decoy_ids:
        tier = "decoy_cleared"
        summary = "Looks active (physical evidence present) but no corroborating channel implicates — correctly cleared."
    elif n >= 4 and wl:
        tier = "implicated_multichannel"
        summary = f"{n} independent channels converge, and on the watchlist. The confident call."
    elif wl:
        tier = "implicated_anchored"
        summary = "On the watchlist with a curated anchor; corroboration present but thinner."
    elif n >= 2:
        tier = "circumstantial"
        summary = f"{n} channels place this entity in scope; no anchoring watchlist entry."
    else:
        tier = "cleared"
        summary = "Single-channel presence only; nothing corroborating — cleared."
    strands = [{
        "channel": c, "stance": "implicates" if tier.startswith("implicated") else "notes",
        "finding": STRAND_FINDING[c], "source": ref("FR", 100, 899)
    } for c in e["channels"]]
    e["verdict"] = {"tier": tier, "summary": summary, "strands": strands}

# ---- edges (typed, mostly-unsigned, heavy-tailed convergence) -----------------
CONV_WEIGHTS = [(1, 0.80), (2, 0.13), (3, 0.045), (4, 0.017), (5, 0.008)]
def sample_conv():
    r = random.random(); c = 0
    for k, w in CONV_WEIGHTS:
        c += w
        if r <= c:
            return k
    return 1

edges = []
seen = set()
tries = 0
while len(edges) < N_EDGES and tries < N_EDGES * 40:
    tries += 1
    a = random.choice(hub_ids if random.random() < 0.55 else [e["id"] for e in entities])
    b = random.choice([e["id"] for e in entities])
    if a == b:
        continue
    key = tuple(sorted((a, b)))
    if key in seen:
        continue
    seen.add(key)
    shared = list(set(by_id[a]["channels"]) & set(by_id[b]["channels"])) or CH_KEYS
    n = min(sample_conv(), len(shared))
    chans = random.sample(shared, n)
    etype = random.choice(EDGE_TYPES)
    directed = etype in SIGNED_TYPES
    sign = (random.choice(["+", "+", "+", "-"]) if directed else "")
    edges.append({
        "a": a, "b": b, "type": etype, "directed": directed, "sign": sign,
        "sign_conflict": False,
        "channels": chans, "n_channels": n,
        "tier": ("corroborated" if n >= 3 else "single_channel" if n == 1 else "supported"),
        "provenance": sorted({ref("WT", 10, 99) for _ in range(random.randint(1, 2))}),
    })
# one rare sign conflict (mirrors the single real conflict)
for e in edges:
    if e["directed"]:
        e["sign_conflict"] = True
        e["sign"] = "conflict"
        break

# ---- the marquee directed sequence (a reconstructed chain of events) ----------
STAGES = ["tip-off", "casing", "inside access", "vault breach", "extraction", "handoff", "fence"]
seq_actors = hub_ids[:len(STAGES)]
sequence = {
    "id": "seq_azure",
    "context": "azure_room",
    "label": "Reconstructed sequence — The Azure Room",
    "note": f"{len(STAGES)-1} directed links, each grounded to a source.",
    "steps": []
}
for i in range(len(STAGES) - 1):
    sequence["steps"].append({
        "order": i + 1,
        "from": STAGES[i], "to": STAGES[i + 1],
        "actor": by_id[seq_actors[i]]["codename"], "actor_id": seq_actors[i],
        "sign": random.choice(["+", "+", "-"]),
        "channels": random.sample(CH_KEYS, k=random.randint(1, 3)),
        "provenance": [ref("CF", 1000, 1999)],
    })

# ---- benchmark (ground truth incl. adversarial decoys) + scoreboard -----------
culprits = [e for e in entities if e["verdict"]["tier"].startswith("implicated")]
innocents = [e for e in entities if e["verdict"]["tier"] == "cleared"]
decoys = [e for e in entities if e["verdict"]["tier"] == "decoy_cleared"]
def item(e, truth, kind):
    tier = e["verdict"]["tier"]
    passed = (truth == "culprit" and tier.startswith("implicated")) or \
             (truth == "innocent" and tier in ("cleared", "decoy_cleared"))
    return {"id": e["id"], "codename": e["codename"], "truth": truth, "kind": kind,
            "verdict_tier": tier, "pass": passed}
bench_items = ([item(e, "culprit", "culprit") for e in culprits[:18]]
               + [item(e, "innocent", "innocent") for e in innocents[:12]]
               + [item(e, "innocent", "adversarial_decoy") for e in decoys])
benchmark = {
    "context": "azure_room",
    "totals": {
        "culprits_recovered": f"{sum(1 for i in bench_items if i['kind']=='culprit' and i['pass'])}/"
                              f"{sum(1 for i in bench_items if i['kind']=='culprit')}",
        "innocents_cleared":  f"{sum(1 for i in bench_items if i['kind']=='innocent' and i['pass'])}/"
                              f"{sum(1 for i in bench_items if i['kind']=='innocent')}",
        "decoys_not_fooled":  f"{sum(1 for i in bench_items if i['kind']=='adversarial_decoy' and i['pass'])}/"
                              f"{sum(1 for i in bench_items if i['kind']=='adversarial_decoy')}",
        "errors": sum(1 for i in bench_items if not i["pass"]),
    },
    "items": bench_items,
}

# ---- two contexts, with a subset of verdicts that flip ------------------------
flip = random.sample([e["id"] for e in entities], k=8)
contexts = {
    "contexts": [
        {"id": "azure_room", "label": "The Azure Room",
         "anchor": "The reference case — the fully reconstructed sequence lives here."},
        {"id": "meridian_vault", "label": "The Meridian Vault",
         "anchor": "A second, partially-resolved case over the same cast."},
    ],
    "cross": [{"id": i, "codename": by_id[i]["codename"],
               "azure_room": by_id[i]["verdict"]["tier"],
               "meridian_vault": random.choice(TIERS)} for i in flip],
}

# ---- provenance dictionary (ref id -> neutral source line) --------------------
allrefs = set()
for e in entities:
    allrefs |= set(e["provenance"]); allrefs |= {s["source"] for s in e["verdict"]["strands"]}
for e in edges:
    allrefs |= set(e["provenance"])
for s in sequence["steps"]:
    allrefs |= set(s["provenance"])
SRC_KINDS = {"CF": "Case file", "FR": "Forensic report", "WT": "Wiretap log"}
references = {r: {"kind": SRC_KINDS.get(r.split("-")[0], "Source"),
                 "citation": f"{SRC_KINDS.get(r.split('-')[0],'Source')} {r} (fictional)"}
             for r in sorted(allrefs)}

# ---- write files --------------------------------------------------------------
def dump(name, obj):
    with open(os.path.join(HERE, name), "w") as f:
        json.dump(obj, f, indent=1)

channels_meta = [{"key": k, "label": d, "coverage_rate": rate,
                  "role": "broad" if rate > 0.6 else "mid" if rate > 0.18 else "selective"}
                 for k, d, rate in CHANNELS]
dump("channels.json", channels_meta)
dump("entities.json", entities)
dump("edges.json", edges)
dump("sequence.json", sequence)
dump("benchmark.json", benchmark)
dump("contexts.json", contexts)
dump("references.json", references)
dump("dataset.json", {  # convenience: everything in one file
    "meta": {"note": "Toy dataset — fictional, structure-preserving. See SCHEMA.md.",
             "n_entities": len(entities), "n_edges": len(edges), "channels": CH_KEYS},
    "channels": channels_meta, "entities": entities, "edges": edges,
    "sequence": sequence, "benchmark": benchmark, "contexts": contexts,
    "references": references,
})

# ---- report distributions (to confirm we mirror the real shape) ---------------
import collections
mem = collections.Counter(e["n_channels"] for e in entities)
perch = collections.Counter(c for e in entities for c in e["channels"])
econv = collections.Counter(e["n_channels"] for e in edges)
tiers = collections.Counter(e["verdict"]["tier"] for e in entities)
print("TOY entity->#channel membership:", dict(sorted(mem.items())))
print("TOY per-channel entity counts:", dict(perch.most_common()))
print("TOY edge convergence:", dict(sorted(econv.items())), "| signed:", sum(1 for e in edges if e["sign"]))
print("TOY verdict tiers:", dict(tiers))
print("TOY scoreboard:", benchmark["totals"])
print("wrote 8 json files to", HERE)
