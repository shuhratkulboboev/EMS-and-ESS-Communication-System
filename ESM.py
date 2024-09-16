import paho.mqtt.client as mqtt
import sqlite3
import csv
import time
from datetime import datetime

# SQLite database connection
def get_db_connection():
    conn = sqlite3.connect('C:/Users/HP/testDB.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TestDB (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        power_actual REAL,
        temperature REAL,
        state_of_charge REAL
    )
    ''')
    conn.commit()
    conn.close()

create_table()

# MQTT broker configuration
broker = "localhost"
port = 1883
topic = "EMS/ESS"


# Callback when the EMS receives a message from the ESS
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received message from ESS: {message}")

    # Parse the message received from ESS
    try:
        timestamp_str, power_actual, temperature, state_of_charge = message.split(',')
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S').isoformat()

        # Insert the data into the SQLite database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO TestDB (timestamp, power_actual, temperature, state_of_charge)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, float(power_actual), float(temperature), float(state_of_charge)))
        conn.commit()
        conn.close()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error processing message: {e}")

# Read power targets from CSV file and publish to ESS
def publish_power_targets(client, power_target_file):
    with open(power_target_file, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            timestamp_str = row[0]
            power_target = float(row[1])
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

            # Publish the power target to the ESS via MQTT
            message = f"{timestamp},{power_target}"
            client.publish(topic, message)
            print(f"Published to ESS: {message}")

            time.sleep(5)  # Wait for 5 seconds before sending the next message

# Initialize the MQTT client
client = mqtt.Client()
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker, port, 60)
client.subscribe("ESS/EMS")

# Start the MQTT client loop
client.loop_start()

# Publish power targets from the CSV file to the ESS
power_target_file = 'D:/AI_based_control/Project_laboratory_2/ESM/power_target.csv'
publish_power_targets(client, power_target_file)

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Stopping EMS...")

# Stop the MQTT client loop and close the database connection
client.loop_stop()
client.disconnect()
conn.close()