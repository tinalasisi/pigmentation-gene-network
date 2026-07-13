#!/usr/bin/env Rscript
# ============================================================================
# Phylomorphospace of pigmentation vs. hormone selection load
# across a 102-tip primate phylogeny (genome-sampled subset).
#
# Reproduces fig_phylomorphospace.png from the module data bundle.
#
# Inputs (relative to this script's --data-dir, default "./data"):
#   primate_species_tree.nex   304-tip Nexus tree
#   branch_rates.csv           gene x branch aBSREL results (pigmentation/hormone)
#   species_coding.csv         species -> dichromatic (0/1)
#
# Method:
#   - Prune the 304-tip tree to the 102 genome-sampled tips present in
#     branch_rates (branch, is_tip==TRUE).
#   - For each tip, pigmentation load = # distinct pigmentation genes with
#     selected_flag==TRUE on that terminal branch (episodic selection,
#     aBSREL corrected p<0.05); hormone load = same for hormone-module genes.
#   - Ancestral states at internal nodes are estimated by maximum-likelihood
#     Brownian-motion reconstruction (phytools::fastAnc) independently on
#     each axis, then phytools::phylomorphospace projects the whole tree
#     (tips + reconstructed internal nodes) into this 2-D selection space.
#   - Dichromatic species (species_coding$dichromatic==1, intersected with
#     the 102 genome tips; n=21) are highlighted in red; all other tips are
#     grey. Points along the diagonal show joint pigmentation+hormone
#     selection; points on the x-axis only are pigmentation-driven; points
#     on the y-axis only are hormone-driven.
# ============================================================================

suppressPackageStartupMessages({
  library(ape)
  library(phytools)
  library(tidyverse)
})

## ---------------------------------------------------------------------
## 0. Paths
## ---------------------------------------------------------------------
data_dir <- "data"
out_png  <- "fig_phylomorphospace.png"

tree_path    <- file.path(data_dir, "primate_species_tree.nex")
rates_path   <- file.path(data_dir, "branch_rates.csv")
coding_path  <- file.path(data_dir, "species_coding.csv")

## ---------------------------------------------------------------------
## 1. Load data
## ---------------------------------------------------------------------
tree_full      <- read.nexus(tree_path)
branch_rates   <- read_csv(rates_path, show_col_types = FALSE)
species_coding <- read_csv(coding_path, show_col_types = FALSE)

# normalize species naming: tree uses underscores, species_coding may use spaces
species_coding$species <- gsub(" ", "_", species_coding$species)

## ---------------------------------------------------------------------
## 2. Define the 102-tip genome-sampled subset & prune the tree
## ---------------------------------------------------------------------
genome_tips <- unique(branch_rates$branch[branch_rates$is_tip])
stopifnot(all(genome_tips %in% tree_full$tip.label))

tree102 <- keep.tip(tree_full, genome_tips)
stopifnot(is.binary(tree102), is.rooted(tree102))

## ---------------------------------------------------------------------
## 3. Selection load per tip: # distinct selected genes per module
## ---------------------------------------------------------------------
tip_load <- branch_rates %>%
  filter(is_tip, branch %in% genome_tips) %>%
  group_by(branch, set) %>%
  summarise(n_selected = sum(selected_flag, na.rm = TRUE), .groups = "drop") %>%
  pivot_wider(names_from = set, values_from = n_selected, values_fill = 0)

if (!"pigmentation" %in% names(tip_load)) tip_load$pigmentation <- 0
if (!"hormone"      %in% names(tip_load)) tip_load$hormone      <- 0

tip_load <- tip_load %>%
  rename(pig_load = pigmentation, hor_load = hormone) %>%
  select(branch, pig_load, hor_load)

# 102 x 2 tip matrix in tree tip order
X <- as.matrix(tip_load %>% select(pig_load, hor_load))
rownames(X) <- tip_load$branch
X <- X[tree102$tip.label, ]
colnames(X) <- c("Pigmentation selection load", "Hormone selection load")

## ---------------------------------------------------------------------
## 4. Dichromatic tips (highlight set)
## ---------------------------------------------------------------------
dichrom_tips <- intersect(
  species_coding$species[species_coding$dichromatic == 1],
  tree102$tip.label
)
stopifnot(length(dichrom_tips) == 21)  # sanity check against known panel composition

