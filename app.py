import requests
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager  # For session-based authentication
from flask_jwt_extended import JWTManager  # For token-based API authentication
from flask_migrate import Migrate  # For database migrations

# Import configuration and components
from config import Config  # Application configuration
from models import db, User  # Database models
from auth import auth  # Authentication blueprint
from weather import weather  # Weather functionality blueprint

# Create Flask application instance
app = Flask(__name__)
# Load configuration from Config class
app.config.from_object(Config)

# Add MD5 filter for Gravatar email hashing
@app.template_filter('md5')
def md5_filter(s):
    # Converts email to MD5 hash for Gravatar profile images
    return hashlib.md5(s.lower().encode()).hexdigest()

# Context processor to make current year available to all templates
@app.context_processor
def inject_current_year():
    # Used for copyright year in footer
    return {'current_year': datetime.utcnow().year}

# Initialize database with the Flask app
db.init_app(app)
# Set up database migrations
migrate = Migrate(app, db)

# Configure Flask-Login for session-based authentication
login_manager = LoginManager()
login_manager.init_app(app)
# Redirect users to login page when @login_required is used
login_manager.login_view = 'auth.login'
# Style for flash messages
login_manager.login_message_category = 'info'

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    # Load user from database by ID for session management
    return User.query.get(int(user_id))

# Configure JWT for API authentication
jwt = JWTManager(app)
# JWT settings are in Config class (token expiration, secret key)

# Register blueprints to organize routes by feature
app.register_blueprint(auth)  # Authentication routes (/login, /register, etc.)
app.register_blueprint(weather)  # Weather routes (/, /history, etc.)

# Create all database tables defined in models
with app.app_context():
    db.create_all()

# Run the application in debug mode when executed directly
if __name__ == '__main__':
    app.run(debug=True)