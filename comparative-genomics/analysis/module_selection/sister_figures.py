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

# ---- Figure A: split-cell matrix ----
layout=[]; y=0; fam_hdr=[]; cur=None
for p in pairs:
    if p["family"]!=cur:
        cur=p["family"]; fam_hdr.append((y,fam_disp.get(cur,cur))); y+=1.1
    layout.append((y,p)); y+=1
nrow_units=y; ncol=len(cols)
def tl(x,y,s=0.9): return [(x,y-s/2),(x+s,y-s/2),(x,y+s/2)]
def tr(x,y,s=0.9): return [(x+s,y-s/2),(x+s,y+s/2),(x,y+s/2)]
fig,ax=plt.subplots(figsize=(max(12,ncol*0.36+5),nrow_units*0.40+3.2))
for yy,p in layout:
    for j,g in enumerate(cols):
        modc=PIG if gmod.get(g)=="pigmentation" else HOR
        ax.add_patch(Rectangle((j,yy-0.45),0.9,0.9,facecolor="white",edgecolor="#dedede",lw=0.4,zorder=1))
        ax.add_patch(Polygon(tl(j,yy),closed=True,facecolor=modc if g in p["sd"] else BLANK,edgecolor="none",zorder=2))
        # monochromatic sister triangle drawn faded (alpha) so the solid dichromatic triangle stands out
        ax.add_patch(Polygon(tr(j,yy),closed=True,facecolor=(modc if g in p["sm"] else BLANK),
                             alpha=(0.32 if g in p["sm"] else 1.0),edgecolor="none",zorder=2))
        ax.plot([j,j+0.9],[yy+0.45,yy-0.45],color="white",lw=0.6,zorder=3)
ax.axvline(len(pig_g),color="#333",lw=1.5,zorder=6)
top=-1.0
for j,g in enumerate(cols):
    modc=PIG if gmod.get(g)=="pigmentation" else HOR
    ax.text(j+0.45,top,g,rotation=90,ha="center",va="bottom",fontsize=5.0,color=modc,fontweight="bold" if rec[g]>=3 else "normal")
ax.text(len(pig_g)/2,top-2.4,"PIGMENTATION",ha="center",fontsize=8,color=PIG,fontweight="bold")
ax.text(len(pig_g)+len(hor_g)/2,top-2.4,"HORMONE",ha="center",fontsize=8,color=HOR,fontweight="bold")
for yy,p in layout:
    ax.text(-0.5,yy-0.12,p["dich"].replace("_"," "),ha="right",va="center",fontsize=5.8,color=RED,fontweight="bold",fontstyle="italic")
    ax.text(-0.5,yy+0.26,f"vs {p['mono'].replace('_',' ')}",ha="right",va="center",fontsize=4.6,color=GY,fontstyle="italic")
for yy,label in fam_hdr:
    ax.text(-0.5,yy+0.15,label,ha="right",va="center",fontsize=6.8,fontweight="bold",color="#333")
    ax.axhline(yy+0.6,color="#ccc",lw=0.6,zorder=0)
ax.set_xlim(-0.5,ncol+0.3); ax.set_ylim(nrow_units-0.3,top-3.0)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_visible(False)
ax.legend(handles=[Patch(fc=PIG,label="pigmentation gene under selection"),Patch(fc=HOR,label="hormone gene under selection"),Patch(fc=BLANK,label="not under selection")],loc="lower right",frameon=False,fontsize=5.6,bbox_to_anchor=(1.0,-0.02))
kx,ky=ncol-9,top-2.1
ax.add_patch(Polygon(tl(kx,ky,0.9),closed=True,facecolor=HOR,edgecolor="none"))
ax.add_patch(Polygon(tr(kx,ky,0.9),closed=True,facecolor=HOR,alpha=0.32,edgecolor="none"))
ax.plot([kx,kx+0.9],[ky+0.45,ky-0.45],color="white",lw=0.6)
ax.text(kx+1.2,ky,"left = dichromatic taxon (solid)    right = monochromatic sister (faded)",fontsize=5.2,va="center",color="#333")
ax.text(-0.5,top-4.2,"Selection in each dichromatic taxon vs its closest monochromatic relative, grouped by clade",fontsize=10,fontweight="bold",ha="left")
ax.text(-0.5,top-3.55,"each cell split diagonally: lower-left = the dichromatic species (solid), upper-right = its nearest monochromatic sister (faded); colored = gene under episodic selection",fontsize=5.6,color="#555",ha="left")
fig.text(0.01,0.004,"aBSREL episodic selection (corrected p<0.05). Bold gene = selected in dichromatic taxon of >=3 pairs. Trachypithecus block shares one sister (T. vetulus). Marks lineage-specific selection, not proven causation.",fontsize=4.4,color="#777")
fig.tight_layout(rect=[0,0.02,1,1])
fig.savefig(f"{base}/fig_sister_pair_contrast.png",dpi=300,bbox_inches="tight"); plt.close(fig)

