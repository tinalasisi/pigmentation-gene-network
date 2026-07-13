#!/usr/bin/env Rscript
# tree_figures.R — regenerate phylogenetic tree visualizations from frozen data/.
# Run: Rscript tree_figures.R   (needs ape, phytools, tidyverse)
# Produces: fig_circular_tree_balance.png, fig_phylo_heatmap.png
suppressMessages({library(ape); library(phytools); library(tidyverse)})
base <- dirname(sub("--file=", "", grep("--file=", commandArgs(trailingOnly=FALSE), value=TRUE)))
if (length(base)==0 || base=="") base <- "."
dd <- file.path(base, "data")
BR <- read_csv(file.path(dd,"branch_rates.csv"), show_col_types=FALSE)
OA <- read_csv(file.path(dd,"origin_assignments.csv"), show_col_types=FALSE)
COD<- read_csv(file.path(dd,"species_coding.csv"), show_col_types=FALSE) %>% mutate(species=gsub(" ","_",species))
tr <- read.nexus(file.path(dd,"primate_species_tree.nex"))
PIG<-"#C97B0A"; HOR<-"#2E6E9E"
ramp <- colorRampPalette(c(HOR,"#f2f2f2",PIG))
col_for <- function(b) if(is.na(b)) "#e8e8e8" else ramp(101)[round((b+1)/2*100)+1]

sel <- BR %>% filter(selected_flag==TRUE, is_tip==TRUE)
tipbal <- sel %>% group_by(branch) %>%
  summarise(nP=n_distinct(gene[set=="pigmentation"]), nH=n_distinct(gene[set=="hormone"]), .groups="drop") %>%
  mutate(balance=(nP-nH)/(nP+nH), n_sel=nP+nH)
dich <- COD %>% filter(dichromatic==1) %>% pull(species)
gtips <- unique(BR$branch[BR$is_tip]); trg <- keep.tip(tr, intersect(tr$tip.label, gtips))
n_sel_v<-setNames(rep(0,Ntip(trg)),trg$tip.label); n_sel_v[tipbal$branch]<-tipbal$n_sel
bal_v <- setNames(rep(NA_real_, Ntip(trg)), trg$tip.label); bal_v[tipbal$branch]<-tipbal$balance
labcol <- ifelse(trg$tip.label %in% dich, "#B22222", "grey55")

# --- Fig: circular fan tree ---
png(file.path(base,"fig_circular_tree_balance.png"), width=3000, height=2900, res=300)
par(mar=c(0,0,0,0), xpd=NA)
plotTree(trg, type="fan", fsize=0.001, lwd=0.7, part=0.88, color="grey45")
obj<-get("last_plot.phylo", envir=.PlotPhyloEnv); rng<-max(abs(c(obj$xx,obj$yy)),na.rm=TRUE)
for(i in 1:Ntip(trg)){ ns<-n_sel_v[trg$tip.label[i]]
  cex_i<-if(ns>0) 0.55+1.7*sqrt(ns)/sqrt(max(n_sel_v)) else 0.45
  points(obj$xx[i],obj$yy[i],pch=21,bg=col_for(bal_v[trg$tip.label[i]]),col="grey25",cex=cex_i,lwd=0.5)}
for(i in 1:Ntip(trg)){ a<-atan2(obj$yy[i],obj$xx[i]); deg<-a*180/pi
  srt<-if(obj$xx[i]<0) deg+180 else deg
  text(obj$xx[i]*1.03,obj$yy[i]*1.03,gsub("_"," ",trg$tip.label[i]),srt=srt,
       adj=if(obj$xx[i]<0)1 else 0,cex=0.40,col=labcol[i],
       font=if(trg$tip.label[i]%in%dich)4 else 3,xpd=NA)}
text(0,0.20*rng,"Selection module-balance\nacross the primate tree",cex=0.85,font=2)
text(0,0.04*rng,"dichromatic species",col="#B22222",font=4,cex=0.62)
text(0,-0.01*rng,"monochromatic species",col="grey55",font=3,cex=0.62)
add.color.bar(rng*0.5,ramp(101),title="Module balance",lims=c(-1,1),digits=1,prompt=FALSE,
              x=-rng*0.25,y=-0.11*rng,subtitle="",lwd=9,fsize=0.58)
text(0,-0.17*rng,"< hormone        pigmentation >",cex=0.52,col="grey20")
points(-rng*0.11,-0.27*rng,pch=21,bg="grey80",col="grey25",cex=0.7)
points(rng*0.02,-0.27*rng,pch=21,bg="grey80",col="grey25",cex=1.9)
text(-rng*0.075,-0.27*rng,"few",cex=0.5,col="grey30",pos=2)
text(rng*0.10,-0.27*rng,"many genes",cex=0.5,col="grey30",pos=4)
dev.off()

# --- Fig: phylo.heatmap ---
origin_sp <- OA$species[OA$species %in% trg$tip.label]
trh <- keep.tip(trg, origin_sp)
sel_tip <- BR %>% filter(selected_flag==TRUE, is_tip==TRUE, branch %in% origin_sp)
genes_h <- sel_tip %>% count(gene, set) %>% arrange(set, desc(n))
M <- matrix(0, nrow=length(origin_sp), ncol=nrow(genes_h), dimnames=list(origin_sp, genes_h$gene))
for(i in 1:nrow(sel_tip)) M[sel_tip$branch[i], sel_tip$gene[i]] <- if(sel_tip$set[i]=="pigmentation") 1 else -1
gord <- c(genes_h$gene[genes_h$set=="hormone"], genes_h$gene[genes_h$set=="pigmentation"]); M <- M[, gord]
png(file.path(base,"fig_phylo_heatmap.png"), width=3000, height=2200, res=300)
phylo.heatmap(trh, M, fsize=c(0.5,0.55,0.7), colors=c(HOR,"#f7f7f7",PIG),
              standardize=FALSE, labels=TRUE, split=c(0.35,0.65), lwd=1.2)
dev.off()
cat("wrote fig_circular_tree_balance.png, fig_phylo_heatmap.png\n")
