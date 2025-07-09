import paho.mqtt.client as mqtt
import os

mqtt_broker = os.environ.get('MQTT_BROKER', 'localhost')
mqtt_port = int(os.environ.get('MQTT_PORT', 1883))
mqtt_topic = os.environ.get('MQTT_TOPIC', 'smartgarden/sensors')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode()))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting. Other loop*() functions are available that
# enable integrating this call into your program.
client.loop_forever()