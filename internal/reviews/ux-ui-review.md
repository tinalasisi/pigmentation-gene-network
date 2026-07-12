# UX/UI Review: Pigmentation Gene Network Site

**Scope note up front:** This is a review of **presentation only** — look, feel, navigation, first impression, accessibility, and share-ability. It says nothing about your science, your claims, or whether the analysis is correct; assume all of that is strong and untouched here. The site is a Quarto report of a Claude Science project, and it will be judged the way hackathon sites usually are: skimmed in a hurry, often on a projector or a phone, and frequently reached through a link someone pasted into a chat. Everything below is aimed at that reality, and almost all of it is a few lines of YAML or SCSS away.

The honest headline: your typography, palette discipline, and information architecture are already better than most hackathon submissions. What's missing is the *packaging* — the first-screen hook, the shareable link card, and a few polish tells. Those are exactly the cheap, high-visibility things a judge notices.

*A note on evidence:* the findings below come from inspecting the live site. Where a specific filename or path is needed for a fix, verify it against your repo before pasting it into config — those spots are marked "verify."

---

## The 10-second test

A judge opens your link. In the first 10 seconds they see a teal navbar, a clean title, and then **two paragraphs of prose** — no image, no figure, nothing that says "here is the result." For a project about a gene **network**, the landing page shows no network, and the homepage renders **zero `<img>` tags**. Yet the project's main scientific figure exists as a rendered PNG; it simply never appears on the page a judge is guaranteed to see.

**The single highest-leverage fix is to put one strong figure above the fold on the homepage.** It converts the first impression from "README" to "designed project," and the asset already exists. If you do only one visual thing before submitting, do this.

---

## What's already working

Preserve these. They do real work, and a judge feels them even without naming them.

- **It reads like a publication.** A restrained two-color system (teal `#2F5D62` + amber `#B06A1E` over near-black on white) reads as *chosen*, not the default cosmo blue.
- **Body typography is genuinely excellent** — 17px, ~1.65 line-height, ~628px reading measure, **14.9:1 contrast** (past WCAG AAA). Long console blocks stay comfortable and survive projector glare.
- **Code is folded by default** behind a native `<details>` "Show code" toggle, so a skimming judge meets prose and figures first, not walls of Python. Most hackathon sites get this wrong.
- **The navigation plumbing is wired**: working search, resolving deep-link anchors (`#tldr`), reader mode, prev/next pager, and a right-hand "On this page" TOC. Search in particular is the fastest route a rushed judge has to your headline result — worth pointing them at it (see the "Start here" signpost below).
- **The sidebar tells a story** (Foundation → Data extraction → Networks & substrate → Rescue screen → Direction & ancestry) with human-readable `NBx · Verb-phrase` labels instead of raw filenames.
- **Mobile works** — a clean single-column collapse at 375px with no horizontal scroll and good line length.

---

## Fix before you submit — quick wins

High-impact items, ordered by impact. Most are low-effort; where one isn't, it's flagged.

### 1. Put a hero figure on the homepage
**Why it matters to a judge:** The landing page is the one screen you're guaranteed they see, and right now it has nothing to look at. The most impressive artifact you built — the network — never gets to make a first impression.
**The fix:** Embed one figure immediately under the subtitle in `index.qmd`:
```markdown
![](path/to/figure.png){fig-align="center"}
```
Point it at your most legible rendered asset — the network overview or the direction-law figure. **Confirm the exact path in your repo first** (the notebooks write PNGs under a figures directory; use the real filename). Optionally add `title-block-banner: true`. The PNG already exists, so this is near-zero cost.

### 2. Add Open Graph / Twitter cards, a description, and a favicon
**Why it matters to a judge:** Your submission travels as a pasted link. Right now the live `<head>` has **no `og:*`, no `twitter:*`, no `<meta name="description">`, and no favicon**, so in Slack, iMessage, or a judging sheet it unfurls as a bare blue title with no thumbnail and no hook. It looks unfinished before the page even loads.
**The fix:** In `_quarto.yml` under `website:`:
```yaml
site-url: https://tinalasisi.github.io/pigmentation-gene-network/
image: path/to/figure.png   # use the same verified figure path as #1
favicon: assets/favicon.png
open-graph: true
twitter-card: true
```
Add a per-page `description:` in the `index.qmd` front matter (a site-level description string is not reliably emitted on the live page; a per-page one is). A simple monogram or cropped network node in your teal/amber works as the favicon.

### 3. Scrub the leaked `/Users/tlasisi/...` path
**Why it matters to a judge:** A hard-coded home-directory path reads as "ran it once on my laptop and pasted the output" — the opposite of the reproducibility story the rest of the site tells. It currently renders as **visible stdout on the NB10 page**.
**The fix:** Print a repo-relative path instead — `print(f"saved {path.relative_to(REPO_ROOT)}")` — or silence the save line with `#| output: false`, then re-render. Before submitting, sweep the other notebooks for the same pattern (`grep -rl '/Users/tlasisi' notebooks/`) in case it surfaces elsewhere; if re-running is risky before the deadline, hand-scrub the stored `.ipynb` outputs and re-render.
**Effort note:** this is the highest-effort item in this section — it touches notebook source and requires a re-render — but its impact justifies the top-three placement.

