#!/usr/bin/env python3
"""PROTOTYPE (scratchpad): the full hormone->MITF->melanogenesis pathway in 3D, as an HOURGLASS.
TOP: four signal axes (ligand->receptor) funnel down onto the shared cAMP->MITF waist.
BOTTOM: MITF (+SOX10) fan out to the melanogenesis genes (Raghunath edges) -> melanin.
Click any node for its role / mechanism / citation / signal flow.
"""
import math, json
import plotly.graph_objects as go

OUT = "interactive/coupled_pathway_3d.html"
INK = "#26303a"
# Nodes are colored by ROLE (not hormone axis) — colorblind-safe palette (min CIEDE2000 31.35; ≥12 under
# deutan/protan), melanin unique dark brown. Axis is still shown by hourglass corner position + dossier.
PAL  = {"signal": "#E69A17", "recept": "#154C99", "messenger": "#42C0D0",
        "tf": "#CC3D7A", "melano": "#3F8C3F", "melanin": "#3A2A22"}
RLBL = {"signal": "Diffusible signal (ligand)", "recept": "Melanocyte receptor", "messenger": "Second messenger (cAMP)",
        "tf": "Transcription factor", "melano": "Melanogenesis gene", "melanin": "Melanin (final product)"}
RTXT = {"signal": "#26303a", "recept": "white", "messenger": "#26303a", "tf": "white", "melano": "white", "melanin": "white"}
ROLES = ("signal", "recept", "messenger", "tf", "melano", "melanin")   # top → bottom of the hourglass
KSZ  = {"signal": 17, "recept": 21, "messenger": 24, "tf": 22, "melano": 19, "melanin": 30}
D = {"melanocortin": (-1, 1), "estrogen": (-1, -1), "androgen": (1, -1), "endothelin": (1, 1)}
def corner(ax, r, z): return (D[ax][0]*r, D[ax][1]*r, z)

# id -> (x, y, z, label, kind, axis, hover)
N = {
 "aMSH": (*corner("melanocortin", 3.4, 3.55), "α-MSH", "signal", "melanocortin", "Melanocortin ligand (cleaved from POMC)"),
 "E2":   (*corner("estrogen", 3.4, 3.55), "Estradiol", "signal", "estrogen", "17β-estradiol (endocrine + local aromatase)"),
 "DHT":  (*corner("androgen", 3.4, 3.55), "DHT", "signal", "androgen", "Dihydrotestosterone (5α-reduced androgen)"),
 "EDN3": (*corner("endothelin", 3.4, 3.55), "EDN3", "signal", "endothelin", "Endothelin-3 (keratinocyte-derived)"),
 "MC1R": (*corner("melanocortin", 2.5, 3.0), "MC1R", "recept", "melanocortin", "Melanocortin-1 receptor — established α-MSH→cAMP→CREB→MITF"),
 "GPER1": (D["estrogen"][0]*2.6+1.05, D["estrogen"][1]*2.6+0.55, 3.0, "GPER1", "recept", "estrogen", "Membrane estrogen receptor. Natale 2016: estradiol→GPER→cAMP→pCREB→MITF (+208% melanin). PMID 27115344"),
 "ESR2":  (D["estrogen"][0]*2.6-1.05, D["estrogen"][1]*2.6-0.75, 3.0, "ESR2", "recept", "estrogen", "ERβ — in ~90% of epidermal melanocytes (Spałkowska 2021). Nuclear; secondary to GPER. WEAK. PMID 34833446"),
 "AR":    (*corner("androgen", 2.5, 3.0), "AR", "recept", "androgen", "Androgen receptor — DHT→AR→↑tyrosinase in genital melanocytes (Tadokoro 1997). REGIONAL. PMID 9326383"),
 "EDNRB": (*corner("endothelin", 2.5, 3.0), "EDNRB", "recept", "endothelin", "Endothelin receptor B — established EDN3→EDNRB→MITF"),
 "cAMP":  (-1.0, 0.25, 2.0, "cAMP", "messenger", "core", "Shared 2nd messenger — melanocortin AND estrogen(GPER) converge here. Filardo 2002. PMID 11773440"),
 "MITF":  (0.0, 0.0, 1.05, "MITF", "tf", "core", "Master melanocyte transcription factor — the waist of the hourglass: signals converge here, melanogenesis begins here"),
 "SOX10": (1.95, -0.35, 1.5, "SOX10", "tf", "pigment", "Transcription factor — activates MITF and co-activates the melanin enzymes (TYR, TYRP1, DCT)"),
 "MEL":   (0.0, 0.0, -1.0, "Melanin", "melanin", "product", "Melanin — the pigment produced (eumelanin / pheomelanin)"),
}
MEL = [("TYR", "Tyrosinase — the rate-limiting enzyme of melanin synthesis"),
       ("TYRP1", "Tyrosinase-related protein 1 — stabilises TYR / eumelanin"),
       ("DCT", "Dopachrome tautomerase (TYRP2) — melanin-synthesis enzyme"),
       ("MLANA", "Melan-A / MART-1 — melanosome biogenesis"),
       ("PMEL", "Premelanosome protein — the melanosome structural matrix"),
       ("OCA2", "OCA2 melanosomal transmembrane protein — melanosome pH / ion balance"),
       ("SLC45A2", "Solute carrier 45A2 — melanosome transporter")]
