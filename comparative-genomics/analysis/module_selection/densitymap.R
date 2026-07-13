#!/usr/bin/env Rscript
# ---------------------------------------------------------------------------
# fig_densitymap_dichromatism.png
#
# Stochastic-character-map density map of the dichromatic hair-coloration
# state across a 102-tip primate phylogeny (the genome-sampled subset of a
# 304-tip primate species tree). Shows where on the tree gains and losses of
# sexual dichromatism concentrate, painted as posterior probability of the
# dichromatic state along every branch.
#
# Inputs (from the module data bundle):
#   data/primate_species_tree.nex   304-tip Nexus tree (Genus_species tips)
#   data/branch_rates.csv           aBSREL panel; used only to define the
#                                    102 genome-sampled tips
#                                    (unique(branch_rates$branch[is_tip]))
#   data/species_coding.csv         species -> dichromatic (0/1) coding
#
# Method:
#   1. Prune the 304-tip tree to the 102 genome tips.
#   2. Fit an all-rates-different (ARD) 2-state Markov model of dichromatism
#      with fitMk (FitzJohn root prior) to confirm loss >> gain.
#   3. Sample nsim=200 stochastic character histories with make.simmap
#      (model="ARD"), and summarize the posterior probability of the
#      dichromatic state along every branch with phytools::densityMap.
#   4. Color the density map with a two-color ramp: monochromatic hair
#      (blue, #2E6E9E) -> dichromatic hair (red, #B22222) -- NOT the
#      diverging pigmentation/hormone ramp, because this trait is a binary
#      state probability (0->1), not a signed rate contrast.
#
# Output: fig_densitymap_dichromatism.png (3000 x 4500 px @ 300 dpi)
# ---------------------------------------------------------------------------

suppressMessages({
  library(ape)
  library(phytools)
})

set.seed(42)
NSIM <- 200

## ---- 1. load data ---------------------------------------------------------
tree <- read.nexus("data/primate_species_tree.nex")
br   <- read.csv("data/branch_rates.csv", stringsAsFactors = FALSE)
sc   <- read.csv("data/species_coding.csv", stringsAsFactors = FALSE)
sc$species_us <- gsub(" ", "_", sc$species)

genome_tips <- unique(br$branch[br$is_tip == "True"])
stopifnot(length(genome_tips) == 102)
stopifnot(all(genome_tips %in% tree$tip.label))

tr102 <- keep.tip(tree, genome_tips)
stopifnot(Ntip(tr102) == 102, is.binary(tr102))

trait_num <- setNames(sc$dichromatic[match(genome_tips, sc$species_us)], genome_tips)
stopifnot(!anyNA(trait_num))
n_dichromatic <- sum(trait_num == 1)
stopifnot(n_dichromatic == 21)

trait <- setNames(factor(ifelse(trait_num == 1, "dichromatic", "monomorphic")), genome_tips)

## ---- 2. fit ARD Mk model (sanity check: loss >> gain) --------------------
fitARD <- fitMk(tr102, trait, model = "ARD", pi = "fitzjohn")
Q <- as.Qmatrix(fitARD)
cat("Fitted ARD rates:\n"); print(fitARD)
loss_rate <- Q["dichromatic", "monomorphic"]
gain_rate <- Q["monomorphic", "dichromatic"]
cat(sprintf("loss rate = %.4f, gain rate = %.4f (loss/gain = %.1fx)\n",
            loss_rate, gain_rate, loss_rate / gain_rate))

## ---- 3. stochastic character mapping + density map ------------------------
smap <- make.simmap(tr102, trait, model = "ARD", nsim = NSIM,
                     pi = "fitzjohn", message = FALSE)
dmap <- densityMap(smap, states = c("monomorphic", "dichromatic"),
                    plot = FALSE, res = 200)
dmap <- setMap(dmap, c("#2E6E9E", "#B22222"))

