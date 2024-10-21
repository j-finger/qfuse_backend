# scripts/mqtt_listener.py

import paho.mqtt.client as mqtt
import json
import logging
import time
from data_handler import handle_data_message
from settings_handler import handle_settings_message
from logs_handler import handle_logs_message
from utils import DATABASES_DIR

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPICS = [
    ('sensor/data', 0),
    ('sensor/settings', 0),
    ('sensor/logs', 0),
    ('time/request', 0)  # Subscribe to 'time/request' topic
]

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
    logging.info(f"Received message on topic {topic}")

    if topic == 'sensor/data':
        try:
            data = json.loads(payload)
            handle_data_message(data)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON format in sensor/data: {e}")
    elif topic == 'sensor/settings':
        try:
            data = json.loads(payload)
            handle_settings_message(data)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON format in sensor/settings: {e}")
    elif topic == 'sensor/logs':
        try:
            data = json.loads(payload)
            handle_logs_message(data)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON format in sensor/logs: {e}")
    elif topic == 'time/request':
        handle_time_request(client)  # Handle time request
    else:
        logging.warning(f"Unhandled topic: {topic}")

def handle_time_request(client):
    current_time = int(time.time())
    time_message = {'time': current_time}
    time_json = json.dumps(time_message)
    client.publish('time/response', time_json)
    logging.info(f"Responded to time request with time {current_time}")

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
