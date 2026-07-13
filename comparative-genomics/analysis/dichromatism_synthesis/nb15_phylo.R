#!/usr/bin/env Rscript
# nb15_phylo.R — tree-only recompute for NB15 (sexual-dichromatism synthesis).
# Reproducible: reads the repo phenotype tree + full-resolution coding, recomputes
# trait lability (ARD vs ER), the stochastic-map origin count, and writes the
# densityMap figure. Emits result CSVs consumed by the NB15 Python cells.
#
# Inputs (repo copies — NOT the grant repo):
#   comparative-genomics/analysis/coevolution_test/data/primate_phenotype_tree.nex  (235 tips)
#   comparative-genomics/config/primate_dichromatism_coding.csv                     (238 species)
# Outputs (written next to this script, under data/ and figures/):
#   data/nb15_lability_fits.csv       — ER/ARD logLik, AIC, dAIC, rates, loss:gain
#   data/nb15_origin_counts.csv       — stochastic-map origin-count distribution
#   figures/nb15_densitymap.png       — posterior density of dichromatism on the tree
#   data/nb15_phylo_manifest.csv      — inputs + sha256 + tip/overlap counts (provenance)

suppressMessages({library(ape); library(phytools); library(tools)})
set.seed(1)

REPO <- Sys.getenv("PIGNET_REPO", unset = "/Users/tlasisi/GitHub/pigmentation-gene-network")
here <- file.path(REPO, "comparative-genomics/analysis/dichromatism_synthesis")
dir.create(file.path(here, "data"),    showWarnings = FALSE, recursive = TRUE)
dir.create(file.path(here, "figures"), showWarnings = FALSE, recursive = TRUE)

tree_path <- file.path(REPO, "comparative-genomics/analysis/coevolution_test/data/primate_phenotype_tree.nex")
cod_path  <- file.path(REPO, "comparative-genomics/config/primate_dichromatism_coding.csv")

tr  <- read.nexus(tree_path)
cod <- read.csv(cod_path, stringsAsFactors = FALSE)
cod$tip <- gsub(" ", "_", cod$species_binom)

# --- overlap + binary trait (hair_dichromatism_any) ---
sp   <- intersect(tr$tip.label, cod$tip)
x    <- setNames(as.integer(cod$hair_dichromatism_any[match(sp, cod$tip)]), sp)
sp   <- names(x)[!is.na(x)]; x <- x[sp]
trO  <- keep.tip(tr, sp)
n_tip <- length(sp); n_dich <- sum(x == 1)

# --- lability: ER vs ARD (Mk) ---
er  <- fitMk(trO, x, model = "ER")
ard <- fitMk(trO, x, model = "ARD")
aic <- function(f) 2 * length(f$rates) - 2 * as.numeric(logLik(f))
im  <- ard$index.matrix                    # [1,2]=0->1 (gain); [2,1]=1->0 (loss)
gain <- ard$rates[ im[1, 2] ]
loss <- ard$rates[ im[2, 1] ]
dAIC <- aic(er) - aic(ard)

fits <- data.frame(
  model       = c("ER", "ARD"),
  n_rates     = c(length(er$rates), length(ard$rates)),
  logLik      = c(as.numeric(logLik(er)), as.numeric(logLik(ard))),
  AIC         = c(aic(er), aic(ard)),
  gain_0to1   = c(NA, gain),
  loss_1to0   = c(NA, loss),
  loss_gain   = c(NA, loss / gain),
  dAIC_ER_ARD = c(NA, dAIC)
)
write.csv(fits, file.path(here, "data/nb15_lability_fits.csv"), row.names = FALSE)

# --- origin count via stochastic character mapping under ARD ---
smap <- make.simmap(trO, x, model = "ARD", nsim = 500, Q = "empirical", message = FALSE)
count_origins <- function(m) {
  sum(sapply(m$maps, function(seg) {
    st <- names(seg); if (length(st) < 2) return(0)
    sum(st[-length(st)] == "0" & st[-1] == "1")
  }))
}
origins <- sapply(smap, count_origins)
oc <- data.frame(statistic = c("mean", "median", "q05", "q95", "min", "max"),
                 n_origins = c(mean(origins), median(origins),
                               quantile(origins, .05), quantile(origins, .95),
                               min(origins), max(origins)))
write.csv(oc, file.path(here, "data/nb15_origin_counts.csv"), row.names = FALSE)