## ---- 4. render --------------------------------------------------------------
dichromatic_tips <- names(trait_num)[trait_num == 1]
tip_font <- setNames(rep(3L, length(genome_tips)), genome_tips)   # 3 = italic
tip_font[dichromatic_tips] <- 4L                                   # 4 = bold italic
tip_cols <- setNames(rep("black", length(genome_tips)), genome_tips)
tip_cols[dichromatic_tips] <- "#B22222"

out_png <- "fig_densitymap_dichromatism.png"
png(out_png, width = 3000, height = 4500, res = 300)
layout(matrix(1:2, nrow = 2), heights = c(0.955, 0.045))

plot(dmap, fsize = c(0.001, 0.9), lwd = c(1.6, 4), ftype = c("off", "reg"),
     legend = FALSE, direction = "rightwards", type = "phylogram",
     outline = FALSE, mar = c(1, 1, 5, 11))

pp <- get("last_plot.phylo", envir = .PlotPhyloEnv)
tip_order <- tr102$tip.label  # order matches pp$xx / pp$yy for tips 1..Ntip
xt <- pp$xx[1:pp$Ntip]
yt <- pp$yy[1:pp$Ntip]
labels_plot <- gsub("_", " ", tip_order)
text(x = xt, y = yt, labels = labels_plot, pos = 4, offset = 0.3,
     cex = 0.42, col = tip_cols[tip_order], font = tip_font[tip_order],
     xpd = TRUE)

mtext("Posterior density of the dichromatic state across the primate tree",
      side = 3, line = 2.6, font = 2, cex = 1.3, adj = 0)
mtext(sprintf("102 genome-sampled primate tips; bold red tip labels = coded dichromatic (n = %d)",
              n_dichromatic),
      side = 3, line = 0.8, font = 1, cex = 0.85, adj = 0)

# custom horizontal color-bar legend (title above, ticks below -> no overlap)
maxH <- max(nodeHeights(tr102))
bar_x0 <- 0.02 * maxH
bar_x1 <- bar_x0 + 0.30 * maxH
bar_y  <- 4
ncols  <- length(dmap$cols)
xs <- seq(bar_x0, bar_x1, length.out = ncols + 1)
for (i in 1:ncols) rect(xs[i], bar_y - 0.7, xs[i + 1], bar_y + 0.7,
                         col = dmap$cols[i], border = NA)
rect(bar_x0, bar_y - 0.7, bar_x1, bar_y + 0.7, border = "black", lwd = 0.8)
text(bar_x0, bar_y - 0.7, "0", pos = 1, cex = 0.8, xpd = TRUE)
text(bar_x1, bar_y - 0.7, "1", pos = 1, cex = 0.8, xpd = TRUE)
text((bar_x0 + bar_x1) / 2, bar_y + 0.7,
     "Posterior probability of dichromatic state", pos = 3, cex = 0.8, xpd = TRUE)

# caption panel: spans the full figure width so long lines wrap cleanly
cap <- paste0(
  "Stochastic character mapping of hair sexual dichromatism (binary trait) on the 102 genome-sampled primate tips, ",
  "model = ARD (loss rate ", sprintf("%.3f", loss_rate),
  " > gain rate ", sprintf("%.3f", gain_rate),
  " per unit branch length, ", sprintf("%.1f", loss_rate / gain_rate), "x), nsim = ", NSIM, " simulated histories. ",
  "Branch color = posterior probability of the dichromatic state (blue = monomorphic, red = dichromatic); ",
  "hot (red) branches mark high posterior support for dichromatism and concentrate on multiple, phylogenetically ",
  "scattered branches, consistent with repeated independent origins rather than a single ancestral acquisition."
)
par(mar = c(0, 1, 0, 1))
plot.new()
cap_wrapped <- paste(strwrap(cap, width = 175), collapse = "\n")
text(0, 0.9, cap_wrapped, adj = c(0, 1), cex = 0.72, xpd = TRUE)

dev.off()
cat("Saved:", out_png, "\n")
