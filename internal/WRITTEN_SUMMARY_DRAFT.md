# Written summary — draft (Researcher Track, "Build From the Bench")

**Status:** DRAFT for PI review. **Three-act build voice** (per PI, 2026-07-13): the story is the
process — pigmentation network → sex-hormone network → phylogenetic test — where each act ends on a
scientific result, the tools are shown in the doing (never narrated), and self-correction is just
what iteration looks like, not a theme. Result-independent by construction. All numbers verified
against the repo. ~430 words.

---

## Title

**Building an instrument from scratch, one question at a time: from a pigmentation gene network to
a phylogeny-controlled test of how sexual dichromatism evolved across primates.**

## Summary

I started this week not knowing most of the methods below. I finished with a reproducible pipeline
that answered a real evolutionary-genomics question — because each answer forced me to build the
next piece.

**Act 1 — a gene network for pigmentation.** The first question was simply *which genes matter, and
how do we know?* So I built a harmonized, provenance-sealed resource: an 803-gene × 74-feature table
over a cited multi-source network (STRING v12, OmniPath, a MITF/SOX10/PAX3 regulon, the signed
Raghunath 2015 melanogenesis pathway), plus an interactive explorer showing which source implicates
each gene, every input checksummed to the exact bytes read. **Result:** pigmentation architecture is
context-dependent, not one-gene-one-trait — a reusable substrate a second lab can point at its own
question.

**Act 2 — the question pulled in hormones.** To ask *why sexual dichromatism evolves* — a
sex-difference trait — pigment genes alone are insufficient; the sex-hormone axis has to be in the
model. So the network grew a second module. **Result:** a two-module (pigmentation × sex-hormone)
selection panel — a coupled system I could now *test* rather than assume.

**Act 3 — point the instrument at deep time.** I placed 117 published primate genome assemblies
(pulled from NCBI — not assembled by me) on a 238-species phenotype tree and ran a documented
CDS-extraction → codon-alignment → HyPhy selection pipeline on an HPC cluster, then the phylogenetic
comparative tests locally. **Results, graded by what the data support:** sexual dichromatism arose
**~15 times independently**, is **polygenic every time** (*MC1R* is not the hit), and is lost **~9×
more readily than gained**. Testing the pigment–hormone coupling directly: the two modules
**co-evolve with each other** (concordant per-lineage selection, PGLS β ≈ 0.42, *p* ≈ 1e-4) but that
coupling **does not track the trait** — the network is coupled to itself, not to the phenotype. And
run as a cross-species GWAS, with the phylogeny standing in for population-structure control, the
scan returns **one suggestive candidate**, *AKR1C4*, a sex-hormone-module steroid reductase (one hit
among ~80 genes at ~24 cases — a lead to chase, not an established locus).

**The through-line.** A vague "coupled system" intuition, turned into tested, honestly-graded
results by an instrument I built end to end — literature mining, network biology, comparative
genomics, HyPhy, phylogenetic comparative methods, and reproducible-research engineering — most of
it for the first time, in one week (220 commits, 2026-07-09 to 2026-07-13). The pipeline is the
deliverable; the biology is what it proves the pipeline can do.

---

## Optional worked illustration (drop in if space allows)

The network lets the two data types check each other: *KITLG* is a convergence (selection-significant,
OMIM-flagged, GWAS-mapped) while *TYR* is an informative disagreement (strong human-genetics support
but a rejected selection hit on alignment QC) — the cross-scale check the resource enables.
