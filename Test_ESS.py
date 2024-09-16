import paho.mqtt.client as mqtt
import random
from datetime import datetime
import time
import csv
import os
import logging

# Setup logging for data quality issues
logging.basicConfig(filename="D:/AI_based_control/Project_laboratory_2/ESM/data_quality.log", level=logging.WARNING,
                    format='%(asctime)s %(message)s')

# MQTT broker configuration
broker = "localhost"
port = 1883
topic_ems = "EMS/ESS"
topic_ess = "ESS/EMS"
fallback_file = "D:/AI_based_control/Project_laboratory_2/ESM/fallback_data.csv"

# Load unsent data from the fallback file (if any)
def load_fallback_data():
    if os.path.exists(fallback_file):
        with open(fallback_file, 'r') as f:
            reader = csv.reader(f)
            data = []
            for row in reader:
                data.append(row)
            return data
    return []

# Save unsent data to the fallback file
def save_fallback_data(data):
    with open(fallback_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
        
# Clear the fallback data once sent successfully
def clear_fallback_data():
    if os.path.exists(fallback_file):
        os.remove(fallback_file)

# Attempt to resend unsent data when the connection is restored
# Attempt to resend unsent data when the connection is restored
def resend_fallback_data(client):
    unsent_data = load_fallback_data()
    if unsent_data:
        print(f"Resending {len(unsent_data)} messages from fallback storage...")
        for message in unsent_data:
            # Convert the list to a string if it's not already a string
            message_str = ','.join(message) if isinstance(message, list) else message
            result = client.publish(topic_ess, message_str)
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                print(f"Failed to resend: {message_str}")
                return False
        clear_fallback_data()
        print("Sent successfully.")
    return True


# Callback when ESS receives a message from the EMS
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received message from EMS: {message}")

    timestamp_str, power_target = message.split(',')
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

    temperature = random.uniform(10.0, 100.0)  
    state_of_charge = random.uniform(10.0, 110.0) 

    if not (10.0 <= temperature <= 50.0):
        logging.warning(f"Temperature {temperature} out of range (10-50)!")
    if not (10.0 <= state_of_charge <= 90.0):
        logging.warning(f"State of charge {state_of_charge} out of range (10-90)!")

    power_actual = power_target
    response_message = f"{timestamp},{power_actual},{temperature},{state_of_charge}"

    # Simulate publish failure
    result = mqtt.MQTT_ERR_UNKNOWN  # Force failure

    if result == mqtt.MQTT_ERR_SUCCESS:
        print(f"Published to EMS: {response_message}")
        resend_fallback_data(client)
    else:
        print(f"Failed to publish message: {response_message}. Storing in fallback.")
        unsent_data = load_fallback_data()
        unsent_data.append(response_message.split(','))
        save_fallback_data(unsent_data)


# Callback when the MQTT connection is lost
def on_disconnect(client, userdata, rc):
    print(f"Disconnected with result code {rc}. Messages will be stored locally.")

# Callback when the MQTT connection is established
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}.")
    client.subscribe(topic_ems)
    resend_fallback_data(client)  # Resend any locally stored data

# Initialize the MQTT client
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Connect to the MQTT broker
try:
    client.connect(broker, port, 60)
except Exception as e:
    print(f"Connection failed: {e}. Starting in offline mode.")

# Start the MQTT client loop to listen for EMS messages
client.loop_start()

# Keep the ESS running and simulating data
try:
    while True:
        time.sleep(5)  # ESS sends/receives data every 5 seconds
except KeyboardInterrupt:
    print("Stopping ESS...")

# Stop the MQTT loop and disconnect
client.loop_stop()
client.disconnect()