# --- origin count, model-free, under BOTH coding scopes (sampling-scope comparison) ---
# Maximal all-dichromatic clades: topology-only, does not depend on a rate model.
suppressMessages(library(phangorn))
count_clades <- function(tree, tips) {
  rem <- tips; k <- 0
  while (length(rem) > 0) {
    t1 <- rem[1]; anc <- Ancestors(tree, which(tree$tip.label == t1), "all")
    best <- which(tree$tip.label == t1)
    for (a in anc) { d <- Descendants(tree, a, "tips")[[1]]
      if (all(tree$tip.label[d] %in% tips)) best <- d else break }
    ct <- tree$tip.label[best]; rem <- setdiff(rem, ct); k <- k + 1
  }
  k
}
# full 238-species coding on the 224-tip overlap tree
dich_full <- names(x)[x == 1]
n_full <- count_clades(trO, dich_full)
gen117 <- read.csv(file.path(REPO, "comparative-genomics/analysis/data/dichromatism_coding.csv"),
                   stringsAsFactors = FALSE)
gen117$tip <- gsub(" ", "_", gen117$species)
n_full_genomic <- {
  rem <- dich_full; k <- 0
  while (length(rem) > 0) {
    t1 <- rem[1]; anc <- Ancestors(trO, which(trO$tip.label == t1), "all"); best <- which(trO$tip.label == t1)
    for (a in anc) { d <- Descendants(trO, a, "tips")[[1]]; if (all(trO$tip.label[d] %in% dich_full)) best <- d else break }
    ct <- trO$tip.label[best]; if (any(ct %in% gen117$tip)) k <- k + 1; rem <- setdiff(rem, ct)
  }; k
}
# 117-genome coding on the tree pruned to those tips
sp117  <- intersect(trO$tip.label, gen117$tip)
tr117  <- keep.tip(trO, sp117)
x117   <- setNames(as.integer(gen117$dichromatic[match(sp117, gen117$tip)]), sp117)
n_117  <- count_clades(tr117, names(x117)[x117 == 1])

est <- data.frame(
  scope     = c("full coding (238 species)", "full coding, genome-sampled clades",
                "genome-subset coding (117 species)", "stochastic map ARD (mean)"),
  n_origins = c(n_full, n_full_genomic, n_117, mean(origins)),
  method    = c("maximal dichromatic clades (topology, model-free)",
                "clades with >=1 genome-sampled tip",
                "maximal dichromatic clades (topology, model-free)",
                "500 simmaps (flicker-inflated by high loss rate)")
)
write.csv(est, file.path(here, "data/nb15_origin_estimates.csv"), row.names = FALSE)
cat(sprintf("origins: full-238=%d (genomic %d) | 117-subset=%d | simmap mean=%.1f\n",
            n_full, n_full_genomic, n_117, mean(origins)))

# --- densityMap figure: state posterior on the tree + right-side clade bar + clean legend ---
dm <- densityMap(smap, states = c("0", "1"), plot = FALSE)

# map each tip to a recognizable major clade (for the orientation bar)
fam <- setNames(cod$family[match(trO$tip.label, cod$tip)], trO$tip.label)
clade_of <- function(f) {
  if (is.na(f)) return("Other")
  if (f == "Cercopithecidae") "Old World monkeys"
  else if (f == "Hominidae")   "Apes"
  else if (f == "Hylobatidae") "Gibbons"
  else if (f %in% c("Atelidae","Cebidae","Callitrichidae","Pitheciidae","Aotidae")) "New World monkeys"
  else if (f %in% c("Lemuridae","Cheirogaleidae","Lepilemuridae","Indriidae","Daubentoniidae")) "Lemurs"
  else if (f %in% c("Lorisidae","Galagidae")) "Lorises & galagos"
  else if (f == "Tarsiidae") "Tarsiers"
  else "Other"
}
clade <- vapply(fam, clade_of, character(1))
clade_levels <- c("Old World monkeys","Apes","Gibbons","New World monkeys",
                  "Lemurs","Lorises & galagos","Tarsiers")
clade_cols <- setNames(c("#4e79a7","#f28e2b","#e15759","#59a14f",
                         "#b07aa1","#9c755f","#edc948"), clade_levels)

