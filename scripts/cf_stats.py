#!/usr/bin/env python3
"""Cloudflare traffic + security summary for the Visit Modoc site.

Queries Cloudflare's GraphQL Analytics API for the zone fronting
visit-modoc.com and prints a per-day rollup (requests, page views, unique
visitors, cache ratio, threats) plus aggregate top countries and response
codes over the window. Read-only.

Auth: reads a Cloudflare API token from the CF_API_TOKEN environment
variable. The token needs zone-scoped **Analytics:Read** and **Zone:Read**
(the latter lets the script discover the zone id from the domain name, so
you don't have to hardcode it).

On the laptop, fetch the token from 1Password at run time — never store it
on disk:

    CF_API_TOKEN=$(op read "op://credentials/cloudflare-visitmodoc-token/credential") \
        python scripts/cf_stats.py

Options:
    --days N      window size in days (default 7; Cloudflare free-plan
                  retention for the 1d dataset is limited, ~30 days)
    --domain D    zone domain (default visit-modoc.com)
    --json        emit raw JSON instead of the formatted table
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import sys

import requests

API_BASE = "https://api.cloudflare.com/client/v4"
GRAPHQL = f"{API_BASE}/graphql"
TIMEOUT = 30

GRAPHQL_QUERY = """
query ($zoneTag: String!, $since: Date!, $until: Date!) {
  viewer {
    zones(filter: {zoneTag: $zoneTag}) {
      httpRequests1dGroups(
        limit: 31,
        filter: {date_geq: $since, date_leq: $until},
        orderBy: [date_ASC]
      ) {
        dimensions { date }
        uniq { uniques }
        sum {
          requests
          pageViews
          cachedRequests
          bytes
          threats
          countryMap { clientCountryName requests }
          responseStatusMap { edgeResponseStatus requests }
        }
      }
    }
  }
}
"""


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def discover_zone(token: str, domain: str) -> str:
    """Resolve a domain name to its Cloudflare zone id."""
    resp = requests.get(
        f"{API_BASE}/zones",
        headers=auth_headers(token),
        params={"name": domain},
        timeout=TIMEOUT,
    )
    try:
        data = resp.json()
    except ValueError:
        die(f"zone lookup returned non-JSON (HTTP {resp.status_code})")
    if not data.get("success"):
        errs = "; ".join(e.get("message", "?") for e in data.get("errors", []))
        die(f"zone lookup failed: {errs or resp.status_code} "
            f"(token needs Zone:Read for {domain})")
    results = data.get("result") or []
    if not results:
        die(f"no Cloudflare zone found for '{domain}' (is it on this account?)")
    return results[0]["id"]


def fetch_analytics(token: str, zone_tag: str, days: int) -> list[dict]:
    until = datetime.date.today()
    since = until - datetime.timedelta(days=days - 1)
    payload = {
        "query": GRAPHQL_QUERY,
        "variables": {
            "zoneTag": zone_tag,
            "since": since.isoformat(),
            "until": until.isoformat(),
        },
    }
    resp = requests.post(GRAPHQL, headers=auth_headers(token),
                         json=payload, timeout=TIMEOUT)
    try:
        data = resp.json()
    except ValueError:
        die(f"analytics query returned non-JSON (HTTP {resp.status_code})")
    if data.get("errors"):
        msg = "; ".join(e.get("message", "?") for e in data["errors"])
        die(f"GraphQL error: {msg} (token needs Analytics:Read on this zone)")
    zones = (data.get("data", {}) or {}).get("viewer", {}).get("zones", [])
    if not zones:
        die("no zone data returned (check token zone scope)")
    return zones[0].get("httpRequests1dGroups", [])


def human_bytes(n: int) -> str:
    f = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if f < 1024 or unit == "TB":
            return f"{f:.1f}{unit}"
        f /= 1024
    return f"{f:.1f}TB"


def render(groups: list[dict], domain: str, days: int) -> None:
    if not groups:
        print(f"No analytics rows for {domain} in the last {days} days "
              "(zone may be new, or outside free-plan retention).")
        return

    tot_req = tot_pv = tot_uniq = tot_cached = tot_bytes = tot_threats = 0
    countries: dict[str, int] = {}
    statuses: dict[int, int] = {}

    print(f"\nCloudflare traffic — {domain} — last {days} days\n")
    print(f"  {'date':<12}{'requests':>10}{'pageviews':>11}"
          f"{'uniques':>9}{'cached':>8}{'threats':>9}")
    print("  " + "-" * 57)
    for g in groups:
        date = g["dimensions"]["date"]
        s = g["sum"]
        req, pv = s["requests"], s["pageViews"]
        uniq = g["uniq"]["uniques"]
        cached, threats = s["cachedRequests"], s["threats"]
        cache_pct = (cached / req * 100) if req else 0
        print(f"  {date:<12}{req:>10,}{pv:>11,}{uniq:>9,}"
              f"{cache_pct:>7.0f}%{threats:>9,}")
        tot_req += req
        tot_pv += pv
        tot_uniq += uniq
        tot_cached += cached
        tot_bytes += s["bytes"]
        tot_threats += threats
        for c in s.get("countryMap", []):
            countries[c["clientCountryName"]] = (
                countries.get(c["clientCountryName"], 0) + c["requests"])
        for st in s.get("responseStatusMap", []):
            statuses[st["edgeResponseStatus"]] = (
                statuses.get(st["edgeResponseStatus"], 0) + st["requests"])

    print("  " + "-" * 57)
    cache_pct = (tot_cached / tot_req * 100) if tot_req else 0
    print(f"  {'TOTAL':<12}{tot_req:>10,}{tot_pv:>11,}{tot_uniq:>9,}"
          f"{cache_pct:>7.0f}%{tot_threats:>9,}")
    print(f"\n  Bandwidth served: {human_bytes(tot_bytes)}")

    top_countries = sorted(countries.items(), key=lambda x: -x[1])[:6]
    print("\n  Top countries:  " + ", ".join(
        f"{c} ({n:,})" for c, n in top_countries))
    top_statuses = sorted(statuses.items(), key=lambda x: -x[1])[:6]
    print("  Response codes: " + ", ".join(
        f"{code}: {n:,}" for code, n in top_statuses))
    print()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--domain", default="visit-modoc.com")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    token = os.environ.get("CF_API_TOKEN")
    if not token:
        die("CF_API_TOKEN not set. Fetch it from 1Password, e.g.\n"
            '  CF_API_TOKEN=$(op read "op://credentials/'
            'cloudflare-visitmodoc-token/credential") python scripts/cf_stats.py')

    zone_tag = discover_zone(token, args.domain)
    groups = fetch_analytics(token, zone_tag, args.days)

    if args.json:
        print(json.dumps({"zone": zone_tag, "domain": args.domain,
                          "days": args.days, "groups": groups}, indent=2))
    else:
        render(groups, args.domain, args.days)
    return 0


if __name__ == "__main__":
    sys.exit(main())
