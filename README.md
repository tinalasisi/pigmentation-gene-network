# The architecture of pigmentation genetics

**What decides how a gene's effect on pigmentation plays out — is it a fixed, one-gene-one-trait
rule, or does it depend on context?** This project asks that question at two very different
scales — across millions of years of primate evolution, and within a single human genome — and
finds the same answer both times: context decides.

## The flagship finding: dichromatism arose ~15 times, polygenically, and is readily lost

**Dichromatism** means males and females of the same species look different in color (in this
case, hair color). In birds, this trait is close to a single genetic on/off switch: one gene,
*MC1R*, controls it almost everywhere it appears. Primates are different. Hair color dichromatism
has evolved **independently roughly 15 separate times** across the primate family tree — meaning
15 different ancestral species, each on its own branch, separately evolved the trait rather than
inheriting it from one shared ancestor. We identified these separate origins using **ancestral-state
reconstruction**, a method that works backward from which living species have the trait today to
infer, at each branching point in the family tree, whether the common ancestor there most likely
had it or not.

For the origins we could sequence genomes for, we asked a further question: which genes changed
under evolutionary selection to produce that particular origin's dichromatism? We looked at two
candidate groups of genes — a **pigmentation module** (genes that directly control pigment production) and a
**sex-hormone module** (genes in the hormone pathways that often drive sex differences in
appearance). "Module" here just means a functionally related group of genes we analyze together.
To detect selection, we used two statistical methods from the field of molecular evolution:
**aBSREL** and **RELAX**. Both compare the rate at which a gene's DNA sequence is changing on a
given branch of the family tree to the rate expected if the gene were evolving with no functional
consequence; a significantly faster or altered rate is evidence that natural selection acted on
that gene on that branch.

**The result: dichromatism is polygenic in every origin we could test, and *MC1R* — the bird
switch — is not the gene.** Of the origins with genomes to test, the 11 that carry at least one
gene under detectable selection each fall somewhere on a descriptive spectrum from "only
pigmentation-module genes selected" to "only sex-hormone-module genes selected." The lemur genus
*Eulemur* shows selection only in the sex-hormone module; the monkey genus *Pithecia* only in the
pigmentation module; the richest-sampled origin, the langur genus *Trachypithecus*, shows both.

**What we can and cannot yet conclude from that spread.** It is tempting to read the spread as a
*heterogeneous, origin-specific architecture* — different genes building the same trait in
different lineages. The data do not currently support that stronger claim. Only 3 origins have
enough foreground tips for the powered selection test (RELAX); the rest rest on single-tip aBSREL,
and the two "pure" poles (*Eulemur*, *Pithecia*) are each defined by just one or two selected
genes — a small-sample funnel effect, not a measured contrast. A homogeneity test across all 11
origins does **not** reject a single shared architecture (χ² p = 0.42), and the apparent
hormone-tilt disappears once the panel's own 2:1 hormone:pigmentation gene ratio is accounted for
(binomial p = 0.17). The honest statement is that **whether the genetic architecture is shared or
heterogeneous across origins is currently underpowered to resolve** — what is established is that
the trait is polygenic, not a single-gene switch. (Power detail:
[`comparative-genomics/results/perorigin_v1/README.md`](comparative-genomics/results/perorigin_v1/README.md).)

We also asked how easily the trait is gained versus lost over evolutionary time, using a method
modeled on prior work analyzing the evolution of mating systems (Opie et al. 2012). We found that
dichromatism is lost roughly **9 times more readily than it is gained** — consistent with a trait
that can be built through several alternative genetic routes (so it is easy to lose any one of
them) rather than through one fixed, hard-to-remove mechanism.

**Why this matters.** A trait that is nearly a single-gene switch in one vertebrate class (birds,
*MC1R*) is, in primates, polygenic, not driven by *MC1R*, and evolutionarily labile — arising ~15
times and readily lost. That alone reframes sexual dichromatism as a network-level rather than
single-locus trait; whether the network is remodeled at the *same* points across origins or
different ones is the open question this design sets up but is not yet powered to answer. The full
pipeline, data, and figures are in
[`comparative-genomics/`](comparative-genomics/); the specific analysis behind this finding is in
[`comparative-genomics/analysis/module_selection/`](comparative-genomics/analysis/module_selection/).

![Module balance across the origins of primate hair dichromatism. Each bar is one of the 11 origins that carry at least one gene under detectable selection, positioned from all sex-hormone-module selection (left, −1) through mixed (center) to all pigmentation-module selection (right, +1). No two origins sit at the same point.](comparative-genomics/analysis/module_selection/fig_module_balance.png)

## The second arm: grading human genetic evidence by convergence

The same project also works at the scale of a single human genome. Genome-wide association studies
(GWAS) routinely report statistical links between a DNA variant and a trait like skin color, but a
statistical link alone does not prove the variant causes the trait through a known biological
mechanism — and a mechanism that holds in one human population sometimes does not hold in another.
This arm of the project builds a curated network of the genes known to control pigment production
and uses it to grade how much independent evidence — statistical association, known biological
mechanism, and experimental validation — actually converges on each reported variant. This is
ongoing work; its current state, open questions, and materials are tracked in
[`internal/START_HERE.md`](internal/START_HERE.md).

## Why pigmentation is a good system for this

Pigmentation is unusually well suited to asking these questions because it is highly heritable,
shows almost no environmental influence on the trait itself, has a well-understood underlying
biology, and is directly visible and measurable — in a single human genome and across an entire
primate family tree alike.

## Repository orientation

- [`comparative-genomics/`](comparative-genomics/) — the primate dichromatism evolutionary analysis
  (the flagship finding above): pipeline, per-origin selection results, and figures.
- `data/processed/gene_network_{nodes,edges}.csv`, `raghunath_*` — the curated human melanin-production
  gene network.
- `data/case_records/EXTRACT_*.csv`, `data/raw/papers/*` — curated source papers and their extracted data.
- `data/processed/discordance_loci.csv` — a locus-by-locus view of genetic variants whose reported
  effect on pigmentation does not fully match expectation.
- `scripts/` — data-pull and harmonization tools.
- `internal/` — project planning, decision history, and provenance records;
  [`internal/START_HERE.md`](internal/START_HERE.md) is the current, authoritative account of project
  status and open questions; `DATA_SOURCES.md` documents where every dataset came from and its license.

License: MIT (see `LICENSE`).
