#!/usr/bin/env Rscript
# =============================================================================
# fig_contmap_module_balance.R
#
# Reconstructs and plots module balance of episodic positive selection
# (pigmentation vs. hormone gene modules) across the primate phylogeny,
# using a phytools contMap (ancestral ML reconstruction of a continuous
# trait mapped onto branches).
#
# Inputs (relative to this script's working directory, under ./data/):
#   data/primate_species_tree.nex   304-tip primate phylogeny (Nexus)
#   data/branch_rates.csv           per-gene x branch aBSREL episodic-selection calls
#   data/species_coding.csv         species x dichromatism coding
#   data/gene_modules.csv           gene -> module (pigmentation | hormone) lookup
#
# Output:
#   fig_contmap_module_balance.png  (3000 x ~3900 px @ 300 dpi)
#
# Requires: ape, phytools, tidyverse (dplyr/tidyr/tibble)
# =============================================================================

suppressPackageStartupMessages({
  library(ape)
  library(phytools)
  library(tidyverse)
})

set.seed(42)

# ---- 1. Load data -----------------------------------------------------------

tree <- read.nexus("data/primate_species_tree.nex")

branch_rates <- read.csv("data/branch_rates.csv", stringsAsFactors = FALSE)
# is_tip / selected_flag / tested arrive as the strings "True"/"False"
branch_rates$is_tip        <- branch_rates$is_tip        == "True"
branch_rates$selected_flag <- branch_rates$selected_flag == "True"
branch_rates$tested        <- branch_rates$tested        == "True"

species_coding <- read.csv("data/species_coding.csv", stringsAsFactors = FALSE)
species_coding$species <- gsub(" ", "_", species_coding$species)  # normalize to tree naming

gene_modules <- read.csv("data/gene_modules.csv", stringsAsFactors = FALSE)

# ---- 2. Identify the 102 genome-sampled tips --------------------------------

genome_tips <- unique(branch_rates$branch[branch_rates$is_tip])
stopifnot(length(genome_tips) == 102)
stopifnot(all(genome_tips %in% tree$tip.label))

dichrom_tips <- intersect(species_coding$species[species_coding$dichromatic == 1], genome_tips)
stopifnot(length(dichrom_tips) == 21)

# ---- 3. Per-tip module balance ----------------------------------------------
# balance = (n_pigmentation_selected - n_hormone_selected) /
#           (n_pigmentation_selected + n_hormone_selected)
# Tips with zero selected genes in either module (no episodic selection
# detected on that terminal branch, in either module) are set to 0 (neutral),
# NOT dropped -- this is a deliberate modeling choice, flagged in the caption.

tip_module_counts <- branch_rates %>%
  filter(is_tip, branch %in% genome_tips, selected_flag) %>%
  distinct(branch, gene, set) %>%
  count(branch, set) %>%
  pivot_wider(names_from = set, values_from = n, values_fill = 0)

if (!"pigmentation" %in% names(tip_module_counts)) tip_module_counts$pigmentation <- 0
if (!"hormone"       %in% names(tip_module_counts)) tip_module_counts$hormone       <- 0

full_tips <- tibble(branch = genome_tips) %>%
  left_join(tip_module_counts, by = "branch") %>%
  mutate(
    pigmentation = replace_na(pigmentation, 0),
    hormone       = replace_na(hormone, 0),
    balance = ifelse((pigmentation + hormone) == 0, 0,
                      (pigmentation - hormone) / (pigmentation + hormone))
  )

n_neutral_tips <- sum(full_tips$pigmentation + full_tips$hormone == 0)

# ---- 4. Prune tree to genome-sampled tips and build the named trait vector --

tree102 <- keep.tip(tree, genome_tips)
if (!is.binary(tree102)) tree102 <- multi2di(tree102)
tree102$edge.length[tree102$edge.length <= 0] <- 1e-8  # avoid zero-length edges (anc.ML requirement)

balance_vec <- setNames(full_tips$balance, full_tips$branch)
balance_vec <- balance_vec[tree102$tip.label]
stopifnot(length(balance_vec) == 102, !any(is.na(balance_vec)))

# ---- 5. Ancestral reconstruction (contMap, anc.ML) --------------------------
# NOTE: contMap's internal-branch values are maximum-likelihood ancestral
# state reconstructions under a Brownian-motion model of continuous-trait
# evolution -- they are model-based inferences, not observed rates, and
# should be interpreted as such (see caption).

cm <- contMap(tree102, balance_vec, method = "anc.ML", plot = FALSE)

