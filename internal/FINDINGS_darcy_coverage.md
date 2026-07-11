# Findings: mechanistic-network and disease-gene coverage of the case discordance set

## Substrate and question

The project's mechanistic substrate is a signed, directed backbone integrated with a 168-gene
pigmentation network. Its central claim under test is bidirectional genotype-phenotype
discordance: D1 cases (a canonical causal variant is present but the expected phenotype is
absent — reduced penetrance) and D2 cases (the phenotype is present but the canonical variant is
absent — the phenotype is reached through a non-canonical variant or gene). At gene level, the
`case_discordance_direction` column in `case_gene_coverage_master.csv` also uses two derived
labels: `both` (the gene has both D1-type and D2-type evidence) and `mixed` (the direction varies
across the papers or cases citing that gene). `D2` does not appear as a standalone value at gene
level in the 31-gene table; every gene with D2 evidence is labelled `both` or `mixed` because it
is cited alongside D1 evidence somewhere in the case set. This claim was curated from a 13-paper,
694-record case set spanning 31 genes (`discordance_case_classification.csv`, sum of
`n_records_extracted` across the 13 papers).

This memo asks a narrower, prior question: how much of that 31-gene case set does the mechanistic
network — with or without a disease-gene annotation layer — actually cover, and what does the gap
look like.

## Coverage result

Of the 31 case genes, 9 (29 percent) are present in the mechanistic network
(`case_gene_coverage_master.csv`, `coverage_tier = in_network`; `in_nb2_network` True count = 9/31).
These 9 are EGFR, KITLG, MC1R, OCA2, PAX3, POMC, PPP3CA, TYR, TYRP1.

Adding D'Arcy and Kiel (2023; https://doi.org/10.3390/bioengineering10010013, PMC9854651) Table S1
— a 243-gene OMIM-backed disease-gene table carrying hypopigmentation / hyperpigmentation / mixed
phenotype-direction labels — as an annotation layer
recovers a disease-direction label for 7 additional case genes not present in the network: BNC2,
HERC2, IRF4, LRMDA, RALY, SLC24A5, SLC45A2 (`coverage_tier = darcy_recoverable`,
`in_darcy_S1 = True`). This raises labelled coverage from 9/31 (29 percent) to 16/31
(52 percent; `in_nb2_network OR in_darcy_union` = 16/31 in `case_gene_coverage_master.csv`).

This is an annotation-layer result, not a network-edge result. D'Arcy's STRING-derived interaction
edges (Tables S4/S5) are excluded from the mechanistic backbone because they are computationally
predicted rather than literature-curated; only Table S1, the OMIM-backed disease-gene annotation
table, is used here, and only to attach a disease-direction label to genes the network does not
otherwise contain.

## Dark matter: genes in neither resource

15 of the 31 case genes (48 percent) are absent from both the mechanistic network and the D'Arcy
disease-gene compendium (`coverage_tier = dark_matter` in `case_gene_coverage_master.csv`):

ATRN, EMCN, KALRN, LTO1, MANBA, MFSD12, MSX2, NPLOC4, PKHD1, SIK1, SLC24A4, SLC39A8, SYT6, TACR3,
TSPAN10.

Every one of these genes is cited by at least one case paper as carrying a discordance direction
(`D1`, `both`, or `mixed`; column `case_discordance_direction`), so this is not a set of peripheral
genes — it is the set that carries discordance signal in the literature but has no representation
in either the mechanistic network or the OMIM-backed disease-gene table used here. This coverage
gap is consistent with the difficulty of genotype-to-phenotype prediction on this phenotype: the
genes carrying case-level discordance signal are disproportionately absent from standard
mechanistic and disease-gene resources. This is a coverage observation, not a demonstration that
the absence causes the prediction difficulty.

## Direction cross-tab: case discordance direction vs. D'Arcy disease direction

