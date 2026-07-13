# Brief for a creative/technical expert — building an immersive data experience

*A self-contained brief to hand to a software / creative-technology expert, so they can give concrete
advice and even prototype. It comes with a **toy dataset** (`toy_dataset/`) that mirrors our real
data's exact structure and distributions in a neutral fictional domain — so their advice and any
prototype drop onto our production data unchanged. The real subject is deliberately withheld.*

---

## What we're trying to make

We want to turn a **static research site** into an **immersive, entity-driven web experience** — the
kind that feels like an *engine you query* rather than a *paper you read*. The target feel: you pick
(or search) an entity and the app composes a **cinematic, provenance-backed "dossier"** for it on the
spot; a **scoreboard** proves the method works at a glance; a **guided first-run** gets a newcomer to
the point in 30 seconds. It must stay **trustworthy and legible for a skeptical expert audience** —
immersive, not gimmicky.

## The data we have (structure only)

- **~800 entities.** Each is "seen" by a subset of **~6 independent evidence channels** — 2 broad
  channels cover most entities, the rest are selective and cover few. How many channels see an entity
  is its **convergence**: heavy-tailed, so most entities sit in 1–2 channels and a tiny **core** sits
  in 5–6. *This convergence is the whole claim — "confidence = how many independent channels agree."*
- **~7,800 typed relationships** between entities. Each is backed by a **subset** of the channels;
  convergence is again heavy-tailed (~87% single-channel). Most are unsigned/undirected; a minority
  are **signed & directed** (+/–), with rare conflicts.
- **A directed sequence** — a reconstructed chain of ~8 events from a trigger to an outcome, each step
  grounded to a source.
