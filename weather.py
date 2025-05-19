from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
import time
from forms import WeatherSearchForm
from models import WeatherSearch, User, db

weather = Blueprint('weather', __name__)

# Add simple in-memory cache for weather API responses
_weather_cache = {}
_cache_timeout = 300  # 5 minutes in seconds

@weather.route('/', methods=['GET', 'POST'])
def index():
    form = WeatherSearchForm()
    
    # Handle query parameter for city (from history link)
    city_param = request.args.get('city')
    if city_param:
        return get_weather_data(city_param)
    
    if form.validate_on_submit():
        return get_weather_data(form.city.data)
    
    return render_template('weather.html', form=form, weather_data=None)

def get_weather_data(city):
    api_key = current_app.config['OPENWEATHERMAP_API_KEY']
    
    # Check cache first (with case-insensitive lookup)
    current_time = int(time.time())
    city_key = city.lower()
    
    if city_key in _weather_cache:
        cached_data, timestamp = _weather_cache[city_key]
        if current_time - timestamp < _cache_timeout:
            # Return cached data if it's still fresh
            return render_template('weather.html', form=WeatherSearchForm(), weather_data=cached_data)
    
    # If not in cache or cache expired, fetch from API
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'
    
    try:
        response = requests.get(url, timeout=5)  # Add timeout
        data = response.json()
        
        if response.status_code == 200:
            weather_data = {
                'city': city,
                'temperature': round(data['main']['temp']),
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'feels_like': round(data['main']['feels_like'])
            }
            
            # Cache the results
            _weather_cache[city_key] = (weather_data, current_time)
            
            # Save search to database if user is logged in
            if current_user.is_authenticated:
                search = WeatherSearch(
                    city=city,
                    temperature=weather_data['temperature'],
                    description=weather_data['description'],
                    humidity=weather_data['humidity'],
                    wind_speed=weather_data['wind_speed'],
                    user_id=current_user.id
                )
                db.session.add(search)
                db.session.commit()
                
            return render_template('weather.html', form=WeatherSearchForm(), weather_data=weather_data)
        else:
            error_message = data.get('message', 'An error occurred')
            flash(f"Error: {error_message}", 'danger')
            return render_template('weather.html', form=WeatherSearchForm(), weather_data=None)
            
    except Exception as e:
        flash(f"Error: {str(e)}", 'danger')
        return render_template('weather.html', form=WeatherSearchForm(), weather_data=None)

@weather.route('/history')
@login_required
def history():
    searches = WeatherSearch.query.filter_by(user_id=current_user.id).order_by(WeatherSearch.timestamp.desc()).all()
    return render_template('history.html', searches=searches)

# API Routes
@weather.route('/api/weather/<city>')
@jwt_required()
def api_get_weather(city):
    api_key = current_app.config['OPENWEATHERMAP_API_KEY']
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            weather_data = {
                'city': city,
                'temperature': round(data['main']['temp']),
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'feels_like': round(data['main']['feels_like'])
            }
            
            # Save search to database
            username = get_jwt_identity()
            user = User.query.filter_by(username=username).first()
            
            search = WeatherSearch(
                city=city,
                temperature=weather_data['temperature'],
                description=weather_data['description'],
                humidity=weather_data['humidity'],
                wind_speed=weather_data['wind_speed'],
                user_id=user.id
            )
            db.session.add(search)
            db.session.commit()
                
            return jsonify(weather_data)
        else:
            return jsonify({'error': data.get('message', 'An error occurred')}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@weather.route('/api/history')
@jwt_required()
def api_history():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    
    searches = WeatherSearch.query.filter_by(user_id=user.id).order_by(WeatherSearch.timestamp.desc()).all()
    result = []
    
    for search in searches:
        result.append({
            'id': search.id,
            'city': search.city,
            'temperature': search.temperature,
            'description': search.description,
            'humidity': search.humidity,
            'wind_speed': search.wind_speed,
            'timestamp': search.timestamp.isoformat()
        })
    
    return jsonify(result)