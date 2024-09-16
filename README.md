# EMS-and-ESS-Communication-System
## Overview
This project implements a simplified model of communication between an Energy Management System (EMS) and an Energy Storage System (ESS), using MQTT for messaging and SQLite for data storage. The task simulates an industrial energy storage unit being controlled by commands issued from a central EMS. The main goal is to ensure that the EMS can monitor and control the ESS in real-time while handling possible connectivity issues.

## Architecture

The system is comprised of four primary components:

### EMS (Energy Management System):
Reads target power values, and sends them to the ESS every 3(it can be 15 minutes but avoid wasting time , it is just 3 s) seconds via MQTT. It also stores ESS data in an SQLite database.
### ESS (Energy Storage System): 
Simulates an energy storage unit, generating mock values for temperature, state of charge, and actual power. Sends this data to EMS every 3 seconds.
### MQTT Broker:
Facilitates communication between the EMS and ESS.
### SQLite Database:
Stores data received from the ESS.
The communication between EMS and ESS occurs via MQTT, with the SQLite database storing all the incoming data from ESS for historical analysis.

![image](https://github.com/user-attachments/assets/22dae66a-e2ce-47c9-86fc-99c140650561)

## Components 
### Energy Management System (EMS)
- **Function:** Reads power_target from a predefined file and sends it to ESS every 3 seconds.
- **timestamp:** Time of sending (year-month-day).
- **power_target:** The target power value to be applied (received from **power_target.csv** file).
- **Database:** Stores data received from ESS, including id, power_actual, temperature, and state_of_charge, with a timestamp.
### Energy Storage System (ESS)
- **Function:** Simulates an energy storage unit. Receives power_target from EMS, sends back power_actual (same as power_target for simplicity) and mock values for temperature and state_of_charge.
- **timestamp:** Time of sending (year-month-day).
- **power_actual:** Same as power_target(because there was no actual devices).
- **temperature:** Simulated value(random value between 10 and 90) and if the value exceeds that interval,the system logs data into **data_quality.log**
- **state_of_charge:** Simulated value.
- **Fallback Mechanism:** In case of a connection issue, the ESS stores data locally into **fallback_data.csv** and sends it to EMS once the connection is restored.This can be tested in **Test_ESS.py**
### MQTT Broker (open source Eclipse Mosquitto broker used)
Facilitates the message exchange between EMS and ESS.
- **Uses channels to transmit data:** localhost used in the project  with port=1883 and broker = "localhost"
- **ems/power_target:** For EMS to send power target to ESS.
- **ess/data:** For ESS to send back data to EMS.
### SQLite Database
Stores the following data from ESS and database and table called "TestDB.db" and TestDB respectively:
- **id** -> Integer
- **timestamp** -> Text
- **power_actual** ->Real
- **temperature** -> Real
- **state_of_charge** -> Real
## Setup & Installation
### Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ems-ess-mqtt.git
   ```
### Create a virtual environment and activate it:
  ```bash
   python3 -m venv venv
   source venv/bin/activate
  ```
### Install the required dependencies:
```bash
   pip install -r requirements.txt
```
### Run the MQTT broker (e.g., Mosquitto) locally:
 ```bash
   mosquitto
 ```
### Start the EMS:
 ```bash
   python ESS.py
 ```
### Start the ESS:
 ```bash
   python ESM.py
 ```
## Test Fallback Mechanism
### Start the ESS:
 ```bash
   python Test_ESS.py
 ```
### Start the ESM:
 ```bash
   python ESM.py
 ```
## Todo List
- Automatic Reconnection: Add logic to automatically reconnect to the MQTT broker with retries.
- Historical Analysis and Predict future performance: Analyze historical data for patterns and anomalies and create ML model for forecasting.
- Cloud integration into ESS part instead of CSV file
- Monitoring Dashboards: Create visual dashboards for data and system status.
- Load Balancing: Consider load balancing and distributed processing for handling increased load.
