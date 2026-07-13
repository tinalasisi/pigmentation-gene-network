# Methods Survey: Gene / Gene-Regulatory Network Analysis on a Phylogenetic Scale

**Scope.** This survey covers computational and statistical method families for analyzing gene or
gene-regulatory networks *across species* (a phylogeny), oriented specifically to what is usable
given the data already assembled in this project:

- Codon-aware multiple alignments for ~80 pigmentation/sex-hormone panel genes across 117 primates
  (`comparative-genomics/results/full_panel_117/aln117_codon.tar.gz`)
- Per-gene HyPhy **RELAX** intensification/relaxation parameter K
  (`comparative-genomics/results/full_panel_117/relax_results.csv`)
- Per-branch HyPhy **aBSREL** episodic-selection omega and p-values
  (`comparative-genomics/results/full_panel_117/absrel/*.ABSREL.json`)
- A curated, signed, directed melanogenesis gene-regulatory network: 168 nodes
  (`gene`, `entrez`, `ensembl`, `chr`, `node_class`, `citation`, `citation_source`) and 309 edges
  (`source`, `target`, `sign`, `edge_class`, `via`, `citation`, `citation_source`)
  (`data/processed/gene_network_nodes.csv` / `gene_network_edges.csv`), plus an 803-node multilayer
  substrate (`data/processed/nb7_substrate_nodes.csv` / `nb7_substrate_edges.csv`)
- A dated species tree, trait states, and 14 independently-evolved dichromatism origins mapped onto
  a 224-tip trait tree (`comparative-genomics/config/primate_species_tree.nex`, `species_states.csv`,
  `origin_assignments.csv`)
- **No cross-species expression data.** This single fact rules out an entire class of methods
  (WGCNA/GENIE3/SCENIC-style expression-based GRN inference, coexpression-network comparison,
  cis-regulatory chromatin-activity comparison) for the "runnable now" tiers, and is flagged
  explicitly wherever it applies below.

Every citation below carries a DOI and/or PMID retrieved live from the PubMed connector
(`host.mcp` → PubMed MCP server, `search_articles` / `get_article_metadata`); none were recalled
from training. The companion table `phylo_grn_methods_papers.csv` lists all 25 papers with the same
fields plus explicit `feasible_with_our_data` calls.

---

## 1. Network/pathway-aware tests of selection

**The idea.** Instead of asking "is this one gene under selection?", ask whether selection signal
is concentrated, in a statistically detectable way, across a *set* of genes that share pathway
membership or network connectivity — i.e., polygenic or coordinated selection at the module level
rather than the single-locus level.

**Seminal method — PolySel.** Daub et al. introduced a gene-set enrichment framework that
aggregates <cite index="1-1">a gene-set enrichment test to identify genome-wide signals of adaptation among human populations</cite>, finding that <cite index="1-1">most pathways globally enriched for signals of positive selection are either directly or indirectly involved in immune response</cite> (Daub et al. 2013, *Mol Biol Evol*, DOI 10.1093/molbev/mst080, PMID 23625889). The same group later applied the identical
framework specifically to branch-resolved selection along **primate lineages ancestral to
humans** (Daub et al. 2017, *Mol Biol Evol*, DOI 10.1093/molbev/msx083, PMID 28333345) — this is
the closest published precedent to what Tier 1/2 of our plan proposes: branch-specific dN/dS-like
scores, aggregated by pathway, tested for enrichment of the selection signal.

**Adjacent method — network-based kernel-machine pathway test.** Freytag et al. built a
SKAT-style kernel-machine test that folds gene-gene network topology into the similarity kernel
used to test whether a pathway is jointly associated with a GWAS phenotype (Freytag et al. 2014,
*Hum Hered*, DOI 10.1159/000357567, PMID 24434848). This is conceptually related (network-topology
–informed set test) but is built for individual-level GWAS genotype-phenotype data, not for
cross-species selection statistics on a fixed species panel — **not directly transferable**.

**Adjacent method — HotNet2 (heat-diffusion module discovery).** Leiserson et al. diffuse a
per-gene score (originally somatic-mutation burden) across a protein-interaction network and
extract statistically "hot" connected subnetworks (Leiserson et al. 2014, *Nat Genet*, DOI
10.1038/ng.3168, PMID 25501392). Substituting per-gene RELAX K as the diffused score is a natural
adaptation, discussed further in Family 5 below (this method straddles both families).

**Applicability to our data.** PolySel-style gene-set enrichment is **directly runnable**: our
per-gene RELAX K and per-branch aBSREL omega/p are exactly the per-gene selection scores PolySel
consumes, and our 168-node network's `node_class` field (or a graph-partition into modules) can
serve as the gene sets. This is arguably the single most turnkey method family for the "runnable
now" tier, because it needs no data we lack.