### 4. Fix the sidebar order — it currently lists 10 → 12 → 11
**Why it matters to a judge:** Surface order reads as a proxy for engineering care. Your `_quarto.yml` sidebar lists NB10, then NB12, then NB11. Because Quarto's prev/next pager follows sidebar order by default, the pager would then walk **10 → 12 → 11**, and "Next" on NB3 would land on the **NB1a** group. At a glance those read as off-by-one bugs.
**The fix:** Reorder `sidebar.contents` in `_quarto.yml` so NB11 precedes NB12 (the pager follows automatically). Either move the `NB1a–NB1d` "Data extraction" group above Foundation if they're prerequisites, or relabel it "Appendix — data extraction" and place it last, so the `1a` prefix stops reading as out-of-sequence.

### 5. Add a footer
**Why it matters to a judge:** A finished page closes deliberately — who made it, for what event, when, under what license. You have **zero `<footer>` elements** site-wide despite shipping an MIT LICENSE and this being a dated "Built with Claude" entry.
**The fix:** One block in `_quarto.yml`:
```yaml
website:
  page-footer:
    left: "© 2026 Tina Lasisi · MIT License"
    right: "Built with Claude — Life Sciences · [GitHub](…)"
```
Confirm the exact event name before publishing so the credit line is accurate.

### 6. Add a "Start here" signpost to the homepage
**Why it matters to a judge:** With 60 seconds and ~15 equal-weight notebook bullets, a judge shouldn't have to reverse-engineer which one is the payoff. There's no "Start here," no featured-result card, and no reading order (the strings "start here" and "in order" are absent from the page). They may open a dense notebook at random and bounce before reaching your headline result.
**The fix:** A single callout at the top of `index.qmd`:
```markdown
::: {.callout-tip}
## Start here
New here? Read the Overview, then NB1 → NB4 → NB10 for the headline result. [See the result →](notebooks/10_mechanism_direction_law.html)
:::
```

### 7. Darken the amber accent to clear WCAG AA
**Why it matters to a judge:** `#B06A1E` on white is **4.26:1 — just under the 4.5:1 AA threshold** for normal text, and it's your link, breadcrumb, and sidebar-label color. A design-savvy judge clocks sub-AA link contrast instantly, and it washes out further on a bright projector.
**The fix:** One line in `theme.scss` — set `$link-color: #834b12;` (~7:1, visually near-identical). That single variable fixes links, breadcrumb, and section labels at once.

### 8. Match the homepage labels to the sidebar
**Why it matters to a judge:** The four extraction notebooks are linked on the homepage as bare "Bajpai CRISPR screen" etc., while the sidebar calls them "NB1a · Bajpai CRISPR screen." Every other homepage link keeps its prefix, so these four can't be matched 1:1 at a glance.
**The fix:** Use identical `NB1a · …` label text in both `index.qmd` and `_quarto.yml`.

---

## Higher-impact improvements

Moderate effort, but these most raise perceived quality.

### Surface the headline numbers as design moments, not console text
Your "22/22 concordant" payoff currently renders as **raw `print()` stdout in a gray `<pre>` block** — visually identical to every other log line. There are **zero tables** on the page (`df-print: paged` is configured but never fires, because the cells print strings instead of returning DataFrames). The most important result on the page is rendered with the least visual weight. Pull the one-to-three headline figures into emphasized UI — a callout, or a small stat-card grid styled in `theme.scss`:
```markdown
::: {.callout-important}
**22 / 22 loss-of-function genes concordant**
:::
```
Keep the detailed stdout underneath the existing code-fold. This is purely a re-presentation of an existing result — no science touched.

### Caption the main figure and give it alt text
The main NB10 figure has **no `alt` attribute** (a screen reader announces the filename or nothing — a WCAG 1.1.1 Level A failure, revisited in the accessibility notes) and **no caption**. A one-line caption is often the single sentence a skimming judge actually reads. Fix at source with chunk options on the plotting cell:
```python
#| fig-cap: "One-sentence takeaway of what the figure shows."
#| fig-alt: "Description of the plot for screen readers."
```
Do the hero/share figure first, then sweep the others. This also feeds your new OG image.

