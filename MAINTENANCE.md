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
- [ ] **Run through the Standing watch list** (next section) — three deferred questions that only
  become work when an external condition flips.

## Standing watch list

Open questions that resolve themselves over time. Check these on the monthly sweep; each one
becomes an action only when the condition flips. Kept in the repo rather than in Claude's memory
store, because there are two checkouts of this repo and the memory store is keyed to only one of
their paths (see "Two checkouts" at the bottom of this file). Anything written here travels with
the repo to either machine.

- [ ] **California Pines Lodge — does it have its own website yet?** Added to the site 2026-09-12
      (`/alturas`, `/where-to-stay`, `/where-to-eat`) from a newspaper ad. It has a Facebook page
      but no real site found, which under the merchant-page policy would make it *eligible* for a
      merchant page. **Deferred deliberately** — the call is to wait and see whether they build one
      themselves. If a real site appears, link it and drop the idea. If it's still Facebook-only
      after a few passes, revisit whether to create `/merchants/california-pines-lodge` (which
      would need the full `alert-warning` menu caveat, since it would have real menu sections).
      Contacts on file: lodge (530) 233-5842, dining reservations (530) 646-5330.
- [ ] **Valley Farm Store — has `valley-farmstore.com` gone live?** Still a password-walled Shopify
      placeholder as of 2026-08-01. The merchant page (`/merchants/valley-farm-store`) exists
      *because* they have no working site. When theirs goes live, link it and retire our page —
      same policy, opposite direction from California Pines.
- [ ] **Modoc Harvest — is `modocharvest.org` back?** Entirely offline since at least 2026-08-01;
      all links now point at their Facebook page. Their own print flyer still advertises the dead
      domain, so they may not know. If it returns, switch the farmers-market links back.

**The policy both lodge items turn on:** create a merchant page only when the business has no
website of its own. A merchant page is a stopgap for an unrepresented business, not a permanent
fixture — when the business can speak for itself, link them and step back.

## When-changed: ad-hoc triggers

- [ ] **After adding/removing an image** — update `licenses.json`, confirm `alt_text`, re-run Lighthouse on the affected page.
- [ ] **After editing a merchant or restaurant page** — re-check the menu rules (`CLAUDE.md` § "Handling Restaurant & Cafe Menus"): no full transcription, no prices, "highlights" framing, caveat alert in place.
- [ ] **After a route or template structural change** — verify `static/sitemap.xml` still lists every public route; `base.html` nav still reaches every page; `licenses.json` still loads on `/technical-details`.

## Audit log

### 2026-09-12 — newspaper-sourced additions + farmers market correction

Charles supplied two print sources: the Modoc County Record's "Lodging & Dining Guide" ad page and
a Modoc Certified Farmers Markets flyer. Both were checked against the site.

**One business was genuinely missing: California Pines Lodge**

Five of the six advertisers were already listed (Wagon Wheel, Antonio's, Country Hearth, Hotel
Niles, Sunrise Motel). **California Pines Lodge appeared nowhere on the site** — no spelling, no
phone, no address. Verified independently as open (Yelp listing updated Sept 2026, TripAdvisor
2026 reviews, active Facebook page) before adding. 750 Shasta View Dr, (530) 233-5842: a 28-room
lodge in the California Pines subdivision *southwest of town*, with its own restaurant, banquet
rooms, and lakes. Added to `/alturas` (Hotels + American & Steakhouses), `/where-to-stay`, and
`/where-to-eat`.

Deliberately **no star rating** — the site's convention is Google ratings and no reliable Google
figure was available. Worth knowing the sentiment is genuinely mixed: TripAdvisor sits at 3.0/5
across 16 reviews (ranked #2 of 2 specialty lodging in Alturas), while the *restaurant* draws
strong praise. Copy describes it factually rather than enthusing.

**Correction to earlier in this same session: I over-corrected the Cedarville market schedule**

Earlier today I changed Cedarville's market from "2nd and 4th Saturdays, June–October" to "every
other Saturday, July–September", using the Surprise Valley Chamber calendar's looser "every other
Saturday" phrasing. The Modoc Harvest flyer — the organizer's own material, and therefore
authoritative — shows the original **"2nd and 4th Saturdays" pattern was right**; only the months
were wrong. Restored. Lesson: the chamber calendar is a secondary source that paraphrases; prefer
Modoc Harvest's own flyer/page for market specifics.

The July–September month fix *was* correct and is confirmed by the flyer.

**Also corrected and added from the flyer**

- **Alturas market venue was wrong.** `/plan-your-visit` gave the Alturas market as "108 S. Main
  St." The flyer says **Veterans Memorial Park**. (108 S. Main appears to be a Modoc Harvest
  office address, not the market site.) Fixed.
