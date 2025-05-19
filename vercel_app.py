import os
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask_login import LoginManager

# Create a simplified app for Vercel
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/weather_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['OPENWEATHERMAP_API_KEY'] = "a6f2ec91bd6a23627a664b37649d0404"

# Create sqlite directory in /tmp
os.makedirs('/tmp', exist_ok=True)

# Initialize database
db = SQLAlchemy(app)

# Import your models 
from models import User, WeatherSearch

# MD5 filter for Gravatar
@app.template_filter('md5')
def md5_filter(s):
    return hashlib.md5(s.lower().encode()).hexdigest()

# Context processor for current year
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.utcnow().year}

# Create a simplified index route
@app.route('/')
def index():
    return render_template('landing.html')

# Static route for health check
def static_response(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Nubion Weather App on Vercel']

# Create dispatcher
app.wsgi_app = DispatcherMiddleware(
    static_response, {'/app': app.wsgi_app}
)

# Initialize database
with app.app_context():
    db.create_all()

# Handle serverless function
def handler(event, context):
    return app(event, context)