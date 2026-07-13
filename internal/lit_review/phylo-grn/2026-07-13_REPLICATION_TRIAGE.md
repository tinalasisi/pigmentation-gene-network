# REPLICATION TRIAGE — what we can actually run

**Written:** 2026-07-13. Companion to `2026-07-13_METHODS_MAP_phylo_grn.md`.
Question answered here: *of the 60 methods in the map, which ones run on assets already in this repo, and
what would they tell us?*

---

## The constraint nobody has written down yet

I checked the actual overlap between our two main assets, and it is the thing that decides this whole plan:

| Asset | Genes | Path |
|---|---|---|
| Core melanogenesis network (signed, directed) | **168** nodes, 309 edges | `data/processed/gene_network_{nodes,edges}.csv` |
| Substrate/extended network + node features | **803** genes × 74 features | `internal/network-evo-explore/output/feature_table.csv` |
| **Primate selection panel** (RELAX K per gene) | **77** genes | `comparative-genomics/results/full_panel_117/relax_results.csv` |
| Per-branch aBSREL (9,229 branch tests) | **78** genes | `comparative-genomics/results/perorigin_v1/branch_rates.csv` |
| Per-origin RELAX K | 76 genes × **3** origins | `comparative-genomics/results/perorigin_v1/per_origin_K.csv` |

> ### ⚠ The overlap between the primate selection panel and the core network is **16 genes**.
> (26 against the 803-gene substrate.) `DCT, EDNRB, KIT, KITLG, LEF1, MC1R, MITF, MLANA, OCA2, PAX3, PMEL, POMC, …`

Every network-level selection test in §7 of the map — signet, HotNet, PicMin, SUMSTAT — needs **a selection
statistic on the network's nodes**. We have one on 16 of 168. So the honest position is:

**This is a data-coverage gap, not a methods gap.** The methods exist, they are mature, they are free, and
they are waiting. The single highest-leverage action in this entire review is not to read another paper — it
is to **extend the miniprot → MAFFT → HyPhy panel from 117 genes to all 168 core network nodes** (and ideally
the 803-gene substrate). The pipeline already exists and already ran; this is more of the same compute, not
new engineering. Once per-gene primate selection statistics cover the network, four tools light up at once.

There is a real intermediate, though — see Track B.

---

## Track A — the unlock (do this first)

**Extend the selection panel to cover the network.** 168 core nodes (+ as much of the 803 substrate as the
compute allows). Same Great Lakes protocol as `comparative-genomics/02b`/`02c`.

Then, in order:

### A1. `signet` — Gouy, Daub & Excoffier 2017 (PMID 28934485) · **top pick**
Simulated annealing searches the network for the **connected subnetwork** carrying the most unusual aggregate
selection signal. Eats: per-gene score + node/edge list. Both are CSVs we already have the shape of.

**What it would tell us:** our current finding is *"different genes in different origins, no shared
signature."* signet asks the next question directly — **do those different genes sit in the same connected
region of the melanogenesis graph?** A significant subnetwork that recurs across origins, built from
non-overlapping gene sets, would convert a negative result into a positive one. That is the paper.

### A2. `PicMin` — Booker, Yeaman & Whitlock 2023 (PMID 36626817) · **top pick**
Order-statistics test: is a gene ranked unusually high across **more independent lineages than chance
predicts**? Power *rises* with lineage count even when each lineage is individually weak — which is precisely
our situation (11 of 15 origins are single tips).

**Input we already have:** `per_origin_K.csv` is nearly PicMin-shaped already (origin × gene × p-value); it
currently covers only the 3 multi-tip origins. `branch_rates.csv` can be pivoted to recover the 11 single-tip
origins as branches. **Caveat, stated plainly:** PicMin's null assumes ranks drawn from a large gene universe.
With a 117-gene candidate panel, ranks are relative to the panel, not the genome — this weakens the test and a
reviewer will say so. Expanding the panel (Track A) fixes this too. Run it genome-wide if the compute allows;
otherwise report it as a within-panel enrichment and be explicit.

### A3. `Hierarchical HotNet` — Reyna, Leiserson & Raphael 2018 (PMID 30423088)
Heat diffusion over the network + a **hierarchy** of significantly altered subnetworks across scales, with
degree-bias correction built in. Complements signet: signet finds *one* optimal subnetwork, HotNet returns the
multi-scale structure and tells you which scale is significant. Read **Visonà 2024** (PMID 38340090) first —
it is the practical guide to the design choices (seed scores, network density) that decide whether this works.

### A4. `SUMSTAT` — Daub et al. 2013 (PMID 23625889)
The simplest version: sum per-gene selection stats over the pathway, test against size-matched random gene
sets. ~40 lines of R, no package. **Run it first anyway** — it is the sanity check that tells you whether
there is any pathway-level signal at all before you spend a week on subnetwork search.

---

## Track B — runnable *this week*, no new compute

