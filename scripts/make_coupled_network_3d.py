#!/usr/bin/env python3
"""PROTOTYPE (scratchpad): two coupled 3D networks, hormone module split into 6 group SUB-PLANES.
Whole hormone STRING net laid out in x,y (connectivity), z = functional group (6 thin slabs,
biological order) + jitter. Pigment core just below. Bridges drop from estrogen/androgen receptors.
"""
import csv
import numpy as np, networkx as nx, plotly.graph_objects as go

SP = "/private/tmp/claude-503/-Users-tlasisi-GitHub-pigmentation-gene-network/06feb813-3332-43b2-9be0-88f6e6bc2edd/scratchpad"
PANEL = "comparative-genomics/config/gene_panel.csv"
NODES = "data/processed/nb7_substrate_nodes.csv"
BRIDGES = "data/processed/nb13_hormone_interlayer_edges.csv"
LAY, DRAW = 0.4, 0.7
INK = "#26303a"
rng = np.random.default_rng(7)

panel = {r["gene"]: (r["set"], r["category"]) for r in csv.DictReader(open(PANEL))}
omim = {r["gene"] for r in csv.DictReader(open(NODES)) if r["omim_disease_flag"] == "True"}
pigset = {g for g, (s, c) in panel.items() if s == "pigmentation"}
hormset = {g for g, (s, c) in panel.items() if s == "hormone"}
HC = {"gnrh_signaling": "#46b06a", "hpg_axis": "#3a8fbf", "steroid_biosynthesis": "#e08a3c",
      "coactivator_corepressor_carrier": "#9aa0a6", "androgen_axis": "#7b4ea3", "estrogen_axis": "#d81b7a"}
HL = {"gnrh_signaling": "GnRH signaling", "hpg_axis": "HPG axis", "steroid_biosynthesis": "Steroid biosynthesis",
      "coactivator_corepressor_carrier": "Coactivators / carriers", "androgen_axis": "Androgen axis", "estrogen_axis": "Estrogen axis"}
# group z-levels (top -> down), close together; estrogen sits just above the pigment core
GZ = {"gnrh_signaling": 2.35, "hpg_axis": 1.95, "steroid_biosynthesis": 1.55,
      "coactivator_corepressor_carrier": 1.15, "androgen_axis": 0.8, "estrogen_axis": 0.5}
PIGZ = -0.35

lay = {"h": [], "p": []}; draw = {"h": [], "p": []}
for r in csv.DictReader(open("data/processed/panel_string_edges.csv")):
    a, b, s = r["gene_a"], r["gene_b"], float(r["score"])
    side = "h" if (a in hormset and b in hormset) else ("p" if (a in pigset and b in pigset) else None)
    if side is None: continue
    if s >= LAY: lay[side].append((a, b))
    if s >= DRAW: draw[side].append((a, b))

def xy(genes, edges, seed, R, mode="stretch", keep=85, cap=1.15):
    G = nx.Graph(); G.add_nodes_from(genes); G.add_edges_from(edges)
    hub = max(dict(G.degree()), key=lambda g: G.degree(g))
    for g in list(genes):
        if G.degree(g) == 0: G.add_edge(g, hub)
    pos = nx.spring_layout(G, seed=seed, k=2.5/np.sqrt(len(genes)), iterations=800)
    if mode == "stretch":                          # per-axis min-max → fills a square (hormone stack)
        xs = np.array([p[0] for p in pos.values()]); ys = np.array([p[1] for p in pos.values()])
        xl, xh = np.percentile(xs, [1, 99]); yl, yh = np.percentile(ys, [1, 99])
        nrm = lambda v, lo, hi: float(np.clip((v-lo)/((hi-lo) or 1), 0, 1))
        return {g: (R*(2*nrm(pos[g][0], xl, xh)-1), R*(2*nrm(pos[g][1], yl, yh)-1)) for g in pos}
    # compact → keep the spring layout's natural cluster, scale so the keep-th pctl radius == R,
    # cap outliers at R*cap so a few weakly-tied genes don't blow the plane up / stretch edges
    gl = list(genes)
    P = np.array([pos[g] for g in gl], float); P -= P.mean(0)
    r = np.hypot(P[:, 0], P[:, 1]); P *= R / (np.percentile(r, keep) or 1)
    r = np.hypot(P[:, 0], P[:, 1]); over = r > R*cap
    if over.any(): P[over] *= (R*cap / r[over])[:, None]
    return {g: (float(P[i, 0]), float(P[i, 1])) for i, g in enumerate(gl)}

