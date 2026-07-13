# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # NB15 · Sexual dichromatism across the primates — a labile, two-module trait
#
# **This is the results notebook for the dichromatism project — start here.** It reports the
# central finding: sexual hair dichromatism has arisen and been lost repeatedly across the
# primate radiation, and where we can test its genetic basis, each origin is built through a
# *different* combination of two coupled gene modules — pigmentation and sex-hormone signalling.
#
# It reads two things:
#
# 1. **The phenotype** — which primates are sexually dichromatic, scored across the radiation
#    (§2), and where those gains and losses fall on the tree (§3).
# 2. **Selection** — per-gene episodic-selection scans on a curated 110-gene panel, run across
#    the primate genomes on an HPC pipeline. The panel itself is *justified* in two upstream
#    notebooks, which this one depends on but sits above in the reading order:
#    - **NB13** (`13_sex_hormone_layer.ipynb`) — why these sex-hormone genes, and how the
#      hormone layer bridges into pigmentation.
#    - **NB14** (`14_hormone_pigment_interface.ipynb`) — the full 110-gene panel, its two
#      modules, and the orthology screen behind every gene.
#
# A reader who wants *the finding* needs only this notebook. A reader who wants *why these
# genes* follows the links down to NB13/NB14. The analysis flows the other way — the panel is
# built there and consumed here — but the science reads top-down from this page.
#
# **What this notebook establishes, in order:**
#
# | § | Question | Result |
# |---|---|---|
# | 2 | How is dichromatism scored, and on how many species? | Coded across 238 species; 117 have sequenced genomes |
# | 3 | Is the trait evolutionarily labile? | Yes — losses outpace gains ~9:1; ~15–19 independent origins |
# | 4 | Where selection can be tested, is one origin like another? | No — the powered origins use non-overlapping gene sets |
# | 5 | Does an origin lean pigmentation or hormone? | Per-origin module balance, corrected for panel composition |
# | 6 | Do independent origins reuse the same genes (convergence)? | No detectable shared signature — power-limited, but divergent where powered |

# %% [markdown]
# ## 0 — Input provenance
#
# Every input below is a version-controlled file in this repository, traced to its producing
# notebook or pipeline and to its external source in `DATA_SOURCES.md`. The manifest is encoded
# as the `INPUTS` dict in the next cell so provenance is **executable**: the loader prints, for
# each file, what it is, where it came from, and a SHA256 of the exact bytes read. The
# phylogenetic results in §3 and §6 are **recomputed here** from the tree and coding — they are
# not read from any precomputed summary table.
#
# | Input | Source | External / DATA_SOURCES.md |
# |---|---|---|
# | `analysis/coevolution_test/data/primate_phenotype_tree.nex` | primate time-tree (235 tips), pruned to the phenotype coding | grant-derived primate supertree; see DATA_SOURCES.md |
# | `config/primate_dichromatism_coding.csv` | full-resolution dichromatism coding, 238 species | expert scoring of published descriptions/plates |
# | `analysis/data/dichromatism_coding.csv` | the 117-species genome subset (dichromatic flag) | subset of the above with a sequenced genome |
# | `results/perorigin_v1/per_origin_K.csv` | HPC per-origin RELAX (K) on the 110-gene panel | selection pipeline; panel justified in NB13/NB14 |
# | `results/perorigin_v1/branch_rates.csv` | HPC full-panel aBSREL per-branch selection | selection pipeline; panel justified in NB13/NB14 |
#
# The phylo recompute is driven by `nb15_phylo.R` (committed beside this notebook); its outputs
# under `dichromatism_synthesis/data/` and `dichromatism_synthesis/figures/` are read below.

# %%
import os, hashlib
import pandas as pd
REPO = os.environ.get("PIGNET_REPO", os.path.abspath(os.path.join(os.getcwd(), "..", "..", "..")))
CG   = os.path.join(REPO, "comparative-genomics")
SYN  = os.path.join(CG, "analysis", "dichromatism_synthesis")   # this notebook's own data/figures

# --- Provenance manifest: every input, where it comes from, how to regenerate it. ---
INPUTS = {
    "tree": {
        "path": "comparative-genomics/analysis/coevolution_test/data/primate_phenotype_tree.nex",
        "what": "Primate time-calibrated phylogeny (235 tips), the tree all rate/ASR estimates run on",
        "source": "Published primate supertree pruned to the phenotype coding; see DATA_SOURCES.md",
        "produced_by": "Upstream phylogenetics; this notebook only reads it",
    },
    "coding_full": {
        "path": "comparative-genomics/config/primate_dichromatism_coding.csv",
        "what": "Full-resolution sexual-dichromatism coding, 238 species "
                "(hair_dichromatism_any + complete/state/type, natal coat, ontogenetic trajectory)",
        "source": "Expert scoring of published species descriptions and plates",
        "produced_by": "Phenotype coding effort; NB15 uses hair_dichromatism_any as the binary trait",
    },
    "coding_genome": {
        "path": "comparative-genomics/analysis/data/dichromatism_coding.csv",
        "what": "The 117-species genome subset with the dichromatic flag "
                "(the species that also have a sequenced genome in the selection scan)",
        "source": "Subset of coding_full restricted to species with a genome assembly",
        "produced_by": "Genome-availability intersection; used to mark which origins are analysable",
    },
    "per_origin_K": {
        "path": "comparative-genomics/results/perorigin_v1/per_origin_K.csv",
        "what": "Per-origin RELAX selection-intensity K per powered origin, on the pigmentation+"
                "hormone panel (target 110 genes; the loaded row/gene count is printed at load "
                "time and grows as the clean-30 expansion and MYO5A/LYST giants land)",
        "source": "HYPHY RELAX on codon alignments (HPC); panel justified in NB13/NB14",
        "produced_by": "Selection pipeline (pulled from HPC); module+category columns from nb14_panel_justification.csv",
    },
    "branch_rates": {
        "path": "comparative-genomics/results/perorigin_v1/branch_rates.csv",
        "what": "Full-panel aBSREL per-branch episodic-selection p-values on the 110-gene panel",
        "source": "HYPHY aBSREL on codon alignments (HPC); panel justified in NB13/NB14",
        "produced_by": "Selection pipeline (pulled from HPC)",
    },
    "relax_pooled": {
        "path": "comparative-genomics/results/perorigin_v1/relax_pooled_results.csv",
        "what": "Pooled RELAX (all dichromatic origins as one foreground set) per gene, used as a "
                "QC cross-check on the per-origin fits: a per-origin hit with an extreme boundary "
                "K that is null when pooled is treated as a boundary artifact",
        "source": "HYPHY RELAX, pooled foreground (HPC); panel justified in NB13/NB14",
        "produced_by": "Selection pipeline (pulled from HPC)",
    },
}