## ---------------------------------------------------------------------
## 5. Ancestral state reconstruction (ML, Brownian motion, per axis)
## ---------------------------------------------------------------------
A <- apply(X, 2, fastAnc, tree = tree102)
colnames(A) <- colnames(X)
rownames(A) <- (Ntip(tree102) + 1):(Ntip(tree102) + tree102$Nnode)

## ---------------------------------------------------------------------
## 6. Colors (data-fidelity: categorical, no continuous ramp needed here
##    since loads are counts with a natural zero — no undefined/infinite
##    values enter this axis, so no diverging-ramp censoring is required)
## ---------------------------------------------------------------------
col_dichromatic <- "#B22222"
col_mono        <- "grey45"
col_pig         <- "#C97B0A"
col_hor         <- "#2E6E9E"

alpha_col <- function(hex, alpha) {
  rgb_ <- col2rgb(hex) / 255
  rgb(rgb_[1], rgb_[2], rgb_[3], alpha = alpha)
}

n_tip  <- Ntip(tree102)
n_node <- tree102$Nnode
max_node <- max(tree102$edge)

# Internal tree-drawing layer stays semi-transparent grey so overlapping
# ancestral-node clusters remain legible; TIP markers are re-drawn fully
# opaque afterwards (categorical dichromatic/monochromatic status must never
# be obscured by alpha blending between overlapping tips).
tip_fill_faint <- setNames(rep(alpha_col(col_mono, 0.55), n_tip), tree102$tip.label)
tip_fill_faint[dichrom_tips] <- alpha_col(col_dichromatic, 0.55)

tip_fill_by_node  <- setNames(tip_fill_faint[tree102$tip.label], as.character(1:n_tip))
node_fill_by_node <- setNames(rep("grey88", n_node), as.character((n_tip + 1):(n_tip + n_node)))
col_node_vec <- c(tip_fill_by_node, node_fill_by_node)[as.character(1:max_node)]
col_edge_vec <- setNames(rep("grey75", nrow(tree102$edge)), as.character(tree102$edge[, 2]))

## ---------------------------------------------------------------------
## 7. Notable tips to label: high joint / high single-module load
## ---------------------------------------------------------------------
notable_df <- tip_load %>%
  filter(pig_load >= 4 | hor_load >= 6) %>%
  arrange(desc(pig_load + hor_load))
notable_tips <- notable_df$branch

## ---------------------------------------------------------------------
## 8. Plot
## ---------------------------------------------------------------------
expand_range <- function(x, factor = 1.15) {
  rr <- x[2] - x[1]; mm <- mean(x)
  c(mm - rr * factor / 2, mm + rr * factor / 2)
}
xlim <- expand_range(range(c(X[, 1], A[, 1])))
ylim <- expand_range(range(c(X[, 2], A[, 2])))
xlim[1] <- min(xlim[1], -0.4)
ylim[1] <- min(ylim[1], -0.4)

png(out_png, width = 3000, height = 2750, res = 300)
layout(matrix(1:2, nrow = 2), heights = c(11, 2.0))

par(mar = c(5, 5.5, 4.5, 2.5), xaxs = "i", yaxs = "i")
plot(NULL, xlim = xlim, ylim = ylim,
     xlab = "", ylab = "", axes = FALSE, main = "")

# quadrant / diagonal guides (drawn first, underneath the tree)
usr <- par("usr")
rect(usr[1], usr[3], 0, 0, col = alpha_col(col_hor, 0.06), border = NA)   # neither axis informative near origin (kept neutral)
abline(v = 0, col = "grey80", lty = 2, lwd = 1)
abline(h = 0, col = "grey80", lty = 2, lwd = 1)
abline(a = 0, b = 1, col = "grey75", lty = 3, lwd = 1.1)  # diagonal: joint pig+hormone load
# soft axis-band tints to mark pigmentation-only vs hormone-only regions
rect(usr[1], 0.001, usr[2], usr[4], col = alpha_col(col_hor, 0.035), border = NA)
rect(0.001, usr[3], usr[2], usr[4], col = alpha_col(col_pig, 0.035), border = NA)

