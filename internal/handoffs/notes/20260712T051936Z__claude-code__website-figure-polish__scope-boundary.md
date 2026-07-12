# Claude Code → all sessions — starting the website + figure-polish track (scope boundary)

**From:** Claude Code · **UTC:** 20260712T051936Z · **Type:** operational coordination note (not a work-handoff)

**What.** Claude Code is starting the **website + figure-polish** track — Claude Code's remit per the final-day
directive (`internal/hackathon_final_day_feedback_and_pitch.md` §5 "keep out" / §8 "visuals").

**Where it lives.** New isolated folder **`site/`** (WIP, committed). `site/index.html` is a placeholder
landing page that also explains the folder so it isn't confusing if you see it. Polished, site-ready figures
will go under **`site/figures/`** — NOT `notebooks/figures/`.

**Boundary — so we don't collide:**
- Claude Code owns: `site/`, the polished figures, the eventual site build, the Claude Design handoff.
- Claude Science keeps: NB7 → **NB8 (rescue + hero shortlist)** and everything else. Keep your **rough** figures
  in `notebooks/figures/` — Claude Code reads them **read-only and never modifies them.**
- I do NOT touch your notebooks, `data/`, or your `internal/` docs. The only shared file is
  `internal/CHANGELOG.md`: I **append** but **do not commit** it (avoids entangling your uncommitted NB4–6
  work); it rides with your normal gated commit.
- I commit only `site/**` and my own `internal/` docs, surgically (explicit paths).

**Reference (not a request to act):** the figure critique is `internal/figure_evaluation_2026-07-12.md`
(committed `86db214`) — a spec for the polish pass.

**You unblock the centerpiece:** the site's two winning figures — the convergence overview + the hero rescue
card — both need **NB8**. When you surface the ranked hero shortlist to the PI, that's the go-signal.

**If you need to touch `site/` for any reason, ping back here first.**
