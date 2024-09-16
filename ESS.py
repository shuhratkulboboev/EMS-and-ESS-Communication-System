import paho.mqtt.client as mqtt
import random
from datetime import datetime
import time

# MQTT broker configuration
broker = "localhost"
port = 1883
topic_ems = "EMS/ESS"
topic_ess = "ESS/EMS"

# Callback when ESS receives a message from the EMS
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received message from EMS: {message}")

    # Parse the message (timestamp and power_target)
    timestamp_str, power_target = message.split(',')
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

    # Mock data for temperature and state_of_charge
    temperature = random.uniform(15.0, 50.0)  
    state_of_charge = random.uniform(10.0, 90.0) 

    # Send the power_actual (same as power_target), temperature, and state_of_charge back to EMS
    power_actual = power_target
    response_message = f"{timestamp},{power_actual},{temperature},{state_of_charge}"
    client.publish(topic_ess, response_message)
    print(f"Published to EMS: {response_message}")

# Initialize the MQTT client
client = mqtt.Client()
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker, port, 60)
client.subscribe(topic_ems)

# Start the MQTT client loop to listen for EMS messages
client.loop_start()

# Keep the ESS running
try:
    while True:
        time.sleep(5)  # ESS sends/receives data every 5 seconds
except KeyboardInterrupt:
    print("Stopping ESS...")

# Stop the MQTT loop and disconnect
client.loop_stop()
client.disconnect()
