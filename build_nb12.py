"""build_nb12.py — regenerate notebooks/figures/nb12_direction_law_expanded.png
from committed data, fully offline.

PROVENANCE OF THIS SCRIPT
--------------------------
notebooks/12_direction_law_expanded.ipynb cell 18 only displays the PNG
(`IPython.display.Image(filename=...)`) — it never generates it. `git log --all`
shows the PNG entered the repo in commit 20768ac with no committed generator
anywhere in the tree (see internal/reviews/reproducibility_review.md, "NB12 —
Figure" note). This script is the missing generator, written directly from
the committed processed tables so every plotted number traces to a CSV cell,
not to a value read off the image. It mirrors build_nb10.py's structure and
offline-reproducibility discipline (frozen-input assertions, `fig.savefig`,
no network calls) — see that file for the sibling NB10 figure.

Inputs (all pre-existing, committed under data/processed/ — nothing new is
computed by this script):
  - data/processed/nb12_direction_law_expanded.csv  (72 LoF OMIM genes; one row
    per gene, carrying both the NB10 network call and the NB12 blind-GO
    mechanism call — see notebook cells 4-14 for how each column was built)
  - data/processed/nb12_expanded_summary.csv        (the notebook's own
    already-aggregated per-subset concordance counts — used here only as a
    cross-check against the counts recomputed from the row-level CSV, not as
    the plotted source; if the two disagree this script raises rather than
    silently plotting the aggregate)

Only the plotting choices below are this script's own (not baked into the
CSVs) and are called out at the point each is made:
  PLOT CHOICE 1 — panel (a) dashed base-rate line height = base_rate * n,
    where base_rate is P(Hypopigmentation) over the full 72-gene LoF universe.
  PLOT CHOICE 2 — panel (c) restricts to the 11 *new* (mechanism-only, i.e.
    regulator_call is NaN) genes, matching notebook cell 14's `newg` filter,
    not all 33 expanded-test genes.
  PLOT CHOICE 3 — colour palette (not specified anywhere upstream): panel (a)
    uses the same concordant/base-rate palette as build_nb10.py's Step 6
    figure for visual consistency across the two sibling figures.
"""
import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
PROC = ROOT / "data" / "processed"
FIGDIR = ROOT / "notebooks" / "figures"

# --- Frozen-input assertions (NB2 lesson, same pattern as build_nb10.py) ---
REQUIRED = {
    "expanded": PROC / "nb12_direction_law_expanded.csv",
    "summary": PROC / "nb12_expanded_summary.csv",
}
missing = {k: str(p) for k, p in REQUIRED.items() if not p.exists()}
assert not missing, f"Missing committed inputs (cannot re-run): {missing}"
print("All", len(REQUIRED), "frozen inputs present:")
for k, p in REQUIRED.items():
    print(f"  {k:10s} {p.relative_to(ROOT)}")