hxy = xy(hormset, lay["h"], 4, 4.5)
pxy = xy(pigset, lay["p"], 11, 3.0, mode="compact")   # compact core: no forced-square stretch, outliers capped
hdeg = {g: sum(g in e for e in lay["h"]) for g in hormset}
pdeg = {g: sum(g in e for e in lay["p"]) for g in pigset}
# 3D positions: hormone z by group (+ jitter); pigment on its own plane
H = {g: (hxy[g][0], hxy[g][1], GZ[panel[g][1]] + float(rng.uniform(-0.07, 0.07))) for g in hormset}
Pp = {g: (pxy[g][0], pxy[g][1], PIGZ) for g in pigset}
POMCZ = 0.1                                   # the pigment<->hormone interface layer, between pigment core and hormone stack
# pigment genes that couple to the hormone module (STRING>=0.7 or curated bridge target) -> interface layer
INTERFACE = {"EDNRB", "KIT", "MITF", "PAX3", "POMC", "TFAP2A", "TYR"}
for g in INTERFACE:
    Pp[g] = (Pp[g][0], Pp[g][1], POMCZ)
POS = {**H, **Pp}
bridges = [(r["source"], r["target"], r["axis"], r["evidence_tier"], r["mechanism"])
           for r in csv.DictReader(open(BRIDGES)) if r["layer"] == "hormone_bridge"]
receptors = {b[0] for b in bridges}

fig = go.Figure()
def e3(edges, pos, col, w):
    x, y, z = [], [], []
    for a, b in edges:
        x += [pos[a][0], pos[b][0], None]; y += [pos[a][1], pos[b][1], None]; z += [pos[a][2], pos[b][2], None]
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color=col, width=w), hoverinfo="skip", showlegend=False))
e3(draw["h"], POS, "#e6c4d5", 1.3)     # hormone STRING edges (within + across sub-planes)
e3(draw["p"], POS, "#a9cfc7", 1.4)     # pigment STRING edges
first = True
for s, t, axis, tier, mech in bridges:
    fig.add_trace(go.Scatter3d(x=[POS[s][0], POS[t][0]], y=[POS[s][1], POS[t][1]], z=[POS[s][2], POS[t][2]],
        mode="lines", line=dict(color="#c0186a", width=6), name="Cited sex-steroid bridge",
        legendgroup="b", legendrank=9, showlegend=first, hoverinfo="text", text=f"{s} → {t} · {axis} · {tier}<br>{mech}")); first = False
# pigment<->hormone coupling — ALL cross-module STRING links (any pigment gene, not just the interface):
# high (>=0.70) solid gold, medium (0.40-0.70) faint. Same >=0.40 floor as the within-module count, so a
# medium association (e.g. BNC2<->ESR2 0.46) is shown rather than silently dropped by an asymmetric cutoff.
firsthi = firstmed = True
for r in csv.DictReader(open("data/processed/panel_string_edges.csv")):
    a, b, sc = r["gene_a"], r["gene_b"], float(r["score"])
    if sc < 0.4: continue
    pg = a if a in pigset else (b if b in pigset else None)
    hg = a if a in hormset else (b if b in hormset else None)
    if not (pg and hg): continue
    hi = sc >= 0.7
    fig.add_trace(go.Scatter3d(x=[POS[pg][0], POS[hg][0]], y=[POS[pg][1], POS[hg][1]], z=[POS[pg][2], POS[hg][2]],
        mode="lines", line=dict(color="#d9930a", width=1.7 if hi else 0.7), opacity=0.5 if hi else 0.16,
        name="Pigment↔hormone coupling · high (≥0.70)" if hi else "· medium (0.40–0.70)",
        legendgroup="cup_hi" if hi else "cup_med", legendrank=10 if hi else 11,
        showlegend=(firsthi if hi else firstmed), hoverinfo="text",
        text=f"{pg} ↔ {hg} · STRING {sc:.2f} · {'high' if hi else 'medium'}"))
    if hi: firsthi = False
    else: firstmed = False