def _sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]

def load_input(key, reader=pd.read_csv):
    """Load a manifest input, printing provenance + a checksum of the exact bytes read.
    Returns None (with a clear notice) if the file is not present yet — the HPC selection
    tables land after the tree-only sections are built."""
    m = INPUTS[key]; fp = os.path.join(REPO, m["path"])
    if not os.path.exists(fp):
        print(f"[{key}] {m['path']}\n    NOT PRESENT YET — {m['what']}\n"
              f"    (produced by: {m['produced_by']})\n")
        return None
    print(f"[{key}] {m['path']}")
    print(f"    what     : {m['what']}")
    print(f"    source   : {m['source']}")
    print(f"    produced : {m['produced_by']}")
    if key == "tree":
        print(f"    loaded   : Nexus tree | sha256[:16]={_sha(fp)}\n"); return fp
    df = reader(fp)
    print(f"    loaded   : {df.shape[0]} rows x {df.shape[1]} cols | sha256[:16]={_sha(fp)}\n")
    return df

TREE_PATH = load_input("tree")
CODING    = load_input("coding_full")
GENOME    = load_input("coding_genome")

# %% [markdown]
# ## 1 — The headline
#
# Sexual dichromatism — males and females differing in hair or pelage colour — is scattered
# across the primate tree, not clustered in one clade. Coded across 238 species, it appears in
# lemurs (*Eulemur*), colobines (*Trachypithecus*, *Colobus*), gibbons (*Nomascus*, *Hylobates*),
# and a handful of other lineages, separated by long monochromatic stretches. That distribution
# is the starting observation: whatever builds dichromatism has been assembled *repeatedly and
# independently*, and lost repeatedly too.
#
# **Two questions, two kinds of data.** The *phylogeny* answers **where, when, and how often** the
# trait arose — that it is labile, lost far faster than gained, and assembled ~15 times (§3). None
# of that needs sequence data. The reason we sequenced is a question the tree cannot answer: **what
# molecular change happened when dichromatism arose** — and here the answer is genuinely
# surprising. In birds, sexual dichromatism repeatedly evolves through **MC1R**, a single
# large-effect coat-colour gene. In primates, MC1R is **not** the recurrent route: across the panel
# it shows no pooled selection signal (K = 0.45, n.s.), surfacing in just one lineage (§4). There is
# no single "dichromatism gene." Instead, the origins we can test recruited **different gene sets
# from a coupled pigmentation–hormone system**, with no shared molecular signature where the
# comparison is powered (§4–§6). That is the payoff of the genetics: not the pattern of origins
# (the tree gives that), but the finding that a trait built one way in birds is built many
# different ways in primates.
#
# Roadmap: §3 quantifies the lability and origin count from the tree; §4–§5 test *which* genes and
# *which module* shifted at the origins with enough sequenced species (only two carry a signal);
# §6 asks whether independent origins converged on the same genes (they do not, where powered).
# Whether origins differ *systematically* in architecture is left as an open, underpowered
# question — only two of ~15–19 origins carry a per-origin signal — not asserted.

# %% [markdown]
# ## 2 — Phenotype: coding and provenance
#
# **Two codings, one trait.** Dichromatism is scored at full taxonomic resolution across
# **238 species** (`coding_full`), using `hair_dichromatism_any` as the binary trait (1 = males
# and females differ in hair colour). A **117-species subset** (`coding_genome`) marks the
# species that *also* have a sequenced genome — these are the ones a selection scan can actually
# run on. The two codings agree on the phenotype; they differ only in taxonomic coverage, and
# that difference matters for one number (the origin count, §3), so both scopes are reported
# throughout rather than silently merged.
#
# The tree (`tree`, 235 tips) and the coding are joined on the binomial with underscores
# substituted for spaces; the intersection used for all rate/ASR work is reported below.

# %%
# Join tree and coding; report the overlap used for all downstream phylo work.
import re
def _tips_from_nexus(path):
    txt = open(path).read()
    return set(re.findall(r"[A-Z][a-z]+_[a-z]+", txt))