for k, (g, desc) in enumerate(MEL):
    ang = 2*math.pi*k/len(MEL) + 0.35
    N[g] = (1.9*math.cos(ang), 1.9*math.sin(ang), 0.2, g, "melano", "pigment", desc)

# edges: (src, dst, axis, established?)
E = [("aMSH", "MC1R", "melanocortin", 1), ("MC1R", "cAMP", "melanocortin", 1),
     ("E2", "GPER1", "estrogen", 1), ("GPER1", "cAMP", "estrogen", 1),
     ("E2", "ESR2", "estrogen", 0), ("ESR2", "MITF", "estrogen", 0),
     ("DHT", "AR", "androgen", 0), ("AR", "TYR", "androgen", 0),
     ("EDN3", "EDNRB", "endothelin", 1), ("EDNRB", "MITF", "endothelin", 1),
     ("cAMP", "MITF", "core", 1), ("SOX10", "MITF", "pigment", 1)]
for g, _ in MEL: E.append(("MITF", g, "pigment", 1))
for g in ("TYR", "TYRP1", "DCT"): E.append(("SOX10", g, "pigment", 1))
for g, _ in MEL: E.append((g, "MEL", "pigment", 1 if g in ("TYR", "TYRP1", "DCT") else 0))

fig = go.Figure()
# faint funnel guide rings (top signalling)
import numpy as np
for z, r in [(3.55, 3.2), (3.0, 2.6)]:
    t = np.linspace(0, 2*np.pi, 60)
    fig.add_trace(go.Scatter3d(x=r*np.cos(t)*0.9, y=r*np.sin(t)*0.9, z=[z]*60, mode="lines",
        line=dict(color="#e8ebee", width=2), hoverinfo="skip", showlegend=False))
for s, d, ax, est in E:                       # edges: hue-free — evidence strength via width + opacity only
    x0, y0, z0 = N[s][:3]; x1, y1, z1 = N[d][:3]
    fig.add_trace(go.Scatter3d(x=[x0, x1], y=[y0, y1], z=[z0, z1], mode="lines",
        line=dict(color="#7c858c" if est else "#b9c0c5", width=6 if est else 3), opacity=0.9 if est else 0.5,
        hoverinfo="skip", showlegend=False))
for ri, kind in enumerate(ROLES):             # one trace per ROLE → color legend + role-colored markers
    ids = [i for i in N if N[i][4] == kind]
    if not ids: continue
    sizes = [28 if i == "MITF" else KSZ[kind] for i in ids]   # emphasise the MITF waist
    # labels sit OUTSIDE the marker in dark ink (white-in-marker text vanishes where it overflows onto the white bg)
    fig.add_trace(go.Scatter3d(x=[N[i][0] for i in ids], y=[N[i][1] for i in ids], z=[N[i][2] for i in ids],
        mode="markers+text", text=[N[i][3] for i in ids],
        textposition="bottom center" if kind == "melanin" else "top center",
        textfont=dict(size=11, color=INK),
        marker=dict(size=sizes, color=PAL[kind], opacity=1.0, line=dict(color="#33404a", width=1)),
        customdata=ids, name=RLBL[kind], legendrank=ri+1, showlegend=True,
        hoverinfo="text", hovertext=[f"<b>{N[i][3]}</b><br>{N[i][6]}" for i in ids]))

fig.update_layout(
    title=dict(text="<b>From signal to pigment — the hourglass, in 3D</b><br>"
        "<span style='font-size:13px;color:#5c656b'>Four hormone axes funnel down onto MITF (the waist);<br>"
        "MITF + SOX10 then fan out to melanogenesis genes → melanin.<br>"
        "Thick = established · thin = weak/regional.<br>Drag to rotate · click a node.</span>",
        x=0.5, xanchor="center", font=dict(color=INK, size=18)),
    scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
        aspectmode="manual", aspectratio=dict(x=1.55, y=1.55, z=1.4),
        camera=dict(eye=dict(x=1.55, y=1.55, z=0.62)), bgcolor="white"),
    paper_bgcolor="white", height=760, margin=dict(l=0, r=0, t=152, b=0), showlegend=True,
    legend=dict(orientation="v", yanchor="top", y=0.98, xanchor="left", x=0.0, font=dict(size=9.5),
        itemsizing="constant", title=dict(text="<b>Node role</b>", font=dict(size=9.5, color="#5c656b"))))

# ---- dossier ----
AXLBL = {"melanocortin": "Melanocortin axis", "estrogen": "Estrogen axis", "androgen": "Androgen axis",
         "endothelin": "Endothelin axis", "core": "Convergence core", "pigment": "Melanogenesis", "product": "Pigment"}
