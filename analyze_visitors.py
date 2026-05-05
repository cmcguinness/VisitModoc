#!/usr/bin/env python3
"""Pull visit-modoc.com Railway logs, parse [HTTP] lines, geolocate by IP.

Usage:
    python analyze_visitors.py                  # last 1000 lines
    python analyze_visitors.py --lines 5000
    python analyze_visitors.py --since 24h
    python analyze_visitors.py --include-bots   # don't filter out crawlers

Geo lookups are cached in .ip_cache.json so re-runs don't re-hit the API.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

import requests

CACHE_PATH = Path(__file__).parent / '.ip_cache.json'
GEO_API = 'http://ip-api.com/json/{ip}?fields=status,country,countryCode,regionName,city,isp,org,as,query'
GEO_RATE_LIMIT_PER_MIN = 40  # ip-api.com free tier is 45/min; leave headroom

# Pre-CF-IPCountry format: 6 pipe-separated fields
LINE_RE_NO_COUNTRY = re.compile(
    r'^\[HTTP\] (?P<ts>\S+ \S+ UTC) \| (?P<ip>\S+) \| '
    r'(?P<method>\S+) (?P<path>\S+) (?P<status>\d+) (?P<size>\S+) \| UA: (?P<ua>.*)$'
)
# Post-CF-IPCountry format: 7 pipe-separated fields
LINE_RE = re.compile(
    r'^\[HTTP\] (?P<ts>\S+ \S+ UTC) \| (?P<ip>\S+) \| (?P<country>\S+) \| '
    r'(?P<method>\S+) (?P<path>\S+) (?P<status>\d+) (?P<size>\S+) \| UA: (?P<ua>.*)$'
)

BOT_RE = re.compile(
    r'bot|crawler|spider|slurp|scrapy|wget|curl|python-requests|go-http|'
    r'facebookexternalhit|headlesschrome|phantomjs|monitor|pingdom|uptimerobot',
    re.IGNORECASE,
)


def parse_line(line):
    """Return dict for an [HTTP] line, or None."""
    m = LINE_RE.match(line) or LINE_RE_NO_COUNTRY.match(line)
    if not m:
        return None
    d = m.groupdict()
    d.setdefault('country', '-')
    return d


def fetch_logs(lines, since):
    cmd = ['railway', 'logs']
    if since:
        cmd += ['--since', since]
    cmd += ['--lines', str(lines)]
    out = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if out.returncode != 0:
        sys.stderr.write(f"railway logs failed:\n{out.stderr}\n")
        sys.exit(1)
    return out.stdout.splitlines()


def load_cache():
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(cache):
    CACHE_PATH.write_text(json.dumps(cache, indent=2, sort_keys=True))


def geo_lookup(ip, cache):
    """Geolocate one IP, with caching. Returns dict or None."""
    if ip in cache:
        return cache[ip]
    try:
        resp = requests.get(GEO_API.format(ip=ip), timeout=8)
        data = resp.json()
        if data.get('status') == 'success':
            cache[ip] = {
                'country': data.get('country', ''),
                'countryCode': data.get('countryCode', ''),
                'region': data.get('regionName', ''),
                'city': data.get('city', ''),
                'isp': data.get('isp', ''),
                'org': data.get('org', ''),
                'asn': data.get('as', ''),
            }
        else:
            cache[ip] = {'error': data.get('message', 'unknown')}
        return cache[ip]
    except Exception as e:
        return {'error': str(e)}


def truncate(s, n):
    if not s:
        return ''
    return s if len(s) <= n else s[: n - 1] + '…'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lines', type=int, default=1000, help='log lines to fetch (default 1000)')
    ap.add_argument('--since', help='time window, e.g. 24h, 7d (overrides default lookback)')
    ap.add_argument('--include-bots', action='store_true', help='do not filter crawler user-agents')
    ap.add_argument('--top', type=int, default=50, help='show top N IPs (default 50)')
    args = ap.parse_args()

    log_lines = fetch_logs(args.lines, args.since)
    requests_by_ip = defaultdict(list)
    for line in log_lines:
        rec = parse_line(line)
        if not rec:
            continue
        if not args.include_bots and BOT_RE.search(rec['ua']):
            continue
        if rec['ip'] in ('-', 'unknown'):
            continue
        requests_by_ip[rec['ip']].append(rec)

    if not requests_by_ip:
        print('No [HTTP] log lines matched. Has the new logging deployed yet?')
        return

    cache = load_cache()
    needed = [ip for ip in requests_by_ip if ip not in cache]
    sleep_per = 60.0 / GEO_RATE_LIMIT_PER_MIN
    for i, ip in enumerate(needed):
        geo_lookup(ip, cache)
        if i % 10 == 9:
            save_cache(cache)
        if i + 1 < len(needed):
            time.sleep(sleep_per)
    save_cache(cache)

    rows = []
    for ip, recs in requests_by_ip.items():
        geo = cache.get(ip, {})
        if 'error' in geo:
            location = f"(geo: {geo['error']})"
            org = ''
        else:
            parts = [p for p in (geo.get('city'), geo.get('region'), geo.get('countryCode')) if p]
            location = ', '.join(parts) if parts else '?'
            org = geo.get('org') or geo.get('isp') or ''
        first = recs[-1]['ts']  # logs come newest-last in railway output, but recs preserves input order
        last = recs[0]['ts']
        # Heuristic: pick the most-recent non-asset-ish path as a sample
        sample = recs[0]['path']
        rows.append({
            'ip': ip,
            'location': location,
            'org': org,
            'count': len(recs),
            'first': first,
            'last': last,
            'sample': sample,
            'cf_country': recs[0]['country'],
        })

    rows.sort(key=lambda r: r['count'], reverse=True)
    rows = rows[: args.top]

    # Header
    fmt = '{:<16} {:<3} {:<28} {:<28} {:>5} {:<19} {}'
    print(fmt.format('IP', 'CF', 'Location', 'Org/ISP', 'Hits', 'Last seen', 'Sample path'))
    print('-' * 130)
    for r in rows:
        print(fmt.format(
            r['ip'],
            r['cf_country'],
            truncate(r['location'], 27),
            truncate(r['org'], 27),
            r['count'],
            r['last'][:19],
            truncate(r['sample'], 40),
        ))

    # Summary
    print()
    total_reqs = sum(r['count'] for r in rows)
    total_ips = len(requests_by_ip)
    by_country = defaultdict(int)
    for ip, recs in requests_by_ip.items():
        cc = cache.get(ip, {}).get('countryCode') or recs[0]['country'] or '?'
        by_country[cc] += len(recs)
    top_countries = sorted(by_country.items(), key=lambda kv: kv[1], reverse=True)[:10]
    print(f"Showing top {len(rows)} of {total_ips} unique IPs ({total_reqs} requests in shown rows).")
    print('Top countries by request count: ' + ', '.join(f'{cc}:{n}' for cc, n in top_countries))


if __name__ == '__main__':
    main()
