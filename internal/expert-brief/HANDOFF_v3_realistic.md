# Handoff v3 — a production-scale toy, and the compromise we're after

*For the software dev, following the v2 "convergence-stack" handoff. Comes with a new toy dataset
(`toy_v2/`) that is the same schema as before but **at production scale** — so the design problems
we're hitting are visible in your own prototype.*

---

## TL;DR

Your stack prototype is the right direction — we love the slices. But we tested it on our real data
and hit problems the 55-entity toy couldn't show. **The toy was too simple.** So here's a new toy at
real scale (~800 entities, ~7,800 edges, our real heavy-tailed distributions), and a request: solve
the at-scale legibility + a specific look we want, against *this* toy.

## What we did with your v2 prototype

We dropped our real data into `convergence-stack.html` unchanged (as designed — thank you, it just
worked) and made two edits from your own advisory:
- **Turned the single-layer edge tail OFF** (drawing only `n_channels≥2 || sign_conflict`). At real
  scale the tail was a solid hairball, exactly as you predicted.
- Confirmed **click-to-source is real**: in production 100% of refs resolve to public URLs
  (PubMed / DOI / UniProt / KEGG / Reactome). (In the toy they're placeholders — treat them as
  resolvable.)

## What broke at scale (the 55-entity toy hid these)

1. **The single-layer majority is huge.** 550 of 803 entities sit on exactly one layer. Even with
   edges off, each plane is a dense field of hollow rings. It reads as clutter, not context.
2. **The thread column is thick and you can't see through it.** The ~250 multi-layer entities bunch
   their vertical threads into a solid central column that occludes everything behind it.
3. **The broad base plane dominates** (one channel covers 694/803).

## The look we're after — a compromise between two things we tried

We built a second, from-scratch exploration and compared. We want to **marry the two**:

- **Keep from your stack:** the slices, the stance rings (implicates/notes), the honest counted
  copy, the docked dossier, the convergence slider, "rotation carries no meaning."
- **Bring in from our exploration:**
  - **A dark / near-black background.** We strongly prefer it — it made the stack feel like an
    object, not a diagram. Make dark work if it can be made legible at scale.
  - **A camera fly-to on select.** Clicking an entity should *fly* the camera to it (then light its
    thread + dock the dossier). That motion was the single most "alive" thing we tried.
- **What we do NOT want:** the heavy additive **glow** we used. It blew out to white and buried the
  data. Cinematic ≠ glowy. Calm nodes, subtle depth — no bloom.

## Questions for you (against `toy_v2/`)

1. **Dark background at scale** — viable for this instrument, or does light genuinely win for
   legibility with 800 nodes + 6 translucent planes? We want dark; tell us the real trade and how to
   make it work (plane alpha, node contrast, fog).
2. **The thick thread column** — how do we keep it *see-through* and readable? (thinner threads,
   transparency, threads only on selection/hover, gentle curvature/bundling, depth-based LOD?)
3. **The 550 single-layer entities** — keep-but-recede, default-hide-with-a-visible-count
   ("550 single-layer entities hidden — show all"), or spatially thin them? Whatever it is must stay
   honest (they're the real denominator; we won't cherry-pick them away).
4. **Fly-to-on-select** — how should it compose with your dim-others + light-thread + dossier dock so
   it feels like one motion, and what's the reduced-motion equivalent?
5. **Cinematic-but-calm on dark** — how do you get depth and "wow" without additive glow (rim light?
   subtle size falloff? a single restrained accent)?
6. **Anything the small toy hid** that ~800 nodes now reveals about occlusion, picking, or perf.

## The new toy

`toy_v2/dataset.js` and `toy_v2/dataset.json` — **same schema as v1**, drop-in: replace the inline
`window.__DATASET__ = …` in `convergence-stack.html` with this file and it runs at real scale. It is
our production substrate with every domain string masked (fictional cold-case skin, real structural
skeleton): **803 entities, 7,818 edges, 6 channels**; entity→#layers = {1:550, 2:127, 3:69, 4:33,
5:15, 6:9}; one broad channel (694) down to a selective one (45); 97% single-channel edges; the one
sign-conflict edge preserved. Hosting target is **Vercel**; single context for v1; verdict tiers are
a provisional derived rule (a caveat, not a claim).

Anything you prototype or advise against this drops onto our real data unchanged.
