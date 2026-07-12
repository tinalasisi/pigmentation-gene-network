# SciComm / claim-honesty review — flagship narrative (hackathon submission)

**Scope.** `internal/PITCH.md`, `internal/START_HERE.md`, and the TL;DR headers of NB4–NB12, checked
against the underlying processed data, STRING/frozen-DB pulls, and CHANGELOG/TODO history. Audience for
this review: the narrative as it will be read by a hackathon judge/reviewer on the Researcher Track, who
has the repo and notebooks available but is reading PITCH.md and the notebook TL;DRs as the entry point.
**This review does not touch analysis logic or re-run any pipeline; it checks defensibility, framing, and
currency of what is already written.**

**Bottom line up front: the narrative is close to submission-honest, and unusually so for a project this
size — the self-correction discipline (the 2026-07-12T16:14Z softening of the direction-law framing, the
validity audit, the citation-completeness gates) is real and visible in the text. Two things still need
fixing before a reviewer reads this cold: (1) one specific number in PITCH's "second thread" is materially
wrong and needs a one-line correction or removal, and (2) the four "positioning" citations at the end of
PITCH are explicitly flagged as unverified but still sit in the document that would ship. Neither is a
deep problem; both are quick.**

---

## Priority 1 — Fix before submission

### 1a. PITCH.md §"Second thread" — the "25 of 49" connectivity number does not match any data on disk

**Location:** `internal/PITCH.md`, lines ~72–80 (second thread, "corrected association-locus rescue").

**Claim as written:** *"With those candidates in the STRING seed (the seeding lesson applied again),
**25 of 49 connect to the melanogenesis core** via high-confidence paths — e.g. SPIRE2→MYO5A,
ATRN→ASIP (mahogany biology as a network edge), OPN4→FOS→MITF."*

**What I found.** The three example edges are real — I pulled the frozen STRING response
(`data/external/db_responses/string_union_plus_candidates_pull_v12.json`, committed in commit `f4f794d`)
and confirmed SPIRE2–MYO5A (score 0.963), ATRN–ASIP (0.83), and OPN4–FOS (0.71) all exist, and FOS–MITF
(0.92) closes the three-hop OPN4 path. But the **count** does not reconcile against any file in the repo:

- The candidate set (`data/processed/nb_effector_uncertain_target_set.csv`) has **51** distinct genes, not
  49 (PITCH's own text says "34 effector_uncertain + 7 ambiguous_near" two lines earlier, which is **41**,
  not 49 either — the denominator itself is stated two different ways nine words apart).
- Of those 51 candidates, only **28** appear in *any* edge in the frozen STRING pull at all (23 are fully
  isolated — no STRING edge of any kind, at any score, including MFSD12).
- Of those 51, only **5** (`AHCY`, `ATRN`, `EGFR`, `LRMDA`, `USP35`) have a **direct** edge to a canonical
  melanogenesis-core gene (TYR/TYRP1/DCT/OCA2/MC1R/MITF/SOX10/PAX3/KIT/EDNRB/EDN3/PMEL/MLANA/SLC45A2/
  SLC24A5/ASIP/POMC/MC2R/HERC2/BNC2/IRF4/KITLG) — the OPN4/SPIRE2 paths in PITCH's own examples are
  *multi-hop*, so "25 of 49 connect via high-confidence paths" is not being measured the same way as the
  literal edge count, and there is no committed table, script, or notebook that shows the ≤N-hop rule that
  would turn 28 (or some other number) into 25. I checked `git log --all -S "25 of 49"` and found the
  commit that introduced this figure (`f4f794d`) touches only the frozen STRING JSON and PITCH.md itself
  — **no notebook, script, or intermediate CSV computed this number; it exists only as prose.**
- This is exactly the failure mode NB9 disciplines against for the *first* seeding-lesson result (93/142,
  which *is* backed by `nb9_orphan_reconciliation.csv` with a re-runnable notebook) — the second thread
  never got the same treatment.

**Why this matters for claim-honesty.** This is the one place in the document where a number a reviewer
could plausibly try to check (git-blame the commit, open the JSON) does not reproduce from anything on
disk. Everywhere else in PITCH the "one number that matters" traces cleanly to a committed CSV or a
notebook's own printed output (verified for NB4, NB5, NB6, NB7, NB9, NB10, NB11 below in the Conclusion
Currency section) — this is the exception.

