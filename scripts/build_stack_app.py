#!/usr/bin/env python3
"""Build immersive-app/public/index.html from the dev's v4 stack prototype
(immersive-app/vendor/convergence-stack-prototype.html) with our real data + small edits:
  1. load real data from data/dataset.js instead of the inlined toy,
  2. make provenance citations real clickable links (access-aware),
  3. rebrand (title / header),
  4. relabel the auto-computed "mixed testimony" door for gene data.

The v4 prototype already single-context-guards the context switch and auto-computes the example
doors from whatever data is loaded, so nothing else is needed.

Regenerate:  python3 scripts/build_stack_app.py   (after scripts/build_engine_data.py)
"""
import re

SRC = "immersive-app/vendor/convergence-stack-prototype.html"
OUT = "immersive-app/public/index.html"
h = open(SRC).read()

def sub1(pat, repl, flags=0, literal=False):
    global h
    p = re.escape(pat) if literal else pat
    h, n = re.subn(p, repl.replace("\\", "\\\\") if literal else repl, h, count=1, flags=flags)
    assert n == 1, f"NO MATCH: {pat[:70]}"

# 1) external real data
sub1(r"<script>window\.__DATASET__=.*?</script>", '<script src="data/dataset.js"></script>', re.DOTALL)

# 2) brand
sub1("Convergence Stack — prototype v3", "Pigmentation substrate — layer stack", literal=True)
sub1("Convergence Stack <small>prototype · toy data</small>",
     "Pigmentation substrate <small>preview · real data · provisional verdicts</small>", literal=True)

# 3) clickable, access-aware citation popover
old = ("  pop.innerHTML=r?`<div class=\"pk\">${esc(r.kind||'source')}</div>"
       "<div class=\"pc\">${esc(r.citation||btn.dataset.ref)}</div>\n"
       "    <div class=\"pnote\">Placeholder in this toy — in production every reference resolves to a "
       "public record (PubMed / DOI / UniProt / KEGG / Reactome).</div>`")
new = ("  pop.innerHTML=r?`<div class=\"pk\">${esc(r.kind||'source')}</div>"
       "<div class=\"pc\">${r.url?`<a href=\"${esc(r.url)}\" target=\"_blank\" rel=\"noopener\" "
       "style=\"color:var(--accent)\">${esc(r.citation||btn.dataset.ref)} ↗</a>`:esc(r.citation||btn.dataset.ref)}</div>\n"
       "    <div class=\"pnote\">${r.access==='public'?'Public source — opens the original record.':"
       "'Access: '+esc(r.access||'unknown')}</div>`")
sub1(old, new, literal=True)

# 4) relabel the auto-computed door for gene data
sub1("— mixed testimony", "— mixed evidence (mechanism + context)", literal=True)

# 5) relabel the confusing "implicates / notes" language as "mechanism / context"
#    (filled = a signed/directed interaction; hollow = co-occurrence / pathway membership).
#    Internal stance keys stay 'implicates'/'notes' (so the fill logic + CSS are untouched);
#    only what the user sees changes.
sub1('<span class="stance ${s.stance}">${s.stance}</span>',
     '<span class="stance ${s.stance}">${({implicates:\'mechanism\',notes:\'context\'}[s.stance]||s.stance)}</span>',
     literal=True)
sub1("● filled dot = layer <b>implicates</b> · ○ hollow = layer only notes presence.",
     "● filled = <b>mechanism</b> (a signed, directed interaction) · ○ hollow = <b>context</b> "
     "(co-occurrence or pathway membership — no direction).", literal=True)
sub1("${impl} implicate · ${strands.length-impl} note",
     "${impl} mechanism · ${strands.length-impl} context", literal=True)
sub1("A strand that merely <em>notes</em> presence never raises a verdict.",
     "A layer that only places the gene in a <em>context</em> (no direction) never raises a verdict.",
     literal=True)
sub1("${implCount(e)} implicate · ${TIERS", "${implCount(e)} mechanism · ${TIERS", literal=True)
sub1("<th>implicating</th>", "<th>mechanism</th>", literal=True)
sub1("● filled means that layer implicates, ○ hollow means it only notes.",
     "● filled means the layer gives a directed mechanism, ○ hollow means it only places the gene in a context.",
     literal=True)
