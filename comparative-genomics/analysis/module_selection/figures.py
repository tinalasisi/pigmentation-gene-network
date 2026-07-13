"""figures.py — regenerate module-selection figures from frozen data in ./data/.
Run: python figures.py   (needs pandas, matplotlib)
Produces: fig_module_balance.png, fig_per_lineage_genes.png
"""
import pandas as pd, matplotlib as mpl, matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import os
base=os.path.dirname(os.path.abspath(__file__)); dd=os.path.join(base,"data")
PIG="#C97B0A"; HOR="#2E6E9E"
mpl.rcParams.update({"font.family":"DejaVu Sans","axes.titleweight":"bold","figure.dpi":100})
BR=pd.read_csv(f"{dd}/branch_rates.csv"); OA=pd.read_csv(f"{dd}/origin_assignments.csv")
K=pd.read_csv(f"{dd}/per_origin_K.csv"); GM=pd.read_csv(f"{dd}/gene_modules.csv")
gmod=dict(zip(GM.gene,GM.module))
fam_order=["hylobatidae","cercopithecidae","cebidae","lemuridae"]
fam_disp={f:f.capitalize() for f in fam_order}
sel=BR[(BR.selected_flag==True)&(BR.is_tip==True)].merge(OA[["species","origin_id"]],left_on="branch",right_on="species")
relax_sig=set(zip(K[K.p_BH<0.05].origin_id,K[K.p_BH<0.05].gene))
bal=sel.groupby("origin_id").apply(lambda s:pd.Series({"nP":s[s.gene.map(gmod)=="pigmentation"].gene.nunique(),"nH":s[s.gene.map(gmod)=="hormone"].gene.nunique()})).reset_index()
bal["balance"]=(bal.nP-bal.nH)/(bal.nP+bal.nH)
meta=OA.groupby("origin_id").agg(family=("family","first"),sp=("species","first"),n=("species","size")).reset_index()
bal=bal.merge(meta,on="origin_id")
bal["family"]=pd.Categorical(bal.family,categories=fam_order,ordered=True)
bal=bal.sort_values(["family","balance"]).reset_index(drop=True)
rep=meta.set_index("origin_id").to_dict("index")
order=bal.origin_id.tolist()

# --- Fig 1: module balance ---
rows=[];y=0;yt=[];yl=[];hd=[]
for fam in fam_order:
    sub=bal[bal.family==fam]
    if len(sub)==0: continue
    hd.append((y,fam_disp[fam]));y+=1
    for _,r in sub.iterrows():
        rows.append((y,r));yt.append(y)
        yl.append((r.sp.replace("_"," "),r.n,r.origin_id));y+=1
    y+=0.4
fig,ax=plt.subplots(figsize=(8,6.4))
for yy,r in rows:
    b=r.balance;col=PIG if b>0 else (HOR if b<0 else "#888")
    ax.barh(yy,b,height=0.62,color=col,alpha=0.9,zorder=3,edgecolor="black" if r.origin_id in ("origin_7","origin_8","origin_14") else "none",linewidth=1.6 if r.origin_id in ("origin_7","origin_8","origin_14") else 0)
    lbl=f"{int(r.nP)}P/{int(r.nH)}H"
    if b<=-0.99: ax.text(0.03,yy,lbl,va="center",ha="left",fontsize=5.4)
    elif b>=0.99: ax.text(b*0.88,yy,lbl,va="center",ha="right",fontsize=5.4,color="white",zorder=5)
    else: ax.text(b+(0.035 if b>=0 else -0.035),yy,lbl,va="center",ha="left" if b>=0 else "right",fontsize=5.4)
ax.axvline(0,color="#444",lw=1,zorder=2)
for yy,f in hd: ax.text(-1.52,yy,f,fontweight="bold",fontsize=7,va="center")
import textwrap as _tw
for yy,(nm,n,oid) in zip(yt,yl):
    spp=sorted(OA[OA.origin_id==oid].species.tolist())
    if n==1: lab, fs = spp[0].replace("_"," "), 6.0
    else:
        g=spp[0].split("_")[0]; epis=[s.split("_")[1] for s in spp]
        full=f"{g} "+", ".join(epis)
        if len(full)<=34: lab, fs = full, 5.6
        else: lab, fs = g+"\n"+_tw.fill(", ".join(epis),width=42), 4.8
    ax.text(-1.52,yy,f"   {lab}",fontstyle="italic",fontsize=fs,va="center")