**Fix.** Either (a) build the missing notebook/script that defines the connectivity rule (edge threshold,
hop limit) and re-derive the number so it matches something reproducible, and fix the 41-vs-49 denominator
inconsistency in the same edit; or (b) since this thread is explicitly **not** part of the three-axis
honest position this review was scoped against (it's presented as a "second thread," secondary to NB4–NB9),
downgrade the wording to what *is* defensible from the frozen pull alone: e.g. *"28 of 51 non-canonical
candidates have at least one STRING association-tier edge (5 directly to a core gene); MFSD12 and 22 others
have no STRING edge at all under this seed."* That is a smaller, correctly-hedged claim, consistent with the
document's own "convergence is thin, report it as such" discipline used everywhere else.

**Severity: High** — this is a specific, checkable number in the pitch document itself, not a supporting
notebook; a judge who spot-checks one number is likely to try exactly this one, since it's presented as a
parallel to the well-documented NB9 seeding result.

### 1b. PITCH.md §Positioning — anchor citations flagged as unverified are still in the shipping document

**Location:** `internal/PITCH.md`, lines ~127–129 ("Positioning" section).

**Text as written:** *"Suggested anchor references (from the PI's final-day directive §9, **NOT yet
verified against the papers in this repo — confirm each citation before it goes in any public
deliverable**): Fagny & Austerlitz 2021; Daub 2013; signet / Gouy 2017; the network-propagation family."*

**What I found.** I searched `DATA_SOURCES.md` and `internal/lit_review/bibliography/` for these four
names — none appear anywhere else in the repo with a DOI, PMID, or full citation. The document's own
caveat is correct and the caveat itself is well-written, but PITCH.md is the document a judge reads first,
and it currently contains four author-year mentions with an explicit internal note that they are unverified
— exactly the kind of "referenced-but-uncited" defect this review's citation check is built to catch,
flagged by the document's own author before I could flag it.

**Fix.** Before submission, either resolve each of the four to a DOI/PMID (a five-minute CrossRef/PubMed
lookup) and cite them properly, or cut the "Positioning" paragraph from the public-facing pitch entirely —
the paragraph is not load-bearing for any of the three answers or the flagship claim, so cutting it costs
nothing and removes the one clearly-unverified citation set in the document. Do not ship the caveat itself
("NOT yet verified... confirm before it goes in any public deliverable") in a document that IS the public
deliverable — that sentence is a note-to-self that leaked into the artifact it warns about.

**Severity: Medium** — self-flagged and low-effort to fix, but as written this is currently in the document
being submitted.

---

## Priority 2 — Should fix, not blocking

### 2a. Internal artifact vocabulary and process history leak into PITCH.md and START_HERE.md