---

## 2. Coevolution of interacting partners across a phylogeny

**The idea.** If two genes physically interact or are functionally coupled (e.g. a
transcription factor and its bound target), their sequences — and hence their substitution-rate
profiles — may be under correlated selective pressure across a phylogeny, detectable without any
expression data.

**Seminal method — mirrortree.** Pazos & Valencia showed that the similarity between two
proteins' phylogenetic-distance matrices (built from multi-species alignments) is an indicator of
physical protein-protein interaction (Pazos & Valencia 2001, *Protein Eng*, DOI
10.1093/protein/14.9.609, PMID 11707606) — the founding "tree-similarity" coevolution test. A later
review by the same group surveys the broader family of tree-similarity and residue-coevolution
methods, including the "in silico two-hybrid" extension (Pazos & Valencia 2008, *EMBO J*, DOI
10.1038/emboj.2008.189, PMID 18818697).

**Seminal method — Evolutionary Rate Covariation (ERC).** Clark et al. introduced ERC: computing
branch-wise *relative* evolutionary rates per gene across a phylogeny (correcting for lineage-wide
effects) and correlating these rate profiles between gene pairs — high correlation across many
species implies shared function or physical interaction, and the paper explicitly demonstrates
this <cite index="6-0">reveals shared functionality and coexpression of genes</cite> even though coexpression is only one of several correlated outcomes, not an input
(Clark et al. 2012, *Genome Res*, DOI 10.1101/gr.132647.111, PMID 22287101).

**Current method — RERconverge.** Kowalczyk et al. built the widely-used R package that computes
per-gene, per-branch relative evolutionary rates (RER) against a background species tree and tests
for association between RER and a convergent phenotype across independent origins, or between the
RER profiles of gene pairs (an ERC analogue) (Kowalczyk et al. 2019, *Bioinformatics*, DOI
10.1093/bioinformatics/btz468, PMID 31192356). Redlich et al. extended the framework to categorical
(non-binary) convergent traits (Redlich et al. 2024, *Mol Biol Evol*, DOI 10.1093/molbev/msae210,
PMID 39404101).

**Applicability to our data.** This is the **best-matched family to our data overall**. Our
117-taxon codon alignments per gene provide exactly the shared-species distance matrices mirrortree
needs; our per-branch aBSREL omega estimates ARE per-branch rate profiles, so an ERC-style
pairwise rate-correlation matrix restricted to network-adjacent (regulator–effector) gene pairs
versus randomly-paired non-adjacent genes is directly computable with zero new data. RERconverge is
an especially strong fit because we already have 14 independent dichromatism origins mapped on a
224-tip tree — precisely the convergent-trait design RERconverge's permulation-based test is built
for — and a `rerconverge` R environment already exists in this project's compute setup.

---

## 3. Phylogenetic comparative methods on network-derived traits

**The idea.** Treat a per-gene evolutionary-rate statistic as a continuous trait, and model it as a
function of network position (degree, betweenness, regulator-vs-effector class) while explicitly
accounting for the fact that gene identity, network position, and rate are not independent samples
— genes descend from a shared regulatory-network history, so naive correlation/regression across
genes risks pseudo-replication in the same way cross-species trait comparisons do.

**Foundational statistical framework.** Pagel introduced the likelihood-based comparative
framework — including the λ (lambda) phylogenetic-signal parameter — for testing how strongly a
trait's cross-taxon variation is structured by shared ancestry (Pagel 1999, *Nature*, DOI
10.1038/44766, PMID 10553904). This is the conceptual basis for any PGLS-style regression: it
justifies (and requires) modeling the "how similar because related" structure before drawing
conclusions from a rate-versus-position correlation.

**Software — phytools.** Revell's actively maintained R ecosystem implements PGLS, phylogenetic
signal estimation, ancestral-state reconstruction, and much else operating on a tree plus
tip/branch trait data (Revell 2024, *PeerJ*, DOI 10.7717/peerj.16505, PMID 38192598); a related
paper from the same author extends this to branch-heterogeneous ("variable-rate") continuous-trait
evolution models fit by penalized likelihood (Revell 2021, *PeerJ*, DOI 10.7717/peerj.11997, PMID
34458025).

