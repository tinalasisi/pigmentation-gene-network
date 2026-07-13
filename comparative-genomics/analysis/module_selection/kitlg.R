#!/usr/bin/env Rscript
# ============================================================================
# kitlg.R
#
# KITLG-focused headline figure for the primate hair sexual-dichromatism
# selection-scan module.
#
# Panel a: fan cladogram of the 102 genome-sampled primate tips. Tip labels
#          are colored red/bold for species coded as sexually dichromatic
#          (species_coding.csv). An outer ring marks tips where KITLG is
#          under episodic positive selection in the pigmentation-gene aBSREL
#          panel (branch_rates.csv, is_tip==TRUE & selected_flag==TRUE).
# Panel b: per-origin summary. For each independently coded dichromatic
#          origin (origin_assignments.csv) present in the genome panel, the
#          fraction of its genomic tips with KITLG selected is plotted as a
#          lollipop, grouped by family and labeled with the species/genus.
#
# Headline number: the count of DISTINCT origin_id values that contain at
# least one KITLG-selected, dichromatic tip -- i.e. the number of
# independent dichromatic lineages in which KITLG selection recurs.
#
# Data fidelity notes:
#  - No baseline_omega value for KITLG tips is infinite; a small number of
#    UNTESTED / non-panel background tips carry a saturated placeholder
#    (1e10, capped) rather than a genuine estimate. These are excluded from
#    every selection call: selection status here is read exclusively from
#    the pre-computed boolean `selected_flag` (multiple-testing-corrected
#    aBSREL p < 0.05), never from raw omega magnitude.
#  - Tree topology (panel a) is the supplied reference primate phylogeny,
#    pruned with ape::keep.tip() to the 102 genome-sampled tips -- it is
#    never re-inferred from the selection or trait data.
#  - Colors: pigmentation/KITLG-positive = #C97B0A, dichromatic label =
#    #B22222. No diverging ramp is needed in this figure (no signed
#    continuous quantity is mapped) -- selection status is a binary flag,
#    encoded categorically rather than on a colormap.
#
# Usage:
#   Rscript kitlg.R /path/to/module_data_bundle.tgz [output_dir]
#   (or, if already extracted, point --bundle-dir at the "data/" parent)
#
# Requires: ape, dplyr, tidyr, stringr, purrr (tidyverse) -- R env with
# ape + tidyverse (e.g. the 'phylo-model' conda env used to develop this).
# ============================================================================

suppressPackageStartupMessages({
  library(ape)
  library(dplyr)
  library(readr)
  library(stringr)
  library(tibble)
})

## ---------------------------------------------------------------------
## 0. Resolve input bundle
## ---------------------------------------------------------------------
args <- commandArgs(trailingOnly = TRUE)
bundle_tgz <- if (length(args) >= 1) args[1] else NULL
out_dir    <- if (length(args) >= 2) args[2] else "."

work_dir <- tempfile("kitlg_bundle_")
dir.create(work_dir)

if (!is.null(bundle_tgz) && file.exists(bundle_tgz)) {
  untar(bundle_tgz, exdir = work_dir)
  data_dir <- file.path(work_dir, "data")
} else if (dir.exists("data")) {
  # already extracted in the current working directory
  data_dir <- "data"
} else {
  stop("Provide a path to the module_data_bundle.tgz as the first argument, ",
       "or run from a directory that already contains data/.")
}

## ---------------------------------------------------------------------
## 1. Load data
## ---------------------------------------------------------------------
branch_rates    <- read_csv(file.path(data_dir, "branch_rates.csv"), show_col_types = FALSE)
species_coding  <- read_csv(file.path(data_dir, "species_coding.csv"), show_col_types = FALSE)
origin_assign   <- read_csv(file.path(data_dir, "origin_assignments.csv"), show_col_types = FALSE)
tree_full       <- read.nexus(file.path(data_dir, "primate_species_tree.nex"))

## ---------------------------------------------------------------------
## 2. Normalize species naming (spaces -> underscores) and define the
##    102-tip genome panel
## ---------------------------------------------------------------------
species_coding <- species_coding %>%
  mutate(species_ = gsub(" ", "_", species))
origin_assign <- origin_assign %>%
  mutate(species_ = gsub(" ", "_", species))

all_tips <- unique(branch_rates$branch[branch_rates$is_tip])
stopifnot(length(all_tips) == 102)
stopifnot(all(all_tips %in% tree_full$tip.label))

## ---------------------------------------------------------------------
## 3. KITLG selection calls (tip-level, pigmentation panel) -- selection
##    status is read only from the corrected boolean flag, never from raw
##    omega (which saturates to a placeholder value for untested
##    background branches and must never be treated as signal)
## ---------------------------------------------------------------------
kitlg_tips <- branch_rates %>%
  filter(gene == "KITLG", is_tip == TRUE, selected_flag == TRUE) %>%
  pull(branch) %>%
  unique()

