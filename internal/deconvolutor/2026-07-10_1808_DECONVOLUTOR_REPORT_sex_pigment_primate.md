# Plan Deconvolutor report — sex-hormone × pigmentation expansion plan

**Subject:** `internal/EXPANSION_PLAN_sex_pigment_primate.md` (TENTATIVE, unauthorized, §6 six questions unanswered)
**Trigger for this report:** PI-imposed hard 48-hour deadline (received mid-review). This report is organized
around that constraint first; the pre-deadline findings are preserved underneath it.
**Status of this document:** pre-approval critique only. No plan edits, no build action, no commit.

---

## Headline verdict

**No part of Stages A–D produces a scientific result in 48 hours.** The plan's own text already flags three
of its four stages as depending on curation tasks it does not budget (a cross-primate dichromatism score, a
CYP/HSD orthology resolution "raised from formality to central task," and phylogenetic-statistics tooling not
yet installed). Live checks run during this review confirm the sharpest version of that problem for the two
tasks the plan treats as tractable:

- **The bridge-edge table's central claim has zero database support.** A live query against OmniPath's 11
  aggregated interaction resources for edges from AR/ESR1/ESR2 to a 14-gene melanogenic/melanocortin set
  returned **zero direct edges** out of 344 interactions pulled touching either gene group. Every bridge edge
  the plan needs must come from hand curation against the ~2 mechanism papers it names — and turning "2 review
  papers" into a defensibly per-edge-cited graph of 30–60 distinct receptor→gene claims is a 10–40 hour task
  by itself, done honestly; done in the time available, it either ships as a short "not supported, excluded"
  list or ships as citation padding.
- **The orthology hazard is real but has not been shown to be the blanket problem the plan implies.** A live
  Ensembl Compara pull for a small gene sample found CYP17A1, CYP19A1, and HSD17B3 clean 1:1 across ~6–14
  primate species each, while HSD3B2 showed real complexity (3 one2one / 2 one2many / 3 many2many across 8
  primate hits). That is exactly the kind of gene-by-gene adjudication the plan's Stage C gate calls for — and
  it does not scale to the full pathway + backbone gene universe in 48 hours; it scales to a half-dozen
  hand-picked genes, which is not what "hard gate before any comparative test" means.

**The only defensible 48-hour deliverable is an explicitly labeled preliminary skeleton, not a finding**: an
installed phylogenetics toolchain, a tip-label mismatch list (not a "reconciliation"), a small single-annotator
orthology audit on a named gene subset (explicitly *not* a pilot for the wider gene universe), and a
citation-gap list scoped to the ~2 named papers (never phrased as "no literature support exists"). Every one of
these is QC/disclosure material, not evidence toward the paper's causal or evolutionary claim. See §3 for the
per-item ship/do-not-ship table.

---

## 1. Streamlined plan (cold read, no session context)

Stripped of its own hedging, the plan commits to:

1. Treat KEGG hsa00140 (steroid biosynthesis) + AR/ESR1/ESR2 as the mechanistic backbone, demoting the
   scoping memo's original candidate (Ríos 2016 gonadal sex-determination) to background context.
2. Hand-curate a small "bridge-edge" table connecting that receptor layer to ~14 melanogenic/melanocortin
   genes, using two named mechanism papers plus the project's existing OmniPath+curated-literature-only edge
   rule.
3. Run a perturbation/signed-path analysis on the coupled graph (Stage B).
4. Resolve orthology for every gene in both layers across primates, gate the comparative test on 1:1 orthologs
   only (Stage C).
5. Run PGLS / phylogenetic logistic regression against a to-be-built standardized cross-primate dichromatism
   score, on a dated tree, with optional dN/dS (Stage D).
6. Put six open questions to the PI (§6 A–F) about scope, sourcing, and sequencing, and treat the plan as
   promoted to "agreed" only once those are answered and logged in a changelog.

**What an outsider would flag immediately, with no other context:**

- The plan asks the PI to approve a four-stage, phylogenetics-plus-molecular-evolution research program via a
  single yes/no per §6 item, when at least two of those items (B: phenotype definition, C: species scope) are
  themselves open research questions, not scoping choices with known answers.
