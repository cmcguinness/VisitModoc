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

## Deployment

The site deploys to Railway automatically from the main branch. Railway environment sets `RAILWAY_ENVIRONMENT` variable which disables debug mode in production.