## ---------------------------------------------------------------------
## 4. Dichromatic species among the 102 genome tips
## ---------------------------------------------------------------------
dichromatic_102 <- species_coding %>%
  filter(dichromatic == 1, species_ %in% all_tips) %>%
  pull(species_)

## ---------------------------------------------------------------------
## 5. Prune tree to the genome panel and build the per-tip status table
## ---------------------------------------------------------------------
tree102 <- keep.tip(tree_full, all_tips)

tip_status <- tibble(species_ = tree102$tip.label) %>%
  mutate(
    dichromatic    = species_ %in% dichromatic_102,
    kitlg_selected = species_ %in% kitlg_tips
  ) %>%
  left_join(origin_assign %>% select(species_, origin_id, dichromatism_level),
            by = "species_") %>%
  left_join(species_coding %>% select(species_, family_sc = family),
            by = "species_")

# re-order to match tree tip order (required for downstream tip-coordinate mapping)
tip_status <- tip_status[match(tree102$tip.label, tip_status$species_), ]
stopifnot(all(tip_status$species_ == tree102$tip.label))

## ---------------------------------------------------------------------
## 6. Headline number: distinct origins with >=1 KITLG-selected,
##    dichromatic tip (independent recruitment count)
## ---------------------------------------------------------------------
kitlg_dich_origins <- tip_status %>%
  filter(kitlg_selected, dichromatic, !is.na(origin_id)) %>%
  pull(origin_id) %>%
  unique()
n_distinct_origins_kitlg_dich <- length(kitlg_dich_origins)

## ---------------------------------------------------------------------
## 7. Per-origin summary for panel b (all origins present in the genome
##    panel, ordered by family block)
## ---------------------------------------------------------------------
family_order <- c("cercopithecidae", "hylobatidae", "cebidae", "lemuridae")

origin_summary <- tip_status %>%
  filter(!is.na(origin_id)) %>%
  group_by(origin_id, family_sc, dichromatism_level) %>%
  summarise(
    n_tips_panel     = n(),
    n_kitlg_selected = sum(kitlg_selected),
    any_kitlg        = any(kitlg_selected),
    .groups = "drop"
  ) %>%
  mutate(
    family_sc  = factor(family_sc, levels = family_order),
    origin_num = as.numeric(gsub("origin_", "", origin_id))
  ) %>%
  arrange(family_sc, origin_num)

origin_spp_label <- tip_status %>%
  filter(!is.na(origin_id)) %>%
  group_by(origin_id) %>%
  summarise(
    spp = if (n() == 1) {
      gsub("_", " ", species_)
    } else {
      paste0(gsub("_.*", "", species_)[1], " (", n(), " spp.)")
    },
    .groups = "drop"
  )

origin_summary <- origin_summary %>%
  left_join(origin_spp_label, by = "origin_id") %>%
  mutate(row_y = n() - row_number() + 1)

n_origins <- nrow(origin_summary)
n_distinct_kitlg_origins <- sum(origin_summary$any_kitlg)  # matches n_distinct_origins_kitlg_dich
stopifnot(n_distinct_kitlg_origins == n_distinct_origins_kitlg_dich)

## ---------------------------------------------------------------------
## 8. Colors (fixed palette, per spec)
## ---------------------------------------------------------------------
col_pig  <- "#C97B0A"   # pigmentation gene / KITLG-selected
col_hor  <- "#2E6E9E"   # hormone gene (not used as a data series here, kept for palette consistency)
col_dich <- "#B22222"   # dichromatic species highlight
diverging_ramp <- colorRampPalette(c(col_hor, "#f2f2f2", col_pig))  # unused (no signed value in this figure)

## ---------------------------------------------------------------------
## 9. Render figure
## ---------------------------------------------------------------------
out_png <- file.path(out_dir, "fig_kitlg_recurrence.png")
png(out_png, width = 3300, height = 2000, res = 300)

layout(matrix(1:2, nrow = 1), widths = c(1.55, 1.15))

## ---- Panel a: fan cladogram ----
par(mar = c(1, 1, 3.8, 1), xpd = NA)
plot.phylo(tree102, type = "fan", show.tip.label = TRUE, cex = 0.34,
           label.offset = 0.9, edge.color = "grey45", edge.width = 0.7,
           tip.color = ifelse(tip_status$dichromatic, col_dich, "grey15"),
           font = ifelse(tip_status$dichromatic, 2, 1),
           no.margin = FALSE, align.tip.label = FALSE)

