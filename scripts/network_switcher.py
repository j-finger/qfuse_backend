import RPi.GPIO as GPIO
import subprocess
import time
import logging
from utils import logging as utils_logging  # Alias to avoid conflict

# Define Network Manager connection names
AP_MODE = "qfnet"
CLIENT_MODE = "preconfigured"

# Pin Definitions
SWITCH_PIN = 21  # GPIO pin connected to the toggle switch
LED_WIFI_PIN = 7
LED_LAN_PIN = 10
first_run = True

BLINK_TIME = 0.3

# Callback function to handle switch events
def switch_callback(channel):
    global first_run
    if first_run:
        GPIO.output(LED_WIFI_PIN, GPIO.HIGH)  # Corrected comma
        first_run = False
        logging.info("First run detected, skipping switch callback.")
        return

    # Read the current state of the switch
    switch_state = GPIO.input(SWITCH_PIN)
    if switch_state == GPIO.HIGH:
        logging.info("Switch is ON - Switching to AP Mode")
        switch_to_ap_mode()
        GPIO.output(LED_LAN_PIN, GPIO.HIGH)  # Corrected comma
    else:
        logging.info("Switch is OFF - Switching to Client Mode")
        switch_to_client_mode()
        GPIO.output(LED_WIFI_PIN, GPIO.HIGH)  # Corrected comma

# Function to switch to AP Mode
def switch_to_ap_mode():
    try:
        GPIO.output(LED_WIFI_PIN, GPIO.LOW)
        # Disconnect from Client mode
        blink_led(LED_LAN_PIN)
        subprocess.run(["sudo", "nmcli", "connection", "down", CLIENT_MODE], check=True)
        # Activate AP Mode
        blink_led(LED_LAN_PIN)
        subprocess.run(["sudo", "nmcli", "connection", "up", AP_MODE], check=True)
        logging.info("Switched to AP Mode successfully.")
        # Restart mqtt_listener.service with delay
        blink_led(LED_LAN_PIN)
        subprocess.run(["sudo", "systemctl", "restart", "mqtt_listener.service"], check=True)
        logging.info("mqtt_listener.service restarted.")
        blink_led(LED_LAN_PIN)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to switch to AP Mode: {e}")

# Function to switch to Client Mode
def switch_to_client_mode():
    try:
        GPIO.output(LED_LAN_PIN, GPIO.LOW)
        # Disconnect from AP Mode
        blink_led(LED_WIFI_PIN)
        subprocess.run(["sudo", "nmcli", "connection", "down", AP_MODE], check=True)
        # Activate Client Mode
        blink_led(LED_WIFI_PIN)
        subprocess.run(["sudo", "nmcli", "connection", "up", CLIENT_MODE], check=True)
        logging.info("Switched to Client Mode successfully.")
        # Restart mqtt_listener.service with delay
        blink_led(LED_WIFI_PIN)
        subprocess.run(["sudo", "systemctl", "restart", "mqtt_listener.service"], check=True)
        logging.info("mqtt_listener.service restarted.")
        blink_led(LED_WIFI_PIN)
        subprocess.run(["sudo", "dhclient", "-r"], check=True)
        blink_led(LED_WIFI_PIN)
        subprocess.run(["sudo", "dhclient"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to switch to Client Mode: {e}")

# GPIO Setup
def setup_gpio():
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set pin 21 as input with pull-up resistor
    GPIO.setup(LED_WIFI_PIN, GPIO.OUT)  # Set the LED pin as output
    GPIO.setup(LED_LAN_PIN, GPIO.OUT)  # Set the LED pin as output

    blink_led(LED_LAN_PIN)
    blink_led(LED_WIFI_PIN)
    # Add event detection on both rising and falling edges
    GPIO.add_event_detect(SWITCH_PIN, GPIO.BOTH, callback=switch_callback, bouncetime=200)

def blink_led(led):
    GPIO.output(led, GPIO.HIGH)
    time.sleep(BLINK_TIME)
    GPIO.output(led, GPIO.LOW)
    time.sleep(BLINK_TIME / 2)

# Cleanup GPIO on exit
def cleanup_gpio():
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        setup_gpio()
        logging.info("Network switcher is running. Waiting for toggle switch events (press Ctrl+C to exit)...")
        print("Network switcher is running. Waiting for toggle switch events (press Ctrl+C to exit)...")
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        logging.info("Exiting program")
        print("Exiting program")
    finally:
        cleanup_gpio()