# hormone nodes by group
for ri, cat in enumerate(HC):
    gs = [g for g in hormset if panel[g][1] == cat]
    if not gs: continue
    fig.add_trace(go.Scatter3d(x=[H[g][0] for g in gs], y=[H[g][1] for g in gs], z=[H[g][2] for g in gs],
        mode="markers", marker=dict(size=[6 + 1.5*np.sqrt(hdeg[g]) + (5 if g in receptors else 0) for g in gs],
            color=HC[cat], line=dict(color="white", width=0.6)),
        name=HL[cat], legendrank=ri+1, customdata=gs, hoverinfo="text",
        hovertext=[f"<b>{g}</b> · {HL[cat]}" + (" · receptor → bridge" if g in receptors else "") + f" · {hdeg[g]} links" for g in gs]))
# pigment CORE nodes (not coupled to hormones) — split OMIM, on the bottom plane
core = [g for g in pigset if g not in INTERFACE]
for sub, lc, lw, sl in [([g for g in core if g not in omim], "white", 0.6, True),
                        ([g for g in core if g in omim], "#b23a48", 2.2, False)]:
    if not sub: continue
    fig.add_trace(go.Scatter3d(x=[Pp[g][0] for g in sub], y=[Pp[g][1] for g in sub], z=[Pp[g][2] for g in sub],
        mode="markers", marker=dict(size=[6 + 1.5*np.sqrt(pdeg[g]) for g in sub], color="#2f9e8f",
            line=dict(color=lc, width=lw)), name="Pigmentation gene" + ("" if sl else " (OMIM)"), customdata=sub,
        legendrank=8, showlegend=sl, hoverinfo="text", hovertext=[f"<b>{g}</b> · pigmentation · {panel[g][1]} · {pdeg[g]} links" for g in sub]))
# INTERFACE genes — pigment genes coupled to the hormone module — on the interface layer, thin gold ring
ig = sorted(INTERFACE)
fig.add_trace(go.Scatter3d(x=[Pp[g][0] for g in ig], y=[Pp[g][1] for g in ig], z=[Pp[g][2] for g in ig],
    mode="markers", marker=dict(size=[8 + 1.5*np.sqrt(pdeg[g]) for g in ig], color="#2f9e8f",
        line=dict(color="#d9930a", width=2)), name="Pigment gene coupled to hormones", legendrank=7, customdata=ig, hoverinfo="text",
    hovertext=[f"<b>{g}</b> · pigmentation · {panel[g][1]} · couples to the hormone axis · {pdeg[g]} links" for g in ig]))
# Layer identity is carried by the legend (ordered top→bottom to match the stack via legendrank), not floating
# 3D text — eight stacked slabs can't all get a collision-free in-scene label. Only per-gene names float (below).
# labels
PIGLAB = {"MITF", "TYR", "TYRP1", "DCT", "OCA2", "SOX10", "PAX3", "KIT", "MC1R", "EDNRB",
          "SLC45A2", "POMC", "ASIP", "KITLG", "MRAP2", "TFAP2A"}