- Section 4's "confidence is the product of three layers, not the sum" is presented as a strengthening insight
  but is not a real probability calculation — none of the three factors (coupling, orthology, phylogenetic
  non-independence) is a calibrated probability, so multiplying them produces a single number that looks more
  rigorous than any of its inputs, not less. A plain reader would ask why this framing is here at all rather
  than three separately reported confidence flags.
- The "reconciliation" in §2 (demoting Ríos 2016, promoting the CYP/HSD hazard to the critical path) reads as
  a decision already made and defended in the same paragraph that asks the PI to confirm it in §6-A. If it is
  genuinely open, arguing for it before asking about it pre-loads the answer.
- The document proposes its own promotion mechanism (a changelog entry) inside a document that says six times
  it is not yet authorized — a plan does not need to specify how it becomes official before anyone has agreed
  it should.
- Nothing in the six-question decision log asks the one question that turns out to dominate everything else
  once a deadline exists: **how much of this is deliverable in the time available, and what does "deliverable"
  mean if the answer is "not much"?** See §4 for the consolidated question set, including this gap.

None of the above is disqualifying on its own — a forward-looking research plan is allowed to look like this.
What follows is why, under a 48-hour constraint, the gap between "here is the design" and "here is what ships"
becomes the whole story.

---

## 2. Adversarial stress-test (2 rounds; converged)

Delegation to sub-agent critics was unavailable in this session (leaf-frame restriction); the stress test was
run instead as two rounds of adversarial/defense fan-out grounded in the live OmniPath and Ensembl Compara
checks above. Round 2 surfaced refinements to round 1's attacks (rater-reliability gaps, mislabeling of
"reconciliation" vs. "mismatch detection," search-scope overclaiming) but no new attack that changed the
bottom line — per the stop rule, the test halted after round 2.

**Round 1 — six independent-sinking attacks on 48h deliverability**, in order of severity:

1. Stage D's dependent variable (a standardized cross-primate dichromatism score) does not exist and cannot be
   built to a defensible standard in 48h — the plan's own two anchor papers measure different traits (facial
   colour vs. Colobinae pelage) in different clades; reconciling them into one validated scale is itself a
   methods contribution, realistically 3–6 weeks for a modest species set.
2. The Stage C hard gate cannot be resolved at the scale the plan requires; the live check's own small sample
   already found one gene (HSD3B2) with real one2many/many2many complexity, meaning full-pathway,
   full-species-set orthology adjudication is a 20–40+ hour task, not a formality.
3. The phylogenetics/molecular-evolution tooling and a dated primate tree are not installed or identified;
   integration QC (tip-label reconciliation across tree/Compara/phenotype tables, tree-choice justification
   against a posterior tree distribution) is a 1–2 day task by itself if done with the rigor the method
   requires.
4. The bridge-edge table's per-edge citation requirement cannot be met by the two named mechanism papers at
   the scale the coupling interface implies (a live OmniPath check found zero database-supported edges, so
   every edge is hand-curation-only); real per-edge sourcing runs 20–40 minutes each across an estimated 30–60
   candidate edges.
5. The multiplicative confidence score requires three calibrated, comparably-scaled probabilities; none of the
   three factors can become one in 48 hours, and multiplying uncalibrated numbers manufactures false precision
   rather than a conservative combined estimate.
6. KEGG's hsa00140 map represents several reaction steps as generic enzyme-class nodes that actually
   correspond to multiple paralogous genes (e.g., HSD3B1/HSD3B2) with different tissue expression; importing
   the pathway without manual node-splitting produces a confidently wrong, not just rough, sign prediction in
   Stage B.

**Defense round — what survived after conceding the above:** five narrow items were proposed as genuinely
deliverable in 48h: (a) a pilot orthology audit on a small named gene subset (CYP/HSD family + 3 receptors),
(b) a tip-label reconciliation audit between tree/Compara/phenotype species names, (c) an edge-citation-gap
list (mostly "not supported, excluded" rather than a filled graph), (d) the R/bioconda package installs, (e)
manual KEGG node disambiguation bounded to the same small pilot set.

**Round 2 — attacking the five survivors:**

- **(a) orthology pilot** — does not survive as scoped. It is a single-annotator, single-pass, unreplicated
  judgment call on a convenience sample (not a random or pre-specified one) that may in fact *be* the entire
  scientifically load-bearing gene set rather than a preview of it. Calling it a "pilot" implies a scalable
  methodology it cannot support.
