# RUN SPEC → greatlakes-hpc: per-origin dN/dS architecture of primate dichromatism

**From:** claude-science / mol-evo-specialist (frame fb237c45)
**To:** claude-code / greatlakes-hpc
**Date:** 2026-07-13T00:40:25Z
**Repo:** github.com/tinalasisi/pigmentation-gene-network — branch `main`

---

## Why this run exists (the science, in one paragraph)

The pooled RELAX in `results/full_panel_117/` tags **all 24 dichromatic tips as one
`{Test}` foreground**. That design can only detect a selection shift shared by *every*
origin of dichromatism — it presupposes a convergent molecular architecture. The new
question is the opposite: **is the genetic architecture of sexual dichromatism heterogeneous
across the independent origins?** In birds dichromatism is ~monogenic (MC1R); in primates it
is already not MC1R and looks distributed. Hypothesis: different pigmentation × hormone gene
combinations produce dichromatism in different lineages, which is why the trait is labile
(gain in one clade, loss in another when either component drifts). This run produces the
three dN/dS layers that test that: **(A) per-branch ω (aBSREL), (B) per-origin RELAX,
(C) RERconverge relative-rate convergence.**

---

## CRITICAL power reality — read before running Stage C

The independent-origins audit resolved **14 genomic origins** (not 4), and **11 of the 14 are
single-tip**. Per-origin RELAX needs ≥2 foreground tips to be identifiable, so **Stage C
(per-origin RELAX) is only powered for 3 origins**:

| origin_id | n tips | species |
|---|---|---|
| origin_7 | 8 | *Trachypithecus* (auratus, cristatus, francoisi, geei, johnii, obscurus, phayrei, pileatus) |
| origin_8 | 3 | *Nomascus* (concolor, gabriellae, leucogenys) |
| origin_14 | 2 | *Eulemur* (flavifrons, macaco) |

The other 11 origins are single genomic tips (`origin_1..6, 9..13`). `02c` will emit
`underpowered_fgN` for them and NOT fit — this is correct, not a failure. **This is exactly why
the run has three layers**: per-origin RELAX (Stage C) characterizes the 3 multi-tip origins;
**aBSREL (Stage A) recovers every single-tip origin as an individual branch** (a per-branch ω +
episodic-selection test needs no ≥2-tip foreground); **RERconverge (Stage R) uses relative
rates across all branches** and asks whether the origins accelerate the same genes without any
per-origin foreground/background split. Report all three; do not treat the 11 single-tip
origins as missing data — they are covered by A and R.

## The paste-back contract (unchanged)

You have data; the chat does not. After each stage, **commit the small report CSV/MD +
`git push`**, and paste the report file back into the chat. Never send alignments, genomes,
or JSON blobs. The exact files to paste are named per-stage below.

---

## Two rounds — the pipeline is roster-parameterized

Everything keys off a **tip-roster / accession list**. Round 1 runs NOW on the existing
117-set. Round 2 re-runs the identical code on an expanded roster once new genomes are in.
**Do Round 1 first and paste results back before starting Round 2.**

| | Round 1 (run now) | Round 2 (after genome expansion) |
|---|---|---|
| accessions | `config/accessions_all_recoverable.csv` (117) | `config/accessions_v2.csv` (117 + new) |
| origin map | `config/origin_assignments.csv` (from phylo audit, incoming) | same file, regenerated with new tips |
| everything else | identical scripts, identical output dirs (namespaced by `$WORK`) | identical |

Round 2 target accessions (Hoolock, Cebidae reinforcement, unsampled-family scan) arrive in a
**separate note** — do not block Round 1 on them.

---

## Inputs you need (all in-repo except one incoming file)

| file | status | role |
|---|---|---|
| `comparative-genomics/config/accessions_all_recoverable.csv` | in repo | 117 genomes |
| `comparative-genomics/config/gene_panel.csv` | in repo | 80 genes (gene,category,set) |
| `comparative-genomics/config/leakey_primate_tree.nex` | in repo | species tree (superset of tips) |
| `comparative-genomics/config/species_states.csv` | in repo | pooled foreground (dichromatic/monochromatic) |
| `comparative-genomics/config/origin_assignments.csv` | **INCOMING** | per-origin foreground map — **required for stage C-per-origin only**; A and B do not need it |
| `comparative-genomics/refs/reference_proteins.faa` | in repo | miniprot query set |

**`origin_assignments.csv`** (columns: `species, family, origin_id, dichromatism_level,
n_genomic_tips_in_origin`) is being produced now by the phylogenetic-structure audit and will
be committed to `config/` in a follow-up push with its own note. **Stages A (aBSREL) and the
pooled RELAX do not depend on it — start those immediately.**

