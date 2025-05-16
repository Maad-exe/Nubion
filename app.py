import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
API_KEY = "a6f2ec91bd6a23627a664b37649d0404"  # My API KEY

@app.route('/')
def index():
    return render_template('weather.html', weather_data=None)

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    
    if not city:
        return redirect(url_for('index'))
    
    # Fetch weather data from OpenWeatherMap API for the city
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}'
    
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

            print (weather_data)
            return render_template('weather.html', weather_data=weather_data)
        else:
            error_message = data.get('message', 'An error occurred')
            return render_template('weather.html', error=error_message, weather_data=None)
            
    except Exception as e:
        return render_template('weather.html', error=str(e), weather_data=None)

if __name__ == '__main__':
    app.run(debug=True)