# Execution plan — internal

> Our own read on how to build the immersive experience, distilled from a 5-lens expert panel
> (data-viz, WebGL/motion, frontend architecture, product/onboarding, performance/a11y). This is
> *not* part of what we'd hand a consultant — it's what we'd build once the direction is confirmed.
> All five lenses converged on the same core inversion, which is a strong signal.

## The one-sentence strategy

**Build the per-entity "dossier" as a single reusable component, precompute the data at build time so
there's no backend, route every surface through the dossier, and add cinematic motion only as a
hydrated enhancement on top of a static, auditable core.**

## Recommended build path

**Phase 0 — The data contract (do first; it's the load-bearing wall).**
One validated build-time script: canonical dataset → **~800 self-contained per-entity JSON records**
(verdict, strands, ego-edges, flags, *fully-resolved citations*) + a lightweight **search index** +
precomputed **benchmark**, **sequence**, and **layout-coordinate** blobs. **Fail the build on schema
drift.** Everything downstream is a pure function of these files. (We already have
`interactive/nb7_multilayer_graph.json` as a starting point; this generalizes it.)

**Phase 1 — The smallest thing that already feels like an app.**
A static-rendered **dossier template** — *the Call* (verdict + tier) → *the Strands* (evidence) →
*collapsible Provenance*, plus the local ego-graph, the entity's role in the sequence, and both-context
verdicts — with **one deep-linkable URL per entity**, an **instant search / command palette** (Cmd-K),
and the **benchmark as a clickable confusion matrix** (truth × verdict tier, every cell linking to the
entity + sources). No 3D, no camera moves yet. This alone is auditable, citable, fast, accessible — a
credible tool a skeptic can already use.

**Phase 2 — The immersive layer (hydrated on top).**
The signature **convergence encoding** (channel-ring glyph / convergence-as-light), the focused **2D
ego-graph** with precomputed positions, **View-Transition morphs** (board→dossier, dossier→dossier),
and — the money moment — the **"naive activity" vs "convergence" toggle** where decoys blaze then
collapse to dark, wired to the scoreboard so the numbers tick in sync. Motion only ever encodes
*change*. The reduced-motion path is authored in parallel, not retrofitted.

**Phase 3 — The full experience.**
The scripted **cold-open camera sequence** (establishing pull-back → fly to the hero core node →
dossier assembles → decoy collapse → context re-light) that **doubles as the screen-recorded video**;
the optional **global overview** (2D default, 3D opt-in only if z is honest); an **UpSet** view for
6-channel membership and a **slopegraph** for the two-context verdict diff. Effect tiers and
`prefers-reduced-motion` gating throughout.

> **Highest-leverage move:** nail Phase 0 + the Phase 1 dossier component, then route *every* surface
> (search results, graph clicks, sequence steps, context comparison, the guided tour) through that one
> atom. Once it exists, the cold-open costs almost nothing — it's just the atom demonstrated on one
> hero case end-to-end — and the "engine you query" feel, the credibility argument, and the video
> deliverable all fall out of the same codepath.

## Advice the panel converged on (pre-empt it)

1. **Invert the IA:** dossier is the product, graph is a supporting act. Build the dossier first.
2. **Precompute everything; ship a deterministic renderer.** Bake graph layout offline; never run a
   live force simulation (non-deterministic, un-auditable, motion-sickness).
3. **Lead with proof as a trust gate:** the benchmark as an interactive confusion matrix, not a static
   "0 errors" banner (which reads as overfit hype).
4. **Make the adversarial decoy the centerpiece:** the naive-vs-convergence toggle is the single most
   persuasive moment — but it needs the *real* naive baseline, not a mock.
5. **Static HTML is the source of truth; the app hydrates on top.** Works with JS off and the graph
   absent → free first-paint, screen-reader support, and locked-down-laptop degradation.
6. **One attribute → one visual dimension.** Color = channel identity, brightness/size = convergence,
   motion = edge sign/direction. No double-encoding.
7. **Don't draw all 7,800 edges.** Default to the queried entity's edges; the single-channel 87% is
   decoration that buries the signal.
8. **Give every state a URL** (entity, context, benchmark filter, open source card). Auditability =
   shareability.
9. **Provenance one interaction away, collapsed by default** — clickable chips → citation drawer,
   never a wall of IDs, never hover-only.
10. **Search-first (Cmd-K) as the primary input** — it *is* the "query the engine" UX and the only sane
    way to reach the rare high-convergence core.
11. **UpSet, never Venn**, for 6-channel membership; **slopegraph** for the two-context verdict diff.
12. **Reduced-motion is a first-class design,** not a kill switch: same final DOM, different tempo;
    never convey state through motion or color alone.

## Pitfalls to avoid

1. **The 3D hairball as the front door** — fails on a reviewer's locked-down laptop, invisible to
   screen readers, tanks first-paint, reads as "pretty noise." Immersive ≠ starts-in-3D.
2. **Live force simulation at runtime** — positions won't match a screenshot in a talk; jitter, hot
   fans, motion sickness. Precompute and bake.
3. **Runtime joins / one monolithic `dataset.json`** — waterfalls, huge payloads, breaks on the next
   rename. Denormalize at build; shard by access pattern.
4. **Telling the decoy story without the naive-baseline contrast** — "decoys not fooled" is invisible
   unless the UI shows what the naive method *would* have wrongly concluded.
5. **Encoding overload / perceptual lies** — too many simultaneous visual variables; sizing by radius
   while meaning area. One attribute → one dimension. (Note: `decoy_cleared` is a *special case*, not a
   rank on the ordinal tier scale — don't put it on the same axis.)
6. **Silent context switching & raw jargon** — if a verdict flips unseen, trust collapses; always show
   the active context, stage every flip as an explicit before/after diff, and translate engine labels
   at the surface.
7. **Motion/hover as the only channel, and un-escapable tours** — every reveal needs a focus/tap
   equivalent; the first-run must be skippable on the first keystroke.

## Candidate stack (starting point, subject to the expert's input)

- **Framework:** static-first islands (Astro-class) — prerender dossiers, hydrate interactive islands.
- **Graph:** precomputed 2D layout, rendered with Canvas/WebGL for the focused ego-graph; the existing
  Plotly 3D demoted to an opt-in "orbit" only if we give z an honest meaning.
- **Motion:** the browser View Transitions API for morphs; a small keyframed camera path for the
  cold-open; `prefers-reduced-motion` branches authored alongside.
- **Search:** a prebuilt client-side index (e.g. a tiny fuzzy index) behind a Cmd-K palette.
- **Data:** the Phase-0 build script emits per-entity JSON + index + benchmark/sequence/layout blobs,
  via the adapter described in `../REAL_MAPPING.md`.