# ---- Figure B: per-pair network with FIXED layout ----
se=pd.read_csv(f"{base}/data/string_diff_edges.tsv",sep="\t")
L=json.load(open(f"{base}/data/network_layout.json")); pos={k:tuple(v) for k,v in L["pos"].items()}
G=nx.Graph()
for _,e in se.iterrows():
    a,b=e.preferredName_A,e.preferredName_B
    if a in gmod and b in gmod and a in pos and b in pos: G.add_edge(a,b,w=e.score)
pairs_to_plot=[("Trachypithecus_francoisi","Trachypithecus_vetulus"),("Nomascus_concolor","Hylobates_agilis"),
               ("Cercopithecus_hamlyni","Cercopithecus_neglectus"),("Alouatta_caraya","Alouatta_belzebul")]
fig,axes=plt.subplots(2,2,figsize=(14,12.5))
for ax,(d,m) in zip(axes.flat,pairs_to_plot):
    sd,sm=selset(d),selset(m)
    ax.axvspan(-0.15,0.5,color=PIG,alpha=0.05); ax.axvspan(0.85,1.5,color=HOR,alpha=0.05)
    ax.text(0.175,1.30,"pigmentation",ha="center",fontsize=7,color=PIG,fontweight="bold")
    ax.text(1.175,1.30,"hormone",ha="center",fontsize=7,color=HOR,fontweight="bold")
    for u,v in G.edges():
        cross=gmod[u]!=gmod[v]
        ax.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]],color="#b0b0b0" if cross else "#e4e4e4",lw=0.8 if cross else 0.4,zorder=1)
    for n in G.nodes():
        bc=PIG if gmod[n]=="pigmentation" else HOR; ind,inm=n in sd,n in sm; x,yy=pos[n]
        if ind and not inm:
            ax.scatter(x,yy,s=210,c=[bc],edgecolors=RED,linewidths=2.6,zorder=5)
            ax.text(x,yy+0.045,n,fontsize=5.0,ha="center",va="bottom",color=RED,fontweight="bold",zorder=6)
        elif ind and inm:
            ax.scatter(x,yy,s=120,c=[bc],edgecolors="#444",linewidths=1.1,zorder=4)
            ax.text(x,yy+0.04,n,fontsize=4.0,ha="center",va="bottom",color="#333",zorder=6)
        elif inm:
            ax.scatter(x,yy,s=110,facecolors="white",edgecolors=bc,linewidths=1.5,zorder=3)
            ax.text(x,yy+0.04,n,fontsize=3.8,ha="center",va="bottom",color="#999",zorder=6)
        else:
            ax.scatter(x,yy,s=40,c=[bc],alpha=0.12,edgecolors="none",zorder=2)
    ax.set_title(d.replace("_"," "),fontsize=8.5,color=RED,fontweight="bold",loc="left",pad=16)
    ax.text(0.0,1.045,f"vs {m.replace('_',' ')} (nearest monochromatic)",transform=ax.transAxes,fontsize=6,color=GY,fontstyle="italic")
    ax.text(1.0,1.045,f"{len(sd-sm)} genes selected in dichromatic only",transform=ax.transAxes,fontsize=5.8,color=RED,ha="right",fontweight="bold")
    ax.set_xlim(-0.22,1.55); ax.set_ylim(-0.15,1.42); ax.axis("off")
leg=[Line2D([0],[0],marker="o",mfc=PIG,mec=RED,mew=3,ls="",ms=13,label="selected in DICHROMATIC only  <- the variation"),
     Line2D([0],[0],marker="o",mfc="#888",mec="#444",mew=1.2,ls="",ms=9,label="selected in both taxa"),
     Line2D([0],[0],marker="o",mfc="white",mec="#888",mew=1.6,ls="",ms=9,label="selected in monochromatic only"),
     Line2D([0],[0],marker="o",mfc="#888",mec="none",ls="",ms=6,alpha=0.3,label="selected in neither")]
fig.legend(handles=leg,loc="lower center",ncol=4,frameon=False,fontsize=6.8,bbox_to_anchor=(0.5,-0.005))
fig.suptitle("Where the selection difference sits in the coupled network (shared gene layout across panels)",fontsize=10.5,y=0.995,x=0.02,ha="left")
fig.text(0.02,0.028,"Nodes = genes (pigmentation left / hormone right, identical positions in every panel); edges = STRING v12 human (score>=0.4). Red-ringed = selected in dichromatic but not sister. Not proven causation.",fontsize=4.8,color="#777")
fig.tight_layout(rect=[0,0.05,1,0.96])
fig.savefig(f"{base}/fig_sister_network_diff.png",dpi=300,bbox_inches="tight"); plt.close(fig)
print("wrote fig_sister_pair_contrast.png, fig_sister_network_diff.png")
