# START HERE — the single source of truth

**Read this first; it is enough to start.** One thing in this document is fixed: **the goal.** Everything
else — which materials to use, in what order, which route to take, how to build it — is **open for redesign.**
If you are Claude Science (or any session) picking this up, your job is to **re-think the execution in service
of the goal.** Do not treat any material below as a mandatory starting point.

Retired working material (earlier framings, superseded data, old plans) lives under `internal/archive/`
(gitignored) and is **not part of the current project** — you do not need it and should not build on it.

For **how the project reached this point** — what was tried, what was retired, and why — and for the two
decisions still open (the contribution's exact framing and the flagship demo visual, which are linked), see
`internal/PROJECT_EVOLUTION.md` (a guide, not a plan).

---

## THE GOAL (the one fixed thing)

**We are building a way to know how much to trust a claimed link between a genetic variant and a phenotype —
by making independent lines of evidence converge.** Statistical association, mechanistic pathway knowledge,
and experimental validation each capture part of the truth; where they agree, we can be confident the link is
real. Applied to pigmentation, the aim is **one resource that grades reported pigmentation associations by how
well independent evidence converges on each, and names the specific next step that would confirm it** — turning
scattered, reported-but-unvalidated results into an actionable, evidence-graded map, and using differences
between populations to reveal the conditional (epistatic) structure behind portability failure.

_(The goal is still being refined with the PI. Hold it as the anchor; propose execution that serves it. If you
believe the goal itself should shift, say so explicitly — do not quietly redesign around a different goal.)_

**Claude Science's first job is to evaluate this goal and _tighten_ it** — into the most interesting,
competitive, and defensible framing these materials can support: specific enough to aim at a concrete
contribution, while leaving room to pivot on the execution specifics. Sharpening the goal into a real,
publishable finding is what we most need you for.

## What a winning submission looks like (this is a hackathon — RESEARCHER TRACK)

This work is a submission to a hackathon's **Researcher Track — "Build From the Bench":** _start from a
biological question, find the existing datasets and tools to answer it, and submit something discrete — a
finding, a trained model, or an analysis others can reproduce — and show how Claude Science got you there._
(It is **not** the Builder track — we are not shipping a tool/website; presentation serves the finding.)

- **Aim at a discrete, concrete finding — one is enough.** The clearest win: **link even ONE previously
  genetically-associated pigmentation locus into the melanogenesis network** — a locus reported as associated
  but whose mechanism the original authors could not explain, shown to connect into melanogenesis (directly,
  or via a KEGG/Reactome/curated layer). **Even one such gene is a winning contribution — actively look for
  it.**
- **But do not tunnel on a single finding — there are other honest ways to win.** A reproducible analysis, a
  small trained model, a clean method others can rerun, or a well-characterized negative result all count.
  Take the easiest honest win the materials support.
- **Show the process.** "How Claude Science got you there" is part of the submission, so the reproducible
  notebooks (the base unit, below) are the record of the work — presentation is in service of the finding, not
  the other way around.

---

## Why pigmentation (grounds the goal)

A model system for the genotype→phenotype map, studied non-invasively in humans, that uniquely combines what
the method needs: high heritability and near-zero environmental variance (so discordance is almost purely
genetic architecture), a well-characterized molecular mechanism (melanogenesis), strong and replicated GWAS
signal across many populations, and a visible, measurable phenotype. It also shares its signaling backbone
with disease (~1 in 6 network nodes are canonical cancer genes). (Pavan & Sturm 2019, PMID 31100995.)

## The scientific problem (motivation)

The core question — *when does a variant actually cause a phenotype?* — is where every method has a blind
spot, so their **convergence** is the strongest signal available from existing data. It becomes visible through
**discordance**: a canonical causal variant present but the phenotype absent (reduced penetrance), or the
phenotype present without the canonical variant (an alternative route). Both are **portability failures** — a
risk model trained in one population predicts poorly in another — driven by the same variant sitting on a
different genetic background with **non-additive** interactions that additive GWAS cannot capture. Pigmentation
makes this concrete: Europe-centred work once thought the trait simple, but GWAS in African, Oceanian, and
East-Asian populations found **different causal loci** (Crawford, Martin, Kenny/Norton TYRP1, Yang OCA2). The
best studies validate functionally (Crawford knocked MFSD12 down in zebrafish/mouse — pull the exact assays);
most stop at association, leaving loci stranded. **Synthesizing them to grade each and suggest the confirming
experiment is the opportunity.**

---

## OPEN — decisions that are Claude Science's to make (not yet decided)

These are deliberately unresolved. Choose in service of the goal; justify the choice.
- **Which route to reported associations?** Options include (a) the 13 curated discordance papers, (b) a direct
  GWAS Catalog pull of pigmentation loci, (c) specific population studies (Crawford, Martin), or (d) some
  combination. **We have NOT committed to the discordance-papers route.** It is one option among several.
- **What is the unit, and where do we start?** Loci, genes, or associations — and which material is the entry
  point — is open. `discordance_loci.csv` is *one processed view of route (a)*, not a required foundation.
- **How to represent/expand/harmonize the network** (which layers, added how, in what order).
- **How to define and compute "convergence"** into a confidence grade.
- **What the final deliverable looks like** (a graded catalog, a figure, a method paper, a tool).

> **Current candidate directions (2026-07-12 — framing is UP IN THE AIR, nothing locked):** three threads are
> live and no flagship is settled. (1) The **rescue screen** (NB4–NB9) — an honest negative on novel effectors,
> with methodological "the choice changes the answer" results. (2) A **convergence-graded direction
> demonstration** (NB10 + NB12) — a functional melanin screen orders Mendelian pigmentation-disorder direction
> under a loss-of-function allele (22/22 → 29/33 expanded, *p*<1e-5) with a partly-predictable failure boundary;
> a literature audit found the *biology* is textbook, so its value is **methodological**, not a new discovery —
> reported as a bounded demonstration of the convergence thesis, not a "law." (3) A **primate-phylogenetics**
> evolutionary direction, under active exploration by the PI. See `PITCH.md` and `project_dashboard.md` for the
> current state; the exact contribution framing remains Claude Science's + the PI's to settle.

### Where to look for the gap (a question worth answering early)

A real contribution needs a real gap. One worth characterizing first: **what does the field actually do today,
and where does it stop?** A common pattern is — run a GWAS, look the hit up in Gene Ontology or a pathway
database, and when nothing obvious comes back, stop. That leaves loci *replicated but unexplained*. The gap we
may be well placed to fill is turning "associated, mechanism unknown" into "here is the specific, cited route
by which this locus plausibly acts on the phenotype." The kind of concrete finding to aim for reads: *"this
pigmentation locus was replicated once and its authors could not say why it was associated; through the
network's KEGG/Reactome layer we show exactly how it connects to melanogenesis."* Characterizing the field's
current stopping point — and where we can honestly go one step further, as good scientific colleagues — is a
first task.

## The notebooks — the base unit of contribution (read these first)

**In this kind of project the notebooks, not the CSV/JSON files, are the unit of work.** Each is a
self-contained **mini-manuscript** — introduction, methods, results, discussion/conclusion, with citations —
that a colleague can read, reproduce, and adapt. The processed tables are their *outputs*, not the
contribution. Any new work should take this manuscript form. The three that matter most (stable, flexible,
foundational — order is not fixed):
- **[Notebook 1 — Reconstruct the published network](../../notebooks/01_reconstruct_published_network.ipynb)**
  — rebuilds the Raghunath 2015 melanogenesis model as a signed, directed network, typing/signing every
  interaction from the published file with a per-edge citation. *The most confident, foundational work.*
- **[Notebook 2 — Resolve the network to genes](../../notebooks/02_resolve_network_to_genes.ipynb)** — resolves
  entities to genes (UniProt/HGNC/Ensembl), builds the explicit gene layer, validates every edge against
  OmniPath; every node and edge carries a resolvable citation. *Also foundational.*
- **[Notebook 3 — Assemble the validation cases](../../notebooks/03_assemble_validation_cases.ipynb)** —
  documents how the discordance cases were pulled from curated papers and counted; reproducible and adaptable.
- Supporting extractors: `notebooks/01a`–`01d` (Bajpai CRISPR, Baxter genes, HIrisPlex markers, GWAS-Catalog
  reproduction). A readable Quarto front door to NB1–NB3 lives at `index.qmd` (rendered from stored outputs).

## The materials we have (an inventory — use any, all, or none; reorder freely)

None of these is a starting point by default; they are assets. Paths are relative to the repo root.

**Mechanistic network / pathways:**
- Raghunath directed, signed melanogenesis network — `data/processed/gene_network_{nodes,edges}.csv`
  (gene-level) and `raghunath_{nodes,edges}_typed*.csv` (raw), built by `notebooks/01,02`. One 2015 model;
  known to be missing much of the broader curated pathway.
- OmniPath curated interactions used to validate that network — `data/processed/nb2_omnipath_validation.csv`.
- External curated pathways reachable live: **KEGG hsa04916** (~101 genes), **Reactome**, **STRING** (public
  REST). Not yet incorporated.

**Reported-association sources (the "route" question above):**
- 13 curated discordance papers → faithful extracts `data/case_records/EXTRACT_*.csv` → one processed
  locus-first view `data/processed/discordance_loci.csv` (105 loci, each with rsID/coord, the paper's own
  verdict, an is_asserted_pigmentation flag, verbatim evidence, a `needs_review` flag). Raw papers +
  supplements: `data/raw/papers/*`.
- GWAS Catalog — a live, config-driven pull engine `scripts/gwas_catalog.py` + frozen trait roots
  `scripts/traits_pigmentation.json` (10 pigmentation trait roots, skin/eye/hair). Not yet run in this repo.
- Source gene/marker sets: `baxter2018_650_pigmentation_genes.csv`, `bajpai2023_crispr_hits.csv`,
  `hirisplexs2018_markers.csv`; D'Arcy 2023 OMIM disease-gene tables in `data/raw/darcy2023/`.

**Connectors + tools:**
- **Claude Science has the human-genetics MCP connector** (GWAS Catalog, eQTL Catalogue, PheWAS) — the natural
  home for locus resolution. Also: OpenAlex/PubMed (literature, DOI/PMID-verified), Open Targets L2G, and the
  KEGG/Reactome/STRING REST endpoints. (Claude Code lacks the human-genetics connector; it used public REST.)
- Repo tools: `scripts/{gwas_catalog,harmonize,validate_locus_tables,build_resolver_manifest,vizhelpers}.py`,
  `traits_pigmentation.json`. Provenance manifest: `DATA_SOURCES.md`. Specs: `docs/specs/*.spec.md`.

## Ideas on the table (candidate approaches — evaluate, revise, reorder, or replace)

These came from the PI's thinking. **They are non-binding.** Treat them as a menu to pressure-test, not a plan.
- **Harmonize a multi-layer network** (Raghunath + literature-directed additions + KEGG/Reactome + a STRING
  expansion + D'Arcy compared-not-merged) and tag each node by which layers support it — convergence across
  layers = confidence. (Comparing D'Arcy to Raghunath — what each has that the other lacks — may itself be a
  finding.)
- **An association-evaluation engine:** for each reported locus, grade by converging evidence and classify —
  mechanistic (in the network) / mediating-gene (via a curated layer) / LD-rescue (in LD with an in-network
  locus the study missed) / likely population-specific false hit / unexplained → Open Targets L2G — with a
  concrete confirmation step per locus.
- **Population + conditionality:** same allele, different penetrance across populations reveals conditional
  structure; the directed network can nominate compensating loci (alternative paths to the pigment endpoint)
  and penetrance-modifiers (gating nodes) as *hypotheses to test*.

## What we've learned that is reliable (lessons, not plans)

Read the two audits for the detail — **for the lessons, not the retired framing they critique:**
`internal/handoffs/HANDOFF_CRITICAL_limitations_and_framing_issues.md` and
`internal/TRACEABILITY_coverage_and_resolution_logic.md`.
- **Work locus-first.** A gene-first extraction previously manufactured spurious "genes" from haplotype
  segments, SNP clusters, and null retests. Keep the variant/region as the unit; attach a gene with a recorded
  basis.
- **Resolve to the causal gene** (a GWAS label is the nearest gene by position; e.g. the blue-eye signal at
  HERC2 routes to OCA2 via a long-range enhancer).
- **Convergence over any single headline number.** Earlier framings over-invested in one metric ("% dark",
  "resolution rate"); those are retired. Counts are diagnostics, recomputed from pinned files, never the claim.
- **Prior work to build on and credit** (do not re-claim): Open Targets L2G (Mountjoy 2021, PMID 34711957) +
  cS2G (Gazal 2022, PMID 35668300) for locus→gene; Kim 2024 (PMID 38849341) population skin-colour atlas;
  Burga & Lehner 2011 (PMID 22158248) network penetrance; Loftus 2023 (PMID 37327787) allele-level pigmentation
  heritability; Aw 2025 (PMID 41043808), which bounds firm mechanistic claims to resolved-causal-variant loci.

## Working conventions (kept minimal)

`internal/` is public (cite by DOI/PMID; no copyrighted full text). Commits clear `REPO_COMPLIANCE_GATE`.
**Datetime-stamp everything** — every changelog entry, governance note, and doc stamp carries a full UTC
datetime (`YYYY-MM-DDTHH:MMZ`), never a bare date; work here spans many hours across days, so a bare date is
ambiguous.
History is append-only in `internal/CHANGELOG.md`; agent coordination goes in `internal/handoffs/notes/`
(one file per message; see `internal/handoffs/README.md` + `MERGE_SAFETY.md`). Verified references:
`internal/lit_review/bibliography/`.

## Current state

> **This section dates quickly.** It is a pointer to the living record, not a substitute for it. For where
> the project actually is right now, read — in this order — `internal/project_dashboard.md` (the snapshot /
> control surface), the tail of `internal/CHANGELOG.md` (dated history), and `internal/TODO.md` (open work).
> Those three are kept current as work happens; the paragraphs below are a point-in-time note that later
> entries may have superseded. When this note and the changelog disagree, **the changelog wins.**

**2026-07-12T01:42Z — where we are now (supersedes the 2026-07-11T22:51Z note below).** An execution
route has been chosen and PI-approved: the convergence-graded rescue screen built as notebooks **NB4–NB8**
(unified association base → compare candidate networks → harmonized multi-layer substrate → resolution +
convergence-graded rescue screen → optional population conditionality). See `CHANGELOG.md` 2026-07-12T00:29Z
for the six decisions behind it and `internal/TODO.md` for the phase tracker; the approved plan is a Claude
Science artifact (id in `TODO.md`). NB1–NB3 are stable and foundational; NB2's reproducibility was restored
and committed (`95f1969`, CHANGELOG 2026-07-12T01:16Z). **NB4–NB5 are in progress in a concurrent session** —
their outputs (`nb5_*.csv`, `discordance_loci_author_explained.csv`, `darcy2023_S*.csv`) are on disk but not
yet committed. A tentative `internal/project_dashboard.md` (the third tracking document) now exists as the
one-screen snapshot; read it first for orientation. The route below ("no execution route is committed") was
accurate at the 2026-07-11T22:51Z restart and is kept for continuity.

**2026-07-11T22:51Z (point-in-time, superseded above for the route question).**
The repo was cleaned to this minimal, framing-neutral set on 2026-07-11; retired material is in
`internal/archive/`. No execution route is committed. The Quarto site (`index.qmd`, `_quarto.yml`) still
carries old framing and references archived notebooks — treat it as stale until the goal's execution is
settled. Next step is **not** predetermined: Claude Science decides the route and the build.
