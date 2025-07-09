from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import paho.mqtt.client as mqtt
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartgarden.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

mqtt_broker = os.environ.get('MQTT_BROKER', 'localhost')
mqtt_port = int(os.environ.get('MQTT_PORT', 1883))
mqtt_topic = os.environ.get('MQTT_TOPIC', 'smartgarden/sensors')

client = mqtt.Client()

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    soil_moisture = db.Column(db.Float)
    temperature = db.Column(db.Float)

    def __repr__(self):
        return f'<SensorData %r>' % self.timestamp

@app.route('/')
def index():
    data = SensorData.query.order_by(SensorData.timestamp.desc()).limit(10).all()
    data.reverse()
    return render_template('index.html', data=data)

@app.route('/manual', methods=['GET', 'POST'])
def manual_control():
    if request.method == 'POST':
        action = request.form['action']
        # Send MQTT message to control the relay (pump)
        if action == 'on':
            client.publish('smartgarden/pump', 'on')
        elif action == 'off':
            client.publish('smartgarden/pump', 'off')

        return redirect(url_for('manual_control'))
    return render_template('manual_control.html')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    try:
        soil_moisture, temperature = map(float, payload.split(','))
        new_data = SensorData(soil_moisture=soil_moisture, temperature=temperature)
        db.session.add(new_data)
        db.session.commit()
        print(f"Received data: Soil Moisture: {soil_moisture}, Temperature: {temperature}")
    except ValueError:
        print(f"Invalid data format: {payload}")

    except Exception as e:
        print(f"Error processing message: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_start()

    app.run(debug=True, host='0.0.0.0')