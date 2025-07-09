# Smart Gardening Assistant

A web application to automate and monitor your home garden, helping you care for your plants more effectively.

## Features:

*   Automated watering based on weather forecasts and soil moisture.
*   Plant identification via image upload and care recommendations.
*   Alerts for potential plant diseases.
*   Tracking and statistics of plant growth over time.
*   Fertilizer recommendations.

## Tech Stack

*   **Backend:** Python, Flask
*   **Hardware:** Raspberry Pi, DHT11/DHT22 sensors, Relay Module
*   **Image Processing:** OpenCV, TensorFlow Lite
*   **Communication:** MQTT

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd smartgardeningassistant
    ```

2.  Create a virtual environment (optional):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Configure environment variables in `.env`:

    ```
    MQTT_BROKER=your_mqtt_broker_address
    MQTT_PORT=1883
    MQTT_TOPIC=smart_gardening
    ```

5.  Run the application:

    ```bash
    python app.py
    ```
