import requests
import hashlib
from datetime import datetime # Add this import
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from config import Config
from models import db, User
from auth import auth
from weather import weather

app = Flask(__name__)
app.config.from_object(Config)

# Add MD5 filter for Gravatar
@app.template_filter('md5')
def md5_filter(s):
    return hashlib.md5(s.lower().encode()).hexdigest()

# Context processor to make current year available to all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.utcnow().year}

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# JWT setup
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(weather)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)