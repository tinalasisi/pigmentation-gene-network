#!/usr/bin/env Rscript
###############################################################################
# 04_rerconverge.R — convergent relative-evolutionary-rate test for dichromatism
#
# RERconverge (Chikina/Robinson/Clark 2016 MBE doi:10.1093/molbev/msw112;
# Kowalczyk et al. 2019 Bioinformatics doi:10.1093/bioinformatics/btz468)
# asks whether genes show CONVERGENT rate shifts on lineages bearing a trait
# — the direct statistical form of "independent origins of dichromatism act on
# the same genes." Complements HyPhy: RERconverge is a rate-vs-trait CORRELATION
# across all genes at once, not a per-gene foreground/background LRT.
#
# INPUT (all produced upstream, no data transfer needed):
#   aln/<gene>.codon.aln.fa      per-gene codon alignments (from 02)
#   primate_species_tree.nex      master primate tree (topology source)
#   species_states.csv           species,dichromatism  (foreground = dichromatic)
# What RERconverge actually needs: a set of per-gene trees WITH BRANCH LENGTHS
# in substitutions/site on a COMMON topology. We build those here with phangorn
# (ML branch lengths per gene on the fixed species topology), then run RER.
#
# OUTPUT (small, paste/commit-able):
#   report/rer_results.csv       gene, set, rho, p, p.adj, n_tip
#   report/rer_enrichment.csv    set-level (pigmentation vs hormone) summary
#   report/rer_plots/<gene>.png  plotRers strip for top hits (optional)
#
# Tools: R with RERconverge, phangorn, ape, geiger. Install:
#   BiocManager or: remotes::install_github("nclark-lab/RERconverge")
###############################################################################
suppressMessages({
  library(ape); library(phangorn)
  ok <- requireNamespace("RERconverge", quietly=TRUE)
})
if (!ok) stop("RERconverge not installed: remotes::install_github('nclark-lab/RERconverge')")
library(RERconverge)

args <- commandArgs(trailingOnly=TRUE)
aln_dir  <- if (length(args)>=1) args[1] else "aln"
tree_nex <- if (length(args)>=2) args[2] else "primate_species_tree.nex"
states_f <- if (length(args)>=3) args[3] else "species_states.csv"
dir.create("report", showWarnings=FALSE)
dir.create("report/rer_plots", showWarnings=FALSE)

panel  <- read.csv("gene_panel.csv", stringsAsFactors=FALSE)   # gene,set
states <- read.csv(states_f, stringsAsFactors=FALSE)           # species,dichromatism,...
states$species <- gsub(" ", "_", states$species)
fg <- states$species[grepl("^dichro", states$dichromatism)]

# --- master topology: prune the primate tree to species we have alignments for
master <- read.nexus(tree_nex)
master$tip.label <- gsub(" ", "_", master$tip.label)

# --- build per-gene trees with ML branch lengths on the fixed topology ----
aln_files <- list.files(aln_dir, pattern="\\.codon\\.aln\\.fa$", full.names=TRUE)
tree_lines <- c(); genes_done <- c()
for (f in aln_files) {
  gene <- sub("\\.codon\\.aln\\.fa$", "", basename(f))
  aln  <- tryCatch(read.phyDat(f, format="fasta", type="DNA"), error=function(e) NULL)
  if (is.null(aln)) next
  tips <- names(aln)
  tips <- intersect(tips, master$tip.label)
  if (length(tips) < 4) next
  gtop <- keep.tip(master, tips)
  # ML branch lengths (GTR+G) on the fixed topology
  aln2 <- subset(aln, subset=tips)
  fit  <- tryCatch(pml(gtop, data=aln2), error=function(e) NULL); if (is.null(fit)) next
  fit  <- tryCatch(optim.pml(fit, optEdge=TRUE, optBf=TRUE, optQ=TRUE,
                             control=pml.control(trace=0)), error=function(e) NULL)
  if (is.null(fit)) next
  tr <- fit$tree
  tree_lines <- c(tree_lines, write.tree(tr)); genes_done <- c(genes_done, gene)
}
if (length(genes_done) < 3) stop("Too few gene trees built (", length(genes_done), ") — need >=3 for RER.")
# RERconverge reads a Newick "trees file": first line = master tree, then <gene>\t<newick>
tf <- "report/gene_trees.txt"
writeLines(c(write.tree(master),
             paste(genes_done, tree_lines, sep="\t")), tf)

# --- RERconverge core ------------------------------------------------------
trees <- readTrees(tf, max.read=Inf)
RERmat <- getAllResiduals(trees, transform="sqrt", weighted=TRUE, scale=TRUE)
# foreground path from the tips (binary trait); infer internal fg edges
fg_in <- intersect(fg, trees$masterTree$tip.label)
paths <- tryCatch(foreground2Paths(fg_in, trees, clade="all"),
                  error=function(e) foreground2Tree(fg_in, trees, clade="all", plotTree=FALSE))
cor  <- correlateWithBinaryPhenotype(RERmat, paths, min.sp=4, min.pos=2)

res <- data.frame(gene=rownames(cor), rho=cor$Rho, p=cor$P, p.adj=cor$p.adj,
                  n=cor$N, stringsAsFactors=FALSE)
res <- merge(res, panel, by="gene", all.x=TRUE)
res <- res[order(res$p), ]
write.csv(res, "report/rer_results.csv", row.names=FALSE)

# --- set-level summary: is pigmentation vs hormone enriched for rate shifts? --
setsum <- do.call(rbind, lapply(split(res, res$set), function(d) {
  data.frame(set=d$set[1], n_genes=nrow(d),
             n_p05=sum(d$p<0.05, na.rm=TRUE),
             median_rho=median(d$rho, na.rm=TRUE),
             # Wilcoxon of rho vs 0 (directional convergent-shift signal)
             wilcox_p=tryCatch(wilcox.test(d$rho)$p.value, error=function(e) NA))
}))
write.csv(setsum, "report/rer_enrichment.csv", row.names=FALSE)

# --- plotRers strips for top hits -----------------------------------------
top <- head(res$gene[!is.na(res$p)], 6)
for (g in top) {
  png(sprintf("report/rer_plots/%s.png", g), width=1400, height=700, res=170)
  tryCatch(plotRers(RERmat, g, phenv=paths), error=function(e) plot.new())
  dev.off()
}
cat("DONE. rer_results.csv (", nrow(res), " genes), rer_enrichment.csv (set-level).\n", sep="")
print(setsum)