Of the 31 genes, 15 carry both a case discordance-direction label and a D'Arcy disease-phenotype
class (`direction_concordance.csv`); the other 16 case genes carry a case-direction label but no
D'Arcy S1 disease-class label, and 0 genes carry a D'Arcy S1 label without a case-direction label
(`direction_concordance_README.md`). The summary count matrix over the 15 dual-labelled genes is:

| case_direction | Hyperpigmentation | Hypopigmentation | Mixed |
|---|---|---|---|
| D1 | 0 | 1 | 0 |
| both | 1 | 5 | 1 |
| mixed | 0 | 4 | 3 |

Descriptively: 10 of the 15 dual-labelled genes sit in the hypopigmentation-disease column, and
within that column the case-direction label is split across D1 (1 gene: PAX3, consistent with the
well-documented incomplete penetrance of Waardenburg-associated alleles), `both` (5 genes), and
`mixed` (4 genes). The 4 genes in the Mixed disease-class column (TYR, KITLG, IRF4, SLC24A5) are
pleiotropic genes with disease associations spanning both directions, so a `mixed` or `both` case
label at those genes is expected from the disease biology and is not informative about
concordance in either direction. One gene, BNC2, pairs a Hyperpigmentation disease class with a
`both` case direction; its case evidence involves a lighter- rather than darker-pigmentation
association, so this pairing does not fit the loss/gain symmetry implied by the other rows and is
noted rather than forced into an interpretation. These are co-occurrence counts across two
differently defined axes (population/case-report penetrance vs. Mendelian disease direction), not
a concordance or agreement test, and no causal relationship between the two axes is asserted.

## Where each paper fits (corpus-wide, not Ang-centric)

The finding above draws on the full 13-paper, 694-record case set, and every paper has a role in it — the
worked examples below lean on Ang 2023 because that is where the dark matter physically concentrates (7 of
the 15 dark-matter genes: ATRN, EMCN, KALRN, MANBA, SLC39A8, SYT6, TACR3), not because the corpus itself is
Ang-centric. Ang 2023 (53 records) is only the fourth-largest paper by record count; Meyer 2020 (211
records), Kastelic 2013 (105 records), and Morgan 2018 (63 records) are all larger. The 13 papers cluster by
phenotype system:

| cluster | papers | role in the finding |
|---|---|---|
| Eye-colour / forensic panel | Abbatangelo 2026, Meyer 2020, Pospiech 2016, Kastelic 2013, Salvo 2023 | The nearest-gene≠causal story (HERC2→OCA2); IRF4, SLC24A4, TSPAN10 dark matter live here |
| Skin pigmentation (population) | Crawford 2017, Yang 2016 | The genuinely-novel dark-matter story: MFSD12 (cited expression mechanism) + SLC24A5/SLC45A2 |
| Albinism / hypopigmentation | Ang 2023 | The LD-passenger / no-signal dark-matter story (chr4 hitchhikers Ang itself excluded) plus the OCA2 D1/D2 anchor |
| Blond hair (TYRP1) | Kenny 2012, Norton 2014, Norton 2016 | D2 depth on one in-network gene (TYRP1 R93C) — not dark matter; three papers reduce to one gene |
| Red hair (MC1R) | Morgan 2018 | D1 penetrance-matrix depth on an in-network gene (MC1R) and a second dark-matter engine (LTO1/MSX2/PKHD1/SIK1/TSPAN10 — TSPAN10 also contributed by Abbatangelo 2026, so paper-level counts overlap) |
| Syndromic | Morell 1997 (Waardenburg, PAX3) | The clean D1 anchor on an in-network gene (incomplete penetrance) |

Two caveats on how this corpus is described: Kastelic 2013 extracted **0 gene symbols** (it is a
model/marker paper — 105 records, no gene column populated), so it must not be read as one of 13 independent
gene contributions; and the three TYRP1 papers (Kenny 2012, Norton 2014, Norton 2016) all reduce to the
single in-network gene TYRP1 — D2 depth on one locus, not three independent genes' worth of breadth. Neither
caveat changes the coverage numbers above (both are already reflected in the 31-distinct-gene count), but
both must be stated when the corpus itself — 13 papers, 694 records — is described. Full evaluation:
`FRAMING_EVALUATION_dark_matter.md` §1–2.