if TREE_PATH is not None and CODING is not None:
    tree_tips = _tips_from_nexus(TREE_PATH)
    CODING = CODING.copy()
    CODING["tip"] = CODING["species_binom"].str.replace(" ", "_", regex=False)
    coded = CODING.dropna(subset=["hair_dichromatism_any"])
    overlap = sorted(set(tree_tips) & set(coded["tip"]))
    n_dich  = int(coded.set_index("tip").loc[overlap, "hair_dichromatism_any"].astype(int).sum())
    n238    = len(CODING); n117 = 0 if GENOME is None else len(GENOME)
    print(f"full coding (coding_full)      : {n238} species")
    print(f"genome subset (coding_genome)  : {n117} species")
    print(f"tree tips                      : {len(tree_tips)}")
    print(f"tree n coding (analysis set)   : {len(overlap)} tips, {n_dich} dichromatic")
    print("\nAll rate and ancestral-state estimates below run on the "
          f"{len(overlap)}-tip intersection.")

# %% [markdown]
# ## 3 — The trait is evolutionarily labile
#
# **Method.** A two-state Markov model (Mk) is fit to `hair_dichromatism_any` on the
# intersection tree, comparing equal rates (ER: one rate for gain and loss) against
# all-rates-different (ARD: separate gain and loss rates). Model fit is compared by AIC; the
# origin count is read from stochastic character maps under the preferred model, and cross-checked
# against a model-free count of maximal dichromatic clades. All of this is recomputed by
# `nb15_phylo.R`; its result tables are read below.
#
# **Table 1.** Model comparison for how dichromatism changes over evolutionary time. ER = one rate
# for gains and losses; ARD = separate gain and loss rates. Lower AIC = better-fitting model; a
# gap (ΔAIC) above ~4 is decisive. ARD wins by ΔAIC ≈ 20, and its two rates show that the trait is
# **lost far faster than it is gained** (loss:gain ≈ 9×). The origin count — how many separate
# times dichromatism appeared — is read from simulations under the winning model and reported for
# both coding scopes, because that one number depends on how many species are included.

# %%
# Read the recomputed lability fits + origin estimates (from nb15_phylo.R).
def _read_syn(name):
    fp = os.path.join(SYN, "data", name)
    return pd.read_csv(fp) if os.path.exists(fp) else None

FITS    = _read_syn("nb15_lability_fits.csv")
ORIGINS = _read_syn("nb15_origin_estimates.csv")
if FITS is not None:
    ard = FITS[FITS.model == "ARD"].iloc[0]
    print("Mk model comparison (delta = ER - ARD):")
    for _, r in FITS.iterrows():
        print(f"  {r['model']:3s}  logLik={r['logLik']:8.2f}  AIC={r['AIC']:8.2f}")
    print(f"\nARD preferred by dAIC = {ard['dAIC_ER_ARD']:.2f}")
    print(f"  gain rate (0->1) = {ard['gain_0to1']:.4f}")
    print(f"  loss rate (1->0) = {ard['loss_1to0']:.4f}")
    print(f"  loss : gain      = {ard['loss_gain']:.1f}x  (losses far outpace gains)")
if ORIGINS is not None:
    print("\nOrigin count - reported under both coding scopes (differ by sampling, not phenotype):")
    for _, r in ORIGINS.iterrows():
        v = "" if pd.isna(r["n_origins"]) else f"{r['n_origins']:.0f}"
        print(f"  {r['scope']:38s} {v:>4s}   [{r['method']}]")

# %% [markdown]
# **Result.** The ARD model is strongly preferred (ΔAIC ≈ 19.8): a single-rate model is a poor
# description. The asymmetry is large and in one direction — **dichromatism is lost roughly nine
# times faster than it is gained**. A trait that is hard to gain but easy to lose, arising in
# scattered clades, is the signature of a labile, repeatedly-assembled phenotype rather than one
# ancient origin retained.
#
# **Origin count — an estimator- and sampling-dependent number.** How many
# times dichromatism arose depends on both the coding scope and the method:
#
# - On the **117-species genome subset** — the coding the selection scan actually runs on — a
#   model-free count of maximal dichromatic clades gives **~15 origins**. This is the figure used
#   in the project's README and walkthrough.
# - On the **full 238-species coding**, the finer taxonomic sampling resolves **19** distinct
#   dichromatic clades (**18** containing at least one genome-sampled species). The extra origins
#   are real clades the genome subset simply did not sample.
# - Model-based counts bracket these: ML ancestral-state reconstruction under ARD *collapses* the
#   estimate (it paints dichromatism deep and loses it repeatedly — a known artifact of the high
#   loss rate, and the reason a naïve "4 deep origins" reading is wrong), while stochastic mapping
#   *inflates* it (mean ≈ 31, from transient 0→1→0 flicker on short branches).
#
# The defensible statement is therefore a range, not a point: **on the order of 15–19 independent
# origins**, ~14–18 of them with a sequenced genome. The exact value is sensitive to how densely
# the clade is sampled — which is itself part of the lability story.

# %% [markdown]
# ### Figure 3 — Where gains and losses fall (stochastic density map)
#
# The figure below paints, on the primate tree, how likely dichromatism was along each branch —
# so gains and losses of the trait are visible as where red appears and disappears. Full caption
# follows the figure.

# %%
from IPython.display import Image, display
_dm = os.path.join(SYN, "figures", "nb15_densitymap.png")
if os.path.exists(_dm):
    display(Image(filename=_dm))
else:
    print("nb15_densitymap.png not built yet - run nb15_phylo.R")

