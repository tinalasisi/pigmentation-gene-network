#!/usr/bin/env python
"""sister_figures.py — regenerate the two sister-pair figures from frozen data/.
Split-cell clade-grouped comparison matrix + fixed-layout per-pair network.
Run: python sister_figures.py   (needs pandas, numpy, matplotlib, networkx)
Layout is loaded from data/network_layout.json so gene positions are identical
across every panel and every re-render.
"""
import json, numpy as np, pandas as pd, networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Patch, Rectangle
from matplotlib.lines import Line2D
import os
base=os.path.dirname(os.path.abspath(__file__))
PIG,HOR,RED,GY,BLANK="#C97B0A","#2E6E9E","#B22222","#8c8c8c","#f0f0f0"
BR=pd.read_csv(f"{base}/data/branch_rates.csv")
GM=pd.read_csv(f"{base}/data/gene_modules.csv"); gmod=dict(zip(GM.gene,GM.module))
OA=pd.read_csv(f"{base}/data/origin_assignments.csv")
SP=pd.read_csv(f"{base}/sister_pairs.csv")
sp2origin=dict(zip(OA.species,OA.origin_id)); sp2fam=dict(zip(OA.species,OA.family))
def selset(sp): return set(BR[(BR.branch==sp)&(BR.selected_flag==True)&(BR.is_tip==True)].gene)
from collections import Counter
pairs=[]
for _,r in SP.iterrows():
    d,m=r.dich,r.sister_mono
    pairs.append(dict(dich=d,mono=m,family=sp2fam.get(d),origin=sp2origin.get(d),
                      sd=selset(d),sm=selset(m),patristic=r.patristic))
allg=set()
for p in pairs: allg|=p["sd"]|p["sm"]
rec=Counter()
for p in pairs:
    for g in p["sd"]: rec[g]+=1
pig_g=sorted([g for g in allg if gmod.get(g)=="pigmentation"],key=lambda g:(-rec[g],g))
hor_g=sorted([g for g in allg if gmod.get(g)=="hormone"],key=lambda g:(-rec[g],g))
cols=pig_g+hor_g
fam_order=["hominidae","hylobatidae","cercopithecidae","cebidae","atelidae","pitheciidae","lemuridae"]
def fkey(p): return (fam_order.index(p["family"]) if p["family"] in fam_order else 99,p["origin"],p["patristic"])
pairs=sorted(pairs,key=fkey)
fam_disp={"hylobatidae":"Hylobatidae (gibbons)","cercopithecidae":"Cercopithecidae (OW monkeys)",
          "cebidae":"Atelidae/Cebidae (NW monkeys)","lemuridae":"Lemuridae (lemurs)"}

# ---- Figure A: split-cell matrix, STACKED as two module panels ----
# Row layout (species order + family headers) is shared by both panels.
layout=[]; y=0; fam_hdr=[]; cur=None
for p in pairs:
    if p["family"]!=cur:
        cur=p["family"]; fam_hdr.append((y,fam_disp.get(cur,cur))); y+=1.1
    layout.append((y,p)); y+=1
nrow_units=y
def tl(x,y,s=0.9): return [(x,y-s/2),(x+s,y-s/2),(x,y+s/2)]
def tr(x,y,s=0.9): return [(x+s,y-s/2),(x+s,y+s/2),(x,y+s/2)]