**The claim being tested — Fraser & Hirsh's connectivity-rate hypothesis.** Fraser et al. reported
the original large-scale finding that a protein's number of interaction partners in a
protein-interaction network is negatively correlated with its rate of sequence evolution (Fraser et
al. 2002, *Science*, DOI 10.1126/science.1068696, PMID 11976460), building on the earlier
observation that <cite index="18-0">highly connected proteins in the yeast interaction network are disproportionately essential</cite> (Jeong et al. 2001, *Nature*, DOI 10.1038/35075138, PMID 11333967).

**The critique/confound this survey must flag.** Zhang & Yang's review establishes that expression
level — not network connectivity per se — is <cite index="14-0">Determinants of the rate of protein sequence evolution</cite>, i.e. the dominant and frequently confounding correlate of protein evolutionary rate, and that connectivity effects are often reduced or eliminated once expression is controlled for (Zhang & Yang 2015, *Nat Rev Genet*, DOI 10.1038/nrg3950, PMID 26055156).

**Applicability to our data.** The regression itself — per-gene RELAX K or branch-summarized
aBSREL omega versus network degree/betweenness/`node_class`, using `phytools`/PGLS on
`primate_species_tree.nex` — is **directly runnable**. However, the Zhang & Yang confound is a
hard limitation we cannot work around: **we have no cross-species expression data to control for**,
which is the single variable this literature identifies as usually dominant. Any centrality-vs-rate
result we produce must be reported as uncontrolled-for-expression, and interpreted with the same
caution that led the adjacent `internal/network-evo-explore/` analysis to find no centrality effect
once other covariates (gnomAD LOEUF, GTEx expression breadth, PBS) were included in a
human-population-genetics (not phylogenetic) setting.

---

## 4. Network / GRN rewiring and topology evolution across species

**The idea.** Reconstruct a gene-regulatory network *per species* (or per lineage) and compare the
resulting network structures — which regulatory edges are gained, lost, or rewired — to infer how
regulatory architecture itself evolves, as distinct from asking whether coding sequence is under
selection.

**Review — comparative GRN reconstruction and evolution.** Thompson et al. review the
computational pipeline from per-species network reconstruction to cross-species comparison,
covering edge gain/loss and rewiring inference (Thompson et al. 2015, *Annu Rev Cell Dev Biol*, DOI
10.1146/annurev-cellbio-100913-012908, PMID 26355593).

**Review — cis-regulatory comparative genomics.** Meireles-Filho & Furlong review methods for
comparing cis-regulatory sequences (enhancers, TF binding sites) across species to assess
conservation and turnover of regulatory information (Meireles-Filho & Furlong 2009, *Curr Opin
Genet Dev*, DOI 10.1016/j.gde.2009.10.006, PMID 19913403).

**Example method — Ornstein-Uhlenbeck models on TF-binding activity.** Naval-Sánchez et al. apply
phylogenetic OU models to quantitative chromatin/TF-binding signal across species to detect
lineage-specific regulatory shifts (Naval-Sánchez et al. 2015, *Mol Biol Evol*, DOI
10.1093/molbev/msv107, PMID 25944915) — illustrating the OU-model class of method that *would*
apply if we had cross-species chromatin/TF-binding data.

**Example resource — cross-species coexpression comparison.** Lee et al.'s CoCoCoNet builds and
compares gene coexpression networks across many species to find conserved/divergent modules (Lee et
al. 2020, *Nucleic Acids Res*, DOI 10.1093/nar/gkaa348, PMID 32392296).

**Applicability to our data — RULED OUT.** Every method in this family requires per-species
regulatory, chromatin, TF-binding, or expression evidence that is explicitly absent from our
inventory. We have one curated, human-centric regulatory network, not per-species reconstructions,
so there is nothing to "rewire" across the 117-primate panel without new noncoding/regulatory or
expression data. This entire family is **out of scope for the runnable-now tiers**, consistent with
the project's stated exclusion of expression-based GRN inference.

---

## 5. Propagation / smoothing of an evolutionary signal over a network

**The idea.** Rather than testing gene sets as fixed, discrete pathways (Family 1) or edges as
independent pairs (Family 2), diffuse a per-gene score across the network graph itself so that
genes *near* strongly-scored genes accumulate elevated combined scores — turning a sparse,
noisy per-gene signal into a spatially smoothed one that respects network topology.

**Foundational method — random-walk-with-restart propagation.** Vanunu et al. formalized the
propagation of an initial per-node disease-association score across network edges via iterative
diffusion, to <cite index="20-0">associate genes and protein complexes with disease via network propagation</cite> (Vanunu et al. 2010, *PLoS Comput Biol*, DOI
10.1371/journal.pcbi.1000641, PMID 20090828).

