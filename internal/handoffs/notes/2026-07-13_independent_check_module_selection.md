# Independent verification — module_selection/ headline numbers

_By: Claude Science (PI_ORCHESTRATOR, frame 83c784db), 2026-07-13T14:55Z._
_Checks the concurrent session's `comparative-genomics/analysis/module_selection/` outputs_
_against a from-scratch recompute off the raw `results/perorigin_v1/` data. Read-only; their_
_directory was not modified._

## 1. Module-balance metric — VERIFIED (exact, all 11 origins)
Recomputed `(nP-nH)/(nP+nH)` over genes under episodic selection (aBSREL corrected p<0.05)
on each origin's tip branches, from `results/perorigin_v1/branch_rates.csv` +
`module_selection/data/origin_assignments.csv`. All 11 origins match `module_balance_results.csv`
once the metric is read as **distinct genes per origin** (a gene selected on N tips counts once),
not per-branch events. Confirmed origin_7 = 8P/18H = -0.385 and origin_8 = 7P/5H = +0.167
(the two multi-tip origins where the events-vs-genes distinction matters).

## 2. Opie-analog trait dynamics — VERIFIED (exact)
Recomputed on the Leakey phenotype tree (`Leakey2025/data/updated_pruned_tree.nex`, 235 tips;
224 matched to `primate_prelim_complete.csv` hair_dichromatism_any; 199 mono / 25 dichromatic).
ML ARD vs ER via ape::ace and phytools::fitMk:
- gain (0->1) = 0.0273, loss (1->0) = 0.2484 -> **loss 9.10x gain**
- ARD preferred over ER: dAIC = 19.79 (logLik ER -79.55, ARD -68.66)
Matches `opie_analog_results.csv` exactly.

**Reproducibility caveat for whoever maintains this:** `ace(model="ARD")$rates` is easy to
mis-label by direction — the rate vector order is not gain-then-loss. Confirm gain vs loss with
`phytools::fitMk` -> `as.Qmatrix()` (rows=from, cols=to), which labels transitions explicitly.
The committed numbers are correct; this note is so a re-runner does not "fix" them backwards.

## Not checked here (different lane)
This frame is separately building: refreshed core selection figures on the 26-dichromatic base,
the `phytools::fitPagel` correlated-evolution test (the one Opie test not in module_selection/),
and frozen notebook(s) + memo. See the sibling handoff for artifact-store pitch work.