# Recolor with a diverging ramp centered at the semantic zero (balanced
# selection pressure between the two modules), independent of contMap's
# default sequential palette.
ramp <- colorRampPalette(c("#2E6E9E", "#f2f2f2", "#C97B0A"))
cm <- setMap(cm, ramp(1001))
stopifnot(cm$lims[1] == -1, cm$lims[2] == 1)  # confirm symmetric limits -> ramp midpoint = 0

# ---- 6. Plot -----------------------------------------------------------------

n_tip <- length(cm$tree$tip.label)
dichrom_flag <- cm$tree$tip.label %in% dichrom_tips

draw_colorbar <- function(cols, lims, x, y, width, height, title, cex = 0.85) {
  n <- length(cols)
  xs <- seq(x, x + width, length.out = n + 1)
  for (i in 1:n) rect(xs[i], y, xs[i + 1], y + height, col = cols[i], border = NA)
  rect(x, y, x + width, y + height, border = "black", lwd = 0.8)
  text(x,            y - 0.15 * height, labels = round(lims[1], 1), pos = 1, cex = cex, xpd = NA)
  text(x + width,    y - 0.15 * height, labels = round(lims[2], 1), pos = 1, cex = cex, xpd = NA)
  text(x + width / 2, y - 0.15 * height, labels = "0",              pos = 1, cex = cex, xpd = NA)
  text(x + width / 2, y + height + 0.25 * height, labels = title,   cex = cex, xpd = NA)
}

png("fig_contmap_module_balance.png", width = 3000, height = 3900, res = 300)
layout(matrix(1:2, nrow = 2), heights = c(9, 1))

par(mar = c(1.0, 0.5, 3.6, 9.5), xpd = FALSE)
plot(cm, fsize = c(0.001, 0.9), lwd = 2.4, ftype = "off", legend = FALSE,
     mar = c(1.0, 0.5, 3.6, 9.5), add = FALSE)
pp <- get("last_plot.phylo", envir = .PlotPhyloEnv)
tip_x <- pp$xx[1:n_tip]
tip_y <- pp$yy[1:n_tip]

label_text <- gsub("_", " ", cm$tree$tip.label)
label_col  <- ifelse(dichrom_flag, "#B22222", "black")
label_font <- ifelse(dichrom_flag, 4, 3)  # bold-italic for dichromatic, italic otherwise

par(xpd = TRUE)
text(tip_x + 0.006 * diff(par("usr")[1:2]), tip_y, labels = label_text,
     col = label_col, font = label_font, cex = 0.42, adj = 0)
title(main = "Module-balance of selection reconstructed across branches",
      cex.main = 1.25, line = 1.6, xpd = NA)

par(xpd = FALSE, mar = c(0, 9.5, 0, 9.5))
plot(0, 0, type = "n", xlim = c(0, 1), ylim = c(0, 1), axes = FALSE,
     xlab = "", ylab = "", xaxs = "i", yaxs = "i")
draw_colorbar(cm$cols, cm$lims, x = 0.30, y = 0.55, width = 0.40, height = 0.28,
              title = "Module balance (pigmentation \u2212 hormone selection)", cex = 0.85)
legend(x = 0.02, y = 0.35, legend = "Dichromatic species", text.col = "#B22222",
       text.font = 4, bty = "n", cex = 0.85, xjust = 0)

dev.off()

cat(sprintf(
  "Saved fig_contmap_module_balance.png | n_tips=%d | dichromatic_tips=%d | neutral_tips=%d\n",
  n_tip, sum(dichrom_flag), n_neutral_tips
))

# -----------------------------------------------------------------------------
# CAPTION (for the manuscript / figure legend):
#
# "Module-balance of selection reconstructed across branches. Per-tip module
# balance is defined as (n_pigmentation - n_hormone) / (n_pigmentation +
# n_hormone), where n_pigmentation and n_hormone are the numbers of distinct
# pigmentation- and hormone-module genes, respectively, with a significant
# (FDR-corrected p<0.05) episodic aBSREL selection signal on that terminal
# branch, among the 102 genome-sampled primate species. Tips with no
# significant selection signal in either module (n=10/102) are set to 0
# (neutral) rather than omitted. Branch colors along internal lineages are
# maximum-likelihood ancestral-state reconstructions of this continuous trait
# under a Brownian-motion model (phytools::contMap, method='anc.ML') and
# should be interpreted as model-based inferences, not directly observed
# selection signal. The diverging color ramp is centered at zero (grey,
# balanced selection pressure between modules); blue indicates a
# hormone-module tilt, orange a pigmentation-module tilt. Dichromatic species
# (n=21/102) are labeled in bold red."
# -----------------------------------------------------------------------------
