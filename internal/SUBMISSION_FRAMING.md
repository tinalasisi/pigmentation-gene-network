# Submission framing — Researcher Track ("Build *From* the Bench")

**Status:** DRAFT v2 for PI review. Single source of truth for the project's result-independent
framing. Once approved, thread the thesis + claimable facts into `README.md` and
`internal/project_dashboard.md`.

---

## What the track actually rewards

> **Researcher Track — Build *From* the Bench.** "Using Claude Science, start from a biological
> question you've been thinking through and find the existing datasets and tools needed to answer
> it. Submit something discrete — a finding, a trained model, **an analysis others can reproduce** —
> and show us how Claude Science got you there."

The deliverable list is *finding / model / reproducible analysis* — **a positive result is not
required.** The rubric rewards the arc: a real question → the right data and tools assembled to
attack it → a discrete, reproducible artifact → a clear account of how you got there. A well-posed
question that returns a clean, reproducible *"not yet resolvable at this power"* is a finding on
this rubric. Two things this project can claim unconditionally answer the ask: **(A)** a reproducible
instrument that poses a real evolutionary question, and **(B)** the range of bench skills exercised
to build it — most for the first time, in a week.

## The thesis (result-independent)

> Starting from a question I had been thinking through — **how is sexual dichromatism, a
> sex-linked pigmentation trait, built across the primate radiation?** — I used Claude Science to
> curate a coupled **pigmentation × sex-hormone** gene resource from many published sources, pull
> the **117 published primate genomes** needed to interrogate it, and build a fully **reproducible**
> pipeline — from gene-network reconstruction through a codon-alignment + molecular-evolution
> selection scan to phylogenetic comparative tests — that poses the selection question **per
> independent origin** of the trait. The instrument is the deliverable: it turned a question I
> could only ask in the abstract into one that is now data-grounded, versioned, and replayable —
> whatever any single selection test concludes. Along the way I picked up and chained together
> roughly seven bioinformatics domains I had mostly never worked in before.

This reframes the project from *"we found a heterogeneous architecture"* (which the internal power
audit shows the current data cannot support) to *"I built the instrument, posed the question
reproducibly, and learned the whole bench to do it"* (which the track asks for and which is
unconditionally true).

## Claimable facts — each true regardless of the evolutionary verdict

1. **A reproducible pipeline, built in notebooks.** 18 notebooks (NB01→NB14) plus the
   comparative-genomics analyses, each a self-contained mini-manuscript that renders from its own
   frozen outputs. The coevolution test carries a closing **replay-equality assertion** that
   reproduces its committed values end-to-end (`comparative-genomics/analysis/coevolution_test/`).
   *This is literally "an analysis others can reproduce."*

2. **A curated gene resource — two nested tiers, integrated from independent sources.**
   - **Broad substrate: ~800 genes**, feature-annotated. A 803-gene × 74-feature table
     (`feature_table.csv`) over an ~803-node / ~7,800-edge interaction network, layering STRING
     co-function, OmniPath literature-curated interactions, a MITF/SOX10/PAX3 regulon, and the
     signed Raghunath 2015 melanogenesis pathway — plus a 200-gene OMIM/GWAS disorder-architecture
     classification.
   - **Focused selection panel: ~78 genes** = 26 pigmentation + 52 sex-hormone (a pigmentation
     melanosome-biogenesis expansion to ~57 is staged), the functionally-justified subset the
     evolutionary test runs on.
   - Sources include a reconstructed melanogenesis network cross-checked against Baxter 2019,
     HIrisPlex, the GWAS Catalog, Bajpai CRISPR screens, and Zhang melanocyte eQTL; the hormone
     module is KEGG-seeded (steroid biosynthesis + GnRH). Every source is recorded in
     `DATA_SOURCES`. *This is the "find the existing datasets and tools" step, done and documented.*

3. **An interactive resource for exploring the genes.** A rotatable, browser-based **multi-layer
   network explorer** (`substrate_multilayer.qmd` → `interactive/substrate_multilayer.html`): every
   pigmentation-implicated gene sits on only the evidence layers that actually carry it (STRING /
   OmniPath / regulon / mechanistic pathway), node size grows with layer count, rings mark OMIM
   clinical genes, diamonds mark Bajpai CRISPR screen hits — hover any gene to read its evidence
   and clinical/functional flags. A genuinely demoable artifact for walking a judge through "which
   sources implicate this gene, and how strongly."

4. **A question extended by biological reasoning.** From pigmentation genes to the sex-hormone genes
   coupled to them through the shared network — the **POMC → α-MSH / ACTH** bridge —
   turning a gene catalogue into a testable *evolutionary* question about a coupled system.

