import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Always use SQLite for the Vercel deployment
    SQLALCHEMY_DATABASE_URI = 'sqlite:///weather_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # OpenWeatherMap API
    OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY') or "a6f2ec91bd6a23627a664b37649d0404"