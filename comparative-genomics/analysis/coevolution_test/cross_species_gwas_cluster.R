#!/usr/bin/env Rscript
# =====================================================================================
# Cross-species GWAS for sexual dichromatism, phylogeny as stratification control.
#
#   phenotype  : dichromatic (case) vs monochromatic (control)   [species_coding.csv]
#   genotype   : per-lineage log1p(omega) at each gene            [branch_rates.csv]
#   strat ctrl : phylogenetic covariance; Pagel's lambda estimated per gene (PGLS),
#                and Ives-Garland phylogenetic logistic regression (phyloglm) as the
#                canonical binary-outcome model.
#
# Runs BOTH methods and writes a joined table + Manhattan plot.
# On the cluster, phyloglm loads from the managed (non-writable) library, so it works
# there even though it is blocked in the sandbox R kernel.
#
# Usage:
#   Rscript cross_species_gwas_cluster.R \
#     --branch_rates <branch_rates.csv> \
#     --tree <primate_species_tree.nex> \
#     --coding <species_coding.csv> \
#     --outdir <dir> [--min_tips 20] [--min_cases 3] [--winsor 0.99] [--nperm 1999]
#
# Defaults resolve to this repo's perorigin_v1 layout when flags are omitted.
# =====================================================================================
suppressMessages({
  library(ape); library(phytools); library(nlme); library(tidyverse)
  has_phyloglm <- requireNamespace("phylolm", quietly = TRUE)
})

## ---- args ----
args <- commandArgs(trailingOnly = TRUE)
getarg <- function(flag, default = NULL) {
  i <- match(flag, args); if (is.na(i) || i == length(args)) return(default); args[i + 1]
}
here <- tryCatch(dirname(normalizePath(sub("--file=", "",
          grep("--file=", commandArgs(FALSE), value = TRUE)[1]))), error = function(e) getwd())
repo_guess <- normalizePath(file.path(here, "../../.."), mustWork = FALSE)

BR_PATH <- getarg("--branch_rates",
  file.path(repo_guess, "comparative-genomics/results/perorigin_v1/branch_rates.csv"))
TREE    <- getarg("--tree",
  file.path(repo_guess, "comparative-genomics/analysis/coevolution_test/data/primate_species_tree.nex"))
SC_PATH <- getarg("--coding",
  file.path(repo_guess, "comparative-genomics/analysis/coevolution_test/data/species_coding.csv"))
OUTDIR  <- getarg("--outdir", file.path(here))
MIN_TIPS  <- as.integer(getarg("--min_tips", "20"))
MIN_CASES <- as.integer(getarg("--min_cases", "3"))
WINSOR    <- as.numeric(getarg("--winsor", "0.99"))
NPERM     <- as.integer(getarg("--nperm", "1999"))
dir.create(OUTDIR, showWarnings = FALSE, recursive = TRUE)
stopifnot(file.exists(BR_PATH), file.exists(TREE), file.exists(SC_PATH))
cat(sprintf("phyloglm available: %s | inputs OK | outdir: %s\n", has_phyloglm, OUTDIR))

## ---- genotype: per-tip omega, winsorized + log1p ----
BR <- readr::read_csv(BR_PATH, show_col_types = FALSE)
SC <- readr::read_csv(SC_PATH, show_col_types = FALSE)
gtr <- read.nexus(TREE)

# module column may be named 'module'; older files use 'set'. Prefer 'module'.
modcol <- if ("module" %in% names(BR)) "module" else "set"
tipdat <- BR %>% filter(is_tip == TRUE, tested == TRUE, !is.na(baseline_omega)) %>%
  transmute(gene, module = .data[[modcol]], branch, omega = baseline_omega)
cap <- quantile(tipdat$omega, WINSOR)
tipdat <- tipdat %>% mutate(log_omega = log1p(pmin(omega, cap)))

tips  <- intersect(gtr$tip.label, SC$species)
tr0   <- keep.tip(gtr, tips)
dichv <- setNames(as.integer(SC$dichromatic[match(tr0$tip.label, SC$species)]), tr0$tip.label)
cat(sprintf("n = %d  cases = %d  controls = %d  genes = %d\n",
            length(tips), sum(dichv), sum(dichv == 0), n_distinct(tipdat$gene)))

genes <- tipdat %>% count(gene, module) %>% filter(n >= MIN_TIPS) %>% arrange(gene)

