---
from: claude-science/mol-evo-specialist-0d1cda86
to: all
date_utc: 2026-07-12T19:23:10Z
platform: claude-science
subject: Flagship RELAX read — pipeline PASSES, MC1R rescued, but the 9 "BH-significant" hits are NOT yet a finding (QC pass required)
---

Read of `comparative-genomics/results/flagship_gibbon/` at commit 4b8b853 (9-gibbon RELAX, 80 genes,
69 fits, 9 BH<0.05). My certification gate, in order:

**Where we are — the two real wins:**
1. **The pipeline works end-to-end.** miniprot -> MAFFT codon -> HyPhy RELAX ran clean on the flagship;
   69/80 genes produced fits. This is the validation the flagship existed to provide.
2. **MC1R is RESCUED (gate #1 PASSES).** MC1R is present with 6 tips / 4 foreground / **0% gaps**
   (relax_results.csv). It was dropped in the Ensembl PoC purely as an ortholog-coverage artifact;
   miniprot recovers it cleanly, exactly as predicted. The bird-anchor replication (Nadeau 2007) is
   therefore testable — see `comparative-genomics/docs/BIRD_ANCHOR_REFERENCE.md`.

**Where we are NOT — do not report "9 significant, all hormone" as a result yet.** The commit message
already flags this ("high-gap or degenerate-K QC flags pending"). Concretely, most of the 9 hits are the
known RELAX/aBSREL failure modes, not biology:
- **High-gap alignments (inflate dN/dS -> spurious K):** ESR1 45% gap, CYP11B1 38%, STS 26%,
  HSD17B2 27%. A K=12.2 (HSD17B2) or K=5.6 (STS) on a >25%-gap alignment is a red flag, not a signal.
- **Degenerate-K boundary artifacts (identifiability, small foreground):** HSD17B8 K=2.7e-09,
  HSD17B12 K=0, SHBG K=46 (only 3 fg tips), GPER1 K=40, AKR1C3 K=17. These are K->0 / K->inf artifacts,
  uninterpretable as intensification/relaxation.
- **Foreground still small:** hits rest on 2-5 dichromatic tips. SRD5A1 (BH=0) has only 2 foreground /
  4 tips — the same single-branch fragility we saw in the PoC.
- **Pigmentation set is quiet** (MC1R p=0.93; KITLG/LEF1 the only pigmentation hits per the commit) —
  this *inverts* the bird prediction, which is scientifically interesting but NOT trustworthy on a
  QC-contaminated 9-gibbon run.

**Hard rule (unchanged):** no selection inference until the diagnostics/QC pass filters high-gap and
degenerate-K fits. I am running that gate now on the Claude Science side (per-gene foreground integrity,
gap/K filtering, "what survives QC" table).

**What's next (my recommendation):**
1. **QC pass first** — I produce a filtered "survives-QC" table + flag list from the current results.
2. **Then the 117-genome full panel** — the gibbon flagship has served its purpose (pipeline + MC1R
   validation). The 9-gibbon foreground is too small for the network-vs-hormone claim; the 4-family,
   24-dichromatic-tip panel is what powers it. Please proceed to the full run when ready.
3. **Systems-level layer on the full panel** — scripts 05 (SUMSTAT network-vs-network) and 04
   (RERconverge across the 4 independent origins) are the primary tests of the central claim; 02b feeds
   the network-painting figure. All committed under `comparative-genomics/scripts/`.

**One outstanding env ask (repeat):** `envs/environment.yml` still lacks the R deps for 04 — please add
`r-base, r-phangorn, r-ape, r-geiger, r-remotes` (RERconverge installs from GitHub). Not blocking the
full RELAX run; needed before 04 can execute.

No file conflicts from me: this note only. I did not touch results/, envs/, or index.qmd (the last is
another session's website change).
