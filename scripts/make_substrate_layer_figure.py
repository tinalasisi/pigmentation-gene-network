#!/usr/bin/env python3
"""Custom figures for the NB7 harmonized multi-layer substrate.

Draws OUR integration (not any single source): the independent evidence layers
merged in NB7, and where they converge on a shared gene core. Renders two
candidate designs from data/processed/nb7_substrate_{nodes,edges}.csv:

  1. nb7_layer_stack.png        — stacked multiplex "layer planes" (2.5D)
  2. nb7_convergence_network.png — flat network, edges/nodes encoded by
                                   how many independent layers support them

Regenerate:  python3.11 scripts/make_substrate_layer_figure.py
"""
import csv
from collections import Counter
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch, Circle
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection

NODES_CSV = "data/processed/nb7_substrate_nodes.csv"
EDGES_CSV = "data/processed/nb7_substrate_edges.csv"
OUTDIR = "notebooks/figures"

# ---- brand palette -----------------------------------------------------------
INK   = "#21282d"
TEAL  = "#2f5d62"
AMBER = "#b06a1e"
CREAM = "#faf6ef"
CRIMSON = "#b23a48"

# Structural edge-layers (as tagged in supporting_layers), display name + color.
# Ordered foundation -> broad (drawn back-to-front / bottom-to-top).
LAYERS = [
    ("Raghunath",           "Mechanistic pathway\n(Raghunath 2015)",      TEAL),
    ("GRN",                 "TF→target regulon\n(MITF / SOX10 / PAX3)", AMBER),
    ("OmniPath_validation", "Literature validation\n(OmniPath)",           "#6b4e71"),
    ("STRING_ours",         "Functional association\n(STRING v12)",        "#5c7d8a"),
]
STRING_MERGE = {"STRING_ours", "DArcy_STRING"}  # both count toward the STRING plane


def load(threshold):
    """Return (core_genes set, node_attrs dict, edges list) for genes in >=threshold layers."""
    nodes = {}
    with open(NODES_CSV) as f:
        for r in csv.DictReader(f):
            try:
                n = int(r["n_edge_bearing_layers"])
            except ValueError:
                n = 0
            nodes[r["gene"]] = dict(
                n=n,
                omim=r["omim_disease_flag"] == "True",
                hypo=r["omim_phenotype_class"] == "Hypopigmentation",
                crispr=r["bajpai_hit_flag"] == "True",
                ms=r["massspec_detected_flag"] == "True",
            )
    core = {g for g, d in nodes.items() if d["n"] >= threshold}
    edges = []
    with open(EDGES_CSV) as f:
        for e in csv.DictReader(f):
            a, b = e["gene_a"], e["gene_b"]
            if a in core and b in core and a != b:
                layers = set(e["supporting_layers"].split("|"))
                edges.append((a, b, layers, int(e["n_supporting_layers"])))
    return core, nodes, edges


def layer_edges(edges, layer_key):
    keys = STRING_MERGE if layer_key == "STRING_ours" else {layer_key}
    return [(a, b) for a, b, ls, _ in edges if ls & keys]


def union_layout(core, edges, seed=7):
    G = nx.Graph()
    G.add_nodes_from(core)
    for a, b, _, _ in edges:
        G.add_edge(a, b)
    pos = nx.spring_layout(G, seed=seed, k=1.7 / np.sqrt(len(core)), iterations=400)
    # normalize to [0,1]^2
    xs = np.array([p[0] for p in pos.values()])
    ys = np.array([p[1] for p in pos.values()])
    for g in pos:
        pos[g] = ((pos[g][0] - xs.min()) / (xs.ptp() or 1),
                  (pos[g][1] - ys.min()) / (ys.ptp() or 1))
    return pos, G


