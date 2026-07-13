# What we have vs. an interactive site like Aitiome

*A plain-software description for a developer — deliberately written with no domain
(subject-matter) jargon, so the architecture and UX are the only things on the table.*
*Reference studied: `https://aitiome.fly.dev/`.*

---

## The one-line difference

We built a **static, pre-rendered document** with one embedded 3-D chart. They built a **live
web application you drive by querying**: you pick an item, and it assembles a custom multi-panel
"dossier" for that item on demand. The two sites sit on the *same kind* of data — a set of
entities, their attributes, the relationships between them, and source citations — but the
delivery model is completely different.

---

## Our data, described generically

- **~800 entities** ("nodes"). Each entity carries: membership flags across **~6 categorical
  "layers,"** a few boolean/enum **attributes**, and a **provenance record** (source citations).
- **Relationships** ("edges") between entities, each attributable to one or more layers/sources,
  each with provenance.
- A handful of small **result tables** (computed classifications over subsets of entities).
- Everything is **fixed and precomputed**, stored as CSV / JSON files in the repo.

So the underlying data is already structured, enumerable, and source-tagged. That matters a lot
below.

---

## What WE have (in developer terms)

- **Delivery:** a static-site generator (Quarto) emits plain HTML; hosted on GitHub Pages, which
  is **pure file hosting with no server-side compute**. Deploy is a GitHub Action on `git push`.
- **Mental model:** it is a **document**. A set of long-form "report" pages (each one a
  pre-executed computational notebook with its outputs baked in at build time) plus a landing
  page. You read it top to bottom.
- **Interactivity:** exactly **one embedded interactive view** — a 3-D visualization built with an
  off-the-shelf charting library (Plotly), embedded in an iframe, reading a single precomputed
  dataset. You can rotate, zoom, hover for tooltips, and toggle categories on/off. Everything
  else is reading: a sidebar, a table of contents, full-text search over the page text, and
  collapsible code blocks.
- **No query loop. No per-entity views. No application state.** A visitor cannot type "show me
  entity X" and get a composed answer — they scroll to wherever we already wrote about it.
- **Aesthetic:** light, clean, "published paper / report" feel; default system fonts.

## What THEY have (in developer terms)

- **Delivery:** a **single-page application** (one bundled JS file with hashed asset names + custom
  web fonts — the signature of a Vite/webpack build) talking to a **REST API backend** on the same
  host, deployed as a **container on Fly.dev** (which, unlike static hosting, can run a live
  server). There is a visible **"engine live" health indicator**, backed by a real `/api/health`
  endpoint.
- **The API surface I actually observed** (all domain-neutral names):
  `/api/list-of-items`, `/api/assess?id=…` (the per-item result), `/api/synthesis?id=…` (the
  per-item narrative), `/api/pathway`, `/api/benchmark`, `/api/health`, `/api/contexts`,
  `/api/candidates`, `/api/discovery-map`. In other words, the frontend is thin and the server
  answers questions per item.
- **Mental model:** an **entity-driven engine**. The primary control is a **search / "resolve"
  box** plus **preset example chips grouped by category**. You pick an item → the app fetches that
  item's result and **composes a bespoke dossier** made of:
  - a headline **verdict / score** with a tier label and a canonical ID;
  - the **result in the other context** as well (they maintain two switchable "contexts," toggled
    at the top);
  - an ordered, numbered **"reasoning pipeline"** (step 1 → step 5) that shows *how* the result was
    derived, presented as auditable and deterministic;
  - a **directed-path visualization** — glowing, animated nodes-and-edges along a chain on a dark
    cinematic canvas, with a dramatic terminal node (this is custom motion/glow work, not an
    off-the-shelf chart);
  - a set of **evidence cards**, each with a finding, a stance, a source, and a **"view provenance"**
    drill-down;
  - an **auto-generated narrative** that explains the result in prose, explicitly separated from the
    deterministic decision ("the model explains the path; it never makes or changes the call").
- **A validation scoreboard:** big number tiles ("13/13 … 15/15 … 0 errors") plus a **full grid of
  every test item with its outcome, colour-coded** — it *proves the method works* in one glance.
- **Onboarding:** a **"guided tour"** button ("a 30-second guided path through the thesis").
- **Extras:** a **light/dark theme toggle**; a **context switch** that rebinds the whole app; and
  **every claim is a clickable, provenance-linked object** (citation links + "view provenance"
  buttons).
- **Aesthetic:** dark, cinematic, motion-rich, "engine / terminal" product feel; a distinctive
  display typeface plus a monospace font.

---

## The core gap (it's the shape of the experience, not the data)

| Dimension | Ours | Theirs |
|---|---|---|
| Mental model | a report you **read** | an engine you **query** |
| Unit of interaction | a **page** | an **entity** |
| Who drives it | the author (pre-written) | the user (on demand) |
| Visualization | one fixed 3-D chart | a **composed, animated dossier per entity** |
| "Does it actually work?" | prose + figures | a **live scoreboard + results grid** |
| First-run help | none | a guided tour + preset examples |
| Explanation | static text | per-item narrative, separated from the logic |
| Tech | static HTML files | SPA + API (or SPA + precomputed JSON) |
| Feel | a paper | a product |

---

## The good news — worth leading with when you talk to the dev

We **already have the hard part**: structured, enumerable, provenance-tagged data, and a result
set that is **fixed and finite**. That strongly implies we **do not need their live backend**.
We can precompute *every* entity's dossier — its attributes, its layer memberships, its neighbours,
its provenance, and any classification — into **static JSON**, and build an entity-driven SPA that
reads those files. That gets roughly 80% of the "immersive app" feel while staying on **free static
hosting** (GitHub Pages). A live server is only strictly required when the set of possible answers
is open-ended; ours is not.

We also already have two reusable seeds: a working **3-D interactive graph** and a portable
**graph JSON** (nodes with per-layer membership + edges). Those can become the "explore" view
inside a search-box-and-dossier shell rather than being rebuilt.

---

## Questions to put to the developer

1. **Backend or not?** Our results are fixed and precomputable. Can we ship a **static SPA +
   bundled JSON** instead of standing up a server, and what would we actually lose by doing so?
2. **What is the "atom" a user explores?** Their whole app centers on *one entity → its dossier*.
   Should ours center on an **entity**, a **relationship**, or a **computed result**? This single
   decision drives the entire information architecture.
3. **Frontend stack** for an entity-driven app: which framework (React / Svelte / Vue), and which
   visualization approach — an existing graph/network library, or **custom Canvas/WebGL** for the
   immersive animated view like theirs?
4. **Immersive but still legible:** how to add motion, glow, and "focus-plus-context" (zoom into one
   entity's neighbourhood, smooth transitions between views) without turning it into an unreadable
   hairball.
5. **Onboarding & progressive disclosure:** a guided tour, preset examples, and inline "explain
   this" affordances — how much of that is cheap to add.
6. **Reuse:** can our existing 3-D graph + graph JSON be dropped straight into the "explore" panel,
   wrapped in a search/resolve + dossier layout?
7. **Effort tiers:** what is the **smallest version that still feels like an app** (a search box +
   a per-entity panel reading static JSON), versus the **full build** (live API, animated canvas,
   scoreboard, guided tour)? Where's the best bang-for-buck stopping point?

---

*Prepared to accompany a request for a software developer's advice on making our data
representation more interactive and immersive. The reference site's specifics above come from
directly inspecting its running frontend and network traffic.*
