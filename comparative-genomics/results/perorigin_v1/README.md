# Per-origin selection analysis (perorigin_v1)

Raw results for the **architecture-heterogeneity** question: across the independent
origins of primate hair dichromatism, do the SAME genes shift selection intensity
(convergent architecture) or DIFFERENT genes (heterogeneous architecture)?

## Files
- `per_origin_K.csv` — per-(origin × gene) HyPhy **RELAX** fits. K>1 = intensified selection
  on that origin's foreground; K<1 = relaxed. Columns: origin_id, gene, set, K, p_value, p_BH
  (Benjamini-Hochberg within origin), LRT, n_fg (foreground tips), n_tips_kept, n_sites, status.
- `branch_rates.csv` — full-panel HyPhy **aBSREL** per-branch dN/dS (9,229 branches, 78 genes;
  `selected_flag` = BH<0.05 episodic selection). Recovers signal on single-tip origins that
  RELAX cannot test.

## Raw result (195 valid fits; 3 origins had enough foreground to test)
| origin | foreground tips | BH-significant genes (p_BH<0.05) |
|--------|-----------------|----------------------------------|
| origin_7  | up to 7 | 12: SRD5A3, KISS1R, HSD17B7, SRD5A1, TYR, TFAP2A, MC1R, SHBG(relaxed), SCARB1, EDN3, ASIP, LDLR |
| origin_8  | 3 | 1: POMC |
| origin_14 | 2 | 0 |

**No gene is BH-significant in more than one origin (zero cross-origin overlap).**

## Caveats — read before interpreting (do NOT report as a clean "heterogeneous architecture" claim)
1. **Power is unequal across origins** (7 vs 3 vs 2 foreground tips). The gene-count gradient
   (12 / 1 / 0) tracks power, so "different genes per origin" is confounded with "different power."
   Convergent vs. heterogeneous cannot be cleanly separated here without a power-matched analysis.
2. **Boundary Ks need QC:** e.g. KISS1R K≈15 (K>10 boundary), SHBG K≈0.017 (near-zero). Apply the
   certification gates (K boundary, foreground branch length, gap fraction) before trusting individual hits.
3. This is **raw output for certification**, not a final result. Interpretation/certification is Claude Science's lane.

## Known gaps
- **LDLR** aBSREL produced an empty JSON (1 of 80 genes) — no branch_rates for LDLR. Re-run needed if LDLR matters.
- Only origins 7/8/14 are RELAX-testable (multi-tip); the other 11 single-tip origins are covered by aBSREL (`branch_rates.csv`) + (planned) RERconverge.

Compute: HyPhy RELAX/aBSREL on the 117-primate panel, Great Lakes HPC. Foreground = per-origin dichromatic tips.
