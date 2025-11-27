import os
import json
import time
import re
from datetime import datetime, timezone
from flask import Flask, render_template, send_from_directory, Response, request

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


def is_valid_route(path):
    """Check if path matches any registered route."""
    adapter = app.url_map.bind('')
    try:
        adapter.match(path)
        return True
    except Exception:
        return False


def tarpit_response():
    """Generate a slow response that wastes scanner resources."""
    # Fake PHP-looking garbage, sent byte by byte
    garbage_lines = [
        b'<?php /* WordPress Security Check */ ?>\n',
        b'<?php require_once("wp-config.php"); ?>\n',
        b'<?php // Validating credentials... ?>\n',
        b'<?php $db = mysqli_connect("localhost", "root", ""); ?>\n',
        b'<?php // Loading admin panel... ?>\n',
        b'<?php session_start(); /* auth pending */ ?>\n',
    ]
    for _ in range(50):  # ~30 seconds total
        for line in garbage_lines:
            yield line
            time.sleep(0.1)


def log_and_tarpit(reason):
    """Log the probe attempt and return a tarpit response."""
    cf_ip = request.headers.get('CF-Connecting-IP', 'unknown')
    x_forwarded = request.headers.get('X-Forwarded-For', 'unknown')
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    print(f"[TARPIT:{reason}] {timestamp} | CF-IP: {cf_ip} | X-Forwarded-For: {x_forwarded} | URL: {request.url}", flush=True)

    return Response(
        tarpit_response(),
        status=200,
        mimetype='text/plain',
        headers={'X-Tarpit': 'enjoy-the-wait'}
    )


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
    return render_template('index.html')


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
    return render_template('plan-your-visit.html')


@app.route('/bartells-backroads')
def bartells_backroads():
    return render_template('bartells-backroads.html')


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


@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')


@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8042))
    app.run(host='0.0.0.0', port=port)
