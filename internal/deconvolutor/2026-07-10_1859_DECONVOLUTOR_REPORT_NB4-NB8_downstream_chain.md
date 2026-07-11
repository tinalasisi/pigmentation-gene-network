# Plan Deconvolutor report — NB4–NB8 downstream analysis chain

**Subject:** `project_dashboard.md` §4 (notebook map, "causality-gated spine") + §5a (open decisions for
TODO #0) — the proposed `NB3 cases → NB4 manifest+causal resolution → NB5 causality-gated connection → NB6
metrics → NB7 figure → NB8 validation` chain (TENTATIVE, unauthorized, gated on TODO #0, §5a's own 11
load-bearing gaps unresolved).
**Trigger for this report:** PI-imposed hard 48-hour deadline, evaluated alongside a second unauthorized
track (sex-hormone × pigmentation expansion) already critiqued — see the comparison in §4 below.
**Status of this document:** pre-approval critique only. No plan edits, no build action, no commit.

---

## Headline verdict

**No notebook in NB4–NB8 ships a scientific result in 48 hours.** Unlike the expansion plan, this chain
starts from a genuinely completed substrate — NB1/NB2 (168 gene nodes / 309 edge rows, OmniPath-validated)
and a 694-record, 13-paper validation-case dataset are real, on disk, and citation-gated. The gap here is not
missing data; it is that the chain's own gating step (NB4's causal-gene resolution) has no decision rule to
execute, and live checks this session show the mechanistic edge source the whole spine depends on
(OmniPath + curated literature) returns almost nothing for the genes that matter most:

- **HERC2 — the chain's own headline illustration — has zero melanogenesis-relevant OmniPath edges.** A live
  pull of all 145 OmniPath interactions touching HERC2 found every one of them in DNA-damage/ubiquitin-ligase
  contexts (ATM, ATR, RNF8, RNF168, PRKDC, a wall of UBE2\* conjugases) and not one touching MITF, TYR, TYRP1,
  OCA2, PAX3, MC1R, or SOX10. §4's own text uses HERC2→OCA2 (rs12913832) as the worked example of causal-gene
  resolution "established biology" — but the OmniPath edge the chain would need to draw *from* HERC2 into the
  melanogenesis backbone does not exist in OmniPath. The connection would have to come entirely from curated
  literature, which is exactly the half of the edge-admission rule §5a gap #3 says has no evidentiary bar.
- **OCA2 itself has only 6 OmniPath edges, all incoming (transcriptional regulators — MITF, MYC, LEF1, HLTF,
  E2F1 — plus HERC2→OCA2 sourced from a single non-referenced dataset, "Wang").** Under the default `omnipath`
  dataset, the 8 non-HERC2 NB5 candidates return between 0 and 9 edges each (SLC24A5 0, SLC24A4 0, MFSD12 0,
  TMEM138 0, SLC45A2 1, IRF4 3, DDB1 6, ASIP 9); broadening to
  `pathwayextra/kinaseextra/ligrecextra/dorothea/tf_target/tf_mirna/mirnatarget/lncrna_mrna` raises SLC24A5
  to 1 edge but leaves MFSD12 and TMEM138 at 0 under every combination tried. Of the nine named NB5 candidate
  genes (SLC45A2, SLC24A5, SLC24A4, IRF4, ASIP, MFSD12, DDB1, TMEM138, HERC2), none is already in the
  168-gene NB2 network, and none connects directly to another candidate or to a known melanogenesis hub in
  OmniPath. NB5 is not a connection step with occasional literature backstops; on the live evidence, it is a
  curated-literature construction project with OmniPath contributing little and, for at least two candidates
  (MFSD12, TMEM138), nothing at all.
- **ClinVar is live and returns real, current pathogenicity calls** (confirmed: an OCA2 missense query
  returned a "Likely pathogenic" classification with OMIM/Orphanet/MONDO cross-refs, gold-star review
  status, and a 2025-11-24 evaluation date) — so NB4's ClinVar half is not blocked by connectivity. Complex
  Portal, by contrast, hung for 60s and errored on a live query and could not be confirmed reachable this
  session; §5a's flagged STRING+Reactome fallback for NB5's structural layer should be treated as the
  operative path, not a backup. Open Targets L2G calls returned "Rate limit exceeded" on every attempt this
  session (5 retries with backoff) — its reachability could not be verified live, which matters directly for
  §5a gap #11 (does L2G cross the anti-leakage boundary) since the gap can't even be tested against real L2G
  output right now.

**The only defensible 48-hour deliverable is a formalized NB3 (Option A from §5a) plus, if time allows, a
non-causal-gated NB4 gene-manifest table** — a join of the case genes against the existing 168-gene network
by string match, tagged `already-in-network` / `absent`, with NO causal-gene resolution and NO new edges
drawn. That is disclosure material (which case genes are and aren't already covered), not a finding. See §3.

---

## 1. Streamlined plan (cold read, no session context)

Stripped of hedging, §4 and §5a commit to:

1. Build NB4: enumerate every (case, gene, anchor-genotype) from the 694-record case set, join to the 168-gene
   network, tag connectivity status, run a three-way causal-gene resolution (nearest-gene / Open Targets L2G /
   ClinVar-OMIM) with a tie-break rule to be written, and attach four evidence tags (HIrisPlex, Bajpai CRISPR,
   GWAS replication count, Baxter).
2. Build NB5: connect each resolved-causal, absent case-gene into the network using only OmniPath + curated
   literature edges, with a literature evidentiary bar to be written, sorting genes into "routes through an
   existing node," "gets new mechanistic edges," or "unconnectable."
3. Build NB6: unify NB2 + NB5 into one graph, recompute signed-path (D1) and alternative-reachability (D2)
   metrics per pigment endpoint, and add a degree-preserving null model for D2 with sign/type-preservation and
   filter-ordering questions still open.
4. Build NB7: a two-panel-per-locus (TYR, OCA2) payoff figure combining D1/D2 outputs with an optional,
   not-yet-formalized disease-bridge annotation.
5. Build NB8: score each of the 13 cases pass/fail/unreachable against a mechanism pre-registered from its
   own paper before the network is consulted, with the case's own NB5 edge and its NB8 validation potentially
   drawn from the same paper.
6. Ask the PI 11 decision-log questions (§5a) covering scope, tie-break, evidentiary bar, anti-leakage, null
   model, and figure/validation merger, gated by three named options (A/B/C).

**What an outsider would flag immediately, with no other context:**

- The chain is presented as one pipeline with a single gate (TODO #0), but it actually bundles three
  independent research decisions — a causal-gene resolution methodology (NB4), a network-construction policy
  (NB5), and a null-model statistics choice (NB6) — each of which could stall the whole sequence on its own.
  Approving "the chain" is not one decision; §5a's own three-option menu (A/B/C) already implicitly
  acknowledges this by letting Option A ship without touching NB4-NB8 at all.
- NB7 and NB8 are flagged in §4 itself (and §5a gap #8) as consuming *identical* D1/D2 outputs and differing
  only in output format, yet are kept as two separate notebooks. A plain reader would ask why a payoff figure
  and a validation table aren't one notebook with two rendering targets, before asking anything about
  causal-gene resolution.
- The causal-gene resolution step (NB4) is described with a fully worked example (HERC2/OCA2, with L2G scores
  to three decimal places: 0.428 vs 0.203) immediately followed by "none of these gene-level outcomes are
  computed." A reader with no other context would ask whether that L2G score was actually queried live this
  session or is a remembered/illustrative number — see §2 below; live Open Targets access could not be
  confirmed this session, so that number's provenance is now a real, not rhetorical, question.
- §5a lists 11 gaps and immediately follows them with a "balancing note" asserting the methodological core is
  sound and the gaps are "about specification and audit trail, not the underlying scientific logic." That
  reassurance sits inside the same section that is supposed to be presenting the gaps neutrally for a PI
  decision — a cold reader would flag this as the document arguing for Option B before the PI has chosen
  between A/B/C, the same pattern this critic's sibling report found in the expansion plan's §2.
- The plan proposes a specific split ("something like a 9-connected / 10-absent split") for a case-gene
  connectivity count that, on this session's direct check against the actual 168-gene node list, does not
  hold: of the 9 case-relevant genes actually named across §4 as connection candidates, all 9 are absent
  from the network, and only 4 of the recurring case-record gene symbols (MC1R, MITF, OCA2, PAX3 among the
  non-NB5-candidate set) are present. A number this specific, sitting next to "to be recomputed if built,"
  invites treating an illustrative guess as a preview of the true count.

None of this is disqualifying — a forward design document is allowed to look like this before a PI has
signed off. What changes under a 48-hour clock is covered next.

---

## 2. Adversarial stress-test

Sub-agent delegation was unavailable in this session (this frame runs as a leaf under the root orchestrator,
which reserves delegation). The stress test below was run as reasoning rounds directly, grounded in the live
connectivity checks recorded in the headline verdict and repeated where relevant. Two rounds are given; a
third surfaced no attack not already covered by round 2's refinements, so the stop condition was met.

### Round 1 — attacks on the chain's core assumptions

1. **Causality-gating is not well-posed at all without the tie-break rule (§5a gap #2), and the live check
   shows this bites on the chain's own headline example, not an edge case.** HERC2/OCA2 is presented as
   settled biology, but nearest-gene, L2G, and ClinVar/OMIM genuinely disagree here (nearest-gene says HERC2,
   causal biology says OCA2) — the chain cannot resolve a single one of its worked examples without a rule
   that does not exist yet. A tie-break rule written under 48-hour pressure, without adjudicating it against
   even a handful of the other ~8 candidate loci, is a rule that has been tested on n=1 (the case the design
   doc already knows the answer to) and is unvalidated everywhere else.
2. **The NB4/NB8 circularity (§5a gap #1) is not a specification gap — it's a validity threat that gets worse,
   not better, the faster NB5 is built.** Under deadline pressure, the fastest way to give a case-gene a
   mechanistic edge is to mine the same paper already used to classify that case as D1/D2 in NB3. A rushed
   NB5 is *more* likely to reuse NB3's source paper for its own edge, not less — meaning speed and the
   circularity risk move in the same direction, and there's no time-pressure-compatible way to defend against
   it except tracking (which §5a gap #1 says doesn't exist yet).
3. **The D2 degree-preserving null is not obviously meaningful at this network's actual scale and degree
   distribution.** A direct check of the current 168-node/309-edge network's degree sequence found a max
   degree of 26 (NFKB1) against a median of 3, with 140 of 168 nodes carrying any edge at all. Degree-preserving
   rewiring on a sequence this skewed, at n≈140-200, is known to produce noisy or artifact-prone empirical
   nulls — exactly the concern §5a's own "feasibility flags" note raises, but stated here against this
   project's actual numbers rather than a generic caveat.
4. **The evidentiary bar for "curated literature" (§5a gap #3) cannot be written and applied consistently to
   nine candidate genes in the time available.** Each candidate (SLC45A2, SLC24A5, SLC24A4, IRF4, ASIP,
   MFSD12, DDB1, TMEM138) needs its own literature search, because live OmniPath checks confirm none of them
   is pre-connected — this is the same 20-40-minutes-per-edge sourcing cost the sibling expansion critique
   found for its bridge-edge table, and it recurs here for the same structural reason: the mechanistic-only
   edge rule (locked decision 5) is strict, and neither chain's target genes are well covered by OmniPath.
5. **NB6's metrics and NB7's figure are contingent on NB5 producing a graph that has causal genes connected at
   all** — if NB5 mostly returns "unconnectable" (a live possibility given the connectivity numbers above),
   NB6 has nothing new to recompute beyond NB2's existing D1/D2 baseline, and NB7's payoff figure has no new
   content to show for TYR/OCA2 beyond what NB2 already supports. The chain's value proposition rests on NB5
   succeeding at connecting genes that the live evidence suggests may mostly fail to connect.
6. **Open Targets L2G reachability is currently unverified**, which is a direct blocker for testing whether
   §5a gap #11 (does L2G cross the anti-leakage boundary) can even be resolved this cycle — a decision about
   L2G's epistemic status can't be tested against real L2G output if the connector can't be reached.

### Defense round — what might survive

- **(a) NB4 manifest without causal resolution** — a join of case genes against the existing network by
  string match (already-in-network vs. absent), no tie-break, no new edges. This does not require attacks
  1, 2, or 4 to be resolved because it draws no causal or mechanistic conclusion; it's inventory, not
  analysis.
- **(b) An honest "no OmniPath edge found" coverage table for the 9 NB5 candidate genes** — mirrors the
  expansion plan's surviving "citation-gap list" item; reports what's absent rather than filling gaps with
  unaudited literature.
- **(c) A written (not yet validated) tie-break rule as prose, applied to zero cases** — a decision-log
  artifact, not an analysis output.

### Round 2 — attacking the three survivors

- **(a) NB4 manifest** — survives, with a caveat: string-matching case-gene symbols against network node
  symbols will silently miss genes present under a different identifier (e.g., a network node keyed by
  Entrez ID or a synonym) unless the join is done through the same MyGene/HGNC resolution NB2 used, not a
  bare string match. Doing the join *without* that resolution discipline reintroduces exactly the
  "hand-typed classification" problem locked decision 6 exists to prevent. Correctly scoped, it survives.
- **(b) Coverage table** — survives cleanly, same reasoning as the expansion critique's analogous item: it is
  disclosure, and this session's own live pulls already are that table's raw material.
- **(c) Written tie-break rule, unvalidated** — does not survive as an independent deliverable. A rule
  written and applied to zero real disagreements is unfalsifiable in the time available; at minimum it needs
  to be run against the HERC2/OCA2 case (the one disagreement already known) before being called a rule
  rather than a proposal. Folded into (a) as an annotation on the manifest, it survives; standing alone as
  "TODO #0 resolved," it does not.

No round-3 attack surfaced anything not already covered by round 2's refinements — the stop condition is met.

---

## 3. Feasibility verdict by notebook, under the 48-hour constraint

| Notebook | Deliverable in 48h? | What ships, if anything | Quality bar |
|---|---|---|---|
| **NB4 — manifest + evidence + causal resolution** | **Manifest only, no causal resolution.** | A case-gene × network join (via MyGene/HGNC resolution, not string match) tagging each case gene `already-in-network` / `absent`; an honest connectivity coverage table. No tie-break rule applied to real disagreements; no causal-gene call made. | Inventory/disclosure only — must not be labeled "causal-gene resolution" or "resolved to causal genes," since none is. |
| **NB5 — causality-gated connection** | **No.** | Nothing defensible. Live OmniPath checks show 0-9 edges for the 8 non-HERC2 candidate genes (SLC24A5/SLC24A4/MFSD12/TMEM138 at 0, ASIP highest at 9), none connecting two candidates directly; any new edge would need same-day literature curation with no evidentiary bar defined (§5a gap #3), which is the same 20-40-min/edge sourcing cost the sibling expansion critique found prohibitive at this scale. | Do not build. A rushed version either draws unaudited literature edges (fails locked decision 6) or returns "mostly unconnectable" with no time left to distinguish "not yet curated" (MFSD12) from "no mechanism" (TMEM138, DDB1) — the distinction §4 itself already flags as needing care. |
| **NB6 — unify + recompute metrics** | **No.** | Nothing — NB6 operates on NB5's output graph, which does not exist in any defensible form in 48h. Even if attempted on NB2 alone, the null-model spec gaps (§5a gap #5) and the skewed degree distribution (max 26 / median 3 at n=140-168, confirmed this session) mean any null-model result ships with unresolved sign/type-preservation and ordering questions baked in. | Do not attempt. |
| **NB7 — payoff figure** | **No.** | Nothing new. Contingent on NB6, which is not deliverable; a figure drawn from NB2 alone would not be the "payoff" the design describes and risks being presented as more than it is. | Do not attempt. |
| **NB8 — case validation** | **No.** | Nothing. Contingent on NB5's edges existing to test against, and the anti-circularity bookkeeping (§5a gap #1) is unaddressed — testing a case's mechanism against a network whose only edge for that gene may come from the same paper is not a validation, it's a paraphrase check. | Do not attempt. |

**Net for the full NB4–NB8 chain in 48h: not deliverable at any defensible standard beyond a manifest.** The
largest defensible sub-deliverable is a **formalized NB3 (§5a Option A) plus an NB4-manifest-without-resolution**
— an inventory of which case genes are already network-connected, which are absent, and an honest
"no-OmniPath-edge-found" list for the absent ones — never presented as causal resolution, network connection,
or a step toward the D1/D2 payoff finding.

> **Caveat that must travel with the 48h deliverable, verbatim in spirit:** this is an inventory of what is
> and is not yet connected, not a resolution of causal genes and not a network extension. No tie-break rule
> has been tested against a real disagreement (including the chain's own HERC2/OCA2 example), no literature
> evidentiary bar has been written, and no new edge has been drawn or defended. Every "absent" tag is
> provisional pending correct MyGene/HGNC-based identifier resolution, not a bare string match.

### Wall-clock cost table for the tasks the chain treats as routine

| Task | §4/§5a's implicit budget | Realistic wall-clock, done properly | 48h-scale corner-cut and its failure mode |
|---|---|---|---|
| Causal-gene tie-break rule, adjudicated across the ~9 candidate loci where nearest-gene/L2G/ClinVar might disagree | Implied: a rule to write once (§5a gap #2) | 4-8 hours to write a defensible rule *and* apply it to even the known disagreement (HERC2/OCA2) plus the other 8 candidates, given Open Targets L2G was unreachable this session (rate-limited) and needs re-verification before it can be queried at all | Write the rule but apply it to zero real cases → an untested policy presented as a resolved decision |
| Curated-literature edge admission for 9 candidate genes, no pre-existing OmniPath coverage for most | Implied: hours, since OmniPath does "most of the work" | 20-40 min/edge × an unknown but likely double-digit count of candidate edges (this session found 0-9 OmniPath edges per gene, none candidate-to-candidate) = 6-15+ hours minimum, before any evidentiary-bar dispute is resolved | Admit literature edges without a stated PMID/evidence-code bar → fails locked decision 6 on inspection |
| Degree-preserving D2 null model on the current 140-168-node, max-degree-26 graph, sign/type-aware | Implied: a standard network-science step (§4 item 6) | 1-2 days to design and validate a sign-and-type-preserving rewiring scheme at this scale and degree skew, plus resolve the pre/post-D1-filter ordering question (§5a gap #5) | Run naive degree-preserving swaps → introduces sign-degree artifacts the project's own feasibility flags note already warns about |
| NB4/NB8 anti-circularity bookkeeping (tracking whether a case's NB5 edge and its NB8 validation share a source paper) | Implied: a design question to answer, not a system to build (§5a gap #1) | 3-6 hours to build even a minimal paper-ID cross-reference across the 13 EXTRACT_* files and whatever NB5 edges get drawn, and it only becomes meaningful once NB5 has actually drawn edges | Skip tracking under time pressure (the likely outcome) → NB8 "passes" become circularity-confirming, not independence-confirming, with no flag saying so |

---

## 4. Comparison to the expansion plan's 48h floor

Both unauthorized tracks land at the same headline verdict — nothing scientific ships in 48 hours — but for
different structural reasons, and the honest floor differs in kind, not just degree. The expansion plan's
floor is a **labeled Stage-A skeleton**: a mechanically imported pathway layer (KEGG hsa00140 + AR/ESR1/ESR2)
plus a citation-gap list against two named papers, where the blocking constraint is that the plan's own
downstream stages (a cross-primate dichromatism phenotype, full-pathway orthology resolution, phylogenetic
statistics) are multi-week research problems the plan understates as data lookups. This chain's floor is an
**NB4 manifest without causal resolution** — an inventory join against a network that already exists, where
the blocking constraint is not a missing multi-week research program but a single unwritten decision rule
(the causal-gene tie-break) that the chain cannot even test against its own worked example without querying a
connector (Open Targets) that could not be confirmed reachable this session. In other words: the expansion
plan is blocked by scale (the honest version of its hardest steps takes weeks, not days, regardless of who
resolves the open questions first); this chain is blocked by a decision the PI has not made yet and a live
mechanistic-edge source (OmniPath) that this session confirmed does not cover the genes the design's own
illustrations depend on. If the PI can only unblock one track's floor before the deadline, the NB4-manifest
floor requires resolving fewer open unknowns (a join methodology, not a phenotype-construction research
program) — but it is also the smaller deliverable of the two: an inventory table versus an installed
toolchain plus a mismatch-list plus a bounded orthology audit. Neither floor is a scientific result; the
choice between them is a choice about which kind of disclosure material is more useful to show a collaborator
on day 2.

---

## 5. Consolidated question set for the PI

**On deliverability (new — beyond §5a's 11 gaps and 11 decision-log questions):**

1. Given the findings above, do you want the 48-hour deliverable to be the NB4-manifest-without-resolution
   floor described in §3, the expansion plan's Stage-A skeleton (see the sibling critique), both in parallel,
   or neither — spending the 48 hours on housekeeping (§5a Option C) instead?
2. HERC2's OmniPath edges are entirely DNA-damage/ubiquitin-pathway, not melanogenesis-pathway (confirmed live
   this session, 145/145 edges). Does this change how you want the HERC2/OCA2 worked example used in §4 — as
   a resolved illustration, or as an open case that itself needs the tie-break rule applied first?
3. Open Targets L2G could not be reached this session (rate-limited on every attempt). Before NB4 is scoped
   around L2G as one of its three resolution inputs, do you want its reachability and typical response
   content re-verified, or should NB4's resolution logic be designed to degrade gracefully (nearest-gene +
   ClinVar only) if L2G access remains unreliable?
4. Complex Portal / CORUM (flagged not-attached in TODO §5 item #3) also failed to respond within 60s on a
   live query this session. Do you want to commit now to the STRING+Reactome fallback for NB5's structural
   layer as the actual plan, rather than as a contingency, given this session's evidence that the primary
   path may not be operational regardless of connector-attachment status?

**On §5a's own 11 gaps, re-asked in light of the live findings above:**

5. (§5a gap #2) Given that the chain's own worked example (HERC2/OCA2) is a real, not hypothetical,
   resolver disagreement, do you want the tie-break rule drafted and tested against this one case before
   NB4 is scoped further, rather than left as prose to write "if built"?
6. (§5a gap #3) Given the live connectivity numbers (0-9 OmniPath edges per NB5 candidate gene, none
   candidate-to-candidate), do you want the literature evidentiary bar set now, before any curation time is
   spent, since the bar will determine whether NB5 is mostly "connected" or mostly "unconnectable, no bar
   met"?
7. (§5a gap #1) Should NB4/NB8 anti-circularity tracking be built as a lightweight prerequisite check (paper
   ID present on both a case's classification and its candidate mechanistic edge) before any NB5 edges are
   drawn, rather than as a retrospective audit after NB8 produces pass/fail results?
8. (§5a gap #5) Should the D2 null model preserve edge sign and type from the start, given this session's
   confirmation that the current graph's degree distribution (max 26, median 3, n=140 non-isolated of 168) is
   exactly the skew the project's own feasibility flags note warns produces noisy naive-swap results?
9. (§5a gap #8, NB7/NB8 duplication) Given both notebooks are confirmed to consume identical D1/D2 outputs,
   should they be merged now, before either is built, rather than kept separate and risking drift?
10. (§5a gap #11, L2G anti-leakage) Now that L2G's live reachability is unconfirmed, do you want this
    question deferred until reachability is verified, or resolved on principle now (independent of whether
    the connector responds) so NB4's design isn't blocked on it later?

**A question §5a does not ask:**

11. NB4's proposed evidence-tag set (HIrisPlex, Bajpai CRISPR, GWAS replication count, Baxter) has no stated
    combination rule when tags disagree on a gene (§5a gap #10 names this gap but doesn't ask what should
    happen). Given the case-gene manifest (item 1 above) is the one NB4 sub-piece that might ship in 48h,
    do you want the evidence tags attached to that manifest at all in this pass, or deferred until the
    combination rule exists — attaching them without a combination rule risks the same "looks more resolved
    than it is" problem §4's own scope-disclosure gap (#9) was reworded to avoid?

---

*No repository commit is made from this document; any commit goes through the compliance gate. This report
critiques the plan; it does not rewrite it.*
