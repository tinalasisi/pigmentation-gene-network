# Roster-parameterized two-round genome expansion

The whole pipeline keys off a **tip roster** (an accession list). Swapping the roster is the
only change needed to expand the taxon set — the scripts, gene panel, tree, foreground map,
and QC gates are identical across rounds.

## Round 1 — `roster_v1_accessions.csv` (117 genomes, runs NOW)

Verbatim copy of `accessions_all_recoverable.csv`: every genome recoverable at build time.
Four families (cercopithecidae 65, cebidae 33, lemuridae 10, hylobatidae 9). This is the
submittable roster — nothing blocks it. Run the full per-origin architecture pipeline on this
first (see the run-spec note in `internal/handoffs/notes/`).

## Round 2 — `roster_v2_targets.csv` (targeted additions)

Rerun the identical pipeline on `roster_v1 + roster_v2` once these genomes are fetched. The
targets were chosen from the independent-origins audit to fix the two real sampling gaps, NOT
to add species for their own sake:

| species | accession | why |
|---|---|---|
| *Hoolock leuconedys* | GCA_047372625.1 (chromosome) | Recovers the Nomascus+Hoolock hylobatid origin genomically. *H. hoolock* (the phenotype-dichromatic dropout) has NO species-level assembly; the genus best is this *H. leuconedys* chromosome-level assembly. |
| *Pithecia pithecia* | GCA_028551515.1 (chromosome) | A better (chromosome-level) assembly for an origin already in v1 — upgrades origin_12 quality. |
| *Presbytis comata* | GCA_963575215.1 (scaffold) | Genus-level proxy near origin_15. *Presbytis hosei* is the one dichromatic origin with ZERO genomic representation and has no assembly of its own. |
| *Alouatta palliata* | GCA_004027835.1 (scaffold) | Monochromatic background reinforcement near the *Alouatta caraya* origin (origin_11, currently n=1). |
| *Alouatta seniculus* | GCA_963574235.1 (scaffold) | Same — strengthens the reference for the *Alouatta* origin. |
| *Cacajao calvus* | GCA_963573955.1 (scaffold) | Pitheciid outgroup near the *Pithecia* origin (origin_12). |

### Deliberately excluded

- **No additional Cercopithecines.** The family is already over-represented (65/117), and
  *Trachypithecus* alone is one origin sampled ~8× — that is the pseudoreplication the
  per-origin design corrects, so adding more would worsen it.
- **No unsampled-family scan hits.** The 238-species phenotype table records hair
  dichromatism only in these four families; there is no dichromatic species in a
  currently-unsampled family to recover. (Confirmed by cross-referencing the 26
  dichromatic-238 species against the v1 genome set: the only two missing are
  *Hoolock hoolock* and *Presbytis hosei*, both in already-sampled families.)

## How Round 2 re-enters the pipeline

1. Fetch the roster_v2 accessions (`01_fetch_and_extract.sh roster_v2_targets.csv`), merging
   CDS into the same `cds/` tree.
2. Build `roster_v2_accessions.csv = roster_v1 + roster_v2` and regenerate
   `origin_assignments.csv` (the phylo audit is re-run on the expanded tip set — new tips may
   split or reinforce origins).
3. Re-run stages 1/A/C/R exactly as in Round 1 under a new `$WORK` (e.g. `perorigin_v2`).
   Nothing else changes.
