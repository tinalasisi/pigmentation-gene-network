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
pom$acp   <- suppressMessages(suppressWarnings(as.numeric(pom$absrel_corrected_p)))
pom$istip <- pom$is_tip %in% c(TRUE, "True", "true", 1, "1")
pom_sel   <- pom[!is.na(pom$acp) & pom$acp < 0.05, ]
sel_tips  <- intersect(pom_sel$branch[pom_sel$istip], trO$tip.label)
sel_nodes <- pom_sel$branch[!pom_sel$istip]

# HYPHY names internal branches NodeNN in each gene's OWN aBSREL tree — those numbers are not
# comparable across genes and mean nothing on the phenotype tree. Resolve each selected internal
# node to the clade it subtends by reading the labelled gene tree from POMC's aBSREL JSON, so the
# figure names a real clade (e.g. "Macaca clade") instead of an opaque "Node45".
resolve_node <- function(node_name) {
  jf <- file.path(REPO, "comparative-genomics/results/full_panel_117/absrel/POMC.ABSREL.json")
  if (!file.exists(jf)) return(node_name)
  jtree <- tryCatch(jsonlite::fromJSON(jf)$input$trees[["0"]], error = function(e) NULL)
  if (is.null(jtree)) return(node_name)
  gt <- tryCatch(read.tree(text = paste0(jtree, ";")), error = function(e) NULL)
  if (is.null(gt) || !(node_name %in% gt$node.label)) return(node_name)
  ni  <- Ntip(gt) + which(gt$node.label == node_name)
  tips <- gt$tip.label[Descendants(gt, ni, type = "tips")[[1]]]
  genera <- unique(sub("_.*", "", tips))
  if (length(genera) == 1) sprintf("%s clade (%d spp.)", genera, length(tips))
  else sprintf("%s clade (%d spp.)", paste(genera, collapse = "/"), length(tips))
}
suppressMessages(suppressWarnings({library(jsonlite); library(phangorn)}))
node_labels <- setNames(vapply(sel_nodes, resolve_node, character(1)), sel_nodes)
# dichromatic fraction within each resolved internal clade (for a data-driven state annotation)
node_dichfrac <- function(node_name) {
  jf <- file.path(REPO, "comparative-genomics/results/full_panel_117/absrel/POMC.ABSREL.json")
  jtree <- tryCatch(jsonlite::fromJSON(jf)$input$trees[["0"]], error = function(e) NULL)
  gt <- tryCatch(read.tree(text = paste0(jtree, ";")), error = function(e) NULL)
  if (is.null(gt) || !(node_name %in% gt$node.label)) return(NA_real_)
  ni <- Ntip(gt) + which(gt$node.label == node_name)
  tips <- gt$tip.label[Descendants(gt, ni, type = "tips")[[1]]]
  st <- x[intersect(tips, names(x))]
  if (!length(st)) return(NA_real_)
  mean(st == 1)
}
node_frac <- setNames(vapply(sel_nodes, node_dichfrac, numeric(1)), sel_nodes)
cat("DEBUG sel rows:", nrow(pom_sel), "tips:", length(sel_tips), "\n")
cat("resolved internal nodes:", paste(sprintf("%s=%s (dich frac %.2f)",
    names(node_labels), node_labels, node_frac[names(node_labels)]), collapse="; "), "\n")

# tip colours: dichromatic vs mono; ring marks POMC-selected tips
dich_col <- ifelse(x[trO$tip.label] == 1, "#c0392b", "#c9ced6")

# dichromatism status of each POMC-selected TIP (the point the user flagged: mixed).
sel_state <- x[sel_tips]                          # 1 = dichromatic, 0 = mono
# order selected tips: dichromatic first, then by name, for a clean lollipop panel
sel_df <- data.frame(tip = sel_tips, dich = sel_state[sel_tips], stringsAsFactors = FALSE)
sel_df <- sel_df[order(-sel_df$dich, sel_df$tip), ]

# TWO-PANEL figure: (left) small phylogram flagging only the selected clade region;
# (right) an explicit lollipop of the selected branches coloured by dichromatism state.
png(file.path(here, "figures/nb15_pomc_tree.png"), width = 2200, height = 1500, res = 200)
par(oma = c(0, 0, 3, 0))
layout(matrix(c(1, 2), nrow = 1), widths = c(1.5, 1))

