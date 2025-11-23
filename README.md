# Visit Modoc County

A tourism website showcasing Modoc County, California - Northeast California's hidden gem.

Currently hosted at https://visit-modoc.com


## About

Simple, content-focused website promoting Modoc County's outdoor recreation, wildlife viewing, small-town charm, and visitor amenities. Features guides to Alturas and Cedarville, dining and lodging listings, and outdoor activities.

## Tech Stack

- **Backend:** Flask 3.0.0
- **Frontend:** Bootstrap 5, Jinja2 templates
- **Hosting:** Railway
- **Standards:** WCAG 2.1 AA accessible, SEO optimized

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

Visit `http://localhost:8042`

## Project Structure

- `app.py` - Flask routes
- `templates/` - Jinja2 HTML templates
- `static/` - Images, sitemap, robots.txt
- `licenses.json` - Image attribution and alt-text (single source of truth)

## Deployment

Automatically deploys to Railway from the main branch.

## License

Website content is public domain (except images from Wikimedia Commons, see `/technical-details` for attribution).