def draw_panel(ax,genes,module_name,modc):
    """Draw the full 21-row species matrix for ONE module's gene set on `ax`."""
    ncol=len(genes)
    for yy,p in layout:
        for j,g in enumerate(genes):
            ax.add_patch(Rectangle((j,yy-0.45),0.9,0.9,facecolor="white",edgecolor="#dedede",lw=0.4,zorder=1))
            ax.add_patch(Polygon(tl(j,yy),closed=True,facecolor=modc if g in p["sd"] else BLANK,edgecolor="none",zorder=2))
            # monochromatic sister triangle drawn faded so the solid dichromatic triangle stands out
            ax.add_patch(Polygon(tr(j,yy),closed=True,facecolor=(modc if g in p["sm"] else BLANK),
                                 alpha=(0.32 if g in p["sm"] else 1.0),edgecolor="none",zorder=2))
            ax.plot([j,j+0.9],[yy+0.45,yy-0.45],color="white",lw=0.6,zorder=3)
    top=-1.0
    botb=nrow_units-0.1  # per-column count strip, just below the last row
    # gene labels (wider columns -> larger, legible font) + per-gene D/M pair counts
    for j,g in enumerate(genes):
        ax.text(j+0.45,top,g,rotation=90,ha="center",va="bottom",fontsize=8.0,color=modc,
                fontweight="bold" if rec[g]>=3 else "normal")
        dc=sum(1 for p in pairs if g in p["sd"]); mc=sum(1 for p in pairs if g in p["sm"])
        ax.text(j+0.45,botb,f"{dc}",ha="center",va="top",fontsize=6.5,color=RED,fontweight="bold")
        ax.text(j+0.45,botb+0.55,f"{mc}",ha="center",va="top",fontsize=6.5,color=GY)
    ax.text(-0.5,botb,"D",ha="right",va="top",fontsize=6.8,color=RED,fontweight="bold")
    ax.text(-0.5,botb+0.55,"M",ha="right",va="top",fontsize=6.8,color=GY)
    ax.text(ncol+0.3,botb+0.3,"# pairs with\ngene selected",ha="left",va="top",fontsize=5.6,color="#777")
    # species (row) labels + family headers on the left of EACH panel
    for yy,p in layout:
        ax.text(-0.5,yy-0.12,p["dich"].replace("_"," "),ha="right",va="center",fontsize=8.0,color=RED,fontweight="bold",fontstyle="italic")
        ax.text(-0.5,yy+0.28,f"vs {p['mono'].replace('_',' ')}",ha="right",va="center",fontsize=6.4,color=GY,fontstyle="italic")
    for yy,label in fam_hdr:
        ax.text(-0.5,yy+0.15,label,ha="right",va="center",fontsize=8.0,fontweight="bold",color="#333")
        ax.axhline(yy+0.6,color="#ccc",lw=0.6,zorder=0)
    # per-pair, this-module row totals in the right margin
    mx=ncol+0.3
    ax.text(mx+0.3,top+0.1,f"{module_name} genes under selection",ha="left",va="bottom",fontsize=6.6,color=modc,fontweight="bold")
    ax.text(mx+0.3,top+1.0,"D = dichromat   M = mono sister",ha="left",va="bottom",fontsize=5.6,color="#777")
    key="pigmentation" if module_name.lower().startswith("pig") else "hormone"
    for yy,p in layout:
        dv=sum(1 for g in p["sd"] if gmod.get(g)==key); mv=sum(1 for g in p["sm"] if gmod.get(g)==key)
        ax.text(mx+0.3,yy,f"D: {dv}    M: {mv}",ha="left",va="center",fontsize=6.6,
                color=(RED if dv>mv else ("#333" if dv==mv else GY)),fontfamily="monospace")
    ax.set_xlim(-6.0,ncol+7.0); ax.set_ylim(nrow_units+1.2,top-2.2)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.text((ncol)/2,top-1.6,module_name.upper(),ha="center",fontsize=13,color=modc,fontweight="bold")
    return top

# two stacked panels: pigmentation on top, hormone below; each panel gets full width for its genes
maxcol=max(len(pig_g),len(hor_g))
panel_h=nrow_units*0.42
fig,(axP,axH)=plt.subplots(2,1,figsize=(maxcol*0.62+10,panel_h*2+3.0),
                           gridspec_kw={"hspace":0.14})
topP=draw_panel(axP,pig_g,"Pigmentation",PIG)
topH=draw_panel(axH,hor_g,"Hormone",HOR)

# shared legend + faded-encoding key (top panel), title, totals
axP.legend(handles=[Patch(fc=PIG,label="pigmentation gene under selection"),
                    Patch(fc=HOR,label="hormone gene under selection"),
                    Patch(fc=BLANK,label="not under selection")],
           loc="lower right",frameon=False,fontsize=7.5,bbox_to_anchor=(1.0,-0.02))
