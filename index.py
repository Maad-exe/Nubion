import os
from app import app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

# Create SQLite directory
os.makedirs('/tmp/db', exist_ok=True)

# Modify SQLite path for Vercel serverless environment
import models
import config
config.Config.SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/db/weather_app.db'

# Initialize the database
with app.app_context():
    models.db.create_all()

# Simple static response for health check
def static_response(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Static response from Nubion Weather App']

# Create dispatcher for paths
app.wsgi_app = DispatcherMiddleware(
    static_response, {'/api': app.wsgi_app}
)

# Lambda handler
def handler(event, context):
    return app(event, context)