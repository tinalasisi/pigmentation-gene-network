#!/usr/bin/env python3
"""Graft new species onto the frozen primate tree as sister to a same-genus congener.
Preserves the established topology (existing tips unmoved); only adds tips. Branch lengths
are re-estimated by RELAX/aBSREL, so grafted lengths are nominal placeholders."""
import dendropy, csv, sys
tree_in, acc, tree_out = sys.argv[1], sys.argv[2], sys.argv[3]
t = dendropy.Tree.get(path=tree_in, schema="nexus")
tns = t.taxon_namespace
norm = lambda s: s.replace(" ", "_")
existing = {norm(l.taxon.label) for l in t.leaf_node_iter()}
# one representative leaf per genus (updated as we graft, so same-genus additions chain)
genus_leaf = {}
for l in t.leaf_node_iter():
    genus_leaf.setdefault(norm(l.taxon.label).split("_")[0], l)

new = [r["species"] for r in csv.DictReader(open(acc))]
added, skipped = 0, []
for sp in new:
    if sp in existing:
        continue
    g = sp.split("_")[0]
    sister = genus_leaf.get(g)
    if sister is None:
        skipped.append(sp); continue
    parent = sister.parent_node
    el = sister.edge.length or 0.01
    half = (el / 2.0) if el else 0.01
    internal = dendropy.Node(); internal.edge.length = half
    parent.remove_child(sister); parent.add_child(internal)
    sister.edge.length = half; internal.add_child(sister)
    nt = dendropy.Node(taxon=tns.new_taxon(label=sp.replace("_", " ")))
    nt.edge.length = half; internal.add_child(nt)
    genus_leaf[g] = nt          # chain further same-genus additions onto the newest
    added += 1

t.write(path=tree_out, schema="nexus", unquoted_underscores=True)
print(f"grafted {added} tips; skipped {len(skipped)}")
if skipped: print("  skipped:", skipped[:12])
# verify
t2 = dendropy.Tree.get(path=tree_out, schema="nexus")
tips2 = {norm(l.taxon.label) for l in t2.leaf_node_iter()}
print(f"expanded tree: {len(tips2)} tips (was {len(existing)}); reparse OK")
miss = [s for s in new if s not in tips2 and s.split('_')[0] in {norm(l.taxon.label).split('_')[0] for l in t.leaf_node_iter()}]
print(f"graftable species now present: {sum(1 for s in new if s in tips2)}/{len(new)}")
