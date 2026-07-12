# NB11 frozen Ensembl responses

All files are verbatim responses from Ensembl REST (https://rest.ensembl.org), GRCh38 /
1000 Genomes phase 3. Query captured 2026-07-12T15:18Z. No live calls are made at notebook run time;
`REQUERY*` guards in the notebook re-hit the live API when run outside the sandbox.

| File | Query | Endpoint |
|---|---|---|
| `nb11_convergent_variants.json` | 7 convergent-gene lead variants (MFSD12 x2, SPIRE2 x2, TSPAN10, BNC2 x2) | POST `variation/human?pops=1` |
| `nb11_baseline_candidate_ids.json` | seeded candidate rsIDs sampled from 88 fixed autosomal windows (22 at seed 1000 + 66 at seed 2000) | GET `overlap/region/human/<region>?feature=variation` |
| `nb11_baseline_variants.json` | per-superpop freqs for baseline candidates, slimmed to 1000GENOMES:phase_3 entries (2979 variants) | POST `variation/human?pops=1` |
| `nb11_baseline_stats.json` | precomputed baseline Fst summary (n=552, mean=0.0864, median=0.0625) | derived |
| `nb11_ld_pairwise.json` | pairwise LD for the MFSD12 and BNC2 mirror pairs, per superpopulation | GET `ld/human/pairwise/<rs1>/<rs2>?population_name=...` |

Superpopulation sample sizes (1000G phase 3, individuals): AFR 661, AMR 347, EAS 504, EUR 503, SAS 489.