The `feature_table.csv` (803 genes × 74 columns) already carries **network position** (degree, betweenness,
PageRank, k-core, eigenvector, module, `dist_to_output`, `pathsign_to_output`) *and* **evolutionary /
population-genetic statistics** (`mean_phylop_100way`, PBS ×4, FST ×5, π ×5, LOEUF incl. ancestry-specific,
tissue breadth, τ) for **all 803 genes**.

That is a complete, ready dataset for the §6 question — *does network position predict evolutionary
constraint?* — with **zero new compute**.

- **Replicate Fraser 2002 / Hahn & Kern 2005 on the melanogenesis network** (PMIDs 11976460, 15616139).
  Do hubs have lower LOEUF? Does betweenness predict phyloP? Does `dist_to_output` (upstream regulator →
  downstream effector, the Stern & Orgogozo axis) predict constraint? This is a same-day analysis and it
  either confirms the classic result in our system — which licenses the network-position framing — or it
  doesn't, which is itself interesting and needs to be known *before* Track A is designed around it.
- **Use the signed, directed structure.** `pathsign_to_output` and edge sign are exactly what **Petit et al.
  2023** (PMID 37070537) simulate. Almost nobody has empirical signed-network position data to test their
  prediction against. We do.
- **Ancestry-stratified LOEUF** (`LOEUF_AFR/EAS/SAS/NFE`) crossed with network position is, as far as this
  review found, **unprecedented** — no paper in §6 has population-stratified constraint on a signed network.
- Caveat to state up front: these are **human population-genetic** statistics. Track B answers *"is network
  position associated with constraint in humans?"* — a real question, but **not** the primate-phylogeny
  question. Do not let the two get conflated in writing. Track B is a rehearsal and a publishable sub-result;
  Track A is the thesis.

---

## Track C — cheap methodological upgrades to work already done

| Do | Instead of / in addition to | Why |
|---|---|---|
| **TRACCER** (PMID 34324001) | the existing RERconverge run (`04`) | RERconverge weights all branches alike; TRACCER weights by topological proximity to the common ancestor, so **scattered single-tip origins stop inflating the convergence signal**. With 11 of our 15 origins being single tips, this is the more defensible test — and it is a near-free re-run on the same inputs. |
| **Forward Genomics** (PMID 23022484) | — | Built for matching *independent phenotype losses* to genomic change. We found dichromatism is **lost ~9× more readily than gained** — the loss signal is the stronger one in our data and we are currently not using it at all. |
| **PhyloAcc** (PMID 30851112) | coding-only aBSREL/RELAX | Asks whether **regulatory/noncoding elements** near melanogenesis genes accelerate on dichromatic branches. Our whole thesis is that the action is regulatory; every test we have run so far is on coding sequence. This is the most conspicuous mismatch between our claim and our evidence. |
| **PhyloAcc-C** (PMID 38656999) | binary trait coding | Handles dichromatism as a **continuous** score rather than a binary — we have raw trait scores, and binarizing throws information away. |
| **Conte et al. 2012** (PMID 23075840) | — | Gives the **expected** probability of gene-level parallelism at a given divergence depth (0.8 for young splits, 0.1–0.4 for old). Our "no shared genetic signature" result is currently uncalibrated: at primate divergence depths, *how much parallelism should we have expected?* If the answer is "almost none," our negative result is unsurprising and needs the network-level reframing to be interesting. **Run this calculation before deciding how to frame the finding.** It is arithmetic, not compute. |

---

## Track D — expensive, probably not now

Inferring **per-species GRNs** and comparing them (§8 of the map: SCENIC+, MRTLE, OrthoClust, NetRep,
ANANSE's differential network score). This is the scientifically ideal version of the project and it needs
matched cross-species expression/ATAC in melanocytes across primates, which as far as this review found **does
not exist**. Costed here so the option is declined deliberately rather than by omission. If a collaborator
turns up with primate melanocyte multiome data, this becomes Track A.

---

## The three papers to actually read

1. **Badyaev et al. 2015** (PMID 26289047) — carotenoid network topology predicts repeated color evolution
   across birds. Same three ingredients as our design. **Read it first.** Every framing of our contribution
   has to survive it — and it is also the proof that the argument can be made and published.
2. **Gouy, Daub & Excoffier 2017** (PMID 28934485) — the method that most directly answers our question.
3. **Conte et al. 2012** (PMID 23075840) — the calibration our negative result is missing.

## Recommended order

```
  Conte 2012 arithmetic  ──► is our negative result even surprising?
            │
            ▼
  Track B (no compute)   ──► does network position predict constraint here at all?
            │                 ├─ yes → the network-position framing is licensed
            │                 └─ no  → find out NOW, not after the panel expansion
            ▼
  Track C: TRACCER re-run ──► a more defensible convergence test, ~free
            │
            ▼
  Track A: expand panel 117 → 168+ genes ──► signet + PicMin + HotNet
            │
            ▼
                       the network-level claim
```

Track B and the Conte calculation cost days, not weeks, and both can *falsify the premise* of Track A before
we spend cluster time on it. That ordering is the point.