kx,ky=len(pig_g)-11,topP-1.6
axP.add_patch(Polygon(tl(kx,ky,0.9),closed=True,facecolor=PIG,edgecolor="none"))
axP.add_patch(Polygon(tr(kx,ky,0.9),closed=True,facecolor=PIG,alpha=0.32,edgecolor="none"))
axP.plot([kx,kx+0.9],[ky+0.45,ky-0.45],color="white",lw=0.6)
axP.text(kx+1.3,ky,"left = dichromatic taxon (solid)    right = monochromatic sister (faded)",fontsize=7.0,va="center",color="#333")
fig.suptitle("Selection in each dichromatic taxon vs its closest monochromatic relative, grouped by clade",
             fontsize=15,fontweight="bold",x=0.02,ha="left",y=0.995)
def _mc(key,mod): return sum(1 for p in pairs for g in p[key] if gmod.get(g)==mod)
dPa,dHa,mPa,mHa=_mc("sd","pigmentation"),_mc("sd","hormone"),_mc("sm","pigmentation"),_mc("sm","hormone")
_enr="NOT enriched in dichromats" if (dPa+dHa)<=(mPa+mHa) else "higher in dichromats"
_tot=(f"Each cell splits diagonally: lower-left = dichromatic species (solid), upper-right = nearest monochromatic sister (faded); colored = gene under episodic selection. "
      f"Totals across {len(pairs)} pairs: dichromats {dPa+dHa} events ({dPa} pigmentation + {dHa} hormone), "
      f"monochromatic sisters {mPa+mHa} ({mPa} pigmentation + {mHa} hormone) - selection is {_enr}.")
fig.text(0.02,0.975,_tot,fontsize=8.0,color="#444",ha="left",fontstyle="italic")
fig.text(0.01,0.004,"aBSREL episodic selection (corrected p<0.05). Bold gene = selected in dichromatic taxon of >=3 pairs. Trachypithecus block shares one sister (T. vetulus). Column margin = # pairs with that gene selected (red=dichromat D, grey=mono sister M); right margin = per-pair gene counts for this module. Marks lineage-specific selection, not proven causation.",fontsize=6.4,color="#777")
fig.tight_layout(rect=[0,0.015,1,0.965])
fig.savefig(f"{base}/fig_sister_pair_contrast.png",dpi=200,bbox_inches="tight"); plt.close(fig)

# ---- Figure B: per-pair network with FIXED layout ----
se=pd.read_csv(f"{base}/data/string_diff_edges.tsv",sep="\t")
L=json.load(open(f"{base}/data/network_layout.json")); pos={k:tuple(v) for k,v in L["pos"].items()}
G=nx.Graph()
for _,e in se.iterrows():
    a,b=e.preferredName_A,e.preferredName_B
    if a in gmod and b in gmod and a in pos and b in pos: G.add_edge(a,b,w=e.score)
pairs_to_plot=[("Trachypithecus_francoisi","Trachypithecus_vetulus"),("Nomascus_concolor","Hylobates_agilis"),
               ("Cercopithecus_hamlyni","Cercopithecus_neglectus"),("Alouatta_caraya","Alouatta_belzebul")]
