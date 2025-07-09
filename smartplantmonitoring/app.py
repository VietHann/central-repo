from flask import Flask, render_template
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# InfluxDB Configuration
influxdb_token = "YOUR_INFLUXDB_TOKEN"
influxdb_org = "YOUR_INFLUXDB_ORG"
influxdb_bucket = "smartplantmonitoring"
influxdb_url = "YOUR_INFLUXDB_URL"

# MQTT Configuration
mqtt_broker = "YOUR_MQTT_BROKER"
mqtt_port = 1883
mqtt_topic = "smartplant/sensors"

# InfluxDB Client
influxdb_client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
query_api = influxdb_client.query_api()

# MQTT Client
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        soil_moisture = data.get('soil_moisture')
        light_intensity = data.get('light_intensity')

        if all([temperature is not None, humidity is not None, soil_moisture is not None, light_intensity is not None]):
            point = Point("sensor_data") \
                .field("temperature", float(temperature)) \
                .field("humidity", float(humidity)) \
                .field("soil_moisture", float(soil_moisture)) \
                .field("light_intensity", float(light_intensity))
            write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)
            print(f"Data written to InfluxDB: Temperature={temperature}, Humidity={humidity}, Soil Moisture={soil_moisture}, Light Intensity={light_intensity}")
        else:
            print("Incomplete data received from MQTT.")

    except json.JSONDecodeError:
        print("Error decoding JSON from MQTT message.")
    except Exception as e:
        print(f"Error processing MQTT message: {e}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker, mqtt_port, 60)
mqtt_client.loop_start()


@app.route('/')
def index():
    # Fetch latest data from InfluxDB
    query = f'from(bucket:"{influxdb_bucket}") |> range(start: -1h) |> last()'
    result = query_api.query(org=influxdb_org, query=query)
    
    temperature = None
    humidity = None
    soil_moisture = None
    light_intensity = None

    if result:
        for table in result:
            for record in table.records:
                if record.get_field() == "temperature":
                    temperature = record.get_value()
                elif record.get_field() == "humidity":
                    humidity = record.get_value()
                elif record.get_field() == "soil_moisture":
                    soil_moisture = record.get_value()
                elif record.get_field() == "light_intensity":
                    light_intensity = record.get_value()
    
    return render_template('index.html', temperature=temperature, humidity=humidity, soil_moisture=soil_moisture, light_intensity=light_intensity)

if __name__ == '__main__':
    app.run(debug=True)