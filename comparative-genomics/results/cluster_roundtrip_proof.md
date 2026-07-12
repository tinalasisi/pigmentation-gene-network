# Cluster round-trip proof

Produced by a job running **on** the Great Lakes cluster (`gl-login5.arc-ts.umich.edu`) at 2026-07-12T17:48:49Z,
then committed to GitHub from the cluster — to verify the compute -> commit -> local loop before the real pipeline.

## Environment (scratch conda env)
- miniprot: `0.18-r281`
- hyphy: `HYPHY 2.5.100(MP) for Linux on x86_64 x86 SSE4 SIMD zlib (v1.3.2)`
- mafft: `v7.526 (2024/Apr/26)`
- datasets: `datasets version: 18.33.1`

## What ran
Queried NCBI for RefSeq gibbon (Hylobatidae) genome assemblies -> `results/gibbon_assemblies.tsv`.
**Metadata only** — no genome sequence was downloaded or committed. These accessions seed
`config/accessions.tsv` for the real run.