# %% [markdown]
# **Figure 3. Where on the primate tree dichromatism was gained and lost (density map).**
#
# *What the data are.* The tree is the 224-species primate phylogeny used throughout this notebook
# (the intersection of the 235-tip phylogeny and our 238-species dichromatism coding, §2); 25 of
# those species are coded dichromatic. The trait is `hair_dichromatism_any` (males and females
# differ in hair colour: yes/no).
#
# *What a density map is.* Every branch of the tree is coloured by how likely it is that
# dichromatism was present along that branch. To estimate this we simulate the trait's evolution
# down the tree 500 times (stochastic character maps under the best-fitting ARD model from §3) and
# average the results, so a branch that comes out dichromatic in most simulations is painted red
# and one that is rarely dichromatic stays blue.
#
# Branch colour runs from blue (probability ≈ 0, monochromatic) through magenta to red
# (probability ≈ 1, dichromatic); the scale bar is at lower-left. A red dot at a tip marks a
# living species that is **actually observed / coded** dichromatic — this is the reality check on
# the reconstruction: the painted-red branches should end in red-dotted tips, and they do, so the
# model is tracking the real states rather than inventing signal. The coloured strip on the right
# labels the major primate groups for orientation (Old World monkeys, apes, gibbons, New World
# monkeys, tarsiers, lemurs, lorises & galagos). Individual species names are left off so the
# 224-species tree stays legible (§2).
#
# Red concentrates in short, terminal patches — the *Trachypithecus* langurs within the Old World
# monkeys, the *Nomascus*/*Hylobates* gibbons, and *Eulemur* among the lemurs — separated by long
# blue (monochromatic) internodes. That scattering, rather than one deep red clade, is the visual
# signature of the many-independent-origins, high-loss pattern quantified in §3.

# %% [markdown]
# ## 4 — Per-origin architecture
#
# **The question.** Of the independent origins, only those with **≥2 sequenced dichromatic tips**
# carry enough branches for a per-origin RELAX test — three do: *Trachypithecus* (origin 7),
# *Nomascus* (origin 8), and *Eulemur* (origin 14). For each, which panel genes show a shift in
# selection intensity (K) along the origin's branches?
#
# **The result** (the loaded panel size is printed below and grows toward 110 as the clean-30
# pigmentation expansion lands — the two giant genes MYO5A/LYST arrive last): the three powered
# origins do *not* share a gene set.
# *Trachypithecus* shows a multi-gene, both-module signal (including a lineage-specific MC1R
# shift); *Nomascus* concentrates on a small pigmentation set — POMC, HGF, HRAS — of which POMC
# (§5b) sits at the pigmentation–hormone interface; *Eulemur* shows no gene passing the per-origin
# threshold. Same phenotype, different genetic routes — quantified in §6. The gene lists are
# printed below; the `fig_per_lineage_genes` panel is regenerated against the completed 110-gene
# tables.

# %%
PER_ORIGIN = load_input("per_origin_K")
BRANCH     = load_input("branch_rates")
if PER_ORIGIN is not None:
    origins = sorted(PER_ORIGIN['origin_id'].unique()) if 'origin_id' in PER_ORIGIN else '?'
    print(f"per_origin_K: {PER_ORIGIN.shape[0]} rows, "
          f"{PER_ORIGIN['gene'].nunique()} genes, origins {origins}")
    if "p_BH" in PER_ORIGIN.columns:
        sig = PER_ORIGIN[PER_ORIGIN.p_BH < 0.05]
        for o in origins:
            g = sorted(sig[sig.origin_id == o].gene)
            print(f"  {o}: {len(g)} genes p_BH<0.05 - {g if g else '(none)'}")
else:
    print("Awaiting per-origin tables (cluster appending clean-30 into perorigin_v1).")

# %% [markdown]
# ### Figure 4 — Per-origin selection architecture
#
# For each origin of dichromatism that contains enough sequenced species to test, the figure below
# shows which panel genes shifted in selection and in which module. Full caption follows the figure.

