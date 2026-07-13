# full_panel_117 — 117-primate comparative RELAX selection scan

Gap-trimmed HyPhy RELAX scan of 80 pigmentation + hormone genes across 117 primates,
testing intensified/relaxed selection on the dichromatic-vision foreground (species_states.csv).

## Files
| file | what |
|---|---|
| `SUMMARY.md` | per-gene K/p/BH table (pigmentation vs hormone) |
| `summary.json` | machine-readable per-gene results |
| `relax_results.csv` | 79 fitted genes: gene,set,K,p_value,p_BH,LRT,n_tips,n_foreground,n_sites,pct_gaps |
| `alignment_qc.csv` | all processed genes: tips, aln_len, pct_gaps, n_cols_trimmed, status, relax_status |
| `fit_health.csv` | **CERTIFICATION LAYER** — fg_branch_len, tree_len, flags. Certify from THIS, not raw p. |
| `tip_roster.csv` | species-per-gene with dichro/mono state (foreground integrity) |
| `extraction_qc.csv` | per gene×species: method (direct/miniprot), miniprot %identity, aln_len, ref_len, ratio |
| `hyphy_failed_genes.txt` | genes that failed hyphy (mostly recovered via the internal-stop QC fix) |
| `aln117_codon.tar.gz` | the codon alignments matching THIS run (for RERconverge / phangorn) |

## fit_health flags
`branch_len_blowup` (tree_len>5 — misaligned/paralogous seqs), `near_zero_fg` (weak foreground),
`gaps_gt_20pct`, `K_boundary` (K<1e-4 or >100), `low_power` (n_fg<3). `clean` = none.

## Headline (certify from fit_health.csv)
Clean & robust BH-sig: **TYR, KIT** (pigmentation, intensified in dichromatic) + HSD17B12 / HSD17B7 /
CYP7B1 (hormone); FOXD3 clean but K extreme. ~10 BH-sig are branch_len_blowup-flagged
(`gap_col_thresh=0.5` too lenient at 117-species divergence — a stricter v3 trim would resolve them).

## Reproduce
`scripts/slurm/fetch_array.sbatch` (`--array=1-117%20`) -> `relax_array.sbatch` (`--array=1-80`) ->
`report_diag.sbatch`. Env: scratch conda `align` (see `../envs/environment.yml`); PATH-only in batch scripts.
Config: `config/{accessions_all_recoverable.csv, gene_panel.csv, species_states.csv, primate_species_tree.nex}`.
Pipeline: `01_fetch_and_extract.sh` (miniprot/direct CDS) -> `02_align_and_relax.py` (MAFFT codon +
gap-trim + internal-stop QC + RELAX) -> `03_report_summary.py` -> `03b_diagnostics.py`.
