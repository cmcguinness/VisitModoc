# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Visit Modoc County is a tourism website showcasing Modoc County, California. Built with Flask and Bootstrap 5, it's a simple, content-focused site promoting the county's outdoor recreation, wildlife, and small-town charm.

## Running the Application

**Development:**
```bash
python app.py
```
Server runs on `http://localhost:8042` with debug mode enabled.

**Production:**
Uses `gunicorn` via Procfile for deployment on Railway.

## Architecture

### Flask Application (app.py)
- Simple route-based architecture with no database
- Each route renders a single static template
- **Special route:** `/technical-details` loads `licenses.json` and passes image credits to template for auto-generation

### Template System
- **Base template:** `templates/base.html` contains:
  - Complete navigation with consolidated dropdown menus
  - Custom CSS with color scheme (--modoc-primary: #2c5530, --modoc-secondary: #8b7355, --modoc-accent: #4a90a4)
  - Bootstrap 5 framework
  - SEO metadata (Open Graph, Twitter cards)
  - Schema.org structured data for LocalBusiness
  - Accessibility features (skip links, focus indicators, WCAG 2.1 AA compliant)
- **Content templates:** Extend base.html using Jinja2 blocks
- **Hero sections:** Most pages use background images with overlays via CSS `hero-section` class

### Image Management System
**CRITICAL:** `licenses.json` is the single source of truth for:
1. Image attribution (auto-rendered on `/technical-details` page)
2. Alt-text for accessibility

**Structure:**
```json
{
  "images": [
    {
      "filename": "image.jpg",
      "author": "Author Name",
      "license": "License Type",
      "alt_text": "Descriptive alt text",
      "source": "https://source-url.com",
      "additional_info": "Optional context"
    }
  ]
}
```

**When adding new images:**
1. Add entry to `licenses.json` with all metadata
2. Place image in `static/` directory
3. Use the exact `alt_text` from licenses.json in templates
4. For hero background images, add `role="img"` and `aria-label` with the alt_text

### Page Types

**Main sections:**
- `/` - Homepage with overview
- `/things-to-do` - Activities (fishing, hiking, wildlife viewing)
- `/places-to-visit` - Towns (Alturas, Cedarville) with detailed info
- `/where-to-stay` - Lodging overview
- `/where-to-eat` - Dining by location with nested lists by cuisine type
- `/plan-your-visit` - Visitor information

**City guides:**
- `/alturas` - Complete guide for county seat (hotels, restaurants, groceries, map)
- `/cedarville` - Complete guide for Surprise Valley town

**Special pages:**
- `/bartells-backroads` - ABC10 video series with YouTube embeds
- `/technical-details` - Auto-generated credits from licenses.json, technology info, contact

### Content Patterns

**Business listings:**
- Include name, rating (★), price where applicable
- Use Google Maps search links: `https://www.google.com/maps/search/?api=1&query=Business+Name+City+CA`
- Organize by category (American & Steakhouses, Mexican, etc.)
- Use nested/indented lists for better readability

**Maps:**
- Embedded Google Maps iframes must have `title` and `aria-label` attributes
- Example: `<iframe src="..." title="Google Map showing..." aria-label="Interactive map of..."></iframe>`

## Key Files

- `app.py` - Flask routes
- `licenses.json` - Image metadata (attribution + alt-text)
- `requirements.txt` - Flask==3.0.0, gunicorn==21.2.0
- `static/sitemap.xml` - SEO sitemap
- `static/robots.txt` - Search engine directives
- `Procfile` - Railway deployment config
- `runtime.txt` - Python version for Railway

## Content Guidelines

**Tone:** Positive, specific, descriptive. Avoid generic phrases like "limited options" or vague descriptions.

**Accessibility (WCAG 2.1 AA):**
- All images need descriptive alt-text (not generic)
- Hero background images need `role="img"` and `aria-label`
- Links need descriptive text (not "click here" or "learn more")
- Color contrast ratio: 8.5:1 (AAA level)
- Skip links present for keyboard navigation
- Reduced motion support via `prefers-reduced-motion` media query

**SEO:**
- Each page has unique meta description
- Canonical URLs defined
- Open Graph and Twitter card metadata
- Schema.org LocalBusiness structured data in base.html

## Handling Restaurant & Cafe Menus

Menus go stale fast — restaurants change items, prices, and seasons constantly. The site is a community guide, not a directory of authoritative menus, and we don't want visitors to drive somewhere expecting a dish that no longer exists.

**Rules for any menu content on the site:**

1. **Never transcribe a full menu.** Even if you have a complete menu image or PDF from the business, only include a small handful of items (typically 3 per category, never more than 4). The goal is to give visitors a flavor of the place, not a comprehensive listing.

2. **Frame menu items as highlights, not as the menu.** Use language like "A few favorites:", "A taste of [section]", "A couple of the regulars:", or "A few to look for:". Avoid headings like "Menu" or "Full Menu" that imply completeness.

3. **Always include a closer line** under each menu section indicating there's more — e.g., "Plus matcha, hot cocoa, organic lemonade, and a rotating cold case." or "The full menu rotates with the seasons and includes other salads, sandwiches, and specials."

4. **Never include prices.** Prices change constantly, are easy to get wrong, and create the impression that the listed price is what visitors will pay. Drop dollar figures, "$X / $Y" size pricing, "Always available $X" notes, etc. If a portion choice matters, describe it without numbers ("available as a whole or half sandwich").

5. **Always include a prominent caveat alert** above the menu sections (Bootstrap `alert-warning` works well) that says something like:
   > These are a small handful of highlights from [Business]'s menu — meant to give you a flavor of the place, not a complete listing. The actual menu is larger and changes with the seasons. **Please double-check current offerings with [Business] directly** — via [their Instagram/website] or in person — before counting on a specific item.

6. **Pick items that show character.** When choosing the small subset to feature, pick items that demonstrate what makes the place distinctive (signature dishes, locally sourced ingredients, unusual specialties) rather than generic items found everywhere.

**Why these rules exist:** A previous iteration of the Valley Farm Store page transcribed the entire menu from photos with prices, which (a) created a maintenance burden, (b) risked misleading visitors when items changed, (c) felt presumptuous on behalf of the business, and (d) made the page feel like an unsanctioned reproduction rather than a tourism guide. The rules above keep merchant pages welcoming and useful without creating false expectations.

**Note on broad-category descriptions:** Cards that describe what a place generally offers in broad terms ("espresso drinks, baked goods, Italian sodas") are fine and don't count as a menu. The rules above apply to specific named items with descriptions ("Sourdough BLT — uncured bacon and raw cheddar on toasted organic sourdough...").

## Security: Tarpit for Scanners

The site includes a tarpit system that slows down malicious vulnerability scanners. Instead of returning a quick 404, probes receive a slow-drip response that wastes attacker resources.

**How it works:**
- `@app.before_request` intercepts requests before routing
- Malicious patterns trigger a 30-second slow response of fake PHP garbage
- Legitimate routes are unaffected

**Two detection methods:**
1. **Pattern matching** (`TARPIT_PATTERNS`): Catches known malicious paths like `/wp-admin`, `.env`, `/phpmyadmin`, etc.
2. **Backdoor detection** (`BACKDOOR_PATTERN`): Catches random 4-12 character paths (e.g., `/q1gpDhK4`) that don't match valid routes - these are probes for pre-installed backdoors

**Log format:**
```
[TARPIT:pattern] 2025-11-27 03:01:07 UTC | CF-IP: 43.200.8.126 | X-Forwarded-For: 43.200.8.126 | URL: http://www.visit-modoc.com/.env
[TARPIT:backdoor] 2025-11-27 03:05:20 UTC | CF-IP: 43.200.8.126 | X-Forwarded-For: 43.200.8.126 | URL: http://www.visit-modoc.com/q1gpDhK4
```

**Adding new patterns:**
Add regex patterns to `TARPIT_PATTERNS` list in `app.py`. Patterns are case-insensitive.

**Gunicorn config:**
The Procfile uses `--workers 4 --timeout 45` to handle multiple concurrent tarpits without affecting legitimate users.

## Deployment

The site deploys to Railway automatically from the main branch. Railway environment sets `RAILWAY_ENVIRONMENT` variable which disables debug mode in production.

**Infrastructure:**
- **Hosting:** Railway
- **CDN/Security:** Cloudflare (handles DDoS, SSL, caching)
- **Workers:** 4 gunicorn workers with 45-second timeout