# %%
# QC gate (from the cluster's pooled-RELAX evaluation): a per-origin hit with an extreme K
# (K>20 or K<0.05) that is NULL in the pooled analysis is a boundary artifact and is dropped
# (e.g. HPS4: per-origin K=30 but pooled K=1.05, p_BH=1.0). Bars are plotted at the pooled K where
# a pooled estimate exists (so a boundary K is shown at its de-inflated value), and marked by
# whether the pooled analysis corroborates the hit.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
_arch = os.path.join(SYN, "figures", "nb15_per_origin_arch.png")
POOL = load_input("relax_pooled")
if PER_ORIGIN is not None and "p_BH" in PER_ORIGIN.columns:
    _labels = {"origin_7": "Trachypithecus\n(origin 7, 8 tips)",
               "origin_8": "Nomascus\n(origin 8, 3 tips)",
               "origin_14": "Eulemur\n(origin 14, 2 tips)"}
    _sig = PER_ORIGIN[PER_ORIGIN.p_BH < 0.05].copy()
    _gmod = PER_ORIGIN.drop_duplicates("gene").set_index("gene")["module"].to_dict()
    _mc = {"pigmentation": "#c0662e", "hormone": "#3b6ea5"}
    # pooled lookup for QC + de-inflation
    _pl = POOL.set_index("gene")[["K", "p_BH"]].to_dict("index") if POOL is not None else {}

    def _keep(row):  # drop boundary-K hits that pooled analysis calls null
        k = row["K"]; pk = _pl.get(row["gene"], {})
        boundary = (k > 20) or (k < 0.05)
        pooled_null = pk.get("p_BH", 0) > 0.05
        return not (boundary and pooled_null)

    _sig = _sig[_sig.apply(_keep, axis=1)].copy()
    # plot K: use pooled K when the per-origin K is boundary-inflated and a pooled value exists
    def _plotK(row):
        k = row["K"]; pk = _pl.get(row["gene"], {})
        if (k > 20 or k < 0.05) and "K" in pk and pk["K"] == pk["K"]:
            return pk["K"]
        return k
    _sig["plotK"] = _sig.apply(_plotK, axis=1)
    _sig["corrob"] = _sig["gene"].map(  # pooled corroborates the intensification/relaxation?
        lambda g: _pl.get(g, {}).get("p_BH", 1.0) < 0.05)

    _origs = [o for o in _labels if o in PER_ORIGIN.origin_id.values]
    fig, axes = plt.subplots(1, len(_origs), figsize=(4.5 * len(_origs), 5.4),
                             gridspec_kw={"wspace": 0.6})
    if len(_origs) == 1:
        axes = [axes]
    for ax, o in zip(axes, _origs):
        s = _sig[_sig.origin_id == o].copy()
        if len(s) == 0:
            ax.text(0.5, 0.5, "no gene passes\np(BH) < 0.05", ha="center", va="center",
                    transform=ax.transAxes, fontsize=12, color="#7f8c8d", style="italic")
            ax.set_title(_labels[o], fontsize=12, fontweight="bold"); ax.axis("off"); continue
        s["logK"] = np.log2(s["plotK"].clip(lower=0.05))
        s = s.sort_values(["module", "logK"])
        y = np.arange(len(s))
        # filled bar = pooled-corroborated; hatched/pale = origin-specific (not corroborated pooled)
        for yi, (_, r) in zip(y, s.iterrows()):
            col = _mc[_gmod.get(r.gene, "pigmentation")]
            ax.barh(yi, r["logK"], color=col if r["corrob"] else "white",
                    edgecolor=col, linewidth=1.6, height=0.7,
                    hatch=None if r["corrob"] else "///")
        ax.set_yticks(y); ax.set_yticklabels(s.gene, fontsize=9, fontstyle="italic")
        ax.axvline(0, color="black", lw=0.8)
        ax.set_title(_labels[o], fontsize=12, fontweight="bold")
        ax.set_xlabel("log$_2$ K (selection intensity)", fontsize=9)
        # directional cues placed on the side they describe: relaxed to the LEFT, intensified RIGHT
        ax.annotate("← relaxed", xy=(0, -0.14), xycoords="axes fraction",
                    ha="left", va="top", fontsize=8, color="#555")
        ax.annotate("intensified →", xy=(1, -0.14), xycoords="axes fraction",
                    ha="right", va="top", fontsize=8, color="#555")
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Per-origin selection architecture: which genes shift, in which module",
                 fontsize=13, fontweight="bold", y=1.03)
    fig.legend(handles=[Patch(facecolor=_mc["pigmentation"], edgecolor="black", label="pigmentation"),
                        Patch(facecolor=_mc["hormone"], edgecolor="black", label="hormone"),
                        Patch(facecolor="white", edgecolor="#555", hatch="///",
                              label="not corroborated by pooled RELAX (origin-specific)")],
               loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.10), fontsize=9)
    fig.savefig(_arch, dpi=150, bbox_inches="tight")
    plt.show()
    print("dropped as boundary+pooled-null:",
          sorted(set(PER_ORIGIN[PER_ORIGIN.p_BH < 0.05].gene) - set(_sig.gene)) or "none")
else:
    print("Per-origin architecture figure builds when the tables are present.")

# %% [markdown]
# **Figure 4. Genes under selection at each independent origin of dichromatism.**
#
# *What the data are.* We scanned a curated panel of ~110 pigmentation and sex-hormone genes
# (built and justified in NB14) for signatures of natural selection, using coding sequences
# extracted from 117 published primate genomes. Selection was tested with **RELAX** (HyPhy), which
# asks whether selection on a gene became *stronger* (intensified) or *weaker* (relaxed) along a
# specified set of branches; its statistic *K* summarises that shift, and we plot log₂ K so that
# intensification (K > 1) and relaxation (K < 1) are symmetric about zero. Values are read from
# `results/perorigin_v1/per_origin_K.csv` (per-origin fits) cross-checked against
# `relax_pooled_results.csv` (all origins pooled).
#
# *What the panels are.* Dichromatism arose ~15 times (§3), but only origins containing **≥ 2
# sequenced dichromatic species** have enough branches to test — three do, one panel each:
# *Trachypithecus* (origin 7, 8 tips), *Nomascus* (origin 8, 3 tips) and *Eulemur* (origin 14, 2
# tips); the heading of each panel gives its origin ID and the number of sequenced species (tips)
# it contains. The other ~12 origins are single species and cannot be tested this way.
#
# *How to read a bar.* Each bar is one gene that shifted significantly in selection at that origin
# (Benjamini–Hochberg p_BH < 0.05). Bar length = log₂ K: bars pointing **right** = selection
# **intensified**, bars pointing **left** = selection **relaxed** (the ← relaxed / intensified →
# guides sit under each axis). Colour = which module the gene belongs to (**orange = pigmentation,
# blue = sex-hormone**). **Solid** bar = the shift is also significant in the independent pooled
# analysis (corroborated); **hatched** bar = significant only within that one origin, so weaker
# evidence. A panel reading *"no gene passes p(BH) < 0.05"* (Eulemur) means no gene reached
# significance there — not that the origin is absent.
#
# *What it shows.* The three origins use **different, non-overlapping gene sets** (quantified in
# §6): *Trachypithecus* recruits many genes from both modules, *Nomascus* a small pigmentation set
# (HRAS, POMC, HGF), and *Eulemur* none. There is no shared "dichromatism gene" — each origin
# reached the same phenotype through different parts of the coupled system.
#
# **QC.** Per-origin RELAX can return an extreme boundary K on a single origin's few branches.
# We cross-check every per-origin hit against the pooled RELAX fit and drop any whose extreme K
# is null when pooled — **HPS4** is the clear case (per-origin K ≈ 30 in *Trachypithecus* but
# pooled K = 1.05, p_BH = 1.0), so it is removed as a boundary artifact. **HRAS** is the opposite:
# its per-origin K is boundary-inflated, but pooled RELAX gives a clean K = 4.3 (p_BH = 4×10⁻⁶),
# so it is retained and plotted at the pooled value. Bars are drawn at the pooled K wherever a
# per-origin K is boundary-inflated, so the figure shows de-inflated, corroborated effect sizes.

