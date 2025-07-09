import os
from dotenv import load_dotenv

load_dotenv()

# Example config variables
MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL', 'broker.hivemq.com')
MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT', 1883))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'smarthome/devices')