### Make the early notebooks announce their result like the later ones
NB05–NB12 lead with a top-of-page TL;DR; **NB01–NB04 don't** — they carry only a bottom-of-page "Summary." But the Foundation notebooks are natural entry points, so the pages a judge is most likely to open cold are the ones with no punchline in the first screenful. Add the same top-of-notebook TL;DR block to NB01–NB04. And everywhere it appears, the TL;DR is currently a **plain `<h2>` heading, not a callout** — the notebook pages use no callouts at all, and the amber-bordered "rule" box on NB10 is a plain blockquote. You already use a `callout-note` for the "Everything here…" info box on the homepage, so the pattern is proven; extend it by wrapping each TL;DR in `::: {.callout-tip}` so it stops the eye instead of blending into body prose.

### Enable click-to-zoom on figures for mobile
Your wide result PNGs (natural 2251×1355) squeeze into a narrow single column on a phone with **no lightbox**, so labels and edges get hard to read and there's no obvious way to inspect them. Set `lightbox: true` in `_quarto.yml` — tapping a figure then opens a zoomable overlay, the standard mobile pattern.

### Cross-link the notebooks where the prose already names them
There are **no body-prose links from one notebook to another** — across all sixteen notebooks, the count of inter-notebook Markdown links is zero. Where a notebook's text refers to another (e.g., "the rescue-target set from NB4"), the reference is plain, unclickable text. The corpus reads as isolated pages rather than one connected argument. Turn those existing textual references into Markdown links, or add a one-line "Related: NBx, NBy" under each TL;DR.

---

## Nice-to-haves / polish

Small items; most are one-line changes.

| Item | Why it matters | Fix |
|---|---|---|
| Sidebar fully expanded (~44 items) behind mobile hamburger | Dense, unfocused tree to scroll past on a phone | `sidebar: collapse-level: 1` in `_quarto.yml` |
| Overlong `<title>` tags | Truncate uselessly in tabs, bookmarks, and future OG cards | Shorten the H1 to the sidebar form; move the long clause to a `subtitle:` |
| H1 prefix (`Notebook 10 —`) ≠ sidebar prefix (`NB10 ·`) | Mismatch on the exact click that should feel confirming | Standardize the prefix across label and H1 |
| Mobile navbar title truncates to "Pigmentation ge…" | The only always-visible branding on a phone gets cut off | Shorter display title or a small `logo:` |
| Navbar has one text link ("Overview") | Mid-site landers get no top-level orientation | Optionally add "Reproducibility" / "Results" to `navbar.left` |
| "On this page" TOC starts at "Step 2" | Reads as a dropped section | Give the Step 1 / Setup content a heading, or renumber from 1 |
| No dark mode | White flash for dark-OS judges; a reader-mode toggle already exists | `theme: {light: [cosmo, theme.scss], dark: [cosmo, theme-dark.scss]}` |
| Print / PDF path unverified | Judges sometimes export or print; the fixed navbar, code-fold `<details>`, and dark chrome all have print implications | Verify how a page prints and, if needed, add a small `@media print` rule (hide the navbar, expand folded code) |
| Consider one distinctive heading typeface | Type + chrome are undifferentiated; distinctiveness is a scoring lever | Set `$headings-font-family` in `theme.scss`; optional accent rule under h2s |

---

## Accessibility notes

The foundation here is strong — **14.9:1 body contrast** (past AAA), `lang="en"` declared (WCAG 3.1.1), semantic ordered headings with working anchors, keyboard-operable native `<details>` toggles, and single-column reflow at 375px (WCAG 1.4.10). Keep all of it. Three focused gaps remain:

- **Contrast (WCAG 1.4.3, AA):** the amber `#B06A1E` at 4.26:1 is sub-threshold for normal text — darken to `#834b12` as in quick-win #7. One caveat to verify: body links should also carry a non-color affordance (an underline). If they're currently color-only, add one, since 1.4.1 (Use of Color) depends on it.
- **Non-text content (WCAG 1.1.1, Level A):** the headline figure has a fully absent `alt` attribute — the most severe of the accessibility items, fixed by the `#| fig-alt:` add in the higher-impact section above.
- **Motion:** the fixed navbar uses a "headroom" auto-hide that slides on every scroll-direction change, and it does not appear to be guarded by `prefers-reduced-motion`. This is an AAA-level concern (2.3.3) affecting motion-sensitive users only, so it's low priority — but cheap to close:
  ```scss
  @media (prefers-reduced-motion: reduce) {
    header.headroom { transition: none !important; transform: none !important; }
  }
  ```
  Or simply pin the navbar to disable the effect for everyone.

---

## If you only do three things

Do these, in this order. **(1)** Put a hero figure on the homepage — it fixes the 10-second test that decides everything. **(2)** Add the OG/Twitter/favicon/description YAML — your submission is judged through a shared link, and right now that link looks empty. **(3)** Scrub the `/Users/tlasisi/` path leak — it's the one visible tell that undercuts your reproducibility story. The first two are minutes of work against assets and config you already have; the third is a little more involved but worth it. Together they move the site from "strong report that looks unfinished" to "finished project." Everything else here is genuine polish on an already-credible foundation — reach for the footer, the sidebar reorder, and the results-as-callouts next if the clock allows.