# %% [markdown]
# ## 5 — Module balance per origin, corrected for panel composition
#
# When dichromatism evolved at a given origin, was the selection concentrated in **pigmentation**
# genes, in **sex-hormone** genes, or split between the two? This section answers that with a
# single number per origin — the *module balance* — and shows it in the table below.
#
# **The metric.** For each origin, module balance = (nP − nH) / (nP + nH), where nP and nH are
# the pigmentation and hormone genes under episodic selection along the origin's branches
# (−1 = every selected gene is a hormone gene, +1 = every selected gene is a pigmentation gene,
# 0 = an even split).
#
# **The correction.** The raw panel is not module-balanced by count: the hormone module was
# assembled as a whole endocrine pathway while the pigmentation module began as the canonical
# melanogenesis core, so a *neutral* lineage does not sit at 0. The clean-30 pigmentation
# expansion (NB14) brings the panel to 57 pigmentation + 53 hormone genes — a **count** balance of
# +0.036 — but for per-origin balance the correct denominator is a **per-gene selection rate**, not
# a raw count, so that an origin is not scored pigmentation-leaning simply because more
# pigmentation genes were tested. This section computes balance as a rate ratio; NB14's +0.036 is
# the panel's *count* balance and is not the same quantity (the two must not be conflated).
#
# **Table 2.** Module balance for each testable origin. `sigP`/`sigH` = number of pigmentation /
# hormone genes under selection; `rateP`/`rateH` = those counts divided by how many genes of each
# module were actually tested (the panel-composition correction); `rate_balance` = the headline
# number, running from −1 (all hormone) through 0 (even) to +1 (all pigmentation). `count_balance`
# is the same idea without the correction, shown alongside so the effect of correcting is visible.
# NaN means no gene of either module reached significance at that origin.

# %%
# Module balance as a per-gene selection RATE per origin, using the module column the collector
# adds to perorigin_v1. rate_M = (genes of module M with p_BH<0.05) / (genes of module M tested);
# balance = (rate_P - rate_H) / (rate_P + rate_H), in [-1 (hormone), +1 (pigmentation)].
if PER_ORIGIN is not None and "module" in PER_ORIGIN.columns and "p_BH" in PER_ORIGIN.columns:
    bal_rows = []
    for o in sorted(PER_ORIGIN.origin_id.unique()):
        sub = PER_ORIGIN[PER_ORIGIN.origin_id == o]
        tP = sub[sub.module == "pigmentation"].gene.nunique()
        tH = sub[sub.module == "hormone"].gene.nunique()
        sP = sub[(sub.module == "pigmentation") & (sub.p_BH < 0.05)].gene.nunique()
        sH = sub[(sub.module == "hormone") & (sub.p_BH < 0.05)].gene.nunique()
        rP = sP / tP if tP else 0.0
        rH = sH / tH if tH else 0.0
        bal = (rP - rH) / (rP + rH) if (rP + rH) > 0 else float("nan")
        cbal = (sP - sH) / (sP + sH) if (sP + sH) > 0 else float("nan")
        bal_rows.append(dict(origin=o, sigP=sP, sigH=sH,
                             rateP=round(rP, 3), rateH=round(rH, 3),
                             rate_balance=round(bal, 3), count_balance=round(cbal, 3)))
    BAL = pd.DataFrame(bal_rows)
    print(BAL.to_string(index=False))
    print("\nRate balance: +1 = purely pigmentation, -1 = purely hormone, NaN = no gene significant.")
    print("count_balance shown alongside to expose where the panel-composition correction matters.")
    print("NB14's +0.036 is the whole-panel COUNT balance (a different quantity - do not conflate).")
else:
    print("Awaiting per-origin tables with module + p_BH columns.")