- **Alturas runs the 1st and 3rd Saturdays**, Cedarville the 2nd and 4th — so there is a market
  most Saturdays of the season. The site previously gave no day pattern for Alturas at all. Both
  now stated on `/alturas`, `/cedarville`, and `/plan-your-visit`.
- **Payment programs added** (genuinely useful and previously absent): EBT, WIC, SunBucks,
  CalFresh, and Senior Farmers Market Nutrition Program are accepted, and Market Match matches
  EBT spending up to $15 per market.
- Note the flyer still prints `www.modocharvest.org`, which has been **offline since at least
  Aug 1** (see the 2026-08-01 entry). Site links continue to point at their Facebook page instead.

Re-audited `/alturas` and `/plan-your-visit` after the edits: both still 100 across all four
categories.

**Not done — offered, awaiting a decision**

The Lodging & Dining ad carries detail the site could absorb for businesses it already lists:
Sunrise Motel's AAA approval / 14 rooms / 3-bedroom Victorian guest house; Hotel Niles's Starbucks
coffee house; Antonio's "open daily for lunch and dinner"; Country Hearth's hours and Thursday
Mexican night. Held back because hours rot fast and some of it brushes against the menu rules in
`CLAUDE.md` (§ Handling Restaurant & Cafe Menus).

### 2026-09-12 — California Pines Lodge menu ad (menu rules applied)

Charles supplied the lodge's "Specials of the Week" newspaper ad. Handled under `CLAUDE.md`
§ Handling Restaurant & Cafe Menus: **nothing from the dish-and-price listings was transcribed.**

**Taken** (durable, structural, no prices):

- **A separate dining reservation line: (530) 646-5330**, call or text, reservations recommended.
  This is *not* the main lodge number (530-233-5842) already on the page. Both now appear, labelled.
