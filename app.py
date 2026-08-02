import os
import json
import time
import re
import threading
import requests
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from flask import Flask, render_template, send_from_directory, Response, request, redirect

# Modoc County observes Pacific time; NWS timestamps arrive in UTC.
PACIFIC = ZoneInfo('America/Los_Angeles')

app = Flask(__name__)

# Production configuration
if os.environ.get('RAILWAY_ENVIRONMENT'):
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = False
else:
    app.config['DEBUG'] = True


# Tarpit for malicious scanners
# Patterns that indicate automated vulnerability scanning
TARPIT_PATTERNS = [
    # WordPress
    r'/wp-',
    r'/wordpress',
    r'/wp\.php',
    r'/xmlrpc\.php',
    r'/wlwmanifest\.xml',
    # PHP admin tools
    r'/phpmyadmin',
    r'/pma',
    r'/myadmin',
    r'/mysql',
    r'/adminer',
    # Other CMS
    r'/joomla',
    r'/drupal',
    r'/administrator',
    r'/typo3',
    r'/magento',
    # Shells and exploits
    r'/shell',
    r'/eval-stdin',
    r'/backdoor',
    r'/c99',
    r'/r57',
    r'/phpinfo',
    # Config files
    r'\.env',
    r'\.git',
    r'\.svn',
    r'\.bak',
    r'\.old',
    r'\.swp',
    r'\.zip$',
    r'\.sql$',
    r'\.tar',
    r'\.log$',
    r'\.log\.',
    r'/config\.',
    r'/backup',
    r'/dump',
    # Common probes
    r'/admin\.php',
    r'/login\.php',
    r'/test\.php',
    r'/info\.php',
    r'/debug',
    r'/\.well-known/security\.txt',  # We don't have one, so it's a probe
    r'/cgi-bin',
    r'/scripts',
    r'/aws',
    r'/\.aws',
    r'/credentials',
]

TARPIT_REGEX = re.compile('|'.join(TARPIT_PATTERNS), re.IGNORECASE)

# Pattern for random backdoor probes (only checked on non-matching routes)
BACKDOOR_PATTERN = re.compile(r'^/[a-zA-Z0-9]{4,12}$')

# Cap how many tarpits can run at once. With gthread workers, each tarpit ties
# up one thread for ~30s; without a cap, a flood of probes can starve real
# requests. Excess probes get redirected somewhere wasteful instead.
TARPIT_MAX_CONCURRENT = 4
_tarpit_sem = threading.Semaphore(TARPIT_MAX_CONCURRENT)
RICK_ROLL_URL = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'


def is_valid_route(path):
    """Check if path matches any registered route."""
    adapter = app.url_map.bind('')
    try:
        adapter.match(path)
        return True
    except Exception:
        return False


def tarpit_response():
    """Generate a slow response that wastes scanner resources.

    Releases one tarpit slot when iteration ends (whether normally or because
    the client disconnected and Flask called close() on the generator).
    Caller must have acquired _tarpit_sem before invoking this.
    """
    garbage_lines = [
        b'<?php /* WordPress Security Check */ ?>\n',
        b'<?php require_once("wp-config.php"); ?>\n',
        b'<?php // Validating credentials... ?>\n',
        b'<?php $db = mysqli_connect("localhost", "root", ""); ?>\n',
        b'<?php // Loading admin panel... ?>\n',
        b'<?php session_start(); /* auth pending */ ?>\n',
    ]
    try:
        for _ in range(50):  # ~30 seconds total
            for line in garbage_lines:
                yield line
                time.sleep(0.1)
    finally:
        _tarpit_sem.release()


def log_and_tarpit(reason):
    """Log the probe attempt and tarpit it, or redirect if at capacity."""
    cf_ip = request.headers.get('CF-Connecting-IP', 'unknown')
    x_forwarded = request.headers.get('X-Forwarded-For', 'unknown')
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    if not _tarpit_sem.acquire(blocking=False):
        # Already at max concurrent tarpits; send the overflow somewhere fun.
        print(f"[TARPIT:{reason}:rickroll] {timestamp} | CF-IP: {cf_ip} | X-Forwarded-For: {x_forwarded} | URL: {request.url}", flush=True)
        resp = redirect(RICK_ROLL_URL, code=302)
        resp.headers['X-Tarpit'] = 'rickroll'
        return resp

    print(f"[TARPIT:{reason}] {timestamp} | CF-IP: {cf_ip} | X-Forwarded-For: {x_forwarded} | URL: {request.url}", flush=True)
    return Response(
        tarpit_response(),
        status=200,
        mimetype='text/plain',
        headers={'X-Tarpit': 'enjoy-the-wait'}
    )