# =============================================================================
# FIGURE 1 — stacked multiplex layer planes
# =============================================================================
def fig_layer_stack(threshold=5, seed=7):
    core, nodes, edges = load(threshold)
    pos, G = union_layout(core, edges, seed)
    deg = dict(G.degree())

    PW, SHEAR, DEPTH, GAP = 6.2, 2.5, 1.9, 3.05  # plane geometry
    def project(g, i):
        x, y = pos[g]
        return (x * PW + y * SHEAR, GAP * i + y * DEPTH)

    fig, ax = plt.subplots(figsize=(12.6, 12.4))
    n_layers = len(LAYERS)
    for i, (key, label, color) in enumerate(LAYERS):      # bottom -> top
        # plane parallelogram
        corners = [(0, 0), (PW, 0), (PW + SHEAR, DEPTH), (SHEAR, DEPTH)]
        corners = [(cx, GAP * i + cy) for cx, cy in corners]
        ax.add_patch(Polygon(corners, closed=True, facecolor=color, alpha=0.07,
                             edgecolor=color, lw=1.2, zorder=i * 10, joinstyle="round"))
        ax.text(SHEAR - 0.35, GAP * i + DEPTH - 0.15, label, ha="right", va="top",
                fontsize=11, color=color, fontweight="bold", zorder=i * 10 + 5, linespacing=0.95)
        # this layer's edges
        segs = [[project(a, i), project(b, i)] for a, b in layer_edges(edges, key)]
        ax.add_collection(LineCollection(segs, colors=color, linewidths=1.3,
                                         alpha=0.55, zorder=i * 10 + 1))
        # nodes
        for g in core:
            X, Y = project(g, i)
            ax.scatter([X], [Y], s=26 + 5 * deg.get(g, 0), color=color, alpha=0.9,
                       edgecolors="white", linewidths=0.6, zorder=i * 10 + 3)

    # vertical convergence "stitch" through all planes + top labels
    top = n_layers - 1
    for g in core:
        pts = [project(g, i) for i in range(n_layers)]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=INK, lw=0.5,
                alpha=0.16, zorder=5)
        X, Y = project(g, top)
        d = nodes[g]
        ring = CRIMSON if d["hypo"] else (AMBER if d["omim"] else "#9aa4ab")
        ax.scatter([X], [Y], s=90, color="white", edgecolors=ring, linewidths=2.0,
                   zorder=top * 10 + 6)
        if d["crispr"]:
            ax.scatter([X], [Y], marker="*", s=70, color=AMBER, edgecolors=INK,
                       linewidths=0.4, zorder=top * 10 + 7)
        ax.text(X, Y + 0.16, g, ha="center", va="bottom", fontsize=8.6,
                color=INK, fontweight="bold", zorder=top * 10 + 8)

    leg = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor="white",
               markeredgecolor=CRIMSON, markeredgewidth=2, markersize=11,
               label="OMIM hypopigmentation gene"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="white",
               markeredgecolor=AMBER, markeredgewidth=2, markersize=11,
               label="OMIM disease gene (other)"),
        Line2D([0], [0], marker="*", color="w", markerfacecolor=AMBER,
               markeredgecolor=INK, markersize=13, label="Bajpai CRISPR melanin hit"),
        Line2D([0], [0], color=INK, alpha=0.3, lw=1, label="same gene across layers"),
    ]
    ax.legend(handles=leg, loc="lower right", frameon=False, fontsize=9.5,
              handletextpad=0.6, borderpad=0.4)
    ax.set_xlim(-2.4, PW + SHEAR + 0.6)
    ax.set_ylim(-0.7, GAP * (n_layers - 1) + DEPTH + 1.1)
    ax.set_aspect("equal"); ax.axis("off")

    # title band reserved ABOVE the axes (no overlap with the plot)
    fig.subplots_adjust(top=0.865, bottom=0.01, left=0.015, right=0.985)
    fig.text(0.5, 0.965, "One gene core, many evidence layers",
             ha="center", va="top", fontsize=20, fontweight="bold", color=INK)
    fig.text(0.5, 0.918,
             f"The NB7 harmonized substrate merges six independent evidence layers. Shown: the "
             f"{len(core)} genes carried by ≥5 of them,\nthreaded through the four network layers "
             "(planes) — vertical lines follow one gene down through all of them. Rings mark "
             "clinical\n(OMIM) genes; stars mark CRISPR melanin-screen hits.",
             ha="center", va="top", fontsize=11, color="#5c656b", linespacing=1.25)
    out = f"{OUTDIR}/nb7_layer_stack.png"
    fig.savefig(out, dpi=200, facecolor="white")
    plt.close(fig)
    print("wrote", out, f"({len(core)} genes)")


