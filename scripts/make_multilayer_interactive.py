#!/usr/bin/env python3
"""Interactive 3D multiplex of the NB7 harmonized substrate.

Unlike the static hero (which showed only the all-layers core), this includes
every gene supported by >=2 of the four network layers, so genes appear ONLY on
the planes that actually support them — the gaps between layers are the point.

Outputs (both regenerated together):
  interactive/nb7_multilayer_graph.json      — portable graph (nodes, edges, layers)
  interactive/substrate_multilayer.html      — rotatable Plotly widget (plotly.js via CDN)

Regenerate:  python3.11 scripts/make_multilayer_interactive.py
"""
import csv
import json
import os
from collections import defaultdict
import numpy as np
import networkx as nx
import plotly.graph_objects as go

NODES_CSV = "data/processed/nb7_substrate_nodes.csv"
EDGES_CSV = "data/processed/nb7_substrate_edges.csv"
JSON_OUT = "interactive/nb7_multilayer_graph.json"
HTML_OUT = "interactive/substrate_multilayer.html"

INK, CREAM, CRIMSON = "#21282d", "#faf6ef", "#b23a48"
STRING_KEYS = {"STRING_ours", "DArcy_STRING"}

# planes bottom (z=0) -> top; each = one network layer, with edges
PLANES = [
    ("string", "Functional association (STRING v12)", "#5c7d8a", 0.0),
    ("omni",   "Literature validation (OmniPath)",    "#6b4e71", 1.0),
    ("grn",    "TF→target regulon (MITF / SOX10 / PAX3)", "#b06a1e", 2.0),
    ("ragh",   "Mechanistic pathway (Raghunath 2015)", "#2f5d62", 3.0),
]
PLANE_Z = {k: z for k, _l, _c, z in PLANES}
PLANE_COLOR = {k: c for k, _l, c, _z in PLANES}
PLANE_LABEL = {k: l for k, l, _c, _z in PLANES}


def load(min_planes=2):
    nodes = {}
    with open(NODES_CSV) as f:
        for r in csv.DictReader(f):
            sl = set(r["supporting_layers"].split("|"))
            nodes[r["gene"]] = dict(
                ragh="Raghunath" in sl, grn="GRN" in sl,
                string=bool(sl & STRING_KEYS), omni=False,
                omim=r["omim_disease_flag"] == "True",
                hypo=r["omim_phenotype_class"] == "Hypopigmentation",
                dz=r["omim_disease_names"].replace("|", "; ")[:80],
                crispr=r["bajpai_hit_flag"] == "True",
                ms=r["massspec_detected_flag"] == "True",
            )
    # per-layer edges among all nodes; OmniPath membership comes from its edges
    layer_edges = defaultdict(list)   # layer_key -> [(a,b)]
    with open(EDGES_CSV) as f:
        for e in csv.DictReader(f):
            a, b = e["gene_a"], e["gene_b"]
            if a == b or a not in nodes or b not in nodes:
                continue
            ls = set(e["supporting_layers"].split("|"))
            if "Raghunath" in ls: layer_edges["ragh"].append((a, b))
            if "GRN" in ls:       layer_edges["grn"].append((a, b))
            if ls & STRING_KEYS:  layer_edges["string"].append((a, b))
            if "OmniPath_validation" in ls:
                layer_edges["omni"].append((a, b))
                nodes[a]["omni"] = nodes[b]["omni"] = True

    def planes_of(d):
        return [k for k in ("ragh", "grn", "omni", "string") if d[k]]

    keep = {g for g, d in nodes.items() if len(planes_of(d)) >= min_planes}
    nodes = {g: d for g, d in nodes.items() if g in keep}
    for g, d in nodes.items():
        d["planes"] = planes_of(d)
    layer_edges = {k: [(a, b) for a, b in es if a in keep and b in keep]
                   for k, es in layer_edges.items()}
    return nodes, layer_edges


def layout(nodes, layer_edges, seed=7):
    # weight the layout by the SELECTIVE layers so STRING's dense mesh does not
    # collapse everything to the centre; STRING still pulls, but weakly.
    W = {"ragh": 1.0, "grn": 1.0, "omni": 0.85, "string": 0.12}
    G = nx.Graph()
    G.add_nodes_from(nodes)
    for k, es in layer_edges.items():
        for a, b in es:
            if G.has_edge(a, b):
                G[a][b]["weight"] = max(G[a][b]["weight"], W[k])
            else:
                G.add_edge(a, b, weight=W[k])
    pos = nx.spring_layout(G, seed=seed, k=7.5 / np.sqrt(len(nodes)),
                           iterations=600, weight="weight")
    xs = np.array([p[0] for p in pos.values()]); ys = np.array([p[1] for p in pos.values()])
    for g in pos:
        pos[g] = (12 * (pos[g][0] - xs.min()) / (xs.ptp() or 1),
                  12 * (pos[g][1] - ys.min()) / (ys.ptp() or 1))
    deg = dict(G.degree())
    return pos, deg


