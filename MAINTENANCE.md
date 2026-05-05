# VisitModoc Maintenance

A pragmatic checklist for keeping the site fresh, accurate, and accessible.
No fixed cadence — run through the relevant section whenever you feel like
a freshen, or hand it to Claude with "let's do a quarterly pass."

## Quarterly: full freshen pass

- [ ] **Accessibility audit (Lighthouse)** — run against home, alturas, cedarville, places-to-visit, where-to-eat, where-to-stay, webcams, plan-your-visit, technical-details. Target ≥95 across all categories. Easy ask: "run a Lighthouse audit on the key pages and triage."
- [ ] **Link checker** — catches dead Google Maps refs, retired source links, closed-business pages.
  ```
  brew install lychee && lychee --max-concurrency 4 --exclude-mail https://visit-modoc.com
  ```
- [ ] **Business listings spot-check** — pick 5 random entries from alturas/cedarville/where-to-eat. Still open? Hours/contact info current? Use Google Maps + the business's own site/social.
- [ ] **Image / licenses.json sync** — every file in `static/` referenced from templates should have a `licenses.json` entry; remove orphans, fill in missing alt-text.
- [ ] **Visitor + scanner log review** — `python analyze_visitors.py --since 30d` for humans, `--include-bots` for the full picture. Look for new probe paths worth adding to `TARPIT_PATTERNS`.

## Monthly-ish: news sweep

- [ ] **"What's new in Modoc"** — events, openings, closures, road news. Sources:
  - **Modoc County Record** — modocrecord.com (also their FB page)
  - **Bartell's Backroads** YouTube channel — new Modoc episodes get embedded on `/bartells-backroads`
  - **Surprise Valley Chamber** — surprisevalleychamber.com events page
  - **Google News** — `"Modoc County" OR "Alturas California" OR "Cedarville California"`
- [ ] **Seasonal/calendar content** — fishing season dates, hunting tags, Modoc District Fair, chili cookoff, farmers' market dates. Confirm nothing's drifted from the linked sources.

## When-changed: ad-hoc triggers

- [ ] **After adding/removing an image** — update `licenses.json`, confirm `alt_text`, re-run Lighthouse on the affected page.
- [ ] **After editing a merchant or restaurant page** — re-check the menu rules (`CLAUDE.md` § "Handling Restaurant & Cafe Menus"): no full transcription, no prices, "highlights" framing, caveat alert in place.
- [ ] **After a route or template structural change** — verify `static/sitemap.xml` still lists every public route; `base.html` nav still reaches every page; `licenses.json` still loads on `/technical-details`.

## Audit log

### 2026-05-05 — initial Lighthouse pass

Ran Lighthouse (desktop, navigation mode) on every public page. Final scores after fixes:

| Page | A11y | BP | SEO | Agentic |
|---|---|---|---|---|
| `/` | 100 | 100 | 100 | 100 |
| `/alturas` | 100 | 100 | 100 | 100 |
| `/cedarville` | 100 | 100 | 100 | 100 |
| `/places-to-visit` | 100 | 100 | 100 | 100 |
| `/things-to-do` | 100 | 100 | 100 | 100 |
| `/where-to-stay` | 100 | 100 | 100 | 100 |
| `/where-to-eat` | 100 | 100 | 100 | 100 |
| `/plan-your-visit` | 100 | 100 | 100 | 100 |
| `/webcams` | 100 | 100 | 100 | 100 |
| `/technical-details` | 100 | 100 | 100 | 100 |
| `/bartells-backroads` | 100 | **96** | 100 | 100 |

**Issues found and resolved**

- **Color contrast on links** (most pages) — Bootstrap's default link blue `#0d6efd` failed WCAG AA (4.5:1) on the `alert-info` cyan and `bg-light` gray. Overrode `--bs-link-color` and `.btn-outline-primary --bs-btn-color` to `#0a58ca` in `base.html`. Single change cleared ~14 deductions.
- **Heading order skips** (alturas, cedarville, places-to-visit, things-to-do, where-to-stay, plan-your-visit, bartells-backroads) — pages jumped `h2 → h4` for card titles and subsection headers, violating axe's `heading-order` rule. Fixed by promoting affected `<h4>` to `<h3 class="h4 ...">` (preserves visual size, fixes semantics).
- **Leaflet marker target-size** (webcams) — markers overlapped at the fitBounds zoom (Perez/Blue Mtn ~3 mi apart, Lakeview/Warner Summit ~7 mi). Added `Leaflet.markercluster` (well-tested plugin) so overlapping markers cluster at zoom-out and spiderfy on click; bumped PTZ icon to 40×40.
- **Non-descriptive link text** (things-to-do) — "Learn more" → "More about Lava Beds National Monument".
- **YouTube cookies** (bartells-backroads) — switched embeds to `youtube-nocookie.com`. Reduces but doesn't eliminate cookie warnings; full fix would require a click-to-load pattern (deferred — see Known Limitations).

**Content edits made during this pass** (responses to user feedback flagged in-flight):

- Removed `text-center` from every intro/lead paragraph wrapper (was applied across most major pages). Body text is never centered — see feedback memory.
- Tightened SEO-marketing prose in intros for `/webcams`, `/places-to-visit`, `/things-to-do`, `/plan-your-visit`, `/where-to-eat`, `/bartells-backroads`. Body copy serves visitors first; meta tags carry the SEO load.

**Known limitations**

- `/bartells-backroads` Best Practices score is 96/100. The 4-point deduction is `inspector-issues` for third-party cookies set by the YouTube nocookie iframes themselves — `youtube-nocookie.com` reduces tracking but doesn't eliminate it pre-interaction. Resolving fully requires a click-to-load pattern (e.g., `lite-youtube-embed`); deferred as a future enhancement, not a blocker.
- Merchant subpages (`/merchants/the-vault`, `/merchants/valley-farm-store`) and the dropdown city guides were not audited individually in this pass. They use the same base template + patterns, so should benefit from the link/button color fix automatically, but a full audit on next pass is warranted.
- `/where-to-stay` has three Airbnb/VRBO/Forest Service cards using `card h-100 text-center`. Single-line taglines on a 3-up card grid — borderline UI vs body text. Left as-is pending review.

## Tooling references

| Task | Tool / file |
|---|---|
| Visitor analysis | `analyze_visitors.py` (uses ip-api.com, caches to `.ip_cache.json`) |
| Tarpit patterns | `TARPIT_PATTERNS` in `app.py` |
| Image attribution | `licenses.json` (single source of truth, see CLAUDE.md) |
| Sitemap | `static/sitemap.xml` |
| SEO/meta | per-page Jinja blocks in templates that extend `base.html` |
| Outreach context | `~/.claude-personal/projects/-Volumes-DataT2-Projects-VisitModoc/memory/` |