png(file.path(here, "figures/nb15_densitymap.png"), width = 1700, height = 2300, res = 200)
# leave room at right for the observed-state dots + clade bar + labels; suppress tiny per-species
# labels and the default (squished) legend — both are redrawn cleanly below.
plot(dm, lwd = 3, outline = TRUE, ftype = "off", legend = FALSE,
     mar = c(2.5, 1.0, 2.5, 9.0),
     colors = setNames(c("#3b5ba5", "#c0392b"), c("0", "1")))
pp <- get("last_plot.phylo", envir = .PlotPhyloEnv)
xmax <- max(pp$xx[1:Ntip(trO)]); yr <- range(pp$yy[1:Ntip(trO)])
# observed (coded) state at each tip — the "tell": does the painted posterior actually land on
# tips that are known to be dichromatic?
obs <- x[trO$tip.label]
ox  <- xmax * 1.015                              # observed-state dot column
bx0 <- xmax * 1.04; bx1 <- xmax * 1.07           # clade colour strip
for (i in seq_len(Ntip(trO))) {
  yy <- pp$yy[i]
  # filled red dot only where the species is coded dichromatic; faint tick otherwise
  if (!is.na(obs[i]) && obs[i] == 1) {
    points(ox, yy, pch = 19, cex = 0.5, col = "#c0392b", xpd = NA)
  } else {
    points(ox, yy, pch = 19, cex = 0.18, col = "#d6dbdf", xpd = NA)
  }
  rect(bx0, yy - 0.5, bx1, yy + 0.5, col = clade_cols[clade[trO$tip.label[i]]],
       border = NA, xpd = NA)
}
# label each contiguous clade run at its vertical midpoint
tip_clade <- clade[trO$tip.label]           # in tip index order (1..Ntip)
runs <- rle(tip_clade)
pos <- 1
for (k in seq_along(runs$lengths)) {
  idx <- pos:(pos + runs$lengths[k] - 1)
  ymid <- mean(pp$yy[idx])
  if (runs$lengths[k] >= 3)   # only label runs big enough to read
    text(bx1 + xmax * 0.015, ymid, runs$values[k], adj = 0, cex = 0.85, xpd = NA)
  pos <- pos + runs$lengths[k]
}
# clean legend: gradient bar bottom-left, title ABOVE the bar so it doesn't collide with 0/1
add.color.bar(leg = xmax * 0.35, cols = dm$cols,
              title = "", lims = c(0, 1), digits = 1, prompt = FALSE,
              x = 0, y = yr[1] - (yr[2]-yr[1]) * 0.03,
              subtitle = "", lwd = 10, fsize = 0.9)
text(0, yr[1] + (yr[2]-yr[1]) * 0.005, "branch colour = posterior P(dichromatic)",
     adj = 0, cex = 0.9, font = 2, xpd = NA)
# observed-state legend (the tell): red dot = species CODED dichromatic
points(0, yr[1] - (yr[2]-yr[1]) * 0.075, pch = 19, cex = 0.6, col = "#c0392b", xpd = NA)
text(xmax * 0.02, yr[1] - (yr[2]-yr[1]) * 0.075,
     "red dot at tip = species observed / coded dichromatic",
     adj = 0, cex = 0.85, xpd = NA)
title(main = "Sexual dichromatism: reconstructed posterior vs. observed tip states",
      cex.main = 1.05, line = 0.5)
dev.off()

# --- provenance manifest ---
man <- data.frame(
  input     = c("primate_phenotype_tree.nex", "primate_dichromatism_coding.csv"),
  path      = c(tree_path, cod_path),
  sha256_16 = c(substr(md5sum(tree_path), 1, 16), substr(md5sum(cod_path), 1, 16)),
  note      = c(sprintf("%d tips", Ntip(tr)), sprintf("%d species", nrow(cod)))
)
man <- rbind(man, data.frame(input = "OVERLAP", path = "tree cap coding (hair_dichromatism_any)",
             sha256_16 = "", note = sprintf("%d tips, %d dichromatic", n_tip, n_dich)))
write.csv(man, file.path(here, "data/nb15_phylo_manifest.csv"), row.names = FALSE)

cat(sprintf("nb15_phylo: overlap=%d dichromatic=%d | loss:gain=%.2f dAIC=%.2f | origins mean=%.1f [%.0f-%.0f]\n",
            n_tip, n_dich, loss / gain, dAIC, mean(origins), min(origins), max(origins)))