hhub = sorted(hormset, key=lambda g: -hdeg[g])[:7]
labs = [(g, H[g]) for g in set(hhub) | receptors] + [(g, Pp[g]) for g in pigset if g in PIGLAB]
fig.add_trace(go.Scatter3d(x=[p[0] for _, p in labs], y=[p[1] for _, p in labs], z=[p[2]+0.12 for _, p in labs],
    mode="text", text=[f"<b>{g}</b>" if g in receptors or g in {"MITF", "TYR"} else g for g, _ in labs],
    textfont=dict(size=9.5, color=INK), hoverinfo="skip", showlegend=False))

fig.update_layout(
    title=dict(text="<b>Two coupled 3D networks: the sex-hormone axis<br>over the pigmentation core</b><br>"
        "<span style='font-size:13px;color:#5c656b'>Hormone module split into 6 group sub-planes (STRING v12),<br>"
        "pigment core below, 3 cited receptor→pigment bridges.<br>Drag to rotate · hover any gene.</span>",
        x=0.5, xanchor="center", font=dict(color=INK, size=18)),
    scene=dict(xaxis=dict(visible=False, range=[-5.0, 5.0]), yaxis=dict(visible=False, range=[-5.0, 5.0]),
        zaxis=dict(visible=False, range=[-0.9, 2.9]),   # fixed ranges → stable framing
        aspectmode="manual", aspectratio=dict(x=2, y=2, z=1.5),
        camera=dict(eye=dict(x=1.55, y=1.55, z=0.55)), bgcolor="white"),
    paper_bgcolor="white", height=760,
    # Transparent legend, top-left, collapsible via the #legtoggle button (CSS/JS below): a see-through
    # key rather than a white box that hides nodes, and one you can dismiss entirely — matters most in
    # the tight iframe embeds. Kept left so it never collides with the right-side Gene-info dossier.
    legend=dict(orientation="v", yanchor="top", y=0.98, xanchor="left", x=0.0, font=dict(size=9), itemsizing="constant",
        bgcolor="rgba(0,0,0,0)",
        title=dict(text="<b>Layers (top → bottom)</b>", font=dict(size=9.5, color="#5c656b"))),
    margin=dict(l=0, r=0, t=150, b=0))
# ---- per-gene dossier data ----
import json
names = {r["gene"]: r["full_name"] for r in csv.DictReader(open("data/processed/panel_gene_names.csv"))}
wnb = {g: {} for g in panel}   # within-module neighbour -> STRING score (>=0.40)
xnb = {g: {} for g in panel}   # cross-module  neighbour -> STRING score (>=0.40) — same floor as within
for r in csv.DictReader(open("data/processed/panel_string_edges.csv")):
    a, b, s = r["gene_a"], r["gene_b"], float(r["score"])
    if a not in panel or b not in panel or s < 0.4: continue
    tgt = wnb if panel[a][0] == panel[b][0] else xnb
    tgt[a][b] = s; tgt[b][a] = s
def nlist(d): return [{"g": k, "s": round(v, 2), "hi": v >= 0.7} for k, v in sorted(d.items(), key=lambda kv: -kv[1])]
BR = {}
for r in csv.DictReader(open(BRIDGES)):
    if r["layer"] != "hormone_bridge": continue
    d = {"src": r["source"], "tgt": r["target"], "axis": r["axis"], "tier": r["evidence_tier"],
         "mech": r["mechanism"], "pmid": r.get("citation_pmid", "")}
    BR.setdefault(r["source"], []).append(d); BR.setdefault(r["target"], []).append(d)
PIGROLE = {"transcription": "Pigment transcription factor", "enzyme": "Melanin-synthesis enzyme",
           "melanosome": "Melanosome protein", "melanosome_transport": "Melanosome transporter",
           "receptor_signaling": "Receptor / signaling", "regulatory": "Regulatory"}
def role(g):
    s, c = panel[g]
    if g in receptors: return "Sex-steroid receptor — cited bridge to the pigment core"
    if g in INTERFACE: return "Pigment gene coupled to the hormone axis (interface)"
    return HL.get(c, c) if s == "hormone" else PIGROLE.get(c, c)