- **(b) tip-label audit** — survives, with a name correction: it is a **mismatch list**, not a
  **reconciliation** — exact-string matching detects mismatches (synonymized taxon names, subspecies-level
  tags) but does not resolve which label is correct. It also creates a hidden dependency: a high mismatch rate
  blocks (a) from being placed on the tree at all.
- **(c) citation-gap list** — survives only with explicit scope language. "Not supported by the 2 named
  papers" is honest; "no support found" silently overclaims a systematic literature review that never
  happened.
- **(d) package installs** — the one item that survives cleanly. Round 1's "1–2 days" estimate conflated
  install with downstream QC; install itself is a minutes-to-hours task.
- **(e) KEGG disambiguation** — does not survive as an independent line item. The HSD3B1/HSD3B2 paralog call
  it requires is the same judgment call as (a), not a corroborating second check — one wrong call corrupts
  both outputs with no independent cross-check between them.

No round-3 attack was needed: round 2 refined rather than overturned round 1's bottom line, satisfying the
stop condition.

---

## 3. Feasibility verdict by stage, under the 48-hour constraint

| Stage | Deliverable in 48h? | What ships, if anything | Quality bar |
|---|---|---|---|
| **A — coupling layer** | **Partially, as a labeled skeleton only.** | KEGG hsa00140 + AR/ESR1/ESR2 imported (mechanical); a citation-gap list against the 2 named mechanism papers (not a filled bridge-edge table); most candidate receptor→melanogenic-gene edges ship as "not supported by the 2 named papers, excluded," not as cited edges. | Preliminary/proof-of-concept **only** — must be labeled as an incomplete skeleton with an explicit gap list, never as "the coupling layer is built." |
| **B — conditional prediction** | **No.** | Nothing defensible — Stage B's perturbation math runs on Stage A's graph, and Stage A's KEGG generic-node paralog problem (HSD3B1/HSD3B2 and likely others) produces silently wrong, not just approximate, sign predictions if the graph is used as-is. | Do not run in 48h; running it produces a result that looks clean and is not. |
| **C — orthology resolution (hard gate)** | **No, as a gate.** A bounded audit is possible but is not a gate. | At most: a single-annotator orthology table over a hand-picked gene subset (CYP/HSD + 3 receptors), explicitly labeled non-representative and unreplicated — not a pilot, not evidence about the wider gene universe. | Cannot be shipped as "the gate is passed" or "the hazard is characterized" — only as a disclosed, narrow, unchecked data point. |
| **D — phylogenetic test** | **No.** | Nothing. The dependent variable (standardized dichromatism score) does not exist; building it defensibly is a multi-week task by the plan's own admission ("its own curation task"). No dated-tree source is identified, no PGLS/phylo-logistic tooling is installed or validated against this dataset's tree format, and any single-tree analysis skips propagating phylogenetic uncertainty across the underlying posterior tree distribution (e.g., 10kTrees-style sources deliver a distribution, not one tree). | Do not attempt; there is no honest partial version of a PGLS result. |

**Net for the full A→D plan in 48h: not deliverable at any defensible standard.** The largest defensible
sub-deliverable is a clearly labeled **Stage-A preliminary skeleton** — an imported hormone-pathway layer, an
honestly-scoped citation-gap list, and an explicit "not yet resolved" list for orthology and phenotype — shown
to a collaborator with the caveat spelled out in the box below, never presented as a step toward a result.

> **Caveat that must travel with the 48h deliverable, verbatim in spirit:** none of this is evidence toward
> the paper's evolutionary or causal claim. It is QC and disclosure material describing what has not yet been
> checked, produced by one rater under deadline pressure on a convenience sample that may be the entire
> scientifically load-bearing gene set, with zero reliability, coverage, or independence guarantees. Every
> number and label in it is provisional pending a second annotator, a properly sampled or complete gene set,
> and resolution of tip-label mismatches — none of which happens before any downstream analysis touches the
> tree.

### Wall-clock cost table for the tasks the plan treats as routine

