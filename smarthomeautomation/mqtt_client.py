import paho.mqtt.client as mqtt
import config

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected to MQTT Broker!')
        client.subscribe(config.MQTT_TOPIC)
    else:
        print(f'Failed to connect, return code {rc}')

def on_message(client, userdata, msg):
    print(f'Received `{msg.payload.decode()}` from `{msg.topic}` topic')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(config.MQTT_BROKER_URL, config.MQTT_BROKER_PORT)

# Keep the script running to maintain the connection
#client.loop_forever()