# %% [markdown]
# ## 5b — POMC at the pigmentation–hormone interface
#
# The module-balance metric (§5) scores each gene into exactly one module, and the panel assigns
# **POMC to pigmentation** (receptor_signaling; OMIM hypopigmentation phenotype). That is defensible
# — POMC is the precursor of α-MSH, the MC1R ligand that drives eumelanin — but it is only half of
# POMC's biology. The same pro-hormone is cleaved into **ACTH and β-endorphin**, the HPA-axis and
# opioid peptides. POMC is therefore a genuine **interface gene**: a single locus whose products
# act in both the pigmentation and the endocrine modules. A one-module label is an accounting
# choice, not a statement that POMC is "not hormonal."
#
# So POMC is worth a dedicated cross-primate view, independent of which module bucket it lands in.
# Below we ask where in the order POMC itself is under selection — not just within the three
# powered origins, but across every branch the full-panel aBSREL scan covers.
#
# **What the data show.** POMC shows a significant per-origin RELAX **intensification** in
# *Nomascus* (origin 8; K = 3.4, p_BH < 0.001 — selection intensified, not relaxed) and episodic
# diversifying selection (aBSREL, corrected p < 0.05) on **five branches**. Figure 5b shows these
# explicitly, coloured by dichromatism state, because the pattern is mixed and that mix is the
# point: two of the selected tips — *Nomascus concolor* and *N. gabriellae* — are **dichromatic**
# and fall exactly on the origin-8 lineage, but a third, *Macaca mulatta*, is **monochromatic**,
# and the two remaining selected branches are internal *Macaca* clades — resolved from the POMC
# gene tree in the aBSREL output (one an 8-species macaque clade that is 12% dichromatic, one a
# 2-species clade with no dichromatic members), i.e. an essentially monochromatic macaque
# radiation. (HYPHY labels internal branches "NodeNN" in each gene's own tree; those numbers are
# not comparable across genes, so the figure names the clade each subtends rather than the raw
# label.) So POMC is under selection on the origin-8 dichromatic lineage,
# **but selection on POMC is not confined to dichromatic lineages** — the same conclusion the
# whole-panel aBSREL scan reached (episodic selection hits dichromatic and monochromatic tips at
# indistinguishable rates). The reading is: POMC is an interface gene evolving in several primate
# lineages, one of which (the *Nomascus* gibbons) is a dichromatism origin. That co-localisation
# is a concrete follow-up target, not evidence that POMC *causes* the phenotype — aBSREL marks
# lineage-specific selection, not causation, and the *Macaca* signal shows the two do not track
# each other one-to-one.

# %% [markdown]
# ### Figure 5b — POMC selection across the primate order
#
# The figure below asks where in the primate order POMC — a gene at the pigmentation–hormone
# interface — is itself under selection, and whether those branches are the dichromatic ones. Full
# caption follows the figure.

# %%
from IPython.display import Image, display
_pomc = os.path.join(SYN, "figures", "nb15_pomc_tree.png")
if os.path.exists(_pomc):
    display(Image(filename=_pomc))
else:
    print("nb15_pomc_tree.png not built yet - run nb15_pomc.R")

# %% [markdown]
# **Figure 5b. Selection on POMC across the primate order.**
#
# *What the data are.* POMC coding sequence from the 117 sequenced primate genomes, tested for
# selection with **aBSREL** (HyPhy), which scans *every* branch of the tree and flags the ones
# showing *episodic* positive selection — a burst of adaptive change confined to that branch.
# Results are from `results/full_panel_117/absrel/POMC.ABSREL.json`. POMC is singled out because
# it sits at the pigmentation–hormone interface (α-MSH drives pigment; ACTH/β-endorphin are
# hormones), so if it were the gene coupling the two modules to produce dichromatism, its selected
# branches should be the dichromatic ones.
#
# *How to read the two panels.* **(A)** The 224-species tree (as in Fig 3). Each tip is coloured by
# its coded dichromatism state (**red = dichromatic, grey = monochromatic**); every branch that
# aBSREL flags as under selection carries a **star** — **red star** if that branch is dichromatic,
# **dark star** if monochromatic. **(B)** The five selected branches ranked by significance; the
# x-axis is **−log₁₀(corrected p-value)**, so longer bars = stronger evidence, and each bar is
# labelled by the branch's dichromatism state.
#
# *What it shows.* Of the five POMC-selected branches, only two are dichromatic (the *Nomascus*
# gibbons *N. concolor* and *N. gabriellae*); the other three are monochromatic macaque lineages —
# the *M. mulatta* tip and two internal *Macaca* clades (labelled by the clade each contains, since
# aBSREL's internal "NodeNN" names are per-gene and not comparable across genes). So POMC selection
# overlaps one dichromatism origin (the gibbons) but is **not** confined to dichromatic lineages —
# the same lesson as the whole-panel branch scan.

# %% [markdown]
# **Table 3.** POMC's per-origin RELAX result, read from `results/perorigin_v1/per_origin_K.csv`.
# One row per testable origin: `module` = the panel's module assignment for POMC (pigmentation);
# `K` = the RELAX selection-intensity statistic (K > 1 intensified, K < 1 relaxed); `p_BH` =
# Benjamini–Hochberg-corrected p-value. POMC is significantly intensified at the *Nomascus* origin
# (origin 8, K ≈ 3.4, p_BH < 0.001) and not at the others — the per-origin counterpart to the
# branch-level scan in Fig 5b.

# %%
# POMC-specific selection evidence, printed from the frozen tables (panel-agnostic).
if PER_ORIGIN is not None:
    pk = PER_ORIGIN[PER_ORIGIN.gene == "POMC"][["origin_id", "module", "K", "p_BH"]]
    print("POMC per-origin RELAX:")
    print(pk.to_string(index=False))
if BRANCH is not None and "absrel_corrected_p" in BRANCH.columns:
    pb = BRANCH[BRANCH.gene == "POMC"].copy()
    pb["cp"] = pd.to_numeric(pb["absrel_corrected_p"], errors="coerce")
    sel = pb[pb.cp < 0.05][["branch", "is_tip", "cp"]]
    print(f"\nPOMC branches under episodic selection (aBSREL corrected p<0.05): {len(sel)}")
    print(sel.to_string(index=False))

