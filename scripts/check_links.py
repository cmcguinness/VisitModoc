#!/usr/bin/env python3
"""Monthly external-link rot checker for the Visit Modoc site.

Walks the Jinja templates, extracts every *external* href/src, and checks each
one over HTTP. The point is a low-noise monthly signal: distinguish links that
are genuinely gone from links that merely refuse robots.

Usage:
    python scripts/check_links.py            # human-readable summary
    python scripts/check_links.py --json     # machine-readable JSON to stdout
    python scripts/check_links.py --delay 1  # seconds between requests (default 0.5)

Exit code is non-zero when at least one BROKEN link is found, so a scheduler
can branch on "something is actually rotten" vs "all clear / only suspects".

No third-party dependencies beyond `requests` (already in requirements.txt);
HTML parsing uses the stdlib so this never bloats the production deploy.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

import requests

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

# Browser-ish UA: a bare python-requests UA gets blocked far more often, which
# would inflate the SUSPECT pile with false alarms.
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 VisitModoc-LinkCheck/1.0"
)

# Hosts whose links are infrastructure/boilerplate, not content we curate. They
# don't rot in a way that matters, and checking them is pure noise.
SKIP_HOSTS = {
    "www.w3.org",            # WAI-ARIA / xmlns namespaces
    "schema.org",           # structured-data vocabulary
    "www.schema.org",
    "visit-modoc.com",      # our own canonical / nav links
    "www.visit-modoc.com",
    "www.googletagmanager.com",
    "cdn.jsdelivr.net",     # pinned CDN assets (bootstrap)
    "unpkg.com",            # pinned CDN assets (leaflet)
    "mirrors.creativecommons.org",
    "tile.openstreetmap.org",
}

# Maps "search" links always resolve 200 regardless of whether the business
# still exists, so an HTTP check tells us nothing. We surface them separately
# as "unverifiable" rather than pretending they passed.
UNVERIFIABLE_SUBSTRINGS = (
    "google.com/maps/search",
    "maps.google.com/maps?q=",
    "google.com/maps/embed",
)

REQUEST_TIMEOUT = 15  # seconds


class LinkExtractor(HTMLParser):
    """Collect href/src URL values from an HTML/Jinja file."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.urls.append(value)


def is_external(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")


def host_of(url: str) -> str:
    return (urlparse(url).hostname or "").lower()


def collect_links() -> dict[str, set[str]]:
    """Return {url: {template names it appears in}} for external, checkable URLs."""
    found: dict[str, set[str]] = defaultdict(set)
    for path in sorted(TEMPLATES_DIR.rglob("*.html")):
        rel = path.relative_to(TEMPLATES_DIR).as_posix()
        parser = LinkExtractor()
        try:
            parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        except Exception as exc:  # noqa: BLE001 - a parse hiccup shouldn't abort the run
            print(f"  ! could not parse {rel}: {exc}", file=sys.stderr)
            continue
        for url in parser.urls:
            if not is_external(url):
                continue
            if host_of(url) in SKIP_HOSTS:
                continue
            found[url].add(rel)
    return found


def classify(url: str) -> tuple[str, str]:
    """Return (status, detail). status in {OK, BROKEN, SUSPECT, UNVERIFIABLE}."""
    if any(s in url for s in UNVERIFIABLE_SUBSTRINGS):
        return "UNVERIFIABLE", "maps/search link — always 200, can't confirm business"

    headers = {"User-Agent": USER_AGENT}
    try:
        # HEAD is cheapest; many servers reject it, so fall back to a GET.
        resp = requests.head(
            url, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=True
        )
        if resp.status_code in (403, 405, 501) or resp.status_code >= 400:
            resp = requests.get(
                url,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
                allow_redirects=True,
                stream=True,
            )
            resp.close()
    except requests.exceptions.SSLError as exc:
        return "SUSPECT", f"SSL error: {exc.__class__.__name__}"
    except requests.exceptions.ConnectionError as exc:
        # DNS/name resolution failures are the clearest sign of true rot.
        msg = str(exc).lower()
        if "name or service not known" in msg or "nodename nor servname" in msg \
                or "failed to resolve" in msg or "getaddrinfo failed" in msg:
            return "BROKEN", "DNS does not resolve (domain gone)"
        return "SUSPECT", f"connection error: {exc.__class__.__name__}"
    except requests.exceptions.Timeout:
        return "SUSPECT", "timeout"
    except requests.exceptions.RequestException as exc:
        return "SUSPECT", f"request error: {exc.__class__.__name__}"

    code = resp.status_code
    if code in (404, 410):
        return "BROKEN", f"HTTP {code}"
    if code in (401, 403, 405, 429) or code >= 500:
        return "SUSPECT", f"HTTP {code} (likely bot-block or transient)"
    if code >= 400:
        return "SUSPECT", f"HTTP {code}"
    return "OK", f"HTTP {code}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="emit JSON to stdout")
    ap.add_argument("--delay", type=float, default=0.5,
                    help="seconds to wait between requests (default 0.5)")
    args = ap.parse_args()

    links = collect_links()
    if not args.json:
        print(f"Checking {len(links)} external links from {TEMPLATES_DIR}...\n")

    results: list[dict] = []
    for i, (url, templates) in enumerate(sorted(links.items())):
        status, detail = classify(url)
        results.append({
            "url": url,
            "status": status,
            "detail": detail,
            "templates": sorted(templates),
        })
        if not args.json:
            mark = {"OK": "  ok ", "BROKEN": "BROKEN", "SUSPECT": "  ?? ",
                    "UNVERIFIABLE": "  -- "}[status]
            print(f"[{mark}] {url}  ({detail})")
        if status != "UNVERIFIABLE" and i < len(links) - 1:
            time.sleep(args.delay)

    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        buckets[r["status"]].append(r)

    if args.json:
        print(json.dumps({
            "checked": len(results),
            "summary": {k: len(v) for k, v in buckets.items()},
            "results": results,
        }, indent=2))
    else:
        print("\n" + "=" * 60)
        print(f"  OK: {len(buckets['OK'])}   BROKEN: {len(buckets['BROKEN'])}   "
              f"SUSPECT: {len(buckets['SUSPECT'])}   "
              f"UNVERIFIABLE: {len(buckets['UNVERIFIABLE'])}")
        print("=" * 60)
        for status in ("BROKEN", "SUSPECT"):
            if buckets[status]:
                print(f"\n{status}:")
                for r in buckets[status]:
                    print(f"  {r['url']}")
                    print(f"      {r['detail']}  —  in: {', '.join(r['templates'])}")

    return 1 if buckets["BROKEN"] else 0


if __name__ == "__main__":
    sys.exit(main())