5. **The genomes pulled to ask it.** **117 published primate genome assemblies** (NCBI), placed on
   a **238-species** phenotype tree — the panel that makes a clade-wide, per-origin selection test
   possible at all.

None of these depends on how RELAX / aBSREL land. The evolutionary test is *one instantiation* the
reproducible system enables.

## The skills arc — "a week, ~7 bench domains, most for the first time"

This is the "show us how Claude Science got you there" evidence, and it is on-thesis for a track
literally named *Build From the Bench*. Each is checkable in the repo:

1. **Literature / data mining** — extracting structured gene sets from CRISPR-screen, GWAS-catalog,
   forensic-marker, and eQTL supplements (NB01a–d).
2. **Network biology** — reconstructing a gene interaction / regulatory network and resolving nodes
   to genes (NB01, NB02, NB06, NB07).
3. **Comparative genomics** — ortholog retrieval, per-gene CDS extraction (incl. `miniprot` for
   unannotated genomes), codon-aware multiple-sequence alignment (MAFFT) + alignment QC.
4. **Molecular evolution** — HyPhy **RELAX** (relaxation/intensification) and **aBSREL**
   (branch-specific positive selection).
5. **Phylogenetic comparative methods** — ancestral-state reconstruction, Mk/ARD transition rates,
   Pagel's λ, `fitPagel` correlated evolution (phytools / ape).
6. **Reproducible-research engineering** — frozen-data notebooks, replay-equality assertions,
   shared-repo version control, SLURM job arrays on an HPC cluster.
7. **Statistical rigor** — permutation / Monte-Carlo nulls, BH correction, and a **power audit that
   caught an over-claim before it shipped** (the judgment to demote one's own headline).

## What ran where — data pulled vs. analyses done (be precise)

| Data **pulled** (public sources) | Analyses **done** with Claude |
|---|---|
| 117 primate genome assemblies (NCBI `datasets`) | Reconstructed the pigmentation network; resolved nodes → genes |
| KEGG pathways (hormone-panel seed) | Assembled + justified the two-module panel (NB13 → NB14) |
| Baxter 2019, HIrisPlex, GWAS Catalog, Bajpai CRISPR, Zhang eQTL, Martin GWAS | Per-gene CDS extraction + MAFFT codon alignment + QC *(on Great Lakes HPC)* |
| Ensembl / UniProt / MyGene gene identity | HyPhy RELAX + aBSREL selection scans per origin *(on Great Lakes HPC)* |
| 238-species phenotype coding | phytools comparative methods: Pagel's λ, ASR / transition rates, fitPagel |
| | Module-balance metric, interactive explorer, figures, frozen-data notebooks + replay assertions |

**Provenance honesty (load-bearing):** we did **not** assemble or align genomes ourselves. We
**pulled published assemblies from NCBI**, extracted per-gene CDS, and ran a **codon-alignment +
selection pipeline** on them. The CDS-extraction + MAFFT + HyPhy steps ran on the **U-Michigan
Great Lakes HPC** (via claude-code, "Cluster Claude"), not inside Claude Science; the network
curation, panel design, interactive resource, and phylogenetic comparative tests ran in Claude
Science. Never write "assembled and aligned genomes."

## The honest results status (what we say about the biology)

- **Solid and reportable:** dichromatism arose **~15 times independently** across primates; it is
  **polygenic in every origin tested**, with no single gene of major effect (and *MC1R* — the
galliform melanin gene — is not the hit); it is
  **evolutionarily labile, lost ~9× more readily than gained** (ARD vs ER, ΔAIC 19.8).
- **Explicitly open / underpowered:** whether different origins recruit the **same** or
  **different** genes — a shared vs. heterogeneous architecture — is **not yet resolvable** (χ²
  homogeneity across the 11 origins with detectable selection p = 0.42; hormone-tilt is panel
  composition, binomial p = 0.17; only 3 origins are RELAX-powered). Named powered next steps:
  PicMin across the 14 origins, and a network-subgraph test (signet).
- **Correlated-evolution test (Opie analog):** module selection does **not** co-evolve with
  dichromatism at the lineage level (fitPagel independent model preferred for both modules) — a
  clean, reproducible negative, consistent with the non-significant set-level contrast.

Reporting the open question honestly is *on-thesis*, not a weakness: it demonstrates the instrument
works and the question is now decidable with more power.

## Placement plan (after approval)

- **`README.md`** — insert the thesis paragraph at the top of the flagship section; keep the
  already-reconciled results wording below it; add a short "what ran where" note and a link to the
  interactive explorer.
- **`internal/project_dashboard.md`** — add the thesis + claimable-facts + skills-arc block near
  the top. NOTE: this file currently holds another session's uncommitted edits — preserve those
  first, fold this in around them, and record it in the handoff.
- Scoped commit by explicit path; compliance gate (object-reads-only); push.