# =============================================================================
# FIGURE 2 — flat convergence network
# =============================================================================
def fig_convergence(threshold=4, seed=7):
    core, nodes, edges = load(threshold)
    pos, G = union_layout(core, edges, seed)
    deg = dict(G.degree())

    # collapse parallel evidence to max layer-support per undirected pair
    pair_support = {}
    for a, b, ls, n in edges:
        k = tuple(sorted((a, b)))
        pair_support[k] = max(pair_support.get(k, 0), n)

    fig, ax = plt.subplots(figsize=(13.2, 11.2))
    ramp = matplotlib.colors.LinearSegmentedColormap.from_list(
        "conv", ["#cfd6da", "#8aa0a6", TEAL, "#243f43"])
    # edges: darker/thicker = more independent layers agree
    order = sorted(pair_support.items(), key=lambda kv: kv[1])
    for (a, b), n in order:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        t = (n - 1) / 4
        ax.plot([x1, x2], [y1, y2], color=ramp(t), lw=0.6 + 2.6 * t,
                alpha=0.35 + 0.5 * t, zorder=1 + n, solid_capstyle="round")

    nfill = matplotlib.colors.LinearSegmentedColormap.from_list(
        "nf", ["#f0d9b8", AMBER, "#7c3d10"])
    for g in core:
        x, y = pos[g]
        d = nodes[g]
        size = 120 + 46 * deg.get(g, 0)
        ax.scatter([x], [y], s=size, color=nfill((d["n"] - 4) / 2),
                   edgecolors=CRIMSON if d["hypo"] else (INK if d["omim"] else "#b9c0c5"),
                   linewidths=2.4 if d["hypo"] else 1.3, zorder=40)
        if d["crispr"]:
            ax.scatter([x], [y], marker="*", s=90, color="white",
                       edgecolors=INK, linewidths=0.5, zorder=41)
        ax.text(x, y - 0.045, g, ha="center", va="top", fontsize=8.2,
                color=INK, fontweight="bold", zorder=42)

    enc = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=AMBER,
               markeredgecolor=CRIMSON, markeredgewidth=2.2, markersize=12,
               label="OMIM hypopigmentation gene"),
        Line2D([0], [0], marker="*", color="w", markerfacecolor="white",
               markeredgecolor=INK, markersize=13, label="Bajpai CRISPR melanin hit"),
        Line2D([0], [0], color=TEAL, lw=3, label="link backed by many layers"),
        Line2D([0], [0], color="#cfd6da", lw=1, label="link backed by one layer"),
    ]
    ax.legend(handles=enc, loc="lower right", frameon=False, fontsize=9.5,
              handletextpad=0.6, borderpad=0.4)
    ax.margins(0.08)
    ax.axis("off")

    fig.subplots_adjust(top=0.885, bottom=0.105, left=0.02, right=0.98)
    fig.text(0.5, 0.965, "Where independent evidence layers converge",
             ha="center", va="top", fontsize=20, fontweight="bold", color=INK)
    fig.text(0.5, 0.923,
             f"NB7 harmonized substrate — the {len(core)}-gene core, each gene supported by ≥4 of "
             "six integrated layers.\nEdge shade and width = how many independent layers back that "
             "link; node fill = layers per gene.",
             ha="center", va="top", fontsize=11, color="#5c656b", linespacing=1.25)
    fig.text(0.5, 0.055,
             "Six integrated layers:  mechanistic pathway (Raghunath) · TF→target regulon (GRN) · "
             "literature validation (OmniPath) ·\nfunctional association (STRING×2) · clinical "
             "(OMIM) · functional screen (Bajpai CRISPR)",
             ha="center", va="bottom", fontsize=9.5, color=INK, linespacing=1.25)
    out = f"{OUTDIR}/nb7_convergence_network.png"
    fig.savefig(out, dpi=200, facecolor="white")
    plt.close(fig)
    print("wrote", out, f"({len(core)} genes)")


if __name__ == "__main__":
    fig_layer_stack(threshold=5)
    fig_convergence(threshold=4)