# Weather data cache
_weather_cache = {'data': None, 'timestamp': 0}
WEATHER_CACHE_DURATION = 900  # 15 minutes

# NWS endpoints for Alturas. The forecast grid is the one api.weather.gov
# returns for 41.4871,-120.5425 (Medford office) — do not hand-edit it; look it
# up via https://api.weather.gov/points/41.4871,-120.5425 if it ever changes.
NWS_FORECAST_URL = 'https://api.weather.gov/gridpoints/MFR/176,20/forecast'
# KAAT = Alturas Municipal Airport, the reporting station in town. The forecast
# endpoint's periods carry a period HIGH or LOW, never a current reading, so the
# observed temperature has to come from a station.
NWS_OBSERVATION_URL = 'https://api.weather.gov/stations/KAAT/observations/latest'
NWS_HEADERS = {'User-Agent': 'VisitModoc/1.0 (visit-modoc.com)'}


def _c_to_f(celsius):
    """NWS observations report metric; the site displays Fahrenheit."""
    return round(celsius * 9 / 5 + 32)


def _fetch_observation():
    """Latest observed conditions at KAAT, or None if unavailable.

    Any field in an observation can be null when a sensor drops out, so the
    caller must treat a missing temperature as "no observation" rather than
    rendering a blank number.
    """
    response = requests.get(NWS_OBSERVATION_URL, headers=NWS_HEADERS, timeout=10)
    response.raise_for_status()
    props = response.json().get('properties', {})

    temp_c = (props.get('temperature') or {}).get('value')
    if temp_c is None:
        return None

    wind_kph = (props.get('windSpeed') or {}).get('value')
    observed = {
        'temperature': _c_to_f(temp_c),
        'description': props.get('textDescription', ''),
        'wind': f'{round(wind_kph * 0.621371)} mph' if wind_kph is not None else '',
    }

    timestamp = props.get('timestamp')
    if timestamp:
        try:
            when = datetime.fromisoformat(timestamp).astimezone(PACIFIC)
            observed['observed_at'] = when.strftime('%-I:%M %p').lower()
        except (ValueError, TypeError):
            pass

    return observed


def _fetch_forecast():
    """The next NWS forecast period (e.g. 'Tonight'), or None if unavailable."""
    response = requests.get(NWS_FORECAST_URL, headers=NWS_HEADERS, timeout=10)
    response.raise_for_status()
    periods = response.json().get('properties', {}).get('periods', [])
    if not periods:
        return None

    period = periods[0]
    return {
        'period_name': period.get('name', 'Next'),
        # A daytime period's temperature is that day's high; a nighttime
        # period's is the overnight low. Label it so neither reads as "now".
        'period_label': 'High' if period.get('isDaytime') else 'Low',
        'period_temperature': period.get('temperature'),
        'period_description': period.get('shortForecast', ''),
        'detailed': period.get('detailedForecast', ''),
        'icon': period.get('icon', ''),
    }


def get_weather():
    """Current conditions and next forecast period for Alturas, cached.

    `temperature` is an actual observation whenever KAAT is reporting; if the
    station is silent we fall back to the forecast period's high/low and set
    `is_observation` False so the templates stop saying "currently".
    """
    now = time.time()

    if _weather_cache['data'] and (now - _weather_cache['timestamp']) < WEATHER_CACHE_DURATION:
        return _weather_cache['data']

    observed = None
    forecast = None

    try:
        observed = _fetch_observation()
    except Exception as e:
        print(f"[WEATHER] Error fetching observation: {e}", flush=True)

    try:
        forecast = _fetch_forecast()
    except Exception as e:
        print(f"[WEATHER] Error fetching forecast: {e}", flush=True)

    if not observed and not forecast:
        return {'success': False}

    weather_data = {'success': True, 'unit': 'F', 'is_observation': bool(observed)}
    if forecast:
        weather_data.update(forecast)

    if observed:
        weather_data.update(observed)
    else:
        # No station reading — show the period's high/low, honestly labelled.
        weather_data['temperature'] = forecast.get('period_temperature')
        weather_data['description'] = forecast.get('period_description', '')

    _weather_cache['data'] = weather_data
    _weather_cache['timestamp'] = now
    return weather_data


@app.before_request
def check_for_probes():
    """Intercept malicious probes and tarpit them."""
    path = request.path

    # Check explicit malicious patterns first
    if TARPIT_REGEX.search(path):
        return log_and_tarpit('pattern')

    # For unknown routes, check if it looks like a backdoor probe
    if not is_valid_route(path) and BACKDOOR_PATTERN.match(path):
        return log_and_tarpit('backdoor')


# Pages whose rendered HTML embeds the (hourly) weather widget. They get a
# shorter edge TTL than the otherwise-static content pages.
WEATHER_PAGES = {'/', '/plan-your-visit'}