sub1("except any single-layer entity the method implicates, which never fades.",
     "except any single-layer entity that has a mechanism layer, which never fades.", literal=True)
sub1("which layers implicate, which only note, every claim with its source.",
     "which layers give a mechanism, which only give context, every claim with its source.", literal=True)

# 6) declutter the bottom control bar. It packed six control clusters into one
#    non-wrapping centered flex row, so on a normal screen the ends clipped off
#    (the whole view [stack|slices] toggle fell off the left edge — unreachable).
#    Fix: keep the two *narrative* controls (view, single-layer) + Reset always
#    visible; tuck the three refinements (threads, Spread, layers≥) into a
#    "Display options" popover. Also let the bar wrap + cap its width as a safety net.

# 6a) the bar wraps and never exceeds the viewport; raise it above the dossier so
#     the popover is never occluded when a gene is selected.
sub1(".controls{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:25;display:flex;",
     ".controls{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:36;display:flex;"
     "flex-wrap:wrap;justify-content:center;max-width:min(94vw,980px);row-gap:8px;", literal=True)

# 6b) popover + trigger styles (appended right after .ctl-label).
#     NB: .morepop sets display:flex, which would defeat the HTML `hidden` attribute,
#     so .morepop[hidden]{display:none} is required to keep it collapsible.
sub1(".ctl-label{font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);padding:0 2px}",
     ".ctl-label{font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);padding:0 2px}\n"
     ".morepop{position:absolute;left:50%;transform:translateX(-50%);bottom:calc(100% + 12px);z-index:37;"
     "display:flex;flex-direction:column;gap:14px;align-items:flex-start;"
     "background:color-mix(in srgb,var(--bg) 90%,transparent);backdrop-filter:blur(11px);"
     "border:1px solid var(--line-soft);border-radius:12px;padding:15px 17px;"
     "box-shadow:0 14px 44px rgba(0,0,0,.5);min-width:232px}\n"
     ".morepop[hidden]{display:none}\n"
     ".morebtn[aria-expanded=\"true\"]{background:var(--panel-2);color:var(--ink);border-color:var(--ink-3)}",
     literal=True)

# 6c) insert the trigger + open the popover just before the threads control.
sub1('<span class="ctl-label">threads</span>',
     '<button class="cbtn morebtn" id="morebtn" aria-expanded="false" aria-controls="morepop" '
     'onclick="var p=document.getElementById(\'morepop\'),o=p.hasAttribute(\'hidden\');'
     'p.toggleAttribute(\'hidden\');this.setAttribute(\'aria-expanded\',o?\'true\':\'false\')">'
     'Display options &#9662;</button>\n'
     '  <div class="morepop" id="morepop" hidden role="group" aria-label="Display options">\n'
     '  <span class="ctl-label">threads</span>', literal=True)

# 6d) close the popover just before Reset view (threads + Spread + layers≥ now live inside it).
sub1('<button class="cbtn" id="homebtn">Reset view</button>',
     '</div>\n  <button class="cbtn" id="homebtn">Reset view</button>', literal=True)

# 6e) clearer label now that Spread sits in an options panel.
sub1('<button class="cbtn" id="spreadbtn" aria-pressed="false">Spread</button>',
     '<button class="cbtn" id="spreadbtn" aria-pressed="false">Spread the stack</button>', literal=True)

# 7) the single flagged "sign conflict" (NFKB1/TP53) is really a FEEDBACK LOOP, not a
#    source disagreement — each direction is consistently sourced (NFKB1 activates TP53,
#    confirmed by OmniPath; TP53 represses NFKB1 via the keratinocyte backbone). And there
#    are ZERO genuine "sources disagree" cases in this data. So: relabel it a feedback loop,
#    render both directions honestly from the enriched `directions` field, add a legend that
#    explains every relationship mark, and delete all "sources disagree" copy.
#    (Internal edge flag stays `sign_conflict` so the draw/pick/pin plumbing is untouched.)

