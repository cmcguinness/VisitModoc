import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Production configuration
if os.environ.get('RAILWAY_ENVIRONMENT'):
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = False
else:
    app.config['DEBUG'] = True


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
    return render_template('technical-details.html')


@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')


@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8042))
    app.run(host='0.0.0.0', port=port)