GENES = {g: {"name": names.get(g, ""),
             "module": "Sex-hormone axis" if panel[g][0] == "hormone" else "Pigmentation",
             "group": HL.get(panel[g][1], panel[g][1]) if panel[g][0] == "hormone" else panel[g][1].replace("_", " "),
             "role": role(g), "deg": len(wnb[g]), "within": nlist(wnb[g]), "cross": nlist(xnb[g]),
             "bridges": BR.get(g, []),
             "mcol": "#a01560" if panel[g][0] == "hormone" else "#1f7a6e",
             "gcol": HC.get(panel[g][1], "#888") if panel[g][0] == "hormone" else ("#c9880a" if g in INTERFACE else "#2f9e8f")}
         for g in panel}

graph_html = fig.to_html(include_plotlyjs="cdn", full_html=False, div_id="graph",
    config={"displaylogo": False, "responsive": True, "modeBarButtonsToRemove": ["toImage"]})
CSS = """
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#fff}
#dossier{position:fixed;top:0;right:0;bottom:0;width:340px;max-width:88vw;background:#fff;border-left:1px solid #e5e7eb;
 box-shadow:-8px 0 30px rgba(0,0,0,.08);transform:translateX(100%);transition:transform .25s ease;overflow-y:auto;z-index:30;padding:22px;box-sizing:border-box}
#dossier.open{transform:translateX(0)}
#dossier .close{position:absolute;top:12px;right:14px;border:none;background:none;font-size:24px;line-height:1;cursor:pointer;color:#9aa0a6}
#dossier h2{margin:6px 0 2px;font-size:23px;color:#222}
.d-name{color:#5c656b;font-size:14px;margin-bottom:14px}
.d-badges{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px}
.badge{font-size:11px;padding:3px 9px;border-radius:999px;color:#fff;font-weight:600}
.d-role{font-size:13px;color:#333;margin:8px 0 2px}
.d-sec{border-top:1px solid #eef0f2;padding-top:14px;margin-top:14px}
.d-sec h3{font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:#98a0a6;margin:0 0 8px}
.d-note{font-size:12px;color:#5c656b;margin-bottom:8px}
.chip{display:inline-block;font-size:11px;padding:2px 8px;margin:2px;border-radius:6px;background:#eef1f3;color:#334;cursor:pointer}
.chip:hover{filter:brightness(0.95)}
.chip .s{opacity:.6;font-variant-numeric:tabular-nums;margin-left:3px}
.chip.hi{font-weight:600}
.chip.within.hi{background:#d5dde3;color:#1a2a33}
.chip.cross{background:#fdf3dd;color:#8a6d1a}
.chip.cross.hi{background:#f2d485;color:#5a4200}
.bridge{background:#fbe4ef;border-left:3px solid #c0186a;padding:9px 11px;border-radius:6px;margin:7px 0;font-size:12px;color:#3a2230}
.bridge a{color:#c0186a;text-decoration:none}
#dtoggle{position:fixed;top:16px;right:16px;z-index:25;background:#2f6d7a;color:#fff;border:none;padding:8px 15px;border-radius:999px;font-size:13px;font-weight:600;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,.15)}
#legtoggle{position:fixed;top:16px;left:16px;z-index:25;background:rgba(255,255,255,.82);color:#3a4348;border:1px solid #d5dbdf;padding:6px 13px;border-radius:999px;font-size:12px;font-weight:600;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.08)}
"""
PANEL = """
<button id='legtoggle'>&#9662; Layers</button>
<button id='dtoggle'>Gene info &#9656;</button>
<aside id='dossier'>
 <button class='close' aria-label='Close'>&times;</button>
 <h2 id='d-sym'>Click a gene</h2>
 <div class='d-name' id='d-name'>Select any node to see what it is and what it connects to.</div>
 <div class='d-badges' id='d-badges'></div>
 <div class='d-role' id='d-role'></div>
 <div class='d-sec'><h3>Connections within its module</h3><div id='d-links'></div></div>
 <div class='d-sec'><h3>Hormone &#8596; pigment coupling</h3><div id='d-coupling'></div></div>
</aside>
"""
JS = """
function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;');}
function chip(g,cls){return '<span class="chip'+(cls?' '+cls:'')+'" data-gene="'+g+'">'+g+'</span>';}
function schip(x,cls){return '<span class="chip '+cls+(x.hi?' hi':'')+'" data-gene="'+x.g+'">'+x.g+'<span class="s">'+x.s.toFixed(2)+'</span></span>';}
function showGene(g){var d=GENES[g];if(!d)return;
 document.getElementById('d-sym').textContent=g;
 document.getElementById('d-name').textContent=d.name||'';
 document.getElementById('d-badges').innerHTML='<span class="badge" style="background:'+d.mcol+'">'+d.module+'</span><span class="badge" style="background:'+d.gcol+'">'+esc(d.group)+'</span>';
 document.getElementById('d-role').textContent=d.role;
 document.getElementById('d-links').innerHTML='<div class="d-note">'+d.deg+' STRING v12 link'+(d.deg==1?'':'s')+' inside its module (score &#8805;0.40; <b>bold</b> = high &#8805;0.70, drawn as a line)</div>'+(d.within.length?d.within.map(function(x){return schip(x,'within')}).join(''):'<i>none</i>');
 var cs='';d.bridges.forEach(function(b){cs+='<div class="bridge"><b>'+b.src+' &#8594; '+b.tgt+'</b> &middot; '+b.axis+' &middot; '+esc(b.tier)+'<br>'+esc(b.mech)+(b.pmid?('<br>'+b.pmid.split(';').map(function(p){p=p.trim();return '<a href="https://pubmed.ncbi.nlm.nih.gov/'+p+'/" target="_blank">PMID '+p+'</a>'}).join(', ')):'')+'</div>';});
 if(d.cross.length){cs+='<div class="d-note" style="margin-top:8px">STRING links to the other module (score &#8805;0.40; <b>bold</b> = high &#8805;0.70, drawn as a solid gold line):</div>'+d.cross.map(function(x){return schip(x,'cross')}).join('');}
 document.getElementById('d-coupling').innerHTML=cs||'<i>No pigment&#8596;hormone STRING link at &#8805;0.40.</i>';
 document.getElementById('dossier').classList.add('open');}
document.querySelector('#dossier .close').onclick=function(){document.getElementById('dossier').classList.remove('open')};
document.getElementById('dtoggle').onclick=function(){document.getElementById('dossier').classList.toggle('open')};
document.getElementById('dossier').addEventListener('click',function(e){var c=e.target.closest('.chip');if(c&&c.dataset.gene)showGene(c.dataset.gene);});
(function attach(){var gd=document.getElementById('graph');if(gd&&gd.on){gd.on('plotly_click',function(ev){var p=ev.points&&ev.points[0];if(p&&p.customdata)showGene(p.customdata);});}else{setTimeout(attach,200);}})();
(function(){var shown=true,b=document.getElementById('legtoggle'),gd=document.getElementById('graph');if(!b)return;b.onclick=function(){shown=!shown;if(window.Plotly&&gd&&gd.data)Plotly.relayout(gd,{showlegend:shown});b.innerHTML=(shown?'\\u25be':'\\u25b8')+' Layers';};})();
"""
html = ("<!doctype html><html><head><meta charset='utf-8'><title>Coupled network</title><style>"
        + CSS + "</style></head><body>" + graph_html + PANEL
        + "<script>const GENES=" + json.dumps(GENES) + ";" + JS + "</script></body></html>")
open("interactive/coupled_network_3d.html", "w").write(html)
print("wrote interactive/coupled_network_3d.html")