# %% [markdown]
# ## 6 — Convergence and divergence across independent origins
#
# **The question.** If dichromatism arose ~15–19 times, do independent origins reach it through
# the *same* genes (molecular convergence) or *different* ones (divergence)? This is the natural
# test of the two-module hypothesis: convergence would say there is one genetic route;
# divergence would say the coupled system can be perturbed at many points to the same phenotypic
# end.
#
# **Method and framing.** For each powered origin the gene set is those panel genes with
# a significant per-origin selection-intensity shift (RELAX K, p_BH < 0.05); overlap between
# origins is the shared-gene count. On the current panel (size printed by the cell below; the
# clean-30 expansion is still landing), only **two** of the three powered origins carry a
# detectable signal — *Trachypithecus* (a multi-gene, both-module set) and *Nomascus* (a small
# all-pigmentation set: HGF, HRAS and POMC, the last classified as pigmentation in the panel) —
# and they share **zero** genes; *Eulemur* has none passing
# threshold.
# So where the comparison is well-powered it shows **divergence, not convergence**: independent
# origins are built through different genes.
#
# This is stated as divergence-where-powered, not as a clade-wide "no convergence" claim, because
# the test is **power-limited**: with only two signalled origins, and the ~13–17 single-tip
# origins recoverable only by branch scans (not per-origin RELAX), a broader convergence null
# cannot be tested here. The overlap is recomputed live below and refreshes to 110 genes when the
# clean-30 expansion lands (which can only *add* genes to an origin's set, so the zero-overlap
# divergence result is robust unless a new gene happens to hit both origins).

# %% [markdown]
# **Table 4.** Gene-set overlap between the independent origins, computed from the significant
# genes (p_BH < 0.05) in `results/perorigin_v1/per_origin_K.csv`. For each powered origin the
# printout lists its selected gene set, then reports the intersection between every pair of
# signalled origins. "ZERO overlap" means the two origins share no gene under selection — direct
# evidence of *divergence* (different molecular routes to the same phenotype) rather than
# convergence. Only two of the three tested origins carry a multi-gene signal, so this comparison
# is power-limited (see the prose above); it is reported as divergence-where-powered, not a
# clade-wide claim.

# %%
# Per-origin gene-set overlap from the CURRENT perorigin_v1 tables (pre-expansion run; the
# printed panel size is the number of genes with RELAX results, refreshing to 110 when the
# clean-30 expansion lands). Gene set per origin = genes with p_BH<0.05.
import itertools
if PER_ORIGIN is not None and "p_BH" in PER_ORIGIN.columns:
    sig = PER_ORIGIN[PER_ORIGIN["p_BH"] < 0.05]
    sets = {o: set(sig[sig.origin_id == o].gene) for o in sorted(sig.origin_id.unique())}
    powered = sorted(PER_ORIGIN.origin_id.unique())
    print(f"powered origins tested: {powered}  (>=2 dichromatic tips each)")
    for o in powered:
        g = sorted(sets.get(o, set()))
        print(f"  {o}: {len(g)} genes under selection (p_BH<0.05) - {g if g else '(none pass threshold)'}")
    print()
    signalled = [o for o in powered if sets.get(o)]
    if len(signalled) >= 2:
        for a, b in itertools.combinations(signalled, 2):
            inter = sets[a] & sets[b]
            print(f"  {a} n {b}: {len(inter)} shared genes - {sorted(inter) if inter else 'ZERO overlap'}")
    else:
        print("  Only one origin carries a detectable multi-gene signal; a molecular-convergence")
        print("  test needs >=2 signalled origins, so the comparison is power-limited (see prose).")
    print(f"\n(Current: {PER_ORIGIN['gene'].nunique()}-gene panel. Refreshes when clean-30 lands -> 110 genes.)")
else:
    print("Awaiting per-origin tables with p_BH for the overlap recompute.")

# %% [markdown]
# ## 7 — Synthesis
#
# Sexual dichromatism in primates is a **labile, polygenic trait built from two coupled modules**.
# It has arisen on the order of 15–19 times and is lost far faster than it is gained (§3). At the
# two origins where its genetic basis can actually be tested, the signalled gene sets do not
# overlap (§4, §6) and differ in module balance (§5) — divergence where the comparison is powered.
# Whether origins differ *systematically* in architecture across the clade is an open question the
# current sampling cannot resolve (only two of ~15–19 origins carry a per-origin signal), so it is
# framed as underpowered rather than claimed.
#
# **What the sequence data add, beyond the tree.** The lability and origin count (§3) come from
# phenotype and phylogeny alone. The genetics answers what those cannot: *which* molecular change
# accompanied each origin. Three results here require sequence data and would be invisible to a
# tree-only analysis — (1) **MC1R, the gene birds use again and again for dichromatism, is not the
# primate route** (no pooled signal, K = 0.45; it surfaces in one lineage only); (2) the two
# testable origins recruited **non-overlapping gene sets** from both the pigmentation and the
# hormone module (§4, §6); and (3) **POMC**, a gene that sits at the pigment–hormone interface, is
# itself under selection at one origin (§5b). Together these say a trait built one way in birds is
# built *many different ways* in primates, drawing on a coupled pigmentation–hormone system rather
# than a single master gene.
#
# This is exactly what a network framing predicts and a single-gene framing would miss: if
# dichromatism is the output of a coupled system, there are many points at which it can be pushed
# to produce (or lose) the phenotype, and different lineages have used different ones. The panel
# that makes this testable — which genes, and why — is built in **NB14**, with the hormone layer
# developed in **NB13**. The selection evidence is strongest for the three powered origins; the
# single-tip origins and the convergence test are power-limited and framed as such.
