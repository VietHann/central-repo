from flask import Flask, render_template, request, jsonify
import os
import datetime
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MQTT Configuration
mqtt_broker = os.getenv('MQTT_BROKER')
mqtt_port = int(os.getenv('MQTT_PORT'))
mqtt_topic = os.getenv('MQTT_TOPIC')

mqtt_client = mqtt.Client("SmartGardeningWebApp")
mqtt_client.connect(mqtt_broker, mqtt_port)

# Dummy data for demonstration
plant_data = {
    "plant1": {
        "name": "Rose",
        "type": "Flower",
        "last_watered": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "soil_moisture": 60,
        "health": "Healthy"
    },
    "plant2": {
        "name": "Tomato",
        "type": "Vegetable",
        "last_watered": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "soil_moisture": 40,
        "health": "Needs Attention"
    }
}

@app.route('/')
def index():
    return render_template('index.html', plants=plant_data)

@app.route('/water_plant', methods=['POST'])
def water_plant():
    plant_id = request.form['plant_id']
    # Publish to MQTT to trigger watering
    mqtt_client.publish(mqtt_topic, f"Watering plant: {plant_id}")
    plant_data[plant_id]['last_watered'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({'status': 'success'})

@app.route('/plant_details/<plant_id>')
def plant_details(plant_id):
    plant = plant_data.get(plant_id)
    if plant:
        return render_template('plant_details.html', plant=plant)
    else:
        return "Plant not found", 404

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    # Save the image (temporarily)
    image.save('temp_image.jpg') # Replace with secure storage and unique name

    # Perform plant identification (replace with your actual implementation)
    plant_type = identify_plant('temp_image.jpg') # Call your ML model

    # Return the identified plant type
    return jsonify({'plant_type': plant_type})

def identify_plant(image_path):
    # Placeholder for plant identification logic
    # This is where you would integrate your TensorFlow Lite model
    # Example: Load the model, preprocess the image, run inference, and return the predicted plant type
    # For now, return a dummy value
    return "Unknown Plant"

if __name__ == '__main__':
    app.run(debug=True)