down = {i: [] for i in N}; up = {i: [] for i in N}
for s, d, ax, est in E:
    down[s].append(d); up[d].append(s)
INFO = {i: {"label": N[i][3].replace("\n", " "), "role": RLBL[N[i][4]], "axis": AXLBL[N[i][5]],
            "desc": N[i][6], "rcol": PAL[N[i][4]], "down": down[i], "up": up[i]} for i in N}

graph_html = fig.to_html(include_plotlyjs="cdn", full_html=False, div_id="graph",
    config={"displaylogo": False, "responsive": True, "modeBarButtonsToRemove": ["toImage"]})
CSS = """
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#fff}
#dossier{position:fixed;top:0;right:0;bottom:0;width:340px;max-width:88vw;background:#fff;border-left:1px solid #e5e7eb;
 box-shadow:-8px 0 30px rgba(0,0,0,.08);transform:translateX(100%);transition:transform .25s ease;overflow-y:auto;z-index:30;padding:22px;box-sizing:border-box}
#dossier.open{transform:translateX(0)}
#dossier .close{position:absolute;top:12px;right:14px;border:none;background:none;font-size:24px;cursor:pointer;color:#9aa0a6}
#dossier h2{margin:6px 0 8px;font-size:23px;color:#222}
.d-name{color:#5c656b;font-size:14px;margin-bottom:12px}
.d-badges{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px}
.badge{font-size:11px;padding:3px 9px;border-radius:999px;color:#fff;font-weight:600}
.d-sec{border-top:1px solid #eef0f2;padding-top:14px;margin-top:14px}
.d-sec h3{font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:#98a0a6;margin:0 0 8px}
#d-desc{font-size:13px;color:#333;line-height:1.5}
#d-desc a{color:#c0186a;text-decoration:none}
.d-note{font-size:12px;color:#5c656b;margin-bottom:6px}
.chip{display:inline-block;font-size:11px;padding:2px 8px;margin:2px;border-radius:6px;background:#f1f3f5;color:#333;cursor:pointer}
.chip:hover{background:#e2e6ea}
#dtoggle{position:fixed;top:16px;right:16px;z-index:25;background:#2f6d7a;color:#fff;border:none;padding:8px 15px;border-radius:999px;font-size:13px;font-weight:600;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,.15)}
"""
PANEL = """
<button id='dtoggle'>Node info &#9656;</button>
<aside id='dossier'>
 <button class='close'>&times;</button>
 <h2 id='d-sym'>Click a node</h2>
 <div class='d-name' id='d-name'>Select any node in the cascade to see its role, mechanism, and citations.</div>
 <div class='d-badges' id='d-badges'></div>
 <div class='d-sec'><h3>Role / mechanism</h3><div id='d-desc'></div></div>
 <div class='d-sec'><h3>Signal flow</h3><div id='d-flow'></div></div>
</aside>
"""
JS = """
function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;');}
function chip(id){return '<span class="chip" data-node="'+id+'">'+esc(INFO[id].label)+'</span>';}
function showNode(id){var d=INFO[id];if(!d)return;
 document.getElementById('d-sym').textContent=d.label;
 document.getElementById('d-name').textContent='';
 document.getElementById('d-badges').innerHTML='<span class="badge" style="background:'+d.rcol+'">'+d.role+'</span><span class="badge" style="background:#5c656b">'+d.axis+'</span>';
 document.getElementById('d-desc').innerHTML=esc(d.desc).replace(/PMID (\\d+)/g,'<a href="https://pubmed.ncbi.nlm.nih.gov/$1/" target="_blank">PMID $1</a>');
 var f='';
 if(d.up.length)f+='<div class="d-note">Receives from</div>'+d.up.map(chip).join('');
 if(d.down.length)f+='<div class="d-note" style="margin-top:10px">Signals to</div>'+d.down.map(chip).join('');
 document.getElementById('d-flow').innerHTML=f||'<i>&mdash;</i>';
 document.getElementById('dossier').classList.add('open');}
document.querySelector('#dossier .close').onclick=function(){document.getElementById('dossier').classList.remove('open')};
document.getElementById('dtoggle').onclick=function(){document.getElementById('dossier').classList.toggle('open')};
document.getElementById('dossier').addEventListener('click',function(e){var c=e.target.closest('.chip');if(c&&c.dataset.node)showNode(c.dataset.node);});
(function attach(){var gd=document.getElementById('graph');if(gd&&gd.on){gd.on('plotly_click',function(ev){var p=ev.points&&ev.points[0];if(p&&p.customdata)showNode(p.customdata);});}else{setTimeout(attach,200);}})();
"""
html = ("<!doctype html><html><head><meta charset='utf-8'><title>Pathway (3D)</title><style>"
        + CSS + "</style></head><body>" + graph_html + PANEL
        + "<script>const INFO=" + json.dumps(INFO) + ";" + JS + "</script></body></html>")
open(OUT, "w").write(html)
print("wrote pathway_3d.html (hourglass: signals -> MITF -> melanogenesis -> melanin)")