---

## Scripts (all in `comparative-genomics/scripts/`)

Existing, unchanged: `00_setup_env.sh`, `01_fetch_and_extract.sh`, `02_align_and_relax.py`
(pooled RELAX + all alignment/QC), `02b_branch_rates.py` (aBSREL per branch),
`03_report_summary.py`, `04_rerconverge.R`.

**New in this push:**
- `scripts/02c_per_origin_relax.py` — per-(gene,origin) RELAX. Reuses `codon_align` and
  `prune_tag_tree` from `02_align_and_relax.py` (imported directly, so alignment/QC is
  IDENTICAL). For each origin it tags that origin's tips `{Test}` and **drops the other
  origins' dichromatic tips** so the reference is purely monochromatic. Skips a (gene,origin)
  when the origin has <2 tips in that gene's alignment (single-tip foreground is
  unidentifiable — flagged `underpowered_fgN`).
- `scripts/slurm/absrel_array.sbatch` — one array task per gene for 02b.
- `scripts/slurm/per_origin_relax_array.sbatch` — flattened 2-D (gene × origin) array for 02c.

---

## Run order & exact commands

Set `WORK=/scratch/tlasisi_root/tlasisi0/tlasisi/runs/perorigin_v1` (or your convention) and
`REPO=$HOME/pigmentation-gene-network/comparative-genomics`. The `align` conda env
(hyphy 2.5.100, mafft 7.526, miniprot 0.18, ncbi-datasets 18.33.1, biopython, dendropy) is at
`/scratch/tlasisi_root/tlasisi0/tlasisi/envs/align`.

### Stage 0 — CDS (only if `cds/` not already staged for the 117-set)
```
cd $WORK
bash $REPO/scripts/01_fetch_and_extract.sh $REPO/config/accessions_all_recoverable.csv
```

### Stage 1 — pooled RELAX + alignments (produces aln/ that A and C reuse)
```
WORK=$WORK sbatch --array=1-80 $REPO/scripts/slurm/relax_array.sbatch
# after it finishes:
python $REPO/scripts/03_report_summary.py         # -> report/SUMMARY.md, report/summary.json
```
→ **paste back `report/SUMMARY.md`.** (This reproduces the pooled result as a baseline.)

### Stage A — per-branch ω (aBSREL), full panel — NO origin map needed, run in parallel with C-pooled
```
WORK=$WORK sbatch --array=1-80 --dependency=afterok:<relax_array_jobid> \
  $REPO/scripts/slurm/absrel_array.sbatch
# 02b writes report/branch_rates.csv incrementally; after the array:
python $REPO/scripts/02b_branch_rates.py --aln aln --out absrel --panel $REPO/config/gene_panel.csv
```
→ **paste back `report/branch_rates.csv`** (gene, branch, baseline_omega, absrel_corrected_p,
selected_flag). This is the "which branches, which genes" layer.
### Stage A — per-branch ω (aBSREL) — NO origin map needed, run in parallel with C-pooled
Two arrays exist; both apply the stop-codon/non-triplet cleaning aBSREL requires (stops→`---`,
trim to triplet, strip `{Test}` tags):
- `absrel_array.sbatch` — the **9 v3-certified genes** (`--array=1-9`), the focused "who" run.
- `absrel_full_panel_array.sbatch` — the **full 80-gene panel** (`--array=1-80`), needed for the
  network-painting view and as RERconverge's per-branch companion.
```
# certified 9 (fast):
WORK=$WORK sbatch --array=1-9  --dependency=afterok:<relax_array_jobid> $REPO/scripts/slurm/absrel_array.sbatch
# full panel:
WORK=$WORK sbatch --array=1-80 --dependency=afterok:<relax_array_jobid> $REPO/scripts/slurm/absrel_full_panel_array.sbatch
# then flatten all aBSREL JSONs to one tidy CSV:
python $REPO/scripts/02b_branch_rates.py --aln aln --out absrel --panel $REPO/config/gene_panel.csv
```
→ **paste back `report/branch_rates.csv`** (gene, branch, baseline_omega, absrel_corrected_p,
selected_flag). This is the "which branches, which genes" layer — and the layer that **recovers
all 11 single-tip origins** (each as its own tip branch), which Stage C cannot fit.
> aBSREL ω can blow up to a huge value on a branch with near-zero synonymous change — that is
> **undefined (dS≈0), not extreme positive selection**. Flag/drop such branches; read the
> episodic-selection test (corrected p), not raw ω, on those. (Seen on TFAP2A: *Macaca tonkeana*,
> *Mandrillus sphinx* — both monochromatic, non-selected.)