- Hours confirmed exactly as written earlier from secondary sources: **Wed 4&ndash;8 PM, Thu&ndash;Sat 4&ndash;9 PM.**
- Salad and ice cream bar included with dinner; Early Bird pricing Wed&ndash;Sat 4&ndash;5 PM; slow-roasted
  prime rib as the Saturday night fixture. These are broad-offering facts, which the rules
  explicitly permit ("cards that describe what a place generally offers in broad terms ... don't
  count as a menu").

**Not taken:** every priced item (Calamari Steak, Shrimp Alfredo, Filet Mignon, Malibu Chicken,
French Dip, Teriyaki Beef Bowl, the pizza-and-wings add-on) and every dollar figure, including the
"+$2 after 5 p.m." note and the two prime rib portion prices. Verified absent by grep after editing.

**A judgment call worth recording:** the rules require a prominent `alert-warning` caveat *above
menu sections*. This is a single list entry, not a menu section, so a full alert block would be
disproportionate. Instead the entry closes with "Confirm current offerings and hours before you go."
If the lodge ever gets a merchant page with real menu sections, the alert becomes mandatory.

**Open question, not decided:** whether California Pines Lodge should get a merchant page. The
merchant-page policy is "only when the business has no website of their own" — they appear to have
a Facebook presence but no real site, so they may qualify. Left for Charles; not created unilaterally.

Re-audited `/alturas`: still 100 across all four categories.

### 2026-09-12 — quarterly Lighthouse pass (same session as the refresh above)

First full audit since 2026-05-05. Ran navigation-mode Lighthouse (desktop) against production
on all 13 auditable routes. **One CSS regression found, affecting 7 pages and 40 violations.**

| Page | A11y | BP | SEO | Agentic |
|---|---|---|---|---|
| `/` | 100 | 100 | 100 | 100 |
| `/things-to-do` | 100* | 100 | 100 | 100 |
| `/places-to-visit` | 100* | 100 | 100 | 100 |
| `/plan-your-visit` | 100* | 100 | 100 | 100 |
| `/where-to-eat` | 100* | 100 | 100 | 100 |
| `/where-to-stay` | 100* | 100 | 100 | 100 |
| `/alturas` | 100* | 100 | 100 | 100 |
| `/cedarville` | 100* | 100 | 100 | 100 |
| `/webcams` | 100 | 100 | 100 | 100 |
| `/technical-details` | 100 | 100 | 100 | 100 |
| `/bartells-backroads` | 100 | **96** | 100 | 100 |
| `/merchants/the-vault` | 100 | 100 | 100 | 100 |
| `/merchants/valley-farm-store` | 100 | 100 | 100 | 100 |

\* scored 96 before the contrast fix below; re-verified at 100 after.

**The regression: two card-header colors never met WCAG AA**

The site-wide card-header colour treatment (`202a7ee`, `47f39d6`, `dbdccc7` — all after the May
audit) introduced two band colours that fail 4.5:1 against white text:

| Class | Old | Ratio | New | Ratio |
|---|---|---|---|---|
| `theme-green` / `season-spring` / `svc-full` | `#4a8b2a` | 4.19 ✗ | `#427c25` | 5.07 ✓ |
| `theme-amber` / `season-summer` / `svc-some` | `#c2701f` | 3.73 ✗ | `#a35e1a` | 5.03 ✓ |
| `theme-rust` / `season-fall` / `svc-none` | `#92400e` | 7.09 ✓ | unchanged | 7.09 ✓ |
| `theme-blue` / `season-winter` | `#2c5d8a` | 6.91 ✓ | unchanged | 6.91 ✓ |

The trap worth remembering: these headers are **20px normal weight**, which does *not* qualify for
WCAG's relaxed 3.0:1 large-text threshold (that needs ≥24px normal or ≥18.66px bold). Both failing
colours would have passed at 3.0. Hue and saturation were held exactly; only lightness dropped.
Measured ratios are now recorded in a comment above the rules in `base.html` — **keep any new band
colour above 4.5:1**. Visual note: summer amber now sits closer to fall rust than before. Still
clearly distinguishable, but the gap is tighter; don't darken amber further without rechecking.

`CLAUDE.md` claimed "Color contrast ratio: 8.5:1 (AAA level)", which was not true of these headers.
Corrected to state the real AA bar and the tight case.

**Closed out from the May pass**

- **Merchant subpages are clean.** `/merchants/the-vault` and `/merchants/valley-farm-store` both
  score 100 across all four categories — the May "not audited individually" limitation is resolved.
- `/merchants/bidwell-canyon-farm` is a **301 redirect** to their own site, not a page (consistent
  with the merchant-page policy: no merchant page for a business that has its own site). Nothing
  to audit; don't add it to the audit list.
- `/where-to-stay`'s three `card h-100 text-center` cards: Lighthouse is clean on that page, so
  this stays a taste question, not an a11y one.

**Unchanged known limitation**

`/bartells-backroads` is still 96 Best Practices — `inspector-issues` for third-party cookies set
by the YouTube nocookie iframes before interaction. Same as May. A click-to-load pattern
(`lite-youtube-embed`) is the only real fix; still not worth it for 4 points.

**How to re-run:** the Chrome DevTools MCP `lighthouse_audit` action (desktop, navigation mode)
covers a11y/BP/SEO/agentic but **not** performance — that needs `performance_start_trace`.
Note it rejects `outputDirPath` outside the workspace root; omit it and use the temp reports.

**Verify deploys against a cache-busted URL, or you will misread the result**

Re-auditing production right after the deploy still scored 96, which looked like a failed fix. It
wasn't: `cf-cache-status: HIT`, `age: 326`, `cache-control: public, max-age=300, s-maxage=3600`.
Cloudflare's edge was serving HTML cached *before* the deploy, and Lighthouse saw the old colours.
The same URL with a query string (`?lhcheck=1`) is a different cache key, goes to the origin, and
scored 100. Railway itself had the new build live in **45 seconds**.

Consequence worth knowing: with `s-maxage=3600` and **no cache purge on deploy**, a content change
can take up to an hour to reach visitors even though the deploy succeeded immediately. Always append
a cache-buster when verifying, and don't trust a plain-URL check in the hour after a push. Purging
on deploy would need a Cloudflare token with purge rights — the token in 1Password is read-only
(see `reference_cloudflare_analytics.md`), so this is unresolved, not done.

### 2026-09-12 — September refresh

Ran the news sweep + `scripts/check_links.py`. **Link check was clean: 70 OK, 0 broken.** The rot
this month was all *content* rot — dated events that had already happened but still read as upcoming.

**Policy change: recurring events are now evergreen.** Hardcoded years were the recurring failure
mode (every September the site advertises an August fair that already happened). Annual Events and
the seasonal cards now say "held each August", "around the Fourth of July", "a Saturday each June"
and link the organizer for current dates. **Don't reintroduce hardcoded years for annual events** —
if a specific date is genuinely needed, add it as a separate "Next:" line that the monthly pass owns.

**Fixed**

- `plan-your-visit.html` — Modoc District Fair card and the Summer season bullet both still read
  "August 27–30, 2026" (the fair ran Aug 27–30 and was over). Both now evergreen.
- `plan-your-visit.html` — Fandango Days said "check … for the 2026 schedule" (July, past);
  Community Flea Market said "June 6, 2026" (past). Both now evergreen.
- `places-to-visit.html` — listed "Modoc County Fair". The correct name is Modoc **District** Fair.
- **Farmers market season was wrong.** `cedarville.html` claimed "2nd and 4th Saturdays,
  June–October". The Surprise Valley Chamber calendar shows every other Saturday, **July–September**,
  with the last 2026 market on Sept 26 — we were over-promising by a month on both ends. Corrected
  there, in `alturas.html` (had "July–October"), and in the plan-your-visit card.

**Added — the site had no fall events at all**

Every event we listed was a summer event, so an October visitor found nothing. Added four
*recurring* events (deliberately not one-offs, which would need a refresh every pass):

- **First Fridays — Cedarville** — first Friday evenings, 5–9 PM, Main Street. October adds a
  pumpkin-growing contest.
- **Mt Bidwell Celebration** — Fort Bidwell, each October, Saturday-morning parade.
- **Fall Festival — Alturas** — new for 2027, see below.
- **Movie Night in the Park** — Alturas, monthly through the summer from June.

**Alturas Balloon Fest is discontinued — permanently**

The Alturas Chamber ended its decades-old September Balloon Fest; pilots retired and travel/flight
costs made it too hard to attract replacements. A **Fall Festival takes the same September weekend
beginning in 2027**, and the Chamber is adding a monthly summer "Movie Night in the Park" that
closes out at the Fall Festival. The site never listed the Balloon Fest, so nothing had to be
removed — but **do not add it**, and watch for the first Fall Festival details in 2027.

**Known link-checker noise (do not re-investigate) — new entry**

- `surprisevalleychamber.com` returns **HTTP 403** to the checker *and* to `curl` with a browser UA,
  but renders perfectly in a real browser (verified via DevTools — title, nav, and 2026/2027 event
  calendar all load). It is UA/header-based bot blocking, not an outage. This link sits in
  `base.html`, so it appears on every page; don't panic when it shows up as a suspect.

**Tooling gotcha**

`scripts/check_links.py` needs `requests`, which is not installed for any Python on this machine and
the repo has no venv — `direnv exec . python scripts/check_links.py` fails twice over (`python` is
not on PATH; `python3` has no `requests`). Run it as:

```
uv run --with requests python scripts/check_links.py
```

Same for the app when testing locally: `uv run --with flask --with requests python app.py`.

### 2026-08-01 — monthly refresh (manual; cloud routine's digest never arrived)

The "Visit Modoc — monthly refresh" cloud routine fired on schedule (Jul 1 and Aug 1) but
delivered nothing: the Gmail connector has no send tool, only draft tools, so each digest sits
as an unsent draft titled "Visit Modoc — monthly refresh (<Month Year>)". Ran the pass by hand
instead.

**The routine is now retired** (disabled, not deleted — `RemoteTrigger` has no delete action).
The monthly pass is session-driven from here: say "time for the monthly update" and the work
happens in a session, which can fix, commit, and push — none of which the read-only routine
could do. `scripts/check_links.py` is still the first step of that pass.

**Fixed**

- `modocharvest.org` is **entirely offline** — the root serves the host's "Contact Hosting
  Technical Support" page and every sub-path 404s. Replaced the three dead
  `modocharvest.org/modoc-harvest-certified-farmers-markets/` links (`alturas.html`,
  `cedarville.html`, `plan-your-visit.html`) with the
  [Modoc Certified Farmers Markets Facebook page](https://www.facebook.com/ModocCFM/), which is
  their live presence. The `mailto:FarmersMarket@ModocHarvest.org` contacts were left in place.
- Added a "Local Food Hub" card to `/alturas` (Groceries & Supplies) for the Modoc Harvest Food
  Hub at 112 E 2nd St, linking their [Open Food Network shop](https://openfoodnetwork.net/modoc-harvest-food-hub/shop).
  With modocharvest.org down this is their only verifiable live storefront — it had an active
  order cycle (pickup 8/6–8/7) when checked. Their own OFN profile still links the dead
  `modocharvest.org/food-hub` URL.
- The Vault (`merchants/the-vault.html`) hours corrected to Mon + Fri–Sun 6 AM–3 PM, closed
  Tue–Thu. The page previously showed Fri/Sat until 6 PM and omitted Monday entirely. Two
  independent listings agree on the new hours; **confirm against @cedarvillevault on Instagram**.

**Weather widget fixed (two bugs, found while chasing a "site says 59°, NWS says 79°" report)**

- `get_weather()` called the NWS *forecast* endpoint and rendered `periods[0].temperature` under
  the label "Currently". That value is the period's HIGH (daytime) or LOW (overnight), never an
  observation — so the number was wrong nearly all the time, in either direction depending on the
  hour. Current conditions now come from `stations/KAAT/observations/latest` (Alturas Municipal
  Airport), converted from Celsius; the forecast period is shown separately and labelled.
- The hardcoded grid `REV/33,117` wasn't Alturas — that cell sits at 39.705,-120.189 near Portola,
  ~150 miles south, in the Reno office. Corrected to `MFR/176,20` (Medford), which is what
  `api.weather.gov/points/41.4871,-120.5425` returns. **Don't hand-edit the grid**; look it up.
- Degraded paths tested: station silent → falls back to the forecast high/low with an honest label
  ("Alturas — Tonight low: 47°F"); both endpoints down → widget hidden, pages still 200.

**Verified, no change needed**

- Modoc District Fair: Aug 27–30 2026, "America 250" theme — already correct on the site.
- Valley Farm Store: still a password-walled Shopify placeholder, merchant page stays. Its
  published hours match the merchant page exactly.
- ~44 featured businesses: no confirmed closures. The Yelp "LAZY B GRILL - CLOSED" entry is a
  stale duplicate of the still-open Lazy B at the same address; "Cedarville Cafe & Saloon -
  CLOSED" is the predecessor at 415 Main St, now Woody's (open, and the site features Woody's).

**Known link-checker noise (do not re-investigate)**

- `bidwellcanyonfarm.com` reports `SSL error: SSLError` — a false positive. Their cert chains to
  Let's Encrypt's new Generation Y root (ISRG Root YR / intermediate YR2), which the `certifi`
  bundle used by `requests` doesn't yet carry. Browsers and macOS `curl` verify it fine.
- `facebook.com` returns HTTP 400 to the checker's UA; github.com 403, linkedin.com 999,
  vrbo.com 429 — all bot-blocks, all reachable in a browser.

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
| Outreach context | `~/.claude-personal/projects/-Volumes-DataT2-Projects-VisitModoc/memory/` — see the warning below |

## Two checkouts, and a memory store keyed to the wrong one

**Topology** (verified 2026-09-12):

- `/Volumes/DataT1` — a local APFS disk on the **MacBook Air**. The Air's own checkout.
- `/Volumes/DataT2` — an **SMB mount of the Mac mini's drive**, mounted on the Air. So
  `/Volumes/DataT2/Projects/VisitModoc` is the *mini's* checkout, reachable from the Air over the
  network. It is a genuinely separate working copy, not a second path to the same files.

**Keep them in sync through git, not the mount.** As of 2026-09-12 the mini's checkout sat at
`8f4a34c` — five commits behind the Air. Editing the same repo from two checkouts without pulling
is the ordinary way to lose work; `git pull` on whichever machine you sit down at.

**The memory-store consequence.** Claude's per-project memory directory is keyed to the project's
filesystem *path*, and both key directories live under the Air's `$HOME`:

- `~/.claude-personal/projects/-Volumes-DataT2-Projects-VisitModoc/memory/` — **10 memory files**
  (merchant page policy, Modoc Record outreach, the never-center-body-text rule, the Cloudflare
  analytics pointer, and more). Written by Air sessions that worked on the mini's copy over SMB.
- `~/.claude-personal/projects/-Volumes-DataT1-Projects-VisitModoc/memory/` — **empty**. This is
  what a session started from the Air's local checkout is handed.

So a session working here gets an empty memory store and sees none of that context unless someone
goes looking. Consolidating is a plain `mv` into the DataT1-keyed directory, but it hasn't been
done — it's Charles's memory store, not something to reorganise unasked. Until it is, **durable
project knowledge belongs in this file**, which is why the watch list above lives here.
