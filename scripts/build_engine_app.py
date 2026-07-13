#!/usr/bin/env python3
"""Build app/index.html from the commissioned prototype (app/vendor/) by applying
a small set of deterministic edits. Reproducible: re-run to regenerate.

The prototype (an expert handoff, MIT-spirit demonstrator) is kept verbatim in
app/vendor/. We do NOT fork its logic; we only:
  1. load real data from app/data/dataset.js instead of the inlined toy blob,
  2. make provenance citations real clickable links (access-aware),
  3. hide the context switch (cross-context re-binding is deferred),
  4. rebrand (title / header / footnote) to reflect real, preview data,
  5. add radial-layout band 6 (production has up to 6 channels; the toy had ≤5).

Regenerate:  python3 scripts/build_engine_app.py
"""
import re, os

SRC = "app/vendor/convergence-engine-prototype.html"
OUT = "app/index.html"
h = open(SRC).read()

def sub1(pat, repl, flags=0, literal=False):
    global h
    p = re.escape(pat) if literal else pat
    h, n = re.subn(p, repl.replace("\\", "\\\\") if literal else repl, h, count=1, flags=flags)
    assert n == 1, f"NO MATCH: {pat[:70]}"

# 1) external real data
sub1(r"<script>window\.__DATASET__=.*?</script>", '<script src="data/dataset.js"></script>', re.DOTALL)

# 2) brand / title / footnote
sub1("<title>Convergence Engine — prototype</title>",
     "<title>Pigmentation convergence engine — preview</title>", literal=True)
sub1("Convergence Engine <small>prototype · toy data</small>",
     "Convergence Engine <small>preview · real data · provisional verdicts</small>", literal=True)
sub1("Prototype against the fictional toy dataset (55 entities · 170 edges · 6 channels · 30 benchmark items).",
     "Preview on real harmonized-substrate data (803 entities · 7,818 edges · 6 channels). Verdict tiers are a "
     "provisional derived rule pending domain review; the benchmark is the real NB10 direction-law result "
     "(22/22 concordant).", literal=True)

# 3) clickable, access-aware citation popover
old_pop = ('  pop.innerHTML=r?`<div class="pk">${esc(r.kind)}</div><div class="pc">${esc(r.citation)}</div>\n'
           '    <div class="pnote">In production this resolves to the full source record (locator, excerpt, outbound link).</div>`')
new_pop = ('  pop.innerHTML=r?`<div class="pk">${esc(r.kind)}</div><div class="pc">${r.url?`<a href="${esc(r.url)}" '
           'target="_blank" rel="noopener" style="color:var(--accent);text-decoration:underline">${esc(r.citation)} '
           '↗</a>`:esc(r.citation)}</div>\n'
           '    <div class="pnote">${r.access===\'public\'?\'Public source — opens the original record.\':'
           '\'Access: \'+esc(r.access||\'unknown\')}</div>`')
sub1(old_pop, new_pop, literal=True)

# 4) hide the context switch when there is a single context
sub1("  const el=document.getElementById('ctxswitch');\n",
     "  const el=document.getElementById('ctxswitch');\n  if(el && CTXS.length<2){ el.style.display='none'; return; }\n",
     literal=True)

# 5) radial layout: include band 6 and spread radii across 1..6
sub1("  const bandR=n=>1.02-(n-1)*0.20;                    // n=1 → 1.02 … n=5 → .22",
     "  const bandR=n=>1.05-(n-1)*0.165;                   // n=1 → 1.05 … n=6 → .23", literal=True)
sub1("  const bands=[5,4,3,2,1].map(n=>ENTS.filter(e=>e.n_channels===n));",
     "  const bands=[6,5,4,3,2,1].map(n=>ENTS.filter(e=>e.n_channels===n));", literal=True)

open(OUT, "w").write(h)
print(f"wrote {OUT} ({len(h)//1024} KB)")