box(bty = "l")
axis(1, cex.axis = 1.1)
axis(2, cex.axis = 1.1, las = 1)
mtext("Pigmentation selection load  (# genes, episodic selection, aBSREL corrected p<0.05)",
      side = 1, line = 3, cex = 1.05, col = col_pig, font = 2)
mtext("Hormone selection load  (# genes, episodic selection, aBSREL corrected p<0.05)",
      side = 2, line = 3.6, cex = 1.05, col = col_hor, font = 2)

phylomorphospace(tree102, X, A = A, label = "off",
                  control = list(col.edge = col_edge_vec, col.node = col_node_vec),
                  node.size = c(1.0, 1.9), lwd = 1.1, pch = 21,
                  xlim = xlim, ylim = ylim, add = TRUE, axes = FALSE,
                  xlab = "", ylab = "")

# Re-stroke TIP markers fully opaque (never alpha-blended) so categorical
# dichromatic/monochromatic status is never visually diluted by overlap.
# Monochromatic tips are drawn first, dichromatic (rarer, higher-priority
# signal) drawn last so they sit on top at shared coordinates.
tip_xy <- X[tree102$tip.label, ]
is_dichrom <- tree102$tip.label %in% dichrom_tips
draw_order <- order(is_dichrom)  # FALSE (mono) first, TRUE (dichromatic) last
points(tip_xy[draw_order, 1], tip_xy[draw_order, 2], pch = 21, cex = 1.9,
       bg  = ifelse(is_dichrom[draw_order], col_dichromatic, col_mono),
       col = ifelse(is_dichrom[draw_order], "black", "grey20"),
       lwd = ifelse(is_dichrom[draw_order], 1.3, 0.7))

# Label notable tips. Where >=2 notable tips share exact (x,y) (overplotted
# markers), merge into one multi-line label anchored at that point rather
# than drawing overlapping text strings on top of each other.
lab_df <- tip_load %>%
  filter(branch %in% notable_tips) %>%
  mutate(label = gsub("_", " ", branch)) %>%
  group_by(pig_load, hor_load) %>%
  summarise(label = paste(label, collapse = "\n"), .groups = "drop")

pos_vec <- ifelse(lab_df$pig_load > mean(xlim), 2, 4)
text(lab_df$pig_load, lab_df$hor_load, labels = lab_df$label, cex = 0.70, font = 3,
     pos = pos_vec, offset = 0.6, xpd = NA)

title(main = "Phylomorphospace of pigmentation vs hormone selection load",
      cex.main = 1.5, font.main = 1, line = 2.2)

legend("topleft", inset = c(0.01, 0.0),
       legend = c("Dichromatic species (n=21)", "Monochromatic species", "Ancestral node (ML reconstruction)"),
       pch = 21, pt.bg = c(alpha_col(col_dichromatic, 0.85), alpha_col(col_mono, 0.70), "grey88"),
       col = c(col_dichromatic, "grey35", "grey50"),
       pt.cex = c(1.6, 1.6, 1.3), cex = 0.95, bty = "n")

par(mar = c(0.5, 5.5, 0, 2.5))
plot(NULL, xlim = c(0, 1), ylim = c(0, 1), axes = FALSE, xlab = "", ylab = "")
caption_lines <- c(
  "Axes = number of selected genes per module per terminal branch (aBSREL episodic selection, corrected p<0.05).",
  "Tree: n=102 genome-sampled primate tips pruned from a 304-tip backbone. Internal-node positions are maximum-",
  "likelihood ancestral-state reconstructions (Brownian motion, phytools::fastAnc) estimated independently on each",
  "axis, following the phylomorphospace projection of Sidlauskas (2008, Evolution). Dashed diagonal = joint",
  "pigmentation + hormone selection; points hugging the x-axis are pigmentation-driven, points hugging the y-axis",
  "are hormone-driven. Red = dichromatic species (n=21); grey = monochromatic (n=81)."
)
text(0, 1, paste(caption_lines, collapse = "\n"), adj = c(0, 1), cex = 0.80, family = "sans")
dev.off()

cat("Saved:", out_png, "\n")