Both documents are explicitly framed as **internal working documents** ("Living document," "internal
project files, not the public site" is the convention elsewhere in this repo — see the `pigmentation-
governance-layout` convention), and the task brief treats them as the internal source the flagship
narrative is drawn from, not as public artifacts themselves. Held to the *internal* standard, most of the
process language below is appropriate and I am not asking for it to be stripped from PITCH/START_HERE.
**But** a hackathon judge is very likely to open these files directly — they are the natural first click
from README.md's "read this first" pointer — so I flag the handful of places where internal process
language would mislead or distract a judge who does exactly that, and recommend a short reviewer-facing
excerpt rather than a full rewrite of the internal docs:

- **PITCH.md's own framing is honest about being unsettled** ("FRAMING IS UP IN THE AIR," "a primate-
  phylogenetics direction is also being explored") — this is accurate to the project state and I do not
  think it should be smoothed over; a reviewer benefits from knowing the PI has not locked a single
  headline. But a judge skimming for "what is the finding" will need to read past two large-font warning
  banners and three enumerated "candidate directions" before reaching the actual 22/22 result. **Fix:**
  add one lead sentence at the very top of PITCH.md's flagship section stating the single strongest,
  submission-ready claim in one line before the hedging — e.g. *"For this submission: the mechanism→
  direction law (22/22, p<1e-5) is the flagship result; three methodological findings (NB5/NB8-diag/NB9)
  are the supporting due-diligence backbone. Framing nuance follows below."* This does not remove any
  honesty — it just puts the answer before the caveats, the way an abstract precedes its limitations
  section.
- **START_HERE.md is explicitly written for a Claude Science / agent audience** ("If you are Claude
  Science... your job is to re-think the execution"), which is correct for its stated purpose (an
  onboarding doc for the next working session) but means a hackathon judge who follows README's pointer
  there is reading a document addressed to an AI collaborator, not to them. **Fix:** if START_HERE.md is
  likely to be a judge's second click (it is linked from README.md as "read this first"), add a one-line
  redirect near the top: *"Judges/reviewers: see `internal/PITCH.md` for the current pitch and
  `internal/FINDINGS_MEMO.md` for the ranked findings; this document is the project's internal working
  brief."* Two-line fix, does not require touching the rest of the document.

**Severity: Low-Medium** — not a claim-honesty problem, a navigability one; the honest content is all
there, a judge just has to work harder than necessary to find the headline.

### 2b. The four "honest ways to win" candidate framings in START_HERE (§"What a winning submission looks
like") pre-date the actual outcome and could read as inconsistent with PITCH's final position

START_HERE.md's "OPEN — decisions" section still lists candidate directions as live options, including a
"primate-phylogenetics" direction under "active exploration by the PI," dated the same day as PITCH's
"framing is up in the air" banner. This is consistent within the document (both say the same thing), but a
judge who reads START_HERE.md *after* PITCH.md may come away less confident the project settled on
anything, when in fact PITCH.md and FINDINGS_MEMO.md both name a clear pick (§"The pick," FINDINGS_MEMO.md)
for the *within-repo* candidates. **Fix:** in START_HERE.md's "current candidate directions" callout, add
one clause pointing to FINDINGS_MEMO.md's verdict: *"— see `internal/FINDINGS_MEMO.md` for this repo's own
ranking among candidates (1) and (2); (3) is being explored in a separate repo and is not part of this
submission."* This closes the one place a reviewer could reasonably ask "so which is it?" without an
answer in front of them.

**Severity: Low** — a clarity gap, not a contradiction; the underlying documents agree with each other.

---

## Priority 3 — Verified as correct (no action needed, recorded for completeness)

### 3a. Headline claims checked against source data

| Claim (PITCH.md / notebook TL;DR) | Checked against | Result |
|---|---|---|
| NB10: 22/22 recessive/X-linked genes concordant, base rate 54%, permutation p<1e-5 | `data/processed/nb10_direction_law_summary.csv`, notebook's own printed assertion output | **Matches.** Notebook's closing cell prints the identical numbers and a `0 uncited rows` citation gate pass. |
| NB12: 29/33 expanded, core-melanogenesis 14/16 vs syndromic 15/17 | Notebook's own printed output, cells re-inspected directly | **Matches.** `core_melanogenesis: 14/16`, `syndromic_trafficking: 15/17` printed verbatim; 4 discordances (APC2, ATP7B, MC2R, MRAP) listed by name, consistent with PITCH/DEMO's "n=4, ATP7B unflagged" framing. |
| NB5: STRING recovers 59.6% of Raghunath edges; 66.4% / ~34% drift vs D'Arcy | Notebook's own printed output | **Matches exactly** (158/265 = 59.6%; 491/740 = 66.4%, "~34% drift"). Citation-completeness gate: 12,133 elements, 0 uncited. |
| NB9: 0/142 → 93/142 orphans reconciled under symmetric STRING seed | `nb9_orphan_reconciliation.csv` (142 rows), notebook's printed "Citation-completeness gate: PASS (142/142 rows cited)" | **Matches.** This is the one "seeding changes the answer" result that IS fully backed by a reproducible notebook — the standard the "second thread" (1a above) should be held to as well. |
| NB11: MFSD12 rs10424065 Fst=0.26, 96th percentile; LD-independence for MFSD12/BNC2 pairs | `nb11_cross_ancestry_fst.csv` | **Matches** (fst_hudson_5superpop = 0.2598, baseline_percentile = 96.4; both pairs carry a "CONFIRMED independent" LD note in the `ld_independence_evidence` column). |
| NB4: 105 curated loci → 52 author-unexplained → 27 rsID-overlap with GWAS Catalog; unified base 1,177 rows | Notebook's own TL;DR + printed cells | **Internally consistent** (105 + 1,072 = 1,177). Not independently re-run against the raw GWAS Catalog pull in this review, but the arithmetic and the notebook's self-reported gap (Kim 2024 not folded in, "documented as a gap, not fabricated") are both honest and consistent. |
| Anchor PMIDs in START_HERE (31100995, 34711957, 35668300, 38849341, 22158248, 37327787) and Bajpai DOI (10.1126/science.ade6289) | NCBI eSummary / CrossRef | **All six PMIDs and the Bajpai DOI resolve to the correct paper** (titles match). |

### 3b. Negative results are framed as findings, not failures

Both required negatives are framed correctly, matching the task's honest-position brief:

- **Rescue screen (NB8-diagnostic).** The notebook's own verdict header states outright: <br>
  *"of the 18 effector-uncertain loci... **NONE of the 5 is a novel, network-discovered effector**... The
  rescue screen surfaces no novel melanogenesis effector."* PITCH.md's answer to pitch-question 2 repeats
  this without softening: *"did NOT yield a novel network-discovered effector"* and reframes the actual
  positive contribution correctly — the melanocyte-vs-bulk eQTL tissue-correction finding — as a
  **methodological** result, parallel to NB5's network-choice result. This is the strongest instance of
  "negative reported as finding" in the whole narrative and should be a model for 1a above.
- **Cross-ancestry (NB11).** The notebook's own TL;DR states plainly, in bold, before any result table:
  *"HONEST framing up front. MFSD12 is a known effector... What this notebook demonstrates for MFSD12 is
  **cross-population portability of a known gene, not novel effector discovery**."* PITCH's third-thread
  paragraph repeats this verbatim in substance. No overclaim found here.
- **NB10/NB12 flagship itself** is downgraded from "biological discovery" to "methodological
  demonstration" throughout PITCH, START_HERE, FINDINGS_MEMO, and the standalone DEMO_direction_law.md, with
  a dedicated "What would be overclaiming (and we do not claim it)" section in NB12 and a "What NOT to
  claim" section in DEMO_direction_law.md. This is unusually disciplined for a hackathon submission — most
  projects would keep the stronger framing that was live before the 2026-07-12T16:14Z audit; this one
  visibly walked it back in the CHANGELOG and propagated the walk-back to every downstream document I
  checked.

### 3c. No nearest-gene locus dressed up as a confident hit

Checked specifically for the failure mode the `nearest-gene-vs-causal` discipline names: a GWAS "nearest
gene" label presented as if it were a demonstrated causal/functional target.

- NB8-diagnostic explicitly separates "connected via non-canonical route" from "connected only via canonical
  neighbour (NOT our finding)" as two different buckets, and states outright for its strongest candidate,
  **LRMDA**, that *"this is not a discovery — the effector-uncertain label was **wrong**; it should never
  have been in the uncertain set."* That is the correct, honest move — catching and reporting a label error
  rather than quietly keeping the inflated count.
- NB11's SPIRE2 rs34357723 row (`nb11_cross_ancestry_fst.csv`, `functional_target_note` column) explicitly
  flags that the nearest-gene label is ambiguous between FANCA and SPIRE2 and that the paper's own
  hypothesized functional target is actually MC1R via long-range regulation — recorded as a caveat, not
  silently resolved to whichever gene is more convenient for the network story.
- The one place this discipline is *not* yet applied with the same rigor is PITCH's "second thread" (1a
  above) — the SPIRE2→MYO5A / ATRN→ASIP / OPN4→FOS→MITF examples are all *network paths from the nearest-
  gene label*, not independent confirmation that the nearest gene is the causal effector, and the paragraph
  does not carry the same disclaimer NB11 attaches to SPIRE2 elsewhere. This is a second reason to fix 1a,
  not just the arithmetic — the wording as it stands does not distinguish "network association" from
  "causal confirmation" as sharply as the rest of the project does.

### 3d. Conclusion currency — spot-checked against latest notebook output

Every "one number that matters" I could locate a source cell for (NB4, NB5, NB6, NB7, NB9, NB10, NB11, NB12)
matches the notebook's own most recent printed output — none is describing a stale run. NB8's diagnostic
table is hand-transcribed into PITCH.md's progress table but the counts (5 connected / 5 canonical-neighbour
/ 2 needs-review / 6 negative = 18) match the notebook exactly. The `internal/CHANGELOG.md` softening entry
(2026-07-12T16:14Z) is reflected consistently across PITCH, START_HERE, and FINDINGS_MEMO — I did not find
any document still carrying the pre-softening "flagship" language once I checked all four.

### 3e. "Honest"/"honestly" word-family scan

Total occurrences across the reviewed documents: **PITCH.md 11, START_HERE.md 4, FINDINGS_MEMO.md 2,
DEMO_direction_law.md 3, TODO.md 3** (adjective + adverb combined), plus scattered use inside notebook
markdown (NB5 7, NB8-diag 5, NB9 3, NB10 2, NB11 7, NB12 7). The *adverb* form ("honestly") is rare and,
where present, is not a hedge-filler — each instance modifies a genuine epistemic move (PITCH.md line 69:
"reported **honestly** as a negative"; DEMO_direction_law.md line 26: "the boundary, shown **honestly**").
The *adjective* "honest" is used almost entirely as a load-bearing structural label — "honest negative,"
"honest limits," "honest gap," "Honest split," "HONEST framing up front" — functioning as a section-header
convention this project uses consistently to flag exactly the caveats a claim-honesty reviewer looks for,
not as a vouching tic. **No fix needed** — this is the one case where heavy reliance on the word family is
doing real communicative work (flagging every caveat explicitly) rather than filler, and removing it would
make the caveats *less* visible, which would be the wrong direction for this document's purpose. I would
flag it differently in a paper manuscript aimed at a journal audience, where the convention reads as
informal; for an internal-facing pitch/status document it is functioning as intended.

### 3f. US-spelling pass

Scanned PITCH.md, START_HERE.md, FINDINGS_MEMO.md, DEMO_direction_law.md, README.md, index.qmd,
DATA_SOURCES.md, and CHANGELOG.md for the common British/Commonwealth variants. Two real, low-severity
hits, both easy one-word fixes:

- **"skin colour"** appears in PITCH.md (l.26), START_HERE.md (l.189), FINDINGS_MEMO.md (l.12),
  DEMO_direction_law.md (l.51), and twice in CHANGELOG.md (ll.1370, 1407) — all should be **"skin color"**
  for US-English consistency with the rest of the corpus (which otherwise uses "color" throughout, e.g.
  "common-variant skin colour" sits one sentence away from "positive regulator of melanin" using US
  spelling for everything else).
- **"Europe-centred"** (START_HERE.md l.72) → **"Europe-centered."**
- Not flagged: "Catalogue" in "GWAS Catalog"/"eQTL Catalogue" — these are the literal proper names of the
  external databases (NHGRI-EBI GWAS Catalog; EMBL-EBI eQTL Catalogue), not a spelling choice, and should
  stay as-is.

**Severity: Low** — 7 total instances across ~65KB of text, none of them numerically load-bearing.

---

## Overall verdict

**The narrative is close to submission-honest as-is.** The three "choice-changes-the-answer" axes (NB5,
NB9, NB11-portability) and the one correctly-reported negative (NB8-diagnostic rescue) are all framed
exactly as findings, with the honest caveat present at the point of the claim rather than buried, and the
one clean positive (NB10/NB12 direction law) carries an unusually thorough self-audit trail (the validity
audit, the framing softening, the "what would be overclaiming" section) that most hackathon submissions
would not bother writing. The project's own discipline — gate every table on a citation-completeness check,
never let a headline outrun its denominator, report the honest count — is visibly applied almost everywhere
I checked a number against its source.

**The one thing that would make a reviewer's spot-check fail is the "25 of 49" figure in PITCH's second
thread (1a)** — a specific, checkable claim with no reproducible backing, sitting in the exact document a
judge reads first. Fix that one number (or downgrade the wording to what the frozen STRING pull actually
supports) and resolve or cut the four unverified anchor citations (1b), and this narrative is ready to
submit without a claim-honesty reviewer finding anything further to flag.

## Fix list (priority order)

1. **[High] PITCH.md, "second thread" paragraph** — reconcile or remove the "25 of 49 connect... via
   high-confidence paths" claim; no notebook/script backs this number, and the denominator is stated as
   both 41 and 49 within the same paragraph. Suggested replacement wording given above (§1a).
2. **[Medium] PITCH.md, "Positioning" section** — resolve the four anchor citations (Fagny & Austerlitz
   2021; Daub 2013; signet/Gouy 2017; network-propagation family) to DOIs, or cut the paragraph. Do not ship
   the "NOT yet verified... confirm before public deliverable" caveat inside the deliverable itself.
3. **[Low-Medium] PITCH.md flagship section** — add a one-line lead claim above the two framing-warning
   banners so a skimming reviewer reaches the 22/22 result before the hedging.
4. **[Low-Medium] START_HERE.md top** — add a one-line judge/reviewer redirect to PITCH.md +
   FINDINGS_MEMO.md, since README.md points judges here first but the document is written for an agent
   audience.
5. **[Low] START_HERE.md "current candidate directions" callout** — point to FINDINGS_MEMO.md's explicit
   ranking so a reader doesn't have to wonder which candidate direction is actually being submitted.
6. **[Low] Spelling** — "skin colour" → "skin color" (5 instances: PITCH.md, START_HERE.md,
   FINDINGS_MEMO.md, DEMO_direction_law.md, CHANGELOG.md ×2); "Europe-centred" → "Europe-centered"
   (START_HERE.md).

No fix needed for: the "honest"/"honestly" word family (functioning as a structural caveat-flag, not
filler — see §3e); the negative-result framing (already correctly presented as findings); the nearest-gene
discipline (already correctly applied, with the one exception folded into fix #1); or conclusion currency
(every number I could trace to a source cell matched the notebook's latest printed output).
