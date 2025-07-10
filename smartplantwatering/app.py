from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

# Database Models
class WateringRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    duration = db.Column(db.Integer)

class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    watering_time = db.Column(db.String(5), default='08:00') #HH:MM
    watering_duration = db.Column(db.Integer, default=60) #seconds
    moisture_threshold = db.Column(db.Integer, default=30) #percentage

with app.app_context():
    db.create_all()
    if Configuration.query.count() == 0:
        config = Configuration()
        db.session.add(config)
        db.session.commit()


# Helper Functions
def get_weather_data():
    # Replace with actual weather API call using requests and OPENWEATHERMAP_API_KEY
    # For example using OpenWeatherMap:
    city = 'YourCity'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Extract relevant data (e.g., temperature, humidity, rain)
        return data
    else:
        return None

def get_soil_moisture():
    # Replace with actual sensor reading logic (e.g., using Raspberry Pi GPIO)
    # This is a placeholder that returns a random value between 0 and 100.
    import random
    return random.randint(0, 100)


def control_water_valve(duration):
    # Replace with actual valve control logic (e.g., using Raspberry Pi GPIO)
    # This is a placeholder.  You'd likely use RPi.GPIO library for this.
    print(f"Watering valve turned on for {duration} seconds.")
    record = WateringRecord(duration=duration)
    db.session.add(record)
    db.session.commit()

# Routes
@app.route('/')
def index():
    weather_data = get_weather_data()
    soil_moisture = get_soil_moisture()
    config = Configuration.query.first()

    return render_template('index.html', weather_data=weather_data, soil_moisture=soil_moisture, config=config)


@app.route('/water_now')
def water_now():
    config = Configuration.query.first()
    control_water_valve(config.watering_duration)
    return redirect(url_for('index'))

@app.route('/configuration', methods=['GET', 'POST'])
def configuration():
    config = Configuration.query.first()
    if request.method == 'POST':
        config.watering_time = request.form['watering_time']
        config.watering_duration = int(request.form['watering_duration'])
        config.moisture_threshold = int(request.form['moisture_threshold'])
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('configuration.html', config=config)

@app.route('/history')
def history():
    records = WateringRecord.query.order_by(WateringRecord.timestamp.desc()).limit(10).all()
    return render_template('history.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