## ---- per-gene fit: PGLS(estimated lambda) + phyloglm(if available) ----
fit_gene <- function(g) {
  sub <- tipdat %>% filter(gene == g)
  x <- setNames(sub$log_omega[match(tr0$tip.label, sub$branch)], tr0$tip.label)
  ok <- !is.na(x) & !is.na(dichv)
  if (sum(ok) < MIN_TIPS || sd(x[ok]) == 0 || sum(dichv[ok]) < MIN_CASES) return(NULL)
  trg <- keep.tip(tr0, names(x)[ok])
  df  <- data.frame(y = dichv[trg$tip.label], logw = x[trg$tip.label],
                    sp = trg$tip.label, row.names = trg$tip.label)
  # PGLS with estimated Pagel lambda
  pg <- tryCatch(gls(y ~ logw, df, correlation = corPagel(0.5, trg, form = ~sp, fixed = FALSE),
                     method = "ML"), error = function(e) NULL)
  pgls_beta <- pgls_p <- lam <- NA_real_
  if (!is.null(pg)) { st <- summary(pg)$tTable
    pgls_beta <- st["logw","Value"]; pgls_p <- st["logw","p-value"]
    lam <- tryCatch(as.numeric(coef(pg$modelStruct$corStruct, unconstrained = FALSE)),
                    error = function(e) NA) }
  # phyloglm (Ives-Garland logistic) — the canonical binary model
  pgl_beta <- pgl_p <- pgl_alpha <- NA_real_
  if (has_phyloglm) {
    fit <- tryCatch(phylolm::phyloglm(y ~ logw, data = df, phy = trg,
                    method = "logistic_MPLE", btol = 30), error = function(e) NULL)
    if (!is.null(fit)) { co <- summary(fit)$coefficients
      if ("logw" %in% rownames(co)) {
        pgl_beta <- co["logw","Estimate"]; pgl_p <- co["logw",ncol(co)]; pgl_alpha <- fit$alpha } }
  }
  tibble(gene = g, module = genes$module[genes$gene == g][1],
         n_tips = sum(ok), n_dich = sum(dichv[ok]),
         pgls_beta = pgls_beta, pgls_p = pgls_p, lambda = lam,
         phyloglm_beta = pgl_beta, phyloglm_p = pgl_p, phyloglm_alpha = pgl_alpha)
}
set.seed(1)
raw <- purrr::map(genes$gene, fit_gene) %>% bind_rows()

## ---- drop degenerate PGLS fits, BH-correct both methods ----
## A linear-probability PGLS can fail numerically (near-separation): absurd t, ~0 SE, or an
## ill-posed lambda. Flag and drop BEFORE correction so an artifact cannot top the Manhattan plot.
raw <- raw %>%
  mutate(pgls_t = pgls_beta / (pgls_beta / qt(pgls_p/2, df = n_tips - 2, lower.tail = FALSE)),
         degenerate = !is.na(lambda) &
           (lambda < -0.01 | lambda > 1.001 |
            (!is.na(pgls_p) & pgls_p < 1e-12) |
            (!is.na(pgls_beta) & !is.na(pgls_p) & pgls_p > 0 & pgls_p < 1 &
             abs(qnorm(pgls_p/2)) > 50))) %>%
  select(-pgls_t)
res <- raw %>% filter(!degenerate) %>%
  mutate(pgls_p_BH = p.adjust(pgls_p, "BH"),
         phyloglm_p_BH = if (has_phyloglm) p.adjust(phyloglm_p, "BH") else NA_real_) %>%
  arrange(pgls_p)

## ---- tree-structured permutation confirmation for nominal PGLS hits ----
perm_p <- function(g, nperm = NPERM) {
  sub <- tipdat %>% filter(gene == g)
  x <- setNames(sub$log_omega[match(tr0$tip.label, sub$branch)], tr0$tip.label)
  ok <- !is.na(x) & !is.na(dichv); trg <- keep.tip(tr0, names(x)[ok])
  xo <- x[ok][trg$tip.label]; yo <- dichv[ok][trg$tip.label]; obs <- cor(xo, yo)
  set.seed(1); nd <- replicate(nperm, cor(xo, yo[order(fastBM(trg))]))
  (sum(abs(nd) >= abs(obs)) + 1) / (nperm + 1)
}
res <- res %>% rowwise() %>%
  mutate(perm_p = if (!is.na(pgls_p) && pgls_p < 0.05) perm_p(gene) else NA_real_) %>% ungroup()

out_csv <- file.path(OUTDIR, "gwas_omega_results.csv")
write_csv(res, out_csv)
cat(sprintf("wrote %s (%d clean genes; PGLS BH<0.05: %d)\n",
            out_csv, nrow(res), sum(res$pgls_p_BH < 0.05, na.rm = TRUE)))
print(as.data.frame(res %>% filter(pgls_p < 0.05) %>% mutate(across(where(is.numeric), ~signif(., 3)))))

## ---- Manhattan ----
suppressMessages({library(ggplot2); library(ggrepel)})
pd <- res %>% mutate(nlp = -log10(pgls_p), lab = ifelse(pgls_p_BH < 0.05, gene, NA)) %>%
  arrange(module, gene) %>% mutate(idx = row_number())
s <- res %>% arrange(pgls_p); k <- suppressWarnings(max(which(s$pgls_p <= 0.05*seq_len(nrow(s))/nrow(s))))
bh <- if (is.finite(k)) -log10(s$pgls_p[k]) else NA
man <- ggplot(pd, aes(idx, nlp, colour = module)) + geom_point(size = 2.4, alpha = .85) +
  { if (is.finite(bh)) geom_hline(yintercept = bh, linetype = "dashed", colour = "grey40") } +
  ggrepel::geom_text_repel(aes(label = lab), na.rm = TRUE, fontface = "italic",
                           min.segment.length = 0) +
  labs(title = "Cross-species GWAS for sexual dichromatism (phylogeny-controlled)",
       subtitle = sprintf("PGLS dich ~ log(omega), estimated lambda | %d genes, %d cases",
                          nrow(res), sum(dichv)),
       x = "gene (grouped by module)", y = expression(-log[10](p))) +
  theme_bw(base_size = 12) + theme(axis.text.x = element_blank(), axis.ticks.x = element_blank())
ggsave(file.path(OUTDIR, "fig_gwas_manhattan.png"), man, width = 10, height = 5, dpi = 200)
cat("wrote fig_gwas_manhattan.png\n")
cat("DONE\n")
