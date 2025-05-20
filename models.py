from flask_sqlalchemy import SQLAlchemy  # ORM library for database interaction
from flask_login import UserMixin  # Provides methods needed by Flask-Login
from datetime import datetime  # For timestamp handling
import bcrypt  # Secure password hashing library

# Initialize SQLAlchemy without binding to a specific app (will be bound in app.py)
db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
    User model representing registered application users.
    Inherits from UserMixin to provide Flask-Login integration methods.
    """
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each user
    username = db.Column(db.String(64), unique=True, nullable=False)  # Username must be unique and required
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email must be unique and required
    password_hash = db.Column(db.String(128), nullable=False)  # Stores hashed password, never raw password
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Automatic timestamp when user is created
    # One-to-many relationship: one user can have many weather searches
    # lazy='dynamic' returns a query that can be further refined rather than loading all records
    weather_searches = db.relationship('WeatherSearch', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        """
        Hash and store a password securely with bcrypt.
        Converts bytes to string for storage compatibility.
        """
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """
        Verify a password against the stored hash using bcrypt.
        Returns True if password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def __repr__(self):
        """String representation of User object for debugging."""
        return f'<User {self.username}>'

class WeatherSearch(db.Model):
    """
    WeatherSearch model to store historical weather data searched by users.
    Each search is linked to a user through a foreign key relationship.
    """
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each search
    city = db.Column(db.String(100), nullable=False)  # City name that was searched
    temperature = db.Column(db.Float, nullable=False)  # Temperature in Celsius
    description = db.Column(db.String(100), nullable=False)  # Weather condition description
    humidity = db.Column(db.Integer, nullable=False)  # Humidity percentage
    wind_speed = db.Column(db.Float, nullable=False)  # Wind speed in m/s
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # When the search was performed
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key linking to User model
    
    def __repr__(self):
        """String representation of WeatherSearch object for debugging."""
        return f'<WeatherSearch {self.city} at {self.timestamp}>'