from adjustText import adjust_text
fig,axes=plt.subplots(2,2,figsize=(15,14))
for ax,(d,m) in zip(axes.flat,pairs_to_plot):
    sd,sm=selset(d),selset(m)
    ax.axvspan(-0.15,0.5,color=PIG,alpha=0.05); ax.axvspan(0.85,1.5,color=HOR,alpha=0.05)
    # module headers sit inside the plot region, well below the title band
    ax.text(0.175,1.12,"pigmentation",ha="center",fontsize=7.5,color=PIG,fontweight="bold")
    ax.text(1.175,1.12,"hormone",ha="center",fontsize=7.5,color=HOR,fontweight="bold")
    for u,v in G.edges():
        cross=gmod[u]!=gmod[v]
        ax.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]],color="#b0b0b0" if cross else "#e4e4e4",lw=0.8 if cross else 0.4,zorder=1)
    import matplotlib.patheffects as pe
    halo=[pe.withStroke(linewidth=1.8,foreground="white")]
    texts=[]
    for n in G.nodes():
        bc=PIG if gmod[n]=="pigmentation" else HOR; ind,inm=n in sd,n in sm; x,yy=pos[n]
        if ind and not inm:
            ax.scatter(x,yy,s=210,c=[bc],edgecolors=RED,linewidths=2.6,zorder=5)
            texts.append(ax.text(x,yy+0.05,n,fontsize=6.2,ha="center",va="bottom",color=RED,fontweight="bold",zorder=6,path_effects=halo))
        elif ind and inm:
            ax.scatter(x,yy,s=120,c=[bc],edgecolors="#444",linewidths=1.1,zorder=4)
            texts.append(ax.text(x,yy+0.045,n,fontsize=5.0,ha="center",va="bottom",color="#222",zorder=6,path_effects=halo))
        elif inm:
            ax.scatter(x,yy,s=110,facecolors="white",edgecolors=bc,linewidths=1.5,zorder=3)
            texts.append(ax.text(x,yy+0.045,n,fontsize=4.6,ha="center",va="bottom",color="#888",zorder=6,path_effects=halo))
        else:
            ax.scatter(x,yy,s=40,c=[bc],alpha=0.12,edgecolors="none",zorder=2)
    # repel the labels so none overlap; connectors drawn where a label is pushed off its node
    adjust_text(texts,ax=ax,expand=(1.2,1.5),arrowprops=dict(arrowstyle="-",color="#999",lw=0.5),
                force_text=(0.5,0.8),force_static=(0.3,0.5))
    # title band ABOVE the plot region; the two annotation lines on a separate lower line
    ax.set_title(f"{d.replace('_',' ')}   vs {m.replace('_',' ')} (nearest monochromatic sister)",
                 fontsize=8.5,color=RED,fontweight="bold",loc="left",pad=10)
    # count annotation at the BOTTOM of the panel so it never collides with the title
    ax.text(0.0,-0.05,f"{len(sd-sm)} genes selected in the dichromatic taxon only (red-ringed)",
            transform=ax.transAxes,fontsize=6.4,color=RED,fontweight="bold")
    ax.set_xlim(-0.28,1.60); ax.set_ylim(-0.22,1.18); ax.axis("off")
leg=[Line2D([0],[0],marker="o",mfc=PIG,mec=RED,mew=3,ls="",ms=13,label="selected in DICHROMATIC only  <- the variation"),
     Line2D([0],[0],marker="o",mfc="#888",mec="#444",mew=1.2,ls="",ms=9,label="selected in both taxa"),
     Line2D([0],[0],marker="o",mfc="white",mec="#888",mew=1.6,ls="",ms=9,label="selected in monochromatic only"),
     Line2D([0],[0],marker="o",mfc="#888",mec="none",ls="",ms=6,alpha=0.3,label="selected in neither")]
fig.legend(handles=leg,loc="lower center",ncol=4,frameon=False,fontsize=6.8,bbox_to_anchor=(0.5,-0.005))
fig.suptitle("Where the selection difference sits in the coupled network (shared gene layout across panels)",fontsize=10.5,y=0.995,x=0.02,ha="left")
fig.text(0.02,0.028,"Nodes = genes (pigmentation left / hormone right, identical positions in every panel); edges = STRING v12 human (score>=0.4). Red-ringed = selected in dichromatic but not sister. Not proven causation.",fontsize=4.8,color="#777")
fig.tight_layout(rect=[0,0.05,1,0.96])
fig.subplots_adjust(hspace=0.28,wspace=0.10)
fig.savefig(f"{base}/fig_sister_network_diff.png",dpi=300,bbox_inches="tight"); plt.close(fig)
print("wrote fig_sister_pair_contrast.png, fig_sister_network_diff.png")
