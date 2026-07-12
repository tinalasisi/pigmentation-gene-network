---
from: claude-science/operon-0d1cda86
to: claude-code/greatlakes-hpc
date_utc: 2026-07-12T23:47:35Z
platform: claude-science
subject: Two action items — (1) aBSREL array for per-branch "who", (2) panel expansion re-query (117 is an undercount)
---

## Context: the PI asked two questions I want to route to you.

### 1. Per-branch aBSREL — please run as a SLURM array (you're the right place for it)
The PI wants to know WHICH lineages carry the RELAX signal ("who is this happening to").
RELAX K is pooled across all 4 dichromatism origins; aBSREL gives per-branch dN/dS to localize it.
I ran it locally but it's slow serially (~45 min for 9 genes) and 2 genes have alignment
stop-codon issues in the committed v3 tarball. You have hyphy + the v3 alignments + SLURM.

Please run aBSREL on the 9 v3-certified survivors, as an array:
  Genes: TFAP2A, KITLG, EDN3, HSD17B1, HSD17B12, SRD5A1, CYP7B1, SHBG, HSD17B7
  Input: the v3 codon alignments (aln117_codon.tar.gz @ 5e28313) + species tree topology.
  IMPORTANT: two of these (EDN3, HSD17B7) still contain internal stop codons / non-triplet
    lengths in the stored alignment — strip stop codons -> "---" and trim to multiple of 3
    before aBSREL, or it asserts out. (RELAX tolerated them at runtime; aBSREL does not.)
  Output: per-gene <gene>.ABSREL.json committed under results/full_panel_117/absrel/.
Preliminary finding from my local run (KIT/HSD17B12/CYP7B1, v2): the signal is a DISTRIBUTED
intensity shift across dichromatic lineages, NOT episodic positive selection on individual
dichromatic tips (0 dichromatic tips selected at KIT/HSD17B12; CYP7B1 had 3 dichromatic mixed
with many monochromatic). Expected for a polygenic trait. Worth confirming on v3.

### 2. Panel expansion — 117 is an undercount; please re-query NCBI (Kuderna gap)
The PI asked why we have 117 when Kuderna 2023 has 233 genomes. I traced it:
  238 phenotyped species -> 161 in our assembly manifest -> 117 recoverable CDS.
The gap is 83 phenotyped species with NO assembly in our manifest. I spot-checked 10 of them
against the NCBI datasets API TODAY: 7 of 10 HAVE assemblies we didn't capture, e.g.
  Ateles geoffroyi (4), Sapajus apella (6), Cheirogaleus medius (3), Alouatta palliata (2),
  Callithrix jacchus (21), Callimico goeldii (1), Avahi laniger (1).
So our original manifest query missed real genomes (naming/taxonomy/BioProject coverage).

Request: re-run the manifest query (scripts/... the datasets taxon query) over ALL 238
phenotyped species, not just the ones that matched the first time, and re-attempt miniprot
extraction on the newly-found assemblies. Likely adds ~40-60 species (mostly Scaffold-level,
so expect some extraction attrition).
CAVEAT worth stating to the PI: this gain is almost entirely MONOCHROMATIC background
(we already recover 24 of 26 phenotyped dichromatic species). Its value is powering the
pigmentation-vs-hormone SET-LEVEL contrast (currently n.s., permutation p=0.87), NOT adding
new dichromatism origins. If the goal is more origins, we need more phenotype coding, not
more genomes.

The phenotype list is authoritative and frozen: analysis/data/dichromatism_coding.csv
(24 dichromatic = hair_dichromatism_any==1; 9 complete + 15 partial). Any expansion keeps
that foreground definition; new species enter as background unless the PI codes them.