## panel 1: whole tree, POMC-selected tips starred, dichromatism dot at every tip
par(mar = c(4, 1, 4, 9))
plot(trO, type = "phylogram", show.tip.label = FALSE, edge.color = "#95a5a6",
     edge.width = 1.1, x.lim = c(0, max(nodeHeights(trO)) * 1.30))
pp <- get("last_plot.phylo", envir = .PlotPhyloEnv)
xmax <- max(pp$xx[1:Ntip(trO)])
for (i in seq_len(Ntip(trO)))
  points(pp$xx[i] + xmax*0.012, pp$yy[i], pch = 15, cex = 0.32, col = dich_col[i], xpd = NA)
for (t in sel_tips) {
  i <- which(trO$tip.label == t)
  star_col <- if (x[t] == 1) "#c0392b" else "#2c3e50"   # star coloured by the tip's own state
  points(pp$xx[i] + xmax*0.05, pp$yy[i], pch = 8, cex = 1.3, col = star_col, lwd = 2.2, xpd = NA)
}
legend("bottomleft", inset = c(0, 0.02), bty = "n", cex = 0.8,
       pch = c(15, 15, 8, 8), pt.cex = c(1, 1, 1.2, 1.2),
       col = c("#c0392b", "#c9ced6", "#c0392b", "#2c3e50"),
       legend = c("tip: dichromatic", "tip: monochromatic",
                  "POMC-selected & dichromatic", "POMC-selected & monochromatic"))
title(main = "A  POMC episodic selection on the tree", cex.main = 1.0, adj = 0)

## panel 2: explicit lollipop of the 5 selected branches, coloured by dichromatism state
par(mar = c(4, 9, 4, 2))
allsel <- rbind(
  data.frame(branch = sel_df$tip, dich = sel_df$dich, is_tip = TRUE),
  data.frame(branch = sel_nodes,  dich = NA,           is_tip = FALSE))
allsel$cp <- pom_sel$acp[match(allsel$branch, pom_sel$branch)]
allsel$nlp <- -log10(pmax(allsel$cp, 1e-16))
allsel <- allsel[order(allsel$is_tip, allsel$dich, allsel$nlp), ]
yy <- seq_len(nrow(allsel))
lab_col <- ifelse(!allsel$is_tip, "#7f8c8d",
                  ifelse(allsel$dich == 1, "#c0392b", "#2c3e50"))
xr <- max(allsel$nlp)
# state annotation sits INSIDE the panel, so extend the x-limit to hold the longest label
plot(NA, xlim = c(0, xr*2.0), ylim = c(0.5, nrow(allsel)+0.5),
     yaxt = "n", xaxt = "n", xlab = "", ylab = "", bty = "n")
axis(1, at = seq(0, ceiling(xr/5)*5, by = 5))
mtext(expression(-log[10]~italic(p)~"(aBSREL, corrected)"), side = 1, line = 2.5, cex = 0.85)
segments(0, yy, allsel$nlp, yy, col = lab_col, lwd = 2.5)
points(allsel$nlp, yy, pch = 19, cex = 1.5, col = lab_col)
labs <- ifelse(allsel$is_tip, gsub("_", " ", allsel$branch),
               ifelse(allsel$branch %in% names(node_labels),
                      node_labels[allsel$branch], paste0(allsel$branch, " (internal)")))
axis(2, at = yy, labels = labs, las = 1, cex.axis = 0.85,
     col.axis = "black", font = 3, tick = FALSE)
node_state <- function(b) {
  fr <- node_frac[b]
  if (is.na(fr)) "internal branch"
  else if (fr == 0) "all-monochromatic clade"
  else sprintf("mostly mono (%.0f%% dich.)", 100*fr)
}
st <- ifelse(!allsel$is_tip, vapply(allsel$branch, node_state, character(1)),
             ifelse(allsel$dich == 1, "DICHROMATIC", "monochromatic"))
text(allsel$nlp + xr*0.05, yy, st, adj = 0, cex = 0.78, col = lab_col, font = 2, xpd = NA)
title(main = "B  Selected branches, by state", cex.main = 1.0, adj = 0)

mtext("POMC across the primate order: episodic selection is not confined to dichromatic lineages",
      outer = TRUE, line = 0.3, cex = 1.05, font = 2)
dev.off()

cat("POMC selected tips (state):",
    paste(sprintf("%s=%s", sel_df$tip, ifelse(sel_df$dich==1,"dich","mono")), collapse = ", "), "\n")
cat("POMC selected internal branches:", paste(sel_nodes, collapse = ", "), "\n")