def _set_cache_control(response, max_age, s_maxage=None):
    """Replace Cache-Control with `public, max-age=<n>`, overriding any default
    `no-cache` that Flask's send_from_directory adds to static responses.

    `s_maxage` (shared/edge TTL) lets Cloudflare cache longer than browsers:
    browsers honor max-age and re-validate sooner (so a content fix shows up
    quickly), while the edge serves from cache for s-maxage and offloads the
    origin. Cloudflare prefers s-maxage over max-age for its edge TTL."""
    cc = f'public, max-age={max_age}'
    if s_maxage is not None:
        cc += f', s-maxage={s_maxage}'
    response.headers['Cache-Control'] = cc


@app.after_request
def add_cache_headers(response):
    """Set Cache-Control so Cloudflare can serve assets from edge cache."""
    # Never cache tarpit responses or rick-roll redirects.
    if response.headers.get('X-Tarpit') or response.status_code in (302, 301):
        response.headers['Cache-Control'] = 'no-store'
        return response

    path = request.path

    # Sitemap and robots: short cache so search engines see updates promptly.
    if path in ('/sitemap.xml', '/robots.txt'):
        _set_cache_control(response, 3600)  # 1 hour
        return response

    # Static assets (images, CSS, manifests, favicons): long cache.
    # The site has no asset versioning, so 7 days is a balance between
    # cacheability and being able to update an image without renaming.
    if path.startswith('/static/') or path in ('/favicon.ico',):
        _set_cache_control(response, 604800)  # 7 days
        return response

    # HTML pages. Cloudflare won't cache HTML without a Cache Rule, but these
    # headers are correct for one set to "respect origin Cache-Control".
    # Weather pages get a short edge TTL; the rest are effectively static
    # (they only change on deploy) so the edge can hold them much longer.
    if response.mimetype == 'text/html' and response.status_code == 200:
        if request.path in WEATHER_PAGES:
            _set_cache_control(response, 120, s_maxage=600)    # edge 10 min
        else:
            _set_cache_control(response, 300, s_maxage=3600)   # edge 1 hour
        return response

    return response


@app.after_request
def log_http_request(response):
    """One-line access log per request with the real client IP from Cloudflare.

    Skips /static/ assets and tarpit responses (already logged separately) to
    keep the log signal-heavy. Real-IP comes from CF-Connecting-IP since the
    site sits behind Cloudflare; gunicorn's default access log would only see
    Cloudflare's edge IPs."""
    path = request.path
    if path.startswith('/static/') or response.headers.get('X-Tarpit'):
        return response
    cf_ip = request.headers.get('CF-Connecting-IP', '-')
    cf_country = request.headers.get('CF-IPCountry', '-')
    ua = request.headers.get('User-Agent', '-')
    size = response.headers.get('Content-Length', '-')
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    print(f"[HTTP] {timestamp} | {cf_ip} | {cf_country} | {request.method} {path} {response.status_code} {size} | UA: {ua}", flush=True)
    return response


@app.route('/')
def index():
    weather = get_weather()
    return render_template('index.html', weather=weather)


@app.route('/things-to-do')
def things_to_do():
    return render_template('things-to-do.html')


@app.route('/places-to-visit')
def places_to_visit():
    return render_template('places-to-visit.html')


@app.route('/where-to-stay')
def where_to_stay():
    return render_template('where-to-stay.html')


@app.route('/where-to-eat')
def where_to_eat():
    return render_template('where-to-eat.html')


@app.route('/plan-your-visit')
def plan_your_visit():
    weather = get_weather()
    return render_template('plan-your-visit.html', weather=weather)


@app.route('/bartells-backroads')
def bartells_backroads():
    return render_template('bartells-backroads.html')


@app.route('/webcams')
def webcams():
    return render_template('webcams.html')


@app.route('/technical-details')
def technical_details():
    # Load image credits from licenses.json
    with open('licenses.json', 'r') as f:
        licenses_data = json.load(f)
    return render_template('technical-details.html', image_credits=licenses_data['images'])


@app.route('/alturas')
def alturas():
    return render_template('alturas.html')


@app.route('/cedarville')
def cedarville():
    return render_template('cedarville.html')


@app.route('/merchants/the-vault')
def merchant_the_vault():
    return render_template('merchants/the-vault.html')


@app.route('/merchants/bidwell-canyon-farm')
def merchant_bidwell_canyon_farm():
    return redirect('https://www.bidwellcanyonfarm.com/', code=301)


@app.route('/merchants/valley-farm-store')
def merchant_valley_farm_store():
    return render_template('merchants/valley-farm-store.html')


@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')


@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8042))
    app.run(host='0.0.0.0', port=port)
