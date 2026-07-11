# Direction Concordance: case discordance-direction vs. D'Arcy disease-direction

## Scope
This file documents the reasoning used to build `direction_concordance.csv`
from `case_gene_coverage_master.csv`. It covers 31 case genes total; of
these, **15** carry both a case discordance-direction label (D1/D2/both/mixed)
and a D'Arcy Table S1 `phenotype_class` label (Hypopigmentation /
Hyperpigmentation / Mixed / Pigmentation phenotype), and are the only ones
tabulated in the cross-tab. **16** carry a case direction label but no D'Arcy
S1 disease-class label (they are absent from D'Arcy S1 entirely — either
`darcy_recoverable` via S5-only membership, or `dark_matter`). **0** genes
carry a D'Arcy S1 label without a case-direction label (every case gene in
this set was matched to at least one paper in `discordance_case_classification.csv`),
and **0** genes carry neither label. No missing label was imputed or inferred
— genes without one of the two labels are left with a blank value.

## Definitions of the two axes
- **Case discordance direction** (from `discordance_case_classification.csv`,
  joined to genes via the paper(s) mentioning that gene in the corresponding
  `EXTRACT_*` record file): each of the 13 source papers was pre-classified as
  D1 (canonical genotype present, expected phenotype absent — reduced
  penetrance of the causal allele), D2 (phenotype present, canonical
  genotype absent — phenotype achieved through a non-canonical variant or
  gene), or `both` (the paper reports instances of both directions). A gene
  that appears in more than one paper inherits the union of those papers'
  directions; if that union contains more than one distinct value the gene
  is labelled `mixed` in the coverage table (this includes genes whose only
  citing paper is itself labelled `both`, which is left as `both`).
- **D'Arcy disease-direction** (`darcy_s1_phenotype_class`, from D'Arcy et al.
  2023 Table S1): the phenotype_class assigned to each Mendelian/OMIM disease
  associated with the gene — Hypopigmentation (disease = net loss of
  pigment), Hyperpigmentation (net gain/excess pigment), Mixed (disease
  itself presents with both hypo- and hyperpigmented features, e.g.
  dyschromatosis), or "Pigmentation phenotype" (a GWAS/complex-trait
  pigmentation association without a discrete Mendelian direction). Where a
  gene is linked to more than one S1 disease entry with more than one
  distinct phenotype_class, it is bucketed as `Mixed` in this cross-tab
  (matching D'Arcy's own convention on the pre-annotated backbone-overlap
  table for genes such as TYR and KITLG).

## Mapping logic (descriptive, not causal)
The two axes measure different things — one is about penetrance/allelic
architecture in population/case-report data, the other is about the direction
of a Mendelian disease phenotype — so there is no strict logical
"agreement/disagreement" test between them. The pairings below describe the
mechanistically *expected* co-occurrence pattern one might anticipate,
without asserting that the discordance case and the Mendelian disease share
a causal mechanism:

- **Hypopigmentation disease gene + D2 case** (phenotype present, canonical
  variant absent): the expected pairing when a gene's disease-associated
  loss-of-function biology plausibly extends to a non-canonical variant
  that also reduces pigment — e.g. TYRP1, OCA2, SLC45A2 in this table.
- **Hypopigmentation disease gene + D1 case** (canonical variant present,
  phenotype reduced/absent): consistent with the well-documented incomplete
  penetrance of hypopigmentation-disease alleles in population contexts —
  e.g. PAX3/Waardenburg in this table.
- **Hyperpigmentation disease gene + case direction**: no case-direction gene
  in this set pairs with a pure Hyperpigmentation disease class except BNC2
  (`both`); BNC2's case evidence in `Ang2023_eLife_Kalinago` involves lighter,
  not darker, skin pigmentation associations, so this pairing does not fit
  the "expected" loss/gain symmetry described above and is flagged as such
  rather than forced into an interpretation.
- **Mixed disease class genes** (TYR, KITLG, IRF4, SLC24A5): these are
  pleiotropic genes with disease associations spanning both directions
  (e.g. TYR: albinism [hypopig] and melanoma risk / piebaldism), so a case
  gene with `mixed` or `both` discordance direction is unsurprising and not
  informative about concordance in either direction.
- Genes with **no D'Arcy S1 label** (16 of 31) cannot be placed on this axis
  at all — most of these are network-adjacent genes (`in_network`) or
  D'Arcy-recoverable via S5-only membership, not S1 Mendelian-disease genes,
  or are `dark_matter` genes with no disease-database presence in this
  bundle.

## Summary count matrix
See the second table appended to `direction_concordance.csv`
(`case_direction` rows x `disease_class` columns, counts of the 15 dual-labelled
genes). No cell reflects an imputed or inferred label — every count is a
direct tabulation of the two source-verified label sets.