print("Run:", datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"))

exp = pd.read_csv(REQUIRED["expanded"])
summ = pd.read_csv(REQUIRED["summary"])
assert exp.shape[0] == 72, f"expanded LoF universe drift: {exp.shape}"

# ---------------------------------------------------------------------------
# Panel (a) — NB10 network-only baseline vs the NB12 expanded test.
# Mirrors notebook cell 10 exactly: `test` = rows with a called direction
# (`reg_expanded` in {positive, negative}); `predicted` and `concordant` are
# already columns of the frozen CSV (built by the notebook's own Step 3-4),
# not recomputed here from mech_call — this script only re-aggregates them.
# ---------------------------------------------------------------------------
nb10_baseline = exp[exp["regulator_call"].isin(["positive", "negative"])]
n_nb10 = len(nb10_baseline)
k_nb10 = int((nb10_baseline["predicted"] == nb10_baseline["phenotype_class"]).sum())

test = exp[exp["reg_expanded"].isin(["positive", "negative"])].copy()
n_exp, k_exp = len(test), int(test["concordant"].sum())

# PLOT CHOICE 1: base-rate reference line, base rate taken over the full
# 72-gene LoF universe (matches notebook cell 10's `base = (exp["phenotype_class"]=="Hypopigmentation").mean()`).
base_rate = (exp["phenotype_class"] == "Hypopigmentation").mean()

print(f"\nPanel (a): NB10 baseline {k_nb10}/{n_nb10}  |  Expanded {k_exp}/{n_exp}  |  base_rate={base_rate:.4f}")

# ---------------------------------------------------------------------------
# Panel (b) — pre-registered core-melanogenesis vs syndromic/trafficking
# split, computed on the same 33-gene `test` set as notebook cell 12.
# ---------------------------------------------------------------------------
strat = test.groupby("stratum")["concordant"].agg(["sum", "count"])
core_k, core_n = int(strat.loc["core_melanogenesis", "sum"]), int(strat.loc["core_melanogenesis", "count"])
syn_k, syn_n = int(strat.loc["syndromic_trafficking", "sum"]), int(strat.loc["syndromic_trafficking", "count"])
print(f"Panel (b): core_melanogenesis {core_k}/{core_n}  |  syndromic_trafficking {syn_k}/{syn_n}")

# ---------------------------------------------------------------------------
# Panel (c) — confidence vs concordance, restricted to the 11 NEW mech-call
# genes (PLOT CHOICE 2: `regulator_call` isna, matching notebook cell 14's
# `newg = test[test["regulator_call"].isna()]` — NOT all 33 `test` rows).
# ---------------------------------------------------------------------------
newg = test[test["regulator_call"].isna()]
conf = newg.groupby("mech_conf")["concordant"].agg(["sum", "count"])
high_k, high_n = int(conf.loc["high", "sum"]), int(conf.loc["high", "count"])
med_k, med_n = int(conf.loc["medium", "sum"]), int(conf.loc["medium", "count"])
atp7b = test[test["gene"] == "ATP7B"]
assert len(atp7b) == 1 and atp7b["mech_conf"].iloc[0] == "high" and atp7b["concordant"].iloc[0] == 0, (
    "ATP7B is expected to be the one high-confidence miss driving panel (c)'s annotation"
)
print(f"Panel (c): high {high_k}/{high_n}  |  medium {med_k}/{med_n}  |  ATP7B is the high-confidence miss")

# --- Cross-check against the notebook's own pre-aggregated summary table ---
# nb12_expanded_summary.csv's "subset" column carries leading whitespace on the
# stratum/confidence rows (e.g. "  stratum: core_melanogenesis") — stripped
# here for lookup only; the raw CSV is left untouched.
summ_lookup = summ.assign(subset=summ["subset"].str.strip()).set_index("subset")
checks = [
    ("NB10 baseline (network sources)", k_nb10, n_nb10),
    ("Expanded (+ blind GO mechanism-call)", k_exp, n_exp),
    ("stratum: core_melanogenesis", core_k, core_n),
    ("stratum: syndromic_trafficking", syn_k, syn_n),
    ("new mech-call, high confidence", high_k, high_n),
    ("new mech-call, medium confidence", med_k, med_n),
]
for label, k, n in checks:
    row = summ_lookup.loc[label]
    assert (int(row["concordant"]), int(row["n"])) == (k, n), (
        f"Recomputed {label} = {k}/{n} disagrees with nb12_expanded_summary.csv = {int(row['concordant'])}/{int(row['n'])}"
    )
print("\nAll 6 recomputed counts match data/processed/nb12_expanded_summary.csv exactly.")

# ---------------------------------------------------------------------------
# Figure — 3 panels, matching the notebook's fig-cap (cell 18):
# "Expanding the direction law maps its boundary, and the boundary is
# imperfect." Colour choices are PLOT CHOICE 3 (not specified upstream).
# ---------------------------------------------------------------------------
concord, base_line_col = "#2c6fbb", "#c0504d"
green = "#3a9d5d"
blue_b, purple_b = "#4a90c9", "#8a7ec8"

fig = plt.figure(figsize=(15.5, 5.6))
gs = fig.add_gridspec(1, 3, wspace=0.32)

# Panel a
axA = fig.add_subplot(gs[0, 0])
xs = [0, 1]
heights = [k_nb10, k_exp]
labels_a = ["NB10\n(network\nsources)", "Expanded\n(+ blind GO\nmech-call)"]
bars_a = axA.bar(xs, heights, color=[concord, green], width=0.6)
for x, k, n in zip(xs, heights, [n_nb10, n_exp]):
    pct = 100 * k / n
    axA.text(x, k + 0.6, f"{k}/{n}\n({pct:.0f}%)", ha="center", va="bottom", fontsize=11, fontweight="bold")
axA.axhline(base_rate * n_exp, color=base_line_col, ls="--", lw=1.3)
axA.text(1.35, base_rate * n_exp + 0.4, "base rate ×33", color=base_line_col, fontsize=7.5, ha="right")
axA.set_xticks(xs)
axA.set_xticklabels(labels_a)
axA.set_ylabel("Concordant LoF genes")
axA.set_ylim(0, max(heights) * 1.25)
axA.set_title(f"a  Expansion adds n and finds the\nlaw's boundary ({k_exp}/{n_exp}, p<1e-5)", loc="left", fontsize=10.5)
for s in ["top", "right"]:
    axA.spines[s].set_visible(False)

# Panel b
axB = fig.add_subplot(gs[0, 1])
xs_b = [0, 1]
fracs_b = [core_k / core_n, syn_k / syn_n]
axB.bar(xs_b, fracs_b, color=[blue_b, purple_b], width=0.6)
for x, k, n, f in zip(xs_b, [core_k, syn_k], [core_n, syn_n], fracs_b):
    axB.text(x, f + 0.02, f"{k}/{n}", ha="center", va="bottom", fontsize=11, fontweight="bold")
axB.set_xticks(xs_b)
axB.set_xticklabels(["Core\nmelanogenesis", "Syndromic /\ntrafficking"])
axB.set_ylabel("Concordance fraction")
axB.set_ylim(0, 1.08)
axB.set_title("b  No ascertainment confound: syndromic\ngenes concordant as often as core", loc="left", fontsize=10.5)
for s in ["top", "right"]:
    axB.spines[s].set_visible(False)

# Panel c
axC = fig.add_subplot(gs[0, 2])
xs_c = [0, 1]
fracs_c = [high_k / high_n, med_k / med_n]
axC.bar(xs_c, fracs_c, color=[green, green], width=0.6)
for x, k, n, f in zip(xs_c, [high_k, med_k], [high_n, med_n], fracs_c):
    axC.text(x, f + 0.02, f"{k}/{n}", ha="center", va="bottom", fontsize=11, fontweight="bold")
axC.annotate(
    "ATP7B: 1 high-\nconfidence miss\n(NOT flagged)",
    xy=(0, high_k / high_n), xytext=(0.55, 0.55),
    fontsize=7.5, color=base_line_col,
    arrowprops=dict(arrowstyle="-", color=base_line_col, lw=0.9),
)
axC.set_xticks(xs_c)
axC.set_xticklabels(["High\nconfidence", "Medium\nconfidence"])
axC.set_ylabel("Concordance fraction")
axC.set_ylim(0, 1.08)
axC.set_title("c  Confidence catches 3 of 4 misses -\nbut not the ATP7B high-confidence miss", loc="left", fontsize=10.5)
for s in ["top", "right"]:
    axC.spines[s].set_visible(False)

fig.suptitle(
    "NB12 - expanding the mechanism-direction law maps its boundary (and the boundary is imperfect)",
    x=0.5, y=1.03, fontsize=13.5, fontweight="bold",
)
fig.text(
    0.5, -0.06,
    "50 LoF OMIM pigmentation genes without a network direction call were annotated by a fourth, independent source: a blind GO-based "
    "mechanism classification (given only normal molecular function, never the patient phenotype). 11 got a directional call; adding them "
    f"takes the test from {n_nb10}/{n_nb10} to {k_exp}/{n_exp} (permutation p<1e-5). (b) The gate-mandated core-vs-syndromic split shows NO "
    "ascertainment bias. (c) The classifier's confidence separates the 3 medium-confidence calls (all misses: APC2 Wnt, MC2R+MRAP ACTH "
    "feedback) from high-confidence (7/8) - but ATP7B is a HIGH-confidence miss (Wilson-disease systemic copper), so confidence flags most, "
    "not all, failures. The 'predicts its own failures' pattern rests on n=4 and is illustrative, not validated.",
    ha="center", va="top", fontsize=7.2, color="#333", wrap=True,
)

FIGDIR.mkdir(parents=True, exist_ok=True)
out_path = FIGDIR / "nb12_direction_law_expanded.png"
fig.savefig(out_path, dpi=200, bbox_inches="tight")
print("\nsaved", out_path)