## Payoff loci

The project's designated payoff loci are the two albinism causal genes **TYR (OCA1) and OCA2** —
the same genes as the clinical validation cases. Both are `in_network`
(`case_gene_coverage_master.csv`) and carry a D'Arcy disease label (Mixed and Hypopigmentation
respectively), consistent across the mechanistic-network and disease-gene resources. Two further
albinism genes cited in the case set, TYRP1 and MC1R, are likewise `in_network` with D'Arcy
Hypopigmentation labels; they are additional well-covered albinism genes, not payoff loci. For all
four the substrate's coverage is not in question; the coverage gap described above is concentrated
elsewhere in the 31-gene case set.

## D'Arcy x backbone cross-check (reproduced)

Independent of the case-gene coverage table above, a full reproduction of the D'Arcy disease-gene
union against the signed directed backbone gives (`darcy_backbone_crosscheck.csv`): D'Arcy S1 =
243 genes, D'Arcy S5 = 451 genes, D'Arcy union (S1 union S5) = 508 genes, of which 465 genes are
absent from the backbone. Of those 465 backbone-absent genes, 227 carry a disease flag and 118
fall in the hypopigmentation phenotype class. 43 D'Arcy union genes overlap the backbone directly
and form the annotation set described above.

The disease-flagged count among backbone-absent genes is 227; this reproduction supersedes an
earlier dashboard figure of 230, reconciled as a gene-symbol synonym-resolution artifact in
`CHANGELOG.md`. 227 is the current, source-verified figure.

## Framing

This is a coverage and annotation-layer finding: it quantifies how much of the case discordance
set the mechanistic network and a disease-gene compendium jointly label, and identifies the genes
neither resource labels. It is not a causal claim about mechanism and not a predictive claim about
which genes will show discordance in new data. The direction cross-tab in particular reports
co-occurrence counts between two independently defined axes and should not be read as a
concordance test.

## Sources

D'Arcy and Kiel (2023), https://doi.org/10.3390/bioengineering10010013 (PMC9854651).

The 694-record, 13-paper case set is tabulated at the paper level in
`discordance_case_classification.csv` (13 rows, `n_records_extracted` summing to 694). The
individual record-level extracts are the corresponding `EXTRACT_*` files listed in that table's
`extract_artifact` column. Paper shorthand codes used in this memo and in
`case_gene_coverage_master.csv` resolve to:

- Ang2023_eLife_Kalinago — https://doi.org/10.7554/eLife.77514
- Yang2016_MBE_OCA2_EastAsian — https://doi.org/10.1093/molbev/msw003
- Kenny2012_Science_TYRP1 — https://doi.org/10.1126/science.1217849
- Norton2014_AJPA_MelanesianBlond_TYRP1 — https://doi.org/10.1002/ajpa.22466
- Norton2016_AJHB_Bougainville_TYRP1 — https://doi.org/10.1002/ajhb.22795
- Crawford2017_Science_AfricanPigmentation — https://doi.org/10.1126/science.aan8433
- Morell1997_JMedGenet_Waardenburg — https://doi.org/10.1136/jmg.34.6.447
- Morgan2018_NatCommun_HairColour_MC1R — https://doi.org/10.1038/s41467-018-07691-z
- Abbatangelo2026_SciRep_eyecolour_discordance — https://doi.org/10.1038/s41598-026-44580-8
- Meyer2020_PLoSONE_GGbrowneyes — https://doi.org/10.1371/journal.pone.0239131
- Kastelic2013_CroatMedJ_IrisPlex — https://doi.org/10.3325/cmj.2013.54.381
- Pospiech2016_IntJLegalMed_IrisPlex_population — https://doi.org/10.1007/s00414-016-1388-2
- Salvo2023_Genes_AAAGblueeyes — https://doi.org/10.3390/genes14030698
