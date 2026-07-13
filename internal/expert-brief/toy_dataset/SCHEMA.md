# Toy dataset — schema & structure

A **fictional, structure-preserving** dataset for prototyping an immersive, entity-driven web
experience. The story (a set of cold-case investigations resolved by *converging independent
evidence channels*) is invented; what's real is the **shape** of the data and its **distributions**.
Anything you build that works on this will drop onto the production dataset unchanged — same fields,
same cardinalities, same heavy-tailed distributions.

All files are plain JSON. `dataset.json` bundles everything; the rest are the same data split by type.
Regenerate with `python3 generate_toy.py` (deterministic).

## The mental model in one paragraph

There is a set of **entities**. Each entity is "seen" by some subset of a handful of independent
**evidence channels** — a couple of channels are broad (they see most entities), the rest are
selective (they see few). How many channels see an entity is its **convergence**; a tiny **core**
is seen by nearly all channels, most entities by only one or two. Entities are joined by typed
**relationships**, and each relationship is likewise backed by a subset of channels (mostly one;
rarely many). A single **directed sequence** threads a chain of events from a trigger to an outcome.
Every entity gets a **verdict** (a tier + a rationale + the evidence "strands" behind it), and a
**benchmark** of known-answer cases (including decoys planted to fool a naive method) proves the
verdicts are right. Two **contexts** re-bind a subset of verdicts. Nothing is asserted without a
**provenance** ref.

## Files & fields

### `channels.json` — the evidence sources (the "layers")
`[{ key, label, coverage_rate, role: "broad"|"mid"|"selective" }]`
The load-bearing asymmetry: 2 broad channels + 4 progressively selective ones. Convergence across
channels is the core signal.

### `entities.json` — the nodes
```
{ id, codename,
  channels: [channel_key…],        // multi-label membership (which sources see it)
  n_channels,                       // convergence (1–6); heavy-tailed toward 1–2
  flags: { on_watchlist, watchlist_class, physical_evidence, field_flagged },
  verdict: {
    tier,                           // one of 5 tiers (see below)
    summary,                        // one-line rationale
    strands: [ { channel, stance, finding, source } ]   // the evidence, per channel
  },
  provenance: [ ref… ] }
```
**Verdict tiers:** `implicated_multichannel` (many channels converge) · `implicated_anchored`
(on the watchlist, thinner corroboration) · `circumstantial` (a few channels, no anchor) ·
`cleared` (single channel) · `decoy_cleared` (looks active but correctly cleared — the adversarial case).

### `edges.json` — the relationships
```
{ a, b, type, directed, sign: "+"|"-"|""|"conflict",
  sign_conflict, channels: [channel_key…], n_channels, tier, provenance: [ref…] }
```
Most edges are single-channel and unsigned/undirected; a minority are directed & signed; one carries
a sign conflict. `n_channels` on an edge = how many independent sources back that link.

### `sequence.json` — the reconstructed directed chain
```
{ id, context, label, note, steps: [ { order, from, to, actor, actor_id, sign, channels, provenance } ] }
```
An ordered path of events (trigger → … → outcome), each step attributed to an entity and grounded to
sources. This is the "story" spine.

### `benchmark.json` — proof it works
```
{ context, totals: { culprits_recovered, innocents_cleared, decoys_not_fooled, errors },
  items: [ { id, codename, truth, kind, verdict_tier, pass } ] }
```
`kind` includes `adversarial_decoy` (built to fool a naive method). The scoreboard is the credibility
payload.

### `contexts.json` — the switchable views
```
{ contexts: [ { id, label, anchor } ],
  cross: [ { id, codename, <contextA>: tier, <contextB>: tier } ] }   // verdicts that flip
```

### `references.json` — provenance table
`{ ref: { kind, citation } }` — every `source`/`provenance` ref resolves here.

## Distributions to respect (they make the viz interesting)

| Property | Toy | Production (same shape, larger) |
|---|---|---|
| entities | ~55 | ~800 |
| edges | ~170 | ~7,800 |
| entity→#channels | heavy-tailed: most 1–3, tiny core 4–5 | most 1–2, tiny core 5–6 |
| channel coverage | 2 broad (~45/55), tail down to ~7/55 | 2 broad (~455/800) … 1 selective (~45/800) |
| edge convergence | ~88% single-channel | ~87% single-channel |
| signed edges | a directed minority + 1 conflict | a directed minority + 1 conflict |

## Interaction surface this data affords (prompts for prototyping)

- **Query→dossier:** pick/search an entity → compose its verdict, strands, neighbours, provenance.
- **Convergence as the hero encoding:** size/glow/elevation by `n_channels`; the core should *feel* central.
- **Channels as toggleable layers:** isolate a channel; watch the graph thin out (broad vs selective).
- **The sequence as a guided, animated spine** (a cinematic through-line).
- **The scoreboard/benchmark grid** as a "does it work?" proof surface, with drill-down to any item.
- **Context switch** re-binds verdicts (diff/flip animation).
- **Provenance-first:** every element drills to a source; nothing is unattributed.