# 7a) relationships legend, directly under the "Relationships" heading in the dossier
sub1('then by how many layers back each.</p>',
     '''then by how many layers back each.</p>
      <div class="rel-legend" aria-label="What the relationship marks mean">
        <span><span class="sg">→</span>direction</span>
        <span><span class="sg">+</span>activates</span>
        <span><span class="sg">-</span>represses</span>
        <span><span class="sg">·</span>association (no sign)</span>
        <span><span class="sg fb">⇄</span>feedback loop</span>
        <span><span class="sw"></span>evidence layers</span>
      </div>''', literal=True)

# 7b) summary line: suppress the one-way arrow for a feedback edge (a loop has no single
#     direction); the ⇄ sign glyph + "feedback loop" chip carry it instead.
sub1("${esc(edge.type)}${edge.directed?(",
     "${esc(edge.type)}${edge.sign_conflict?'':edge.directed?(", literal=True)

# 7c) summary sign glyph: reciprocal (feedback) instead of the plus/minus glyph
sub1("?'±':esc(edge.sign", "?'⇄':esc(edge.sign", literal=True)

# 7d) chip: "feedback loop" instead of "sources disagree"
sub1('--t-im)">sources disagree</span>', '--t-im)">feedback loop</span>', literal=True)

# 7e) after the neighbor row, spell out each direction: who activates/represses whom, with sources
sub1("""</div>`}).join('')||'<p class="sub">No recorded relationships.</p>'}""",
     """</div>${(edge.sign_conflict&&edge.directions&&edge.directions.length)?`<div class="edgedirs">${edge.directions.map(d=>`<div class="edgedir"><span class="sign ${d.sign==='±'?'conflict':''}">${esc(d.sign)}</span><span><b>${esc((byId[d.from]||{}).codename||d.from)}</b> ${esc(d.verb)} <b>${esc((byId[d.to]||{}).codename||d.to)}</b> · <span class="esrc">${d.sources.map(esc).join(' · ')}</span></span></div>`).join('')}</div>`:''}`}).join('')||'<p class="sub">No recorded relationships.</p>'}""", literal=True)

# 7f) left "Reading the stack" legend: relabel the dashed edge
sub1("Dashed red = sources disagree on sign.",
     "Dashed = a feedback loop: the two genes regulate each other with opposite signs.", literal=True)

# 7g) example door: feedback loop instead of "where sources disagree"
sub1("where sources disagree", "a feedback loop", literal=True)

# 7h) guided-intro beat: retitle + rewrite the body honestly
sub1("t:'Where sources disagree'", "t:'A feedback loop'", literal=True)
sub1("One link in this data carries contradictory signs from two sources. It is drawn dashed red, never averaged away, never faded out",
     "One pair here regulates itself both ways with opposite signs, one gene activating its partner while the partner represses it back. Each direction is independently and consistently sourced, so it is a feedback loop, not a data conflict. It is drawn dashed, never averaged away, never faded out",
     literal=True)

# 7i) styles for the legend + per-direction rows
sub1(".neigh .lch i{width:6px;height:6px;border-radius:2px;display:block}",
     ".neigh .lch i{width:6px;height:6px;border-radius:2px;display:block}\n"
     ".rel-legend{display:flex;flex-wrap:wrap;gap:6px 12px;margin:2px 0 10px;font-size:10.5px;color:var(--ink-3)}\n"
     ".rel-legend span{display:inline-flex;align-items:center;gap:5px}\n"
     ".rel-legend .sg{font-family:var(--mono);font-size:11px;color:var(--ink-2);min-width:12px;text-align:center}\n"
     ".rel-legend .sg.fb{color:var(--t-im);font-weight:700}\n"
     ".rel-legend .sw{width:8px;height:8px;border-radius:2px;background:linear-gradient(90deg,var(--ch-0),var(--ch-3),var(--ch-5))}\n"
     ".edgedirs{margin:1px 0 5px 92px;display:flex;flex-direction:column;gap:3px}\n"
     ".edgedir{font-size:11px;color:var(--ink-2);display:flex;align-items:baseline;gap:6px}\n"
     ".edgedir .sign{font-family:var(--mono);width:12px;text-align:center;flex:none}\n"
     ".edgedir .esrc{color:var(--ink-3);font-size:10px}", literal=True)

open(OUT, "w").write(h)
print(f"wrote {OUT} ({len(h)//1024} KB)")