ax.set_ylim(y,-1);ax.set_xlim(-1.60,1.42);ax.set_yticks([])
for s in ["left","right","top"]: ax.spines[s].set_visible(False)
ax.set_xlabel("<- hormone module          pigmentation module ->",labelpad=6)
ax.set_xticks([-1,-.5,0,.5,1]);ax.set_xticklabels(["-1","","0","","+1"])
ax.set_title("Each dichromatism origin tilts toward a different module",loc="left",fontsize=8,pad=10)
ax.legend(handles=[Patch(fc=HOR,label="hormone-tilted"),Patch(fc=PIG,label="pigmentation-tilted"),Line2D([0],[0],marker="s",mfc="#ccc",mec="black",mew=1.6,ls="",label="RELAX-powered origin")],loc="lower right",frameon=False,fontsize=5.6)
fig.tight_layout();fig.savefig(f"{base}/fig_module_balance.png",dpi=300,bbox_inches="tight")

# --- Fig 2: gene dot-matrix ---
freq=sel.groupby("gene").origin_id.nunique()
hor_g=sorted([g for g in sel.gene.unique() if gmod.get(g)=="hormone"],key=lambda g:(-freq.get(g,0),g))
pig_g=sorted([g for g in sel.gene.unique() if gmod.get(g)=="pigmentation"],key=lambda g:(-freq.get(g,0),g))
genes=hor_g+pig_g;gx={g:i for i,g in enumerate(genes)};oy={o:i for i,o in enumerate(order)}
fig,ax=plt.subplots(figsize=(12,5.8))
for o in order:
    for _,r in sel[sel.origin_id==o].iterrows():
        g=r.gene
        if g not in gx: continue
        ax.scatter(gx[g],oy[o],s=54,color=HOR if gmod.get(g)=="hormone" else PIG,alpha=0.9,zorder=3,edgecolor="black" if (o,g) in relax_sig else "none",linewidth=1.4 if (o,g) in relax_sig else 0)
ax.set_xticks(range(len(genes)));ax.set_xticklabels(genes,rotation=90,fontsize=5.2,fontstyle="italic")
for t,g in zip(ax.get_xticklabels(),genes): t.set_color(HOR if gmod.get(g)=="hormone" else PIG)
ax.set_yticks(range(len(order)));ax.set_yticklabels([rep[o]["sp"].replace("_"," ")+(f" (+{rep[o]['n']-1})" if rep[o]['n']>1 else "") for o in order],fontsize=6,fontstyle="italic")
ax.set_ylim(len(order)-0.5,-0.5);ax.set_xlim(-0.6,len(genes)-0.4)
ax.axvline(len(hor_g)-0.5,color="#bbb",lw=0.8,ls="--")
ax.text((len(hor_g)-1)/2,-1.15,"hormone module",color=HOR,fontsize=7,fontweight="bold",ha="center")
ax.text(len(hor_g)+(len(pig_g)-1)/2,-1.15,"pigmentation module",color=PIG,fontsize=7,fontweight="bold",ha="center")
for s in ["top","right","left"]: ax.spines[s].set_visible(False)
ax.tick_params(left=False)
ax.legend(handles=[Line2D([0],[0],marker="o",mfc=HOR,mec="none",ls="",label="hormone selected"),Line2D([0],[0],marker="o",mfc=PIG,mec="none",ls="",label="pigmentation selected"),Line2D([0],[0],marker="o",mfc="#ccc",mec="black",mew=1.4,ls="",label="RELAX-confirmed")],loc="lower right",bbox_to_anchor=(1,1.06),frameon=False,fontsize=5.8,ncol=3)
ax.set_title("Genes under selection along each dichromatism origin, by module",loc="left",fontsize=8.5,pad=30)
fig.tight_layout();fig.savefig(f"{base}/fig_per_lineage_genes.png",dpi=300,bbox_inches="tight")
print("wrote fig_module_balance.png, fig_per_lineage_genes.png")
