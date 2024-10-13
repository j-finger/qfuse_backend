# scripts/mqtt_listener.py

import paho.mqtt.client as mqtt
import json
import logging
from data_handler import handle_data_message
from settings_handler import handle_settings_message
from logs_handler import handle_logs_message
from utils import DATABASES_DIR

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPICS = [('sensor/data', 0), ('sensor/settings', 0), ('sensor/logs', 0)]

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT Broker")
        client.subscribe(MQTT_TOPICS)
        subscribed_topics = [topic for topic, qos in MQTT_TOPICS]
        logging.info(f"Subscribed to topics: {subscribed_topics}")
    else:
        logging.error(f"Failed to connect to MQTT Broker, return code {rc}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    # logging.info(f"Received message on topic {topic}: {payload}")
    logging.info(f"Received message on topic {topic}")
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON format: {e}")
        return

    if topic == 'sensor/data':
        handle_data_message(data)
    elif topic == 'sensor/settings':
        handle_settings_message(data)
    elif topic == 'sensor/logs':
        handle_logs_message(data)
    else:
        logging.warning(f"Unhandled topic: {topic}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        logging.info(f"Connecting to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")
        client.loop_forever()
    except Exception as e:
        logging.error(f"Failed to connect to MQTT Broker: {e}")

if __name__ == '__main__':
    main()
