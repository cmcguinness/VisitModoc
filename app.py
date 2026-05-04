import os
import json
import time
import re
import threading
import requests
from datetime import datetime, timezone
from flask import Flask, render_template, send_from_directory, Response, request, redirect

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
        return redirect(RICK_ROLL_URL, code=302)

    print(f"[TARPIT:{reason}] {timestamp} | CF-IP: {cf_ip} | X-Forwarded-For: {x_forwarded} | URL: {request.url}", flush=True)
    return Response(
        tarpit_response(),
        status=200,
        mimetype='text/plain',
        headers={'X-Tarpit': 'enjoy-the-wait'}
    )


# Weather data cache
_weather_cache = {'data': None, 'timestamp': 0}
WEATHER_CACHE_DURATION = 3600  # 1 hour


def get_weather():
    """Fetch current weather for Alturas from NWS API with caching."""
    now = time.time()

    # Return cached data if still valid
    if _weather_cache['data'] and (now - _weather_cache['timestamp']) < WEATHER_CACHE_DURATION:
        return _weather_cache['data']

    try:
        headers = {'User-Agent': 'VisitModoc/1.0 (visit-modoc.com)'}

        # NWS API for Alturas, CA area (pre-looked-up grid point)
        forecast_url = 'https://api.weather.gov/gridpoints/REV/33,117/forecast'
        response = requests.get(forecast_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        periods = data.get('properties', {}).get('periods', [])
        if periods:
            current = periods[0]
            weather_data = {
                'name': current.get('name', 'Now'),
                'temperature': current.get('temperature'),
                'unit': current.get('temperatureUnit', 'F'),
                'description': current.get('shortForecast', ''),
                'detailed': current.get('detailedForecast', ''),
                'wind': current.get('windSpeed', ''),
                'icon': current.get('icon', ''),
                'success': True
            }
            _weather_cache['data'] = weather_data
            _weather_cache['timestamp'] = now
            return weather_data

    except Exception as e:
        print(f"[WEATHER] Error fetching weather: {e}", flush=True)

    return {'success': False}


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
