# IoT Interoperability: Edge-based IoT platform

### Overview
The primary focus of this project is achieving technical interoperability, which considers the physical and software compatibility of the devices, 
including the protocols used to communicate between them. The present IoT marketplace ignores this issue, choosing to develop single com-
munication protocol solutions to specific scenarios. These niche systems are isolated, unable to interact with each other. 
This forms a plethora of independent IoT systems, often requiring their own gateway, resulting in the installation of a range of gateways
for different situations. <br/>

This project addresses these challenges and provides a prototype solution through the development of an edge-based IoT Hub. The design is a single gateway interface for a
variety of heterogeneous IoT devices, bridging between disparate communication protocols. 
All the connected devices implement home-automation functionality; however, the aim is to demonstrate an edge-based solution to IoT technical 
interoperability which can be adapted easily for other situations. 
As the IoT continues to expand with more connected devices rapidly, technical interoperability is critical for the scalability of this
technology. Hub-to-hub interoperability is also made possible through cloud integration, outlining the basis of an IoT Hub infrastructure. <br/><br/>

### IoT Hub
The edge-based IoT Hub developed for this project is a centralised gateway to a star network topology, communicating over a range of protocols
to a set of heterogeneous devices. These devices implement a IoT Hub compatible communication protocol, and all provide unique home-automation functionality.
The IoT Hub design is developed on a commercially-available Raspberry Pi 3B and predominately written in Python.
This device has been selected because it has interfacing capabilities with Python and C.
Also, it has a range of in-built communication protocol capabilities as well as available hardware expansions for other protocol implementations. 
The IoT Hub performs the communication interfacing, data management, cloud delivery and hosts a web server that runs a web interface.
Through the web interface, the user can read the status of all connected devices, control the actuators and read the sensor data. 
Select sensor data can also be saved to the user's personal Google Drive3, providing an external cloud storage. <br/><br/>

### End Devices
<i>LoPy4 PySense Multi-Sensorr<br/></i>
The LoPy4 is programmed in MicroPython to communicate through LoRa.This device transmits the temperature, humidity and ambient
light values from a interfaced Pysense multi-sensor board.When the device is not transmitting, it is configured to deep-sleep mode to
heavily reduce power consumption.<br/>

<i>NodeMCU Thermostat</i>
The NodeMCU simulates a wireless thermostat through an output LED to indicate if the thermostat is on or off. It is programmed in
Arduino code and contains an ESP8266WiFi module to communicate to the IoT Hub.The hub uses the most recent temperature readings
from the LoPy4 to determine the on-off state of the thermostat.<br/>

<i>Tradfri Light Bulb and Wall Plug</i>
Through CoAP overWiFi, commands are sent from the hub to the Tradfri Gateway to enable control of the connected Tradfri devices.
These devices consisted of a smart, dimmable light bulb and a wall plug.The Zigbee protocol is implemented for Tradfri device-gateway
connectivity.<br/>

<i>Raspberry Pi BLU Door Sensor Sub-System</i>
The door sensor sub-system is a Raspberry Pi 3B+ programmed in Python which communicates through Bluetooth Low-Energy (BLE).
The Pi is integrated with a PIR sensor and a reed switch to provide a proximity sensor and a open-closed state identifier for the door. <br/>

<i>Who's Home Scan</i>
The system determines who is home through a Bluetooth classic scan.This scan identifies the resident's mobile phones when they are
within the 30m Bluetooth proximity of the hub. If the device is found, the system assumes that specific resident is home. Mobile phones are
suitable for this function as they use Bluetooth requires minimal power and most people do not leave their house without them.<br/><br/>

### Application
The application, written in Python, generates a graphical user interface for the system.This interface displays system information, provides
actuator control, and enables access to cloud storage used for sensor data.The IoT Hub hosts the web server via a Flask application.This
application combines HTML, CSS and JavaScript files, providing the page template form,style and additional functionality,respectively.
<br/><br/>
The Google Cloud Platform was implemented for external storage, which saves the LoPy4 sensor data to the user's personal Google
Drive.This data is also stored locally on the hub to reduce data access speeds from the cloud.