**Heat-diffusion module-discovery — HotNet2 and Hierarchical HotNet.** Leiserson et al.'s HotNet2
diffuses per-gene mutation burden through a heat kernel and extracts significantly "hot" connected
subnetworks by permutation testing (Leiserson et al. 2014, *Nat Genet*, DOI 10.1038/ng.3168, PMID
25501392). Reyna et al. extended this to extract a *hierarchy* of altered subnetworks across
multiple resolution thresholds simultaneously, removing the need to commit to one arbitrary
module-size cutoff (Reyna et al. 2018, *Bioinformatics*, DOI 10.1093/bioinformatics/bty613, PMID
30423088).

**Review — network propagation as a general framework.** Cowen et al. review the mathematical
basis, variants (random walk with restart, heat diffusion, insulated diffusion), and known
pitfalls (degree bias, the need for a permutation-based null) of network propagation as <cite index="22-0">a universal amplifier of genetic associations</cite> (Cowen et al. 2017, *Nat Rev Genet*, DOI 10.1038/nrg.2017.38, PMID 28607512).

**Applicability to our data.** Directly adaptable: substitute per-gene RELAX K (or a per-gene
summary of aBSREL branch omega) as the initial score, diffuse it across our directed 168-node
network's adjacency structure, and test whether selection signal clusters around strongly-selected
"seed" genes along the regulatory topology, using a degree-preserving permutation null as
recommended in Cowen et al. **Caveat:** standard propagation formulations discard edge sign
(activating +/repressing -), so a naive application collapses our signed network to an unsigned
one; preserving directionality (using the directed, not symmetrized, adjacency matrix) is possible
and should be treated as a deliberate methodological choice, flagged in any write-up, rather than a
default.

---

## Summary: what is ruled out, what is runnable now

**Ruled out by lack of cross-species expression data** (Family 4, in full, plus any
coexpression-network step of other families):
- Comparative GRN reconstruction/rewiring across per-species regulatory networks (Thompson et al.
  2015)
- Cis-regulatory sequence/chromatin turnover comparison (Meireles-Filho & Furlong 2009,
  Naval-Sánchez et al. 2015)
- Cross-species coexpression-network comparison (Lee et al. 2020, CoCoCoNet)
- Any WGCNA/GENIE3/SCENIC-style expression-based GRN inference (excluded by the project brief
  itself, and confirmed here as requiring data we do not have)

**Constrained by lack of expression data, but not fully ruled out** (Family 3): the
connectivity-vs-rate regression (Fraser & Hirsh-style) is computable, but Zhang & Yang (2015)
identify expression level as the dominant confound we cannot control for — report with that caveat
explicit.

**Directly runnable now, no new data required:**
1. PolySel-style gene-set/pathway selection enrichment on our per-gene RELAX K / aBSREL omega,
   using network modules as gene sets (Daub et al. 2013, 2017) — Family 1
2. Mirrortree-style pairwise distance-matrix correlation and ERC/RERconverge-style pairwise
   rate-profile correlation, restricted to network-adjacent (regulator-effector) gene pairs versus
   random non-adjacent pairs, using our shared 117-taxon alignments and aBSREL branch omega
   (Pazos & Valencia 2001; Clark et al. 2012; Kowalczyk et al. 2019) — Family 2
3. RERconverge convergent-trait association using the 14 independent dichromatism origins already
   mapped on the 224-tip tree (Kowalczyk et al. 2019) — Family 2
4. PGLS / phylogenetic-signal regression of per-gene selection intensity against network position
   (degree, betweenness, regulator-vs-effector class), explicitly modeling phylogenetic structure
   via `phytools` (Pagel 1999; Revell 2024) — Family 3, with the Zhang & Yang confound flagged
5. Network propagation/diffusion of per-gene selection scores across the signed/directed network,
   with a permutation-based null and explicit handling of edge sign/direction (Vanunu et al. 2010;
   Leiserson et al. 2014; Reyna et al. 2018; Cowen et al. 2017) — Family 5

These five map naturally onto a two-tier plan: **Tier 1** (fast, no new inference) = pathway/module
gene-set enrichment (1) plus network-position PGLS (4); **Tier 2** (moderate compute, new pairwise
computation) = mirrortree/ERC/RERconverge pairwise coevolution tests (2, 3) plus network
propagation/diffusion of the selection score (5).

## Search provenance

All records were retrieved live via the PubMed MCP connector (`search_articles` and
`get_article_metadata`) during this session. OpenAlex (the `literature` connector) returned
`openalex_key_required` for every call attempted in this session (API key present in the credential
store but not yet propagated to the connector runtime) and was not used as a source; every citation
in this survey and the companion CSV is PubMed-sourced with a resolvable DOI and/or PMID. No
citation was taken from memory or from a search-engine snippet.
