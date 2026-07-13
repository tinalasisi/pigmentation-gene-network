#!/usr/bin/env Rscript
# nb15_pomc.R — POMC across the primate order (NB15 §5b).
# POMC (pro-opiomelanocortin) sits at the pigmentation–hormone interface: it is the precursor
# cleaved into alpha-MSH (the MC1R ligand driving eumelanin) AND into ACTH/beta-endorphin
# (HPA/endocrine peptides). The panel classifies it as pigmentation (receptor_signaling, OMIM
# hypopigmentation), but its biology is genuinely dual — so it earns a dedicated cross-primate
# selection view rather than a single module label.
#
# Inputs: the phenotype tree + coding (as in nb15_phylo.R) and the full-panel aBSREL branch
# rates for POMC (results/perorigin_v1/branch_rates.csv). Output: figures/nb15_pomc_tree.png.

suppressMessages({library(ape); library(phytools)})
REPO <- Sys.getenv("PIGNET_REPO", unset = "/Users/tlasisi/GitHub/pigmentation-gene-network")
here <- file.path(REPO, "comparative-genomics/analysis/dichromatism_synthesis")

tr  <- read.nexus(file.path(REPO, "comparative-genomics/analysis/coevolution_test/data/primate_phenotype_tree.nex"))
cod <- read.csv(file.path(REPO, "comparative-genomics/config/primate_dichromatism_coding.csv"), stringsAsFactors = FALSE)
cod$tip <- gsub(" ", "_", cod$species_binom)
br  <- read.csv(file.path(REPO, "comparative-genomics/results/perorigin_v1/branch_rates.csv"), stringsAsFactors = FALSE)
pom <- br[br$gene == "POMC", ]

# analysis tree = tree ∩ coding, as elsewhere
sp  <- intersect(tr$tip.label, cod$tip)
x   <- setNames(as.integer(cod$hair_dichromatism_any[match(sp, cod$tip)]), sp)
sp  <- names(x)[!is.na(x)]; x <- x[sp]; trO <- keep.tip(tr, sp)

# POMC selected branches: aBSREL corrected p < 0.05 (selected_flag is a "True"/"False" string).
pom$acp   <- suppressWarnings(as.numeric(pom$absrel_corrected_p))
pom$istip <- pom$is_tip %in% c(TRUE, "True", "true", 1, "1")
pom_sel   <- pom[!is.na(pom$acp) & pom$acp < 0.05, ]
sel_tips  <- intersect(pom_sel$branch[pom_sel$istip], trO$tip.label)
sel_nodes <- pom_sel$branch[!pom_sel$istip]
cat("DEBUG sel rows:", nrow(pom_sel), "tips:", length(sel_tips), "\n")

# tip colours: dichromatic vs mono; ring marks POMC-selected tips
dich_col <- ifelse(x[trO$tip.label] == 1, "#c0392b", "#c9ced6")

png(file.path(here, "figures/nb15_pomc_tree.png"), width = 1900, height = 2300, res = 200)
par(mar = c(4, 1, 4, 12))                       # generous right margin for star labels
plot(trO, type = "phylogram", show.tip.label = FALSE, edge.color = "#7f8c8d",
     edge.width = 1.4, no.margin = FALSE, x.lim = c(0, max(nodeHeights(trO)) * 1.35))
pp <- get("last_plot.phylo", envir = .PlotPhyloEnv)
xmax <- max(pp$xx[1:Ntip(trO)])
# dichromatism status dot at each tip
for (i in seq_len(Ntip(trO))) {
  points(pp$xx[i] + xmax*0.01, pp$yy[i], pch = 15, cex = 0.35, col = dich_col[i], xpd = NA)
}
# POMC-selected tips: purple star + name; stagger labels vertically to avoid overlap
sel_y <- sapply(sel_tips, function(t) pp$yy[which(trO$tip.label == t)])
ord   <- order(sel_y)
sel_tips_o <- sel_tips[ord]; sel_y_o <- sel_y[ord]
# minimum vertical gap between labels
gap <- Ntip(trO) * 0.035
lab_y <- sel_y_o
for (k in 2:length(lab_y)) if (lab_y[k] - lab_y[k-1] < gap) lab_y[k] <- lab_y[k-1] + gap
for (k in seq_along(sel_tips_o)) {
  i <- which(trO$tip.label == sel_tips_o[k])
  points(pp$xx[i] + xmax*0.04, pp$yy[i], pch = 8, cex = 1.2, col = "#8e44ad", lwd = 2, xpd = NA)
  segments(pp$xx[i] + xmax*0.05, pp$yy[i], xmax*1.12, lab_y[k], col = "#c39bd3", lwd = 0.8, xpd = NA)
  text(xmax*1.13, lab_y[k], gsub("_", " ", sel_tips_o[k]), adj = 0, cex = 0.85,
       font = 3, col = "#8e44ad", xpd = NA)
}
legend("bottomleft", inset = c(0.02, 0.02), bty = "n", cex = 0.95,
       pch = c(15, 15, 8), pt.cex = c(1.1, 1.1, 1.1),
       col = c("#c0392b", "#c9ced6", "#8e44ad"),
       legend = c("dichromatic", "monochromatic", "POMC under episodic selection (aBSREL)"))
title(main = "POMC selection across the primate order",
      sub = "star = branch with episodic diversifying selection on POMC; dot = dichromatism state",
      cex.main = 1.1, cex.sub = 0.85)
dev.off()

cat("POMC selected tips on analysis tree:", paste(sel_tips, collapse = ", "), "\n")
cat("POMC selected internal branches:", paste(sel_nodes, collapse = ", "), "\n")