def write_json(nodes, layer_edges, pos, deg):
    os.makedirs(os.path.dirname(JSON_OUT), exist_ok=True)
    doc = {
        "description": "NB7 harmonized substrate — genes in >=2 of four network layers.",
        "layers": [{"key": k, "label": l, "color": c, "z": z} for k, l, c, z in PLANES],
        "nodes": [{
            "gene": g, "x": round(pos[g][0], 4), "y": round(pos[g][1], 4),
            "planes": d["planes"], "n_planes": len(d["planes"]), "degree": deg.get(g, 0),
            "omim": d["omim"], "hypopigmentation": d["hypo"], "omim_diseases": d["dz"],
            "bajpai_crispr_hit": d["crispr"], "massspec_detected": d["ms"],
        } for g, d in sorted(nodes.items())],
        "edges": [{"a": a, "b": b, "layer": k}
                  for k, es in layer_edges.items() for (a, b) in es],
    }
    json.dump(doc, open(JSON_OUT, "w"), indent=1)
    print("wrote", JSON_OUT, f"({len(nodes)} nodes, {sum(len(e) for e in layer_edges.values())} edges)")


def build_figure(nodes, layer_edges, pos, deg):
    fig = go.Figure()
    xmin = min(p[0] for p in pos.values()) - 0.6; xmax = max(p[0] for p in pos.values()) + 0.6
    ymin = min(p[1] for p in pos.values()) - 0.6; ymax = max(p[1] for p in pos.values()) + 0.6

    for key, label, color, z in PLANES:
        grp = f"layer_{key}"
        # translucent plane
        fig.add_trace(go.Mesh3d(
            x=[xmin, xmax, xmax, xmin], y=[ymin, ymin, ymax, ymax], z=[z] * 4,
            i=[0, 0], j=[1, 2], k=[2, 3], color=color, opacity=0.06,
            hoverinfo="skip", legendgroup=grp, showlegend=False))
        # plane label (floating text at a corner)
        fig.add_trace(go.Scatter3d(
            x=[xmin], y=[ymax], z=[z], mode="text", text=[f"  {label}"],
            textposition="middle right", textfont=dict(color=color, size=12, family="system-ui"),
            hoverinfo="skip", legendgroup=grp, showlegend=False))
        # intra-plane edges
        ex, ey, ez = [], [], []
        for a, b in layer_edges.get(key, []):
            ex += [pos[a][0], pos[b][0], None]
            ey += [pos[a][1], pos[b][1], None]
            ez += [z, z, None]
        if ex:
            fig.add_trace(go.Scatter3d(
                x=ex, y=ey, z=ez, mode="lines",
                line=dict(color=color, width=0.6 if key == "string" else 2.2),
                opacity=0.08 if key == "string" else 0.5,
                hoverinfo="skip", legendgroup=grp, showlegend=False))
        # nodes on this plane (only member genes); size encodes CONVERGENCE
        members = [g for g, d in nodes.items() if key in d["planes"]]
        nx_, ny_, nz_, size, hov = [], [], [], [], []
        for g in members:
            d = nodes[g]
            nx_.append(pos[g][0]); ny_.append(pos[g][1]); nz_.append(z)
            size.append(7 + 5 * (len(d["planes"]) - 1))
            fl = []
            if d["hypo"]: fl.append("OMIM hypopigmentation")
            elif d["omim"]: fl.append("OMIM disease")
            if d["crispr"]: fl.append("CRISPR melanin hit")
            if d["ms"]: fl.append("melanocyte proteome")
            hov.append(
                f"<b>{g}</b><br>network layers: {' · '.join(PLANE_LABEL[p].split(' (')[0] for p in d['planes'])}"
                f"<br>{len(d['planes'])} of 4 layers"
                + (("<br>" + " · ".join(fl)) if fl else "")
                + (f"<br><i>{d['dz']}</i>" if d["omim"] and d["dz"] else ""))
        fig.add_trace(go.Scatter3d(
            x=nx_, y=ny_, z=nz_, mode="markers", name=label.split(" (")[0],
            legendgroup=grp, showlegend=True,
            marker=dict(size=size, color=color, opacity=0.95,
                        line=dict(color="white", width=0.5)),
            text=hov, hovertemplate="%{text}<extra></extra>"))

    # functional-evidence overlays (rings / diamonds on every plane a gene sits on)
    ox, oy, oz, oc, osz = [], [], [], [], []
    dx, dy, dz_, dsz = [], [], [], []
    for g, d in nodes.items():
        base = 6 + 4.5 * (len(d["planes"]) - 1)
        for p in d["planes"]:
            z = PLANE_Z[p]
            if d["omim"]:
                ox.append(pos[g][0]); oy.append(pos[g][1]); oz.append(z)
                oc.append(CRIMSON if d["hypo"] else "#c98a2b"); osz.append(base + 5)
            if d["crispr"]:
                dx.append(pos[g][0]); dy.append(pos[g][1]); dz_.append(z)
                dsz.append(max(5, base * 0.5))
    fig.add_trace(go.Scatter3d(
        x=ox, y=oy, z=oz, mode="markers", name="OMIM disease gene",
        legendgroup="omim", showlegend=True, hoverinfo="skip",
        marker=dict(size=osz, symbol="circle-open", color=oc, opacity=0.9)))
    fig.add_trace(go.Scatter3d(
        x=dx, y=dy, z=dz_, mode="markers", name="Bajpai CRISPR hit",
        legendgroup="crispr", showlegend=True, hoverinfo="skip",
        marker=dict(size=dsz, symbol="diamond", color="white",
                    line=dict(color=INK, width=1))))

    # vertical connectors: each gene threaded through the planes it belongs to
    cx, cy, cz = [], [], []
    for g, d in nodes.items():
        zs = sorted(PLANE_Z[p] for p in d["planes"])
        cx += [pos[g][0], pos[g][0], None]
        cy += [pos[g][1], pos[g][1], None]
        cz += [zs[0], zs[-1], None]
    fig.add_trace(go.Scatter3d(
        x=cx, y=cy, z=cz, mode="lines", name="same gene across layers",
        line=dict(color=INK, width=1), opacity=0.18,
        hoverinfo="skip", legendgroup="stitch", showlegend=True))

    # labels for a curated headline set (kept sparse so they stay readable)
    HEADLINE = {"MITF", "TYR", "TYRP1", "DCT", "MC1R", "OCA2",
                "SOX10", "PAX3", "KIT", "EDNRB"}
    lab = [(g, d) for g, d in nodes.items() if g in HEADLINE]
    fig.add_trace(go.Scatter3d(
        x=[pos[g][0] for g, _ in lab], y=[pos[g][1] for g, _ in lab],
        z=[max(PLANE_Z[p] for p in d["planes"]) + 0.18 for _, d in lab],
        mode="text", text=[g for g, _ in lab],
        textfont=dict(color=INK, size=11, family="system-ui"),
        name="gene labels", legendgroup="labels", showlegend=True,
        hoverinfo="skip"))

    n = len(nodes)
    fig.update_layout(
        title=dict(
            text="<b>The harmonized substrate, layer by layer</b><br>"
                 f"<span style='font-size:13px;color:#5c656b'>{n} genes on ≥2 of four network layers — "
                 "each sits only on the layers that carry it.<br>"
                 "Drag to rotate · hover a gene · click the legend to isolate a layer.</span>",
            x=0.5, xanchor="center", font=dict(color=INK, size=20, family="system-ui")),
        scene=dict(
            xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
            aspectmode="manual", aspectratio=dict(x=2.0, y=2.0, z=1.6),
            camera=dict(eye=dict(x=1.55, y=1.55, z=1.05)),
            bgcolor="white"),
        legend=dict(groupclick="togglegroup", orientation="h", yanchor="top", y=0,
                    xanchor="center", x=0.5, font=dict(size=11, color=INK),
                    bgcolor="rgba(255,255,255,0.65)"),
        paper_bgcolor="white", margin=dict(l=0, r=0, t=96, b=58), height=700)
    return fig


if __name__ == "__main__":
    nodes, layer_edges = load(min_planes=2)
    pos, deg = layout(nodes, layer_edges)
    write_json(nodes, layer_edges, pos, deg)
    os.makedirs(os.path.dirname(HTML_OUT), exist_ok=True)
    fig = build_figure(nodes, layer_edges, pos, deg)
    fig.write_html(HTML_OUT, include_plotlyjs="cdn", full_html=True,
                   config={"displaylogo": False, "responsive": True,
                           "modeBarButtonsToRemove": ["toImage"]})
    print("wrote", HTML_OUT, f"({len(nodes)} nodes)")