### Stage C — per-origin RELAX (needs `config/origin_assignments.csv`)
```
# N_ORIGINS = number of distinct origin_id values in origin_assignments.csv
N_ORIGINS=$(tail -n +2 $REPO/config/origin_assignments.csv | cut -d, -f3 | sort -u | wc -l)
WORK=$WORK N_ORIGINS=$N_ORIGINS \
  sbatch --array=0-$((80*N_ORIGINS-1)) $REPO/scripts/slurm/per_origin_relax_array.sbatch
# merge per-(origin,gene) QC + extract K:
python $REPO/scripts/03_report_summary.py --per-origin \
  --relax-dir relax_per_origin --qc-dir qc/per_origin   # writes report/per_origin_K.csv
```
→ **paste back `report/per_origin_K.csv`** (origin_id, gene, set, K, p_value, p_BH, n_fg,
status). **This is the primary deliverable** — it is the same-genes-or-different-genes matrix.

> `03_report_summary.py --per-origin` is **already implemented in this push**. It walks
> `relax_per_origin/<origin>/<gene>.RELAX.json`, pulls K + LRT p, joins the per-(origin,gene)
> QC rows from `qc/per_origin/`, BH-corrects **within each origin**, and writes
> `report/per_origin_K.csv`. Verified on a synthetic fixture. Pooled mode (no flag) is
> unchanged.

### Stage R — RERconverge (relative-rate convergence across origins)
`04_rerconverge.R` needs per-gene trees with branch lengths (the gene trees from the
alignments) and the binary/origin foreground. Run after Stage 1. Paste back its
`report/rer_results.csv` (gene, rho, p, p.adj). This is the independent cross-check on C:
RERconverge asks "do the origins accelerate the same genes?" without foreground/background
discretization per origin.

---

## Output layout (namespace everything under `$WORK`; commit only `report/*`)

```
$WORK/
  cds/<gene>/<species>.cds.fna
  aln/<gene>.codon.aln.fa , <gene>.tagged.nwk          # shared by pooled RELAX, aBSREL
  relax/<gene>.RELAX.json                               # pooled
  absrel/<gene>.ABSREL.json                             # Stage A
  relax_per_origin/<origin_id>/<gene>.RELAX.json        # Stage C
  qc/alignment_qc.csv , qc/per_origin/<origin>__<gene>.csv
  report/
    SUMMARY.md , summary.json                           # pooled (paste back)
    branch_rates.csv                                    # Stage A (paste back)
    per_origin_K.csv                                    # Stage C (paste back) — PRIMARY
    rer_results.csv                                     # Stage R (paste back)
```

## Round-trip protocol

- **OUTBOUND (me → you):** this note + the new scripts are pushed to `main`.
  `origin_assignments.csv` follows in a second push (own note) — safe to start A/pooled before it lands.
- **ON-CLUSTER (you):** run the stages above under `$WORK`; commit **only** `report/*` files
  (small) to `main` — never `aln/`, `cds/`, `*.json` (they're gitignored / too big).
- **INBOUND (you → me):** `git push` the `report/*` CSVs and paste them into the chat. I pull
  them into the notebook's frozen `analysis/data/` and regenerate the certified figures
  (per-origin K heatmap, per-branch ω tree, RERconverge scatter).
- **Branch convention:** commit results directly to `main` with message prefix
  `[hpc perorigin_v1]`. If a stage needs a code fix, I push to `main` and you `git pull` before
  re-running that stage only.

## QC / multiple-testing gates (apply before anything is called a hit)

- Reuse the notebook's existing gates: gap>25% reject; K>10 or K<1e-3 (boundary) reject;
  tree_len>50 reject; aln/ref ratio outside 0.8–1.2 reject.
- **Per-origin specific:** require n_fg≥2 in that gene (already enforced in 02c);
  BH-correct **within each origin** separately, not across the pooled matrix.
- aBSREL: use Holm-Bonferroni corrected p (already in the JSON) < 0.05 for episodic selection.
- A K→0 or K→∞ in a per-origin fit with tiny n_fg is an identifiability artifact, **not**
  extreme relaxation/intensification — flag, don't interpret.

## What NOT to do

- Do not add more Cercopithecine genomes in Round 2 (already over-represented; Trachypithecus
  is one origin sampled ~8×, which is the pseudoreplication we're correcting).
- Do not run the per-origin stage with a single-tip origin as a real result — report it as
  underpowered.