- **A per-entity verdict** — a classification into ~5 tiers (from "confidently supported across many
  channels" down to "cleared", plus an **"adversarial decoy correctly cleared"** tier), each with a
  short rationale and **evidence "strands"** (channel + finding + source).
- **A benchmark** — labelled ground-truth items (including **adversarial decoys** built to fool a
  naive method), scored pass/fail into a scoreboard (e.g. "18/18 recovered, 12/12 rejected, 5/5 decoys
  not fooled, 0 errors").
- **Two selectable contexts** that re-bind a subset of verdicts.
- **Provenance-first:** every entity, edge, strand, and step carries source references.

## Where we are now

A static-site generator emits HTML on **free static hosting (no backend)**. It reads like a published
paper: long-form pages plus **one embedded 3D graph** (an off-the-shelf charting library) — rotate /
hover / toggle on a single fixed view. No query loop, no per-entity views, no app state.

## Constraints & preferences (please advise within these)

- **The dataset is fixed and fully precomputable.** We believe we do **not** need a live backend — we
  can ship precomputed JSON + a client-side app on free static hosting. (Push back if we're wrong.)
- **Implementation is by a small team plus a capable AI coding agent** — favour well-trodden libraries
  and clear data contracts over bespoke pipelines that need a specialist to babysit.
- **Audience is expert and skeptical.** Credibility, legibility, and auditability beat spectacle;
  every visual claim must reach a source.
- **Desktop-first is fine**; graceful mobile / reduced-motion is a plus.
- **We already have** a working 3D graph and a portable graph JSON — reuse over rebuild where sensible.

## What we're giving you to play with

`toy_dataset/` — a fictional, **structure-identical** sandbox (a "convergence engine" for a set of
cold-case investigations). Same fields, cardinalities, and heavy-tailed distributions as production;
zero real values. See `toy_dataset/SCHEMA.md`. Files: `entities`, `channels`, `edges`, `sequence`,
`benchmark`, `contexts`, `references` (+ a bundled `dataset.json`), regenerable via `generate_toy.py`.
**Anything you prototype against this renders our real data with no UI changes.**

---

## Our current leanings — please tell us where we're wrong

*We pressure-tested the structure with several senior practitioners; here's where our thinking landed.
We'd most value you challenging these five.*

- **A — The atom is the entity "dossier," not the graph.** Land on a searchable, faceted board of
  entities; each opens a composed dossier (verdict + evidence strands + provenance + a small *local*
  graph + its benchmark status). The global graph is something you *enter from* a dossier, not the
  front door. (Unanimous across our advisors — but it trades away the instant graph "wow.")
- **B — No backend; precompute is the load-bearing wall.** Denormalize the fixed data at build time
  into ~800 self-contained per-entity JSON records (citations pre-joined) + a small index; the client
  never joins at runtime. Free static hosting, deterministic output, every state gets a URL.
- **C — 2D by default; 3D only if the depth axis means something.** At this scale a live 3D force
  graph is an occlusion hairball that dies on locked-down laptops and is an accessibility black hole.
  Precompute layout offline; render 2D; offer 3D as an explicit opt-in spectacle *only* if the z-axis
  honestly encodes convergence/tier.
- **D — Static-first "islands," not a single-page app.** Prerender one HTML dossier per entity;
  hydrate only the interactive pieces (graph, search, filters, context toggle). Wins first paint,
  shareable URLs, screen-reader support, and graceful degradation in one move.
- **E — One signature encoding for "convergence."** It's the entire scientific claim, so it gets ONE
  dominant visual (a radial 6-slot "channel-ring" glyph / brightness), used *identically* at every
  scale — never double-encoded via size AND color AND motion.

## What we'd ask you

**Architecture & data**
1. Is the hero path "pick one entity → read its dossier" (a routing problem) or "filter/compose a set
   across channels, tiers, and contexts" (a client-side query engine)? Which do we optimize first?
2. Are the two contexts a global toggle that re-binds a few verdicts, a side-by-side comparison, or
   separate datasets — and should verdicts be precomputed per context or rebound at runtime?
3. How do we lock a **validated schema contract** (types + a build-time validator) so a field rename
   can't silently blank a section of the UI?
4. Do provenance refs resolve to inspectable records or opaque tokens? (Sets the floor on how deep the
   audit trail can go.)

**Visualization**
5. Is convergence the single quantity a viewer must read off any node in **under 2 seconds** — the
   design's spine — or one attribute among many?
6. Should node positions **carry meaning** (high-convergence toward a bright center; cleared/decoys to
   a dim periphery), or stay aesthetic and be explicitly labeled as such?
7. 87% of edges are single-channel — should the default view **hide that long tail** and surface only
   the rare multi-channel, signed, and conflict edges?
8. Are the rare **sign-conflicts** noise to hide, or first-class "here's where the evidence disagrees"
   features (which is exactly what a skeptic hunts for)?

**Immersion & motion**
9. Is the primary deliverable a ~3-minute **scripted video** or an interactive engine — and can one
   keyframed camera codepath serve both the guided first-run and the screen-recorded reel?
10. What should switching context *feel* like — a **re-lighting of the same fixed cast** (positions
    hold, verdicts flip in place) or a scene change?
11. Is there a canonical **hero entity** (a max-convergence core node) to choreograph a cold-open
    around, and do we have a **naive baseline** to show decoys "blaze then collapse" for real?

**Product & onboarding**
12. What is the ONE job an expert arrives to do — audit a specific verdict, discover convergence, or
    stress-test against the naive baseline? Each implies a different landing surface.
13. Where does **trust** live for this audience — the channel *count*, the channel *independence*, or
    only clicking through to the source? Whatever it is should be the most prominent thing on a dossier.

**Performance & accessibility**
14. What's the **first-paint contract** — what must be legible in under 1s with no JS running — and
    what's the worst device/network a skeptical reviewer will open this on?
15. How do we make **reduced-motion a first-class design** (same final state, different tempo) rather
    than a kill switch, and never convey a verdict through motion or color alone?

---

## The reference for "the feel"

The target is an entity-driven "engine": a search / command-palette + example chips; on selection, a
composed dossier (headline verdict + tier, an auditable step-by-step "how it decided", a focused
node-and-edge visualization, evidence cards each with a "view provenance" drill-down, and a narrative
that *explains* but never *decides*); a validation scoreboard rendered as an interactive results grid;
a guided tour; light/dark; and a context switch — all provenance-first. We want our honest version of
that.

*Our internal execution plan (build phases, expected advice, pitfalls) lives in `PLAN.md` — not part
of what we'd hand the expert, but it's what we'd build once they've reacted to the above.*
