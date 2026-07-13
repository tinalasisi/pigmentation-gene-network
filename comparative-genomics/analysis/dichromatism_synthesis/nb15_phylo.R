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

# --- densityMap figure ---
dm <- densityMap(smap, states = c("0", "1"), plot = FALSE)
png(file.path(here, "figures/nb15_densitymap.png"), width = 1500, height = 2200, res = 200)
plot(dm, lwd = 2, outline = TRUE, fsize = c(0.35, 0.8), legend = 0.6,
     colors = setNames(c("#dfe6e9", "#c0662e"), c("0", "1")))
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