| Task | Plan's implicit budget | Realistic wall-clock, done properly | 48h-scale corner-cut and its failure mode |
|---|---|---|---|
| Per-edge-cited bridge table (~30–60 candidate receptor→gene edges) | Implied: hours (2 papers) | 10–40 hours (20–40 min/edge to find, read, and confirm a primary source specifically supports that gene pair and its sign) | Cite the 2 anchor papers on every edge regardless of specific support → citation padding, fails on inspection |
| Standardized cross-primate dichromatism phenotype | Implied: a data-lookup ("anchor datasets exist") | 3–6 weeks for ~30–40 species (reconciling facial-colour and pelage measures from different papers/clades into one validated scale) | Hand-blend the 2 anchor papers' incompatible measures into one ad hoc score → no construct validity, no error structure, not a result |
| CYP/HSD (+ full pathway + backbone) orthology resolution across the Stage-D species set | Implied: a database call (Compara) | 20–40+ hours for genuine gene-tree-level adjudication of paralog-prone families at real species breadth, per this session's own live sample | Accept Compara's automated 1:1 flag at face value outside a hand-picked subset → silently reintroduces exactly the "blanket problem" the plan says it is avoiding |
| MSA/dN/dS/PGLS tooling stand-up + validation | Implied: "routine conda/bioconda" | Install: minutes–hours (genuinely routine). Validation against this dataset (tip-label audit, tree-format checks, posterior-sensitivity) adds a further 1–2 days | Skip validation, run PGLS on the first tree/label set that loads → mismatch- or artifact-driven p-values indistinguishable from a real signal |

---

## 4. Findings not subsumed by the deadline (ranked, for the record)

These stand regardless of timeline and should survive into any future full-scope version of this plan.

1. **[High / load-bearing] Bridge-edge sourcing burden vs. project's own edge rule.** The project's locked
   decision 5 (OmniPath + curated literature only, association sources barred) is the single hardest rule the
   bridge-edge table must clear, and it is the part of the whole coupling layer with the least existing
   coverage (§2, live OmniPath check: 0/344). **Resolution:** treat coverage gaps as first-class output (a
   named "unconnectable, no mechanism found" list), not a temporary curation backlog, mirroring how the
   existing NB4-sketch already handles unconnectable case genes (MFSD12/DDB1/TMEM138).
2. **[High / load-bearing] Multiplicative confidence framing has no statistical grounding.** Presented as an
   insight in §4, it converts three uncalibrated inputs into one number that reads as more rigorous than any
   input alone. **Resolution:** report the three factors as separate qualitative flags (pass/fail/ambiguous
   for orthology, supported/unsupported per edge for coupling, "not computed" for phylogenetic power) rather
   than a single scalar, at least until a real calibration exercise exists.
3. **[Medium / partially load-bearing] The Ríos-2016-demoted-to-context reconciliation is argued and decided
   in the same paragraph it asks the PI to confirm.** Not necessarily wrong — the mechanistic case for
   steroidogenesis+AR/ER over gonadal fate as the pigment-touching layer is defensible — but the plan pre-loads
   its own answer to §6-A. **Resolution:** separate the argument from the question, or accept that §6-A is
   functionally rhetorical as written.
4. **[Medium] Standardized dichromatism phenotype is described as tractable curation but is closer to an open
   comparative-biology research question.** A literature scan located active, separate lines of work on
   primate coloration and facial/pelage colour-pattern evolution (e.g., studies of Neotropical primate facial
   colour patterns and of primate coloration/colour-vision more broadly), but turned up no single existing
   cross-order standardized dichromatism metric — consistent with the plan's own characterization of this as
   "its own curation task," not a lookup. Any single cross-order score still has to solve a construct-validity
   problem (facial vs. pelage vs. skin measures are not interchangeable) before Stage D's statistics can run.
   **Resolution:** treat phenotype curation as its own pre-registered sub-project with its own timeline, not a
   Stage-D input task.
5. **[Medium] Anti-leakage / causal-gene-first rules are not explicitly re-derived for the comparative-genomics
   context.** The project's standing rule (connect the resolved causal gene, never the association marker) was
   built for human GWAS-marker resolution; the plan does not state whether an analogous rule applies to
   orthology calls (e.g., is a paralog-family "1:1 by Compara" call itself association-like evidence needing
   the same causal-gene discipline as an L2G score?). This is the cross-species analog of the open Q11 already
   on the project's own downstream-chain question list (does L2G cross the anti-leakage boundary?), unasked
   here. **Resolution:** decide explicitly whether comparative-genomics inference (Compara orthology calls,
   evo2/borzoi cross-species scoring) counts as "the network" for anti-leakage purposes, the same way the
   existing TODO §5a Q7 asks for L2G.
