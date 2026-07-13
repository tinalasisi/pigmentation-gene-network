# Interactive figure spec — handoff for the rendering agent

`interactive_spec.json` decomposes all five module-selection figures into data +
encoding so you can render them as interactive HTML (D3 / plotly / cytoscape)
with **primate photos embedded**. Each figure block has:

- `static_figure` — path to the code-generated PNG in this repo (the ground
  truth; link back to it as "static version" / download).
- `chart_type` — the recommended interactive form.
- `photo_anchor` — where species photos attach: `species` (one per taxon),
  `both_taxa` / `pair` (dichromatic + its monochromatic sister side by side).
- the raw data rows/nodes/edges.

## Figures

1. **module_balance** — diverging bar per origin (−1 hormone … +1 pigmentation).
   `rows[]`: origin_id, species[], n_pig, n_hor, balance, powered. Photo per
   species; group by `family` in `family_order` (closest→furthest from human).

2. **per_lineage_genes** — dot matrix, origins × genes. `data[].genes[]` carries
   `module` (color) and `relax_K` (non-null = ring it, RELAX-confirmed).

3. **circular_tree** — radial tree. `newick` is the topology (102 tips);
   `tips[]`: species, dichromatic (highlight red), balance (node color via the
   diverging ramp), n_sel (node size). Ideal for photo-on-hover.

4. **sister_pair_contrast** — THE HEADLINE. For each dichromatic taxon, the genes
   under selection that its closest monochromatic relative lacks.
   `pairs[]`: dichromatic, sister_monochromatic, patristic, dich_only_pigmentation[],
   dich_only_hormone[], shared[]. Show the two taxa's photos side by side; the
   `dich_only_*` genes are the candidate loci for the phenotype difference.
   Note `recurrent_gene` — KITLG recurs across independent lineages.

5. **sister_network_diff** — coupled network (nodes=genes colored by module,
   edges=STRING score≥0.4). `node_state_per_pair` keys are "<dich>__vs__<mono>";
   each maps gene→state (dich_only / both / mono_only / neither). Render one
   network, let the user pick a pair to recolor nodes (red ring = dich_only =
   "the variation"). `state_encoding` gives the visual mapping.

## Colors (meta.colors)
pigmentation = #C97B0A (orange), hormone = #2E6E9E (blue),
dichromatic highlight = #B22222 (red), no-selection = #e8e8e8.

## Caveat to preserve (meta.caveat)
aBSREL episodic selection at tips; a gene "difference" between sisters marks
lineage-specific selection, NOT proven causation. Two pairs (Macaca arctoides,
Eulemur flavifrons) have zero differential genes — show them honestly.

## Photos
Openly-licensed primate photos (CC0/CC-BY/CC-BY-SA from Wikimedia) with
attribution were pulled in earlier work; see species_photo_attribution.csv in
the artifact store. Match by the `species` field (Genus_species).
