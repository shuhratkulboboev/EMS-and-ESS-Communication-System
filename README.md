# EMS-and-ESS-Communication-System
## Overview
This project implements a simplified model of communication between an Energy Management System (EMS) and an Energy Storage System (ESS), using MQTT for messaging and SQLite for data storage. The task simulates an industrial energy storage unit being controlled by commands issued from a central EMS. The main goal is to ensure that the EMS can monitor and control the ESS in real-time while handling possible connectivity issues.

## Architecture

The system is comprised of four primary components:

EMS (Energy Management System): Operates in the cloud, reads target power values, and sends them to the ESS every 5 seconds via MQTT. It also stores ESS data in an SQLite database.
ESS (Energy Storage System): Simulates an energy storage unit, generating mock values for temperature, state of charge, and actual power. Sends this data to EMS every 5 seconds.
MQTT Broker: Facilitates communication between the EMS and ESS.
SQLite Database: Stores data received from the ESS.
The communication between EMS and ESS occurs via MQTT, with the SQLite database storing all the incoming data from ESS for historical analysis.

## Components 
### Energy Management System (EMS)
- **Function:** Reads power_target from a predefined file and sends it to ESS every 5 seconds.
- **timestamp:** Time of sending.
- **power_target:** The target power value to be applied.
- **Database:** Stores data received from ESS, including power_actual, temperature, and state_of_charge, with a timestamp.
### Energy Storage System (ESS)
- **Function:** Simulates an energy storage unit. Receives power_target from EMS, sends back power_actual (same as power_target for simplicity) and mock values for temperature and state_of_charge.
- **timestamp:** Time of sending.
- **power_actual:** Same as power_target.
- **temperature:** Simulated value.
- **state_of_charge:** Simulated value.
Fallback Mechanism: In case of a connection issue, the ESS stores data locally and sends it to EMS once the connection is restored.
### MQTT Broker
Facilitates the message exchange between EMS and ESS.
- **Uses channels to transmit data:**
- **ems/power_target:** For EMS to send power target to ESS.
-**ess/data:** For ESS to send back data to EMS.
### SQLite Database
Stores the following data from ESS:
- **id**
- **timestamp**
- **power_actual**
- **temperature**
- **state_of_charge**
## Setup & Installation
### Clone the repository:
   ```bash```
   git clone https://github.com/yourusername/ems-ess-mqtt.git
   cd ems-ess-mqtt
### Create a virtual environment and activate it:
  ```bash```
   python3 -m venv venv
   source venv/bin/activate
### Install the required dependencies:
```bash```
   pip install -r requirements.txt
### Run the MQTT broker (e.g., Mosquitto) locally:
 ```bash```
   mosquitto
### Start the EMS:
   python ems.py
### Start the ESS:
   python ess.py