6. **[Low, but a concrete factual error worth a direct fix] The plan's own citation for the demoted backbone
   candidate is wrong.** §2 cites "Ríos et al. 2016, doi:10.1186/s12918-016-0282-3" for the gonadal
   sex-determination logical model. That DOI resolves to a different paper — Sánchez & Chaouiya (2016),
   "Primary sex determination of placental mammals," *BMC Systems Biology* 10:509. The paper the plan actually
   describes (Ríos, Frías, Rodríguez, Kofman, Merchant, Torres & Mendoza, "A Boolean network model of human
   gonadal sex determination") was published in 2015 in *Theoretical Biology and Medical Modelling* 12:26,
   DOI `10.1186/s12976-015-0023-0` — wrong year, wrong journal, wrong DOI as currently written. **Resolution:**
   a one-line fix in §2; flagged separately from the deliverability findings because it is unrelated to the
   48-hour question but should not ship uncorrected in any promoted version of the plan.
7. **[Low] Capability inventory (§3 of the plan) is accurate but optimistic in framing.** Verified live this
   session: `mcp-genomes` `ensembl_homology` works and returns real ortholog-type calls (tested on
   CYP17A1/CYP19A1/HSD3B2/HSD17B3/TYR/MITF); OmniPath and KEGG REST are directly reachable (already used in
   NB2). Correctly flagged as NOT curated skills: PGLS/phylo-logistic, dN/dS, MSA/tree-building — no skill for
   any of these was found in this session's catalog search, confirming the plan's own "installable, not
   curated" claim. **Not separately flagged by the plan but worth noting:** TOGA/Zoonomia/primate-constraint
   datasets are listed as "Available (data)" but are large published resources requiring bulk
   download/parsing, not queryable APIs — closer to a data-acquisition task than the one-line "available" the
   table implies.

---

## 5. Consolidated question set for the PI

**On deliverability (new — not in the plan's own §6):**

1. Given the findings above, do you want the 48-hour deliverable to be the labeled Stage-A skeleton described
   in §3, or would you rather spend the 48 hours differently (e.g., on the NB4–NB8 chain instead, which is
   also unauthorized but has a completed substrate to work from)?
2. If the skeleton ships, who signs off that the caveat language in §3's box actually accompanies it wherever
   it's shown — you, or does that need to be built into the artifact itself?

**On the plan's own §6 (A–F), largely unaffected by the deadline but worth re-asking in light of the findings above:**

3. §6-A (backbone confirmation): given finding #3 above, do you want to confirm the reconciliation as argued,
   or should the Ríos-2016-vs-steroidogenesis choice be re-opened as a genuinely open question rather than one
   the plan has pre-answered?
4. §6-B (dichromatism phenotype): given finding #4, is a standardized cross-primate score meant to be built as
   part of this expansion, or should Stage D be scoped down to whichever single anchor dataset (facial-colour
   OR Colobinae-pelage) already has usable species coverage, accepting a narrower taxonomic claim?
5. §6-C (primate scope): does narrowing scope to reduce the orthology burden (§4, finding on Stage C) change
   your answer to primate scope, given that broader scope was already flagged as worsening ortholog
   completeness?
6. §6-D (coupling-edge sourcing): given the live OmniPath null result, do you want the literature-curated-only
   answer explicitly changed to "literature-curated with an honest, named coverage-gap list," rather than
   implying a complete bridge table is achievable?
7. §6-E (molecular-evolution depth): given the tooling/validation cost table in §3, do you want dN/dS scoped
   out of this expansion entirely for now, reducing it to orthology + presence/absence only?
8. §6-F (sequencing vs. current build): does the 48-hour deadline change your answer here — specifically,
   should this expansion wait until the NB4–NB8 chain's own TODO #0 is resolved, given that both are
   unauthorized and the substrate the expansion couples to (NB1/NB2) is the only piece that is actually
   settled?
9. **New question the critique surfaces that §6 doesn't ask:** should comparative-genomics inference
   (Ensembl Compara orthology calls, evo2/borzoi cross-species scoring) be held to the same anti-leakage
   discipline as L2G in the downstream human chain (finding #5), and if so, who decides that before Stage C
   is scoped?

---

*No repository commit is made from this document; any commit goes through the compliance gate. This report
critiques the plan; it does not rewrite it.*