pp <- get("last_plot.phylo", envir = .PlotPhyloEnv)
Ntip <- length(tree102$tip.label)
xx <- pp$xx[1:Ntip]; yy <- pp$yy[1:Ntip]
r <- sqrt(xx^2 + yy^2); theta <- atan2(yy, xx)
rmax <- max(r)
r_ring <- rmax * 1.34
points(r_ring * cos(theta), r_ring * sin(theta), pch = 21, cex = 0.95,
       bg  = ifelse(tip_status$kitlg_selected, col_pig, "white"),
       col = ifelse(tip_status$kitlg_selected, col_pig, "grey75"), lwd = 0.7)

legend(x = -rmax * 0.62, y = rmax * 0.62, bty = "n", cex = 0.62, y.intersp = 1.5,
       legend = c("KITLG selected (tip)", "KITLG not selected", "Dichromatic species"),
       pch = c(21, 21, NA), pt.bg = c(col_pig, "white", NA),
       col = c(col_pig, "grey75", NA), pt.cex = 1.1,
       text.col = c("grey15", "grey15", col_dich), text.font = c(1, 1, 2))

mtext("a", side = 3, adj = 0, line = 2.3, cex = 1.5, font = 2)
mtext("KITLG selection recurs across independent dichromatic lineages",
      side = 3, line = 1.0, cex = 0.85, font = 2, adj = 0.5)

## ---- Panel b: per-origin KITLG strip ----
par(mar = c(4.5, 15, 3.8, 5), xpd = TRUE)
plot(NA, xlim = c(0, 1.3), ylim = c(0.3, n_origins + 0.7), axes = FALSE, xlab = "", ylab = "")

x_spp <- -0.08
segments(0, origin_summary$row_y,
          origin_summary$n_kitlg_selected / origin_summary$n_tips_panel,
          origin_summary$row_y, col = "grey65", lwd = 1.3)
points(origin_summary$n_kitlg_selected / origin_summary$n_tips_panel, origin_summary$row_y,
       pch = 21, cex = 2.1,
       bg  = ifelse(origin_summary$any_kitlg, col_pig, "white"),
       col = ifelse(origin_summary$any_kitlg, col_pig, "grey60"), lwd = 1)

# manual axis ticks (avoids axis() tick-thinning at this narrow width)
tick_x <- c(0, 0.5, 1)
segments(tick_x, 0.3, tick_x, 0.3 - 0.28, xpd = TRUE, lwd = 0.8)
text(tick_x, 0.3 - 0.62, labels = c("0", "0.5", "1"), cex = 0.66, xpd = TRUE)
mtext("Fraction of genomic tips with KITLG selected", side = 1, line = 2.4, cex = 0.6)

text(rep(x_spp, n_origins), origin_summary$row_y,
     labels = origin_summary$spp, cex = 0.62, adj = 1, font = 3, col = "grey20")
text(rep(1.18, n_origins), origin_summary$row_y,
     labels = paste0(origin_summary$n_kitlg_selected, "/", origin_summary$n_tips_panel),
     cex = 0.62, adj = 0, col = "grey30")

fam_blocks <- origin_summary %>%
  group_by(family_sc) %>%
  summarise(ymin = min(row_y), ymax = max(row_y), .groups = "drop")
for (i in seq_len(nrow(fam_blocks))) {
  ymid <- mean(c(fam_blocks$ymin[i], fam_blocks$ymax[i]))
  mtext(str_to_title(as.character(fam_blocks$family_sc[i])), side = 2, at = ymid,
        line = 9.5, cex = 0.66, font = 2, col = "grey35", las = 1)
  if (fam_blocks$ymax[i] < n_origins) {
    segments(-0.75, fam_blocks$ymax[i] + 0.5, 1.3, fam_blocks$ymax[i] + 0.5,
              col = "grey88", lwd = 0.6, xpd = TRUE)
  }
}

mtext("b", side = 3, adj = 0, line = 2.3, cex = 1.5, font = 2)
mtext(paste0(n_distinct_kitlg_origins, " of ", n_origins, " sampled dichromatic origins"),
      side = 3, line = 1.9, cex = 0.7, font = 2, adj = 0.5)
mtext("show KITLG selection", side = 3, line = 0.85, cex = 0.7, font = 2, adj = 0.5)

dev.off()

cat(sprintf(
  "Saved %s\nHeadline: KITLG is under selection in %d of %d sampled independent dichromatic origins (%d/%d dichromatic KITLG-selected tips).\n",
  out_png, n_distinct_kitlg_origins, n_origins,
  sum(tip_status$kitlg_selected & tip_status$dichromatic), length(dichromatic_102)
))
