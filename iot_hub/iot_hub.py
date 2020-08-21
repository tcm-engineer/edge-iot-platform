#!/usr/bin/env python3

# LIBRARIES
# Flask framework library
from flask import Flask, flash, render_template, redirect, url_for, request, Response

# Pytradfri library
from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError
from pytradfri.util import load_json, save_json

# Google Drive cloud storage library
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Display charts library
import matplotlib.pyplot as plt
import pandas as pd

import bluepy.btle as btle # Bluetooth Low Energy library

import uuid          # Universal Unique Identifier library
import argparse      # Arguement parser library
import json          # JSON library
import paho.mqtt.client as mqtt # MQTT library
import time          # Time library
import csv           # CSV library
import array         # Array library
import bluetooth     # Bluetooth library
import threading     # Threading library


# Create instance of Flask class for web application
app = Flask(__name__)

# CLASSES
# LoRa sensor node class
class lora_node:
    
    # Initialise lora_node class variables function
    def __init__(self, date, time, identity, temp, humidity, blue, red):
        self.set_date(date)          # Current date variable
        self.set_time(time)          # Current time variable
        self.set_identity(identity)  # Identity number of node variable
        self.set_temp(temp)          # Temperature in °C variable
        self.set_humidity(humidity)  # Humidity in %RH variable
        self.set_blue(blue)          # Colour blue in lux variable
        self.set_red(red)            # Colour red in lux variable
    
    def get_date(self):              # Get current date variable function
        return self.__date
    def get_time(self):              # Get current time variable function
        return self.__time
    def get_identity(self):          # Get identity variable function
        return self.__identity
    def get_temp(self):              # Get temperature variable function
        return self.__temp          
    def get_humidity(self):          # Get humidity variable function
        return self.__humidity      
    def get_blue(self):              # Get blue variable function
        return self.__blue          
    def get_red(self):               # Get red variable function
        return self.__red

    def set_date(self,date):         # Set date variable function
        self.__idate = date
    def set_time(self,time):         # Set time variable function
        self.__time = time
    def set_identity(self,identity): # Set identity variable function
        self.__identity = identity
    def set_temp(self,temp):         # Set temperature variable function
        self.__temp = temp
    def set_humidity(self,humidity): # Set humidity variable function
        self.__humidity = humidity
    def set_blue(self,blue):         # Set blue variable function
        self.__blue = blue
    def set_red(self,red):           # Set red variable function
        self.__red = red

# Bluetooth classic MAC address scan class
class bt_devices:
    
    # Initialise bt_devices class variables function
    def __init__(self, bt_error, bt_add):
        self.set_bt_error(bt_error)  # Bluetooth classic MAC address error variable
        self.set_bt_add(bt_add)      # Add Bluetooth classic MAC address variable

    def get_bt_error(self):          # Get Bluetooth MAC address error variable function
        return self.__bt_error
    def get_bt_add(self):            # Get add Bluetooth MAC address variable function
        return self.__bt_add
        
    def set_bt_error(self,bt_error): # Set Bluetooth MAC address error variable function
        self.__bt_error = bt_error
    def set_bt_add(self,bt_add):     # Set add Bluetooth MAC address variable function
        self.__bt_add = bt_add

# ESP8266 NodeMCU thermostat class
class esp_thermostat:
    
    # Initialise esp_thermostat class variables function
    def __init__(self, esp_toggle, temp_mode, temp_input):
        self.set_esp_toggle(esp_toggle)  # ESP button toggle variable
        self.set_temp_mode(temp_mode)    # Thermostat temperature mode variable 
        self.set_temp_input(temp_input)  # Thermostat temperature input variable

    def get_esp_toggle(self):            # Get ESP button toggle variable function
        return self.__esp_toggle
    def get_temp_mode(self):             # Get thermostat temperature mode variable function
        return self.__temp_mode
    def get_temp_input(self):            # Get thermostat temperature input variable function
        return self.__temp_input
        
    def set_esp_toggle(self,esp_toggle): # Set ESP button toggle variable function
        self.__esp_toggle = esp_toggle
    def set_temp_mode(self,temp_mode):   # Set thermostat temperature mode variable function
        self.__temp_mode = temp_mode
    def set_temp_input(self,temp_input): # Set thermostat temperature input variable function
        self.__temp_input = temp_input

# Tradfri Zigbee light bulb class
class zigbee_devices:
    
    # Initialise zigbee_bulb class variables function
    def __init__(self, light_toggle, socket_toggle, slider): 
        self.set_light_toggle(light_toggle)    # Light toggle variable
        self.set_socket_toggle(socket_toggle)  # Light toggle variable
        self.set_slider(slider)                # Dimmer slider variable

    def get_light_toggle(self):                # Get light toggle variable function
        return self.__light_toggle
    def get_socket_toggle(self):               # Get light toggle variable function
        return self.__socket_toggle
    def get_slider(self):                      # Get dimmer slider variable function   
        return self.__slider
        
    def set_light_toggle(self,light_toggle):   # Set light toggle variable function
        self.__light_toggle = light_toggle
    def set_socket_toggle(self,socket_toggle): # Set light toggle variable function
        self.__socket_toggle = socket_toggle
    def set_slider(self,slider):               # Set dimmer slider variable function
        self.__slider = slider

# Display plot of temperature and humidity class
class display_chart:
    
    # Initialise display_chart class variables function
    def __init__(self, display_chart, temp_filename, humidity_filename):
        self.set_display_chart(display_chart)          # Display chart toggle variable
        self.set_temp_filename(temp_filename)          # Temperature figure file path variable
        self.set_humidity_filename(humidity_filename)  # Humidity figure file path variable
        
    def get_display_chart(self):                       # Get display chart toggle variable function
        return self.__display_chart
    def get_temp_filename(self):                       # Get temperature figure file path variable function
        return self.__temp_filename
    def get_humidity_filename(self):                   # Get humidity figure file path variable function
        return self.__humidity_filename                
        
    def set_display_chart(self,display_chart):         # Set display chart toggle variable function
        self.__display_chart = display_chart
    def set_temp_filename(self,temp_filename):         # Set temperature figure file path variable function
        self.__temp_filename = temp_filename
    def set_humidity_filename(self,humidity_filename): # Set humidity figure file path variable function
        self.__humidity_filename = humidity_filename       

# Bluetooth Low Energy Raspberry Pi sensor class
class ble_pi:
    
    # Initialise ble_pi class variables function
    def __init__(self, pir, reed_switch):
        self.set_pir(pir)                  # Passive Infrared sensor (PIR) variable
        self.set_reed_switch(reed_switch)  # Reed switch variable

    def get_pir(self):                     # Set PIR variable function
        return self.__pir
    def get_reed_switch(self):             # Set reed switch variable function
        return self.__reed_switch
        
    def set_pir(self,pir):                 # Set PIR variable function
        self.__pir = pir
    def set_reed_switch(self,reed_switch): # Set reed switch variable function
        self.__reed_switch = reed_switch
        
# Read BLE delegate to determine if notifying
class ReadDelegate(btle.DefaultDelegate):
    def handleNotification(self, cHandle, data):
        print(data)


# MQTT Setup with topic 'thermostat'
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("thermostat")
    

# TRADFRI Setup
def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',
                        '-c',
                        required=True,
                        type=argparse.FileType('a+'),
                        help="Path to config file")
    args = parser.parse_args()
    return args

def load_identity(config_file):
    config = json.load(config_file)
    return config['identity'], config['psk']


def save_identity(config_file, identity, psk):
    conf = {'identity': identity, 'psk': psk}
    config_file.seek(0)
    json.dump(conf, config_file, indent=2)


# ROUTING
# Homepage
@app.route('/')
def index():
    # Display template "index.html"
    return render_template("index.html")

# About Page
@app.route('/about')
def about():
    # Display template "about.html"
    return render_template("about.html")


# Sensors Page
@app.route('/sensors')
def sensors():
    
    bt_names = [""] # Array to contain all known, discovered Bluetooth Classic devices
    bt_first = 0    # Variable to idenify first element of 'bt_names'
    
    # Check if each entry of bluetooth MAC address lookup file is within range of hub
    with open('bt_mac.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file)   # Return reader object which will iterate over lines in 'bt_mac.csv'
        for row in csv_reader:              # Loop through CSV file
            # If Bluetooth Classic MAC address discovered equates to MAC address in 'bt_mac.csv' add identifier to 'bt_names'
            if(bluetooth.lookup_name(row[0], timeout=0) != None): 
                if(bt_first == 0):
                    bt_names[0] = row[1]
                else:
                    bt_names.append(row[1])
                bt_first = bt_first + 1   
    
    # Read BLE service from door system
    p = btle.Peripheral("B8:27:EB:88:2E:55","public") # Connect to BLE peripheral with public MAC address
    p.withDelegate(ReadDelegate())                    # Read delegate to indicate if Door System is notifying
      
    s = p.getServiceByUUID("00000001-710e-4a5b-8d75-3e5b444bc3cf") # Request thermostat service by entering the UUID
    c = s.getCharacteristics()[0]                                  # Read the characteristics from this UUID
    
    ble1.set_pir(str(c.read())[2])         # Read PIR characteristic
    ble1.set_reed_switch(str(c.read())[3]) # Read reed switch characteristic
    attempt = 0
    p.disconnect()

  
    # Display template "sensors.html" and pass HTML variables
    return render_template("sensors.html", identity = lora1.get_identity(), temp = lora1.get_temp(), humidity = lora1.get_humidity(), blue = lora1.get_blue(), red = lora1.get_red(), bt_names = bt_names, bt_error = bt1.get_bt_error(), bt_add = bt1.get_bt_add(), display_chart = disChart.get_display_chart(), temp_filename = disChart.get_temp_filename(),humidity_filename = disChart.get_humidity_filename(), pi_pir = ble1.get_pir(), pi_reed_switch = ble1.get_reed_switch())
   
                
# Cloud File Storage Button Press
@app.route('/cloud_storage')
def cloud_storage():
    gauth = GoogleAuth()       
    gauth.LocalWebserverAuth() # Start browser and request authentication
    drive = GoogleDrive(gauth) # Creat Google Drive object for file handling

    # View cloud_storage folder (id '****') in Google Drive
    fileList = drive.ListFile({'q':"'****' in parents and trashed=false"}).GetList()
    for file in fileList:
        if(file['title'] == "data.csv"):                    # Find ID of file searching for
            fileID = file['id']
            
    file1 = drive.CreateFile({'id': fileID}) # Initialise file with the discovered ID
    file1.Delete()                           # Delete file, .UnTrash(), .Delete()
    
    # Initialise data.csv file
    file2 = drive.CreateFile({"mimeType": "text/csv", 'title': 'data.csv', "parents": [{"kind": "drive#fileLink", "id": "*****"}]})  
    file2.SetContentFile('data.csv')         # Open data.csv file and set content to the GoogleDriveFile object
    file2.Upload()                           # Upload file
    
    return sensors()


# Bluetooth Classic Scan Button Press
@app.route('/bt_button')
def bt_button():
    
    bt1.set_bt_error(0)               # Reset Bluetooth Classic scan variable to 0
    bt1.set_bt_add(~bt1.get_bt_add()) # Toggle Bluetooth Classic scan button variable 
    
    return sensors()


# Bluetooth Classic Enter New Device Button Press
@app.route('/bt_enter', methods=['POST'])
def bt_enter():
    
    bt1.set_bt_error(0)               # Reset Bluetooth Classic scan variable to 0
    
    bt_mac = request.form['bt_mac']   # Read Bluetooth Classic MAC address entered by user
    bt_name = request.form['bt_name'] # Read device name identifier entered by user
    bt_row = [bt_mac, bt_name]        # Place values in row to be added to 'bt_mac.csv'
    
    # Read 'bt_mac.csv' to determine if user entry is valid
    with open('bt_mac.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if(bt_mac == row[0]):   # ERROR MAC address already entered
                bt1.set_bt_error(1)
            if(bt_name == row[1]):  # ERROR NAME identifier already entered
                bt1.set_bt_error(2)
            if(bt_mac == row[0] and bt_name == row[1]): # ERROR MAC address AND NAME identifier already entered
                bt1.set_bt_error(3)
    
    # Append 'bt_mac.csv' with user entry if no entry errors
    if(bt1.get_bt_error() == 0):
        with open('bt_mac.csv', 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(bt_row)

    return sensors()


# Display Sensor Charts Button Pressed
@app.route('/display_charts')
def display_charts():
    
    if(disChart.get_display_chart() == 0):
        dataframe = pd.read_csv("data.csv") # Use pandas to read CSV file
        
        seconds = int(time.time())  # Seconds since epoch rounded to nearest integer
        
        x = dataframe.Time          # Pandas function to pass 'Time' column of data.csv
        
        # Temperature Graph
        y = dataframe.Temperature   # Pandas function to pass 'Temperature' column of data.csv
        
        plt.scatter(x, y, color="red") # Matplotlib plots scatter graph of 'Time' and 'Temperature'
        plt.gcf().autofmt_xdate()      # Funtion styles 'Time' axis
        plt.plot(x, y, color="red")    # Matplotlib plots graph

        plt.title('Temperature Chart', fontsize=20, color="dimgray") # Label graph title
        plt.xlabel('Time', fontsize=17)                              # Label x-axis
        plt.ylabel('Temperature (°C)', fontsize=17)                  # Label y-axis       
        
        disChart.set_temp_filename("static/images/temp_"+str(seconds)+".png")  # Image name contains time to update image name
                                                                               # Otherwise browser cache and image will not be update
        
        plt.savefig(disChart.get_temp_filename(), format="png", facecolor="#E0FFFF", edgecolor="#E0FFFF")  # Save plot as image, .png file
        disChart.set_temp_filename("../"+disChart.get_temp_filename())                                                   # Save image file name to pass to html
        plt.close()

        # Humidity Graph        
        y = dataframe.Humidity      # Pandas function to pass 'Humidity' column of data.csv
           
        plt.scatter(x, y, color="red") # Matplotlib plots scatter graph of 'Time' and 'Humidity'
        plt.gcf().autofmt_xdate()      # Funtion styles 'Time' axis
        plt.plot(x, y, color="red")    # Matplotlib plots graph

        plt.title('Humidity Chart', fontsize=20, color="dimgray") # Label graph title
        plt.xlabel('Time', fontsize=17)                           # Label x-axis
        plt.ylabel('Humidity (RH%)', fontsize=17)                   # Label y-axis
        
        disChart.set_humidity_filename("static/images/humidity_"+str(seconds)+".png")  # Image name contains time to update image name
                                                                                       # Otherwise browser cache and image will not be update
        
        plt.savefig(disChart.get_humidity_filename(), format="png", facecolor="#E0FFFF", edgecolor="#E0FFFF")  # Save plot as image, .png file
        disChart.set_humidity_filename("../"+disChart.get_humidity_filename())                                               # Save image file name to pass to html
        plt.close()
                
    disChart.set_display_chart(~disChart.get_display_chart())  # Toggle display chart variable to indicate button pressed
    return sensors()


# Actuators Page
@app.route('/actuators')
def actuators():
    
    # Display template "actuators.html" and pass HTML variables   
    return render_template("actuators.html", esp_toggle = esp1.get_esp_toggle(),  light_toggle = zig1.get_light_toggle(), socket_toggle = zig1.get_socket_toggle(), slider = zig1.get_slider(), temp_mode = esp1.get_temp_mode(), temp_input = esp1.get_temp_input())


# Tradfri Light Bulb Button Toggle Pressed
@app.route('/lightToggle')
def lightToggle():

    args = parse_args()
    args.config.seek(0)
    
    try:
        identity, psk = load_identity(args.config)
        api_factory = APIFactory(host="***.***.**.**", psk_id="***************", psk="********")
    except (KeyError, json.JSONDecodeError) as e:
        print("Generating new identity & PSK")
        identity = uuid.uuid4().hex
        api_factory = APIFactory(host="***.***.**.**", psk_id=identity)
        psk = api_factory.generate_psk("********")
        save_identity(args.config, identity, psk)

    api = api_factory.request   # Request access to Tradfri gateway
    
    gateway = Gateway()         # Create Gateway object

    device_commands = api(gateway.get_devices())                # Request identity of connected devices commands
    devices = api(device_commands)                              # Request number of connected devices
    lights  = [dev for dev in devices if dev.has_light_control] # Identify all connected devices that are light bulbs
    
    if(zig1.get_light_toggle() == 0):               # Toggle bulb on
        zig1.set_slider("254")                      # Change slider bulb button value to maximum
        api(lights[0].light_control.set_dimmer(254))# Set bulb to maximum brightness
    else:                                           # Toggle bulb off                                                  
        zig1.set_slider("0")                        # Change slider bulb button value to minimum
        api(lights[0].light_control.set_dimmer(0))  # Set bulb to minimum brightness
    zig1.set_light_toggle(~zig1.get_light_toggle()) # Toggle light bulb on-off state

    return actuators()

# Tradfri Light Bulb Dimmer Slider
@app.route('/lightDimmer', methods=["POST"])
def lightDimmer():

    args = parse_args()
    args.config.seek(0)

    try:
        identity, psk = load_identity(args.config)
        api_factory = APIFactory(host="***.***.**.**", psk_id=identity, psk=psk)
    except (KeyError, json.JSONDecodeError) as e:
        print("Generating new identity & PSK")
        identity = uuid.uuid4().hex
        api_factory = APIFactory(host="***.***.**.**", psk_id=identity)
        psk = api_factory.generate_psk("********")
        save_identity(args.config, identity, psk)

    api = api_factory.request   # Request access to Tradfri gateway
    
    gateway = Gateway()         # Create Gateway object

    device_commands = api(gateway.get_devices())                # Request identity of connected devices commands
    devices = api(device_commands)                              # Request number of connected devices
    lights  = [dev for dev in devices if dev.has_light_control] # Identify all connected devices that are light bulbs
    
    zig1.set_slider(request.form["slider"])     # HTTP Method 'POST' recieves user input brightness value from slider button

    api(lights[0].light_control.set_dimmer(int(zig1.get_slider()))) # Set bulb to slider button brightness
    
    # When brightness entered is 0 turn bulb and bulb button off    
    if((zig1.get_slider() == 0 or zig1.get_slider() == "0") and (zig1.get_light_toggle() != 0)):
        zig1.set_light_toggle(~zig1.get_light_toggle()) # Toggle light bulb on-off state
        
    # When brightness entered greater than 0 turn bulb and bulb button on  
    if((zig1.get_slider() != 0 and zig1.get_slider() != "0") and (zig1.get_light_toggle() == 0)):
        zig1.set_light_toggle(~zig1.get_light_toggle()) # Toggle light bulb on-off state

    return actuators()

@app.route('/socketToggle')
def socketToggle():

    args = parse_args()
    args.config.seek(0)
    
    try:
        identity, psk = load_identity(args.config)
        api_factory = APIFactory(host="***.***.**.**", psk_id="***************", psk="********")
    except (KeyError, json.JSONDecodeError) as e:
        print("Generating new identity & PSK")
        identity = uuid.uuid4().hex
        api_factory = APIFactory(host="***.***.**.**", psk_id=identity)
        psk = api_factory.generate_psk("iwkCf2due4dKzDte")
        save_identity(args.config, identity, psk)

    api = api_factory.request   # Request access to Tradfri gateway
    
    gateway = Gateway()         # Create Gateway object

    device_commands = api(gateway.get_devices())                 # Request identity of connected devices commands
    devices = api(device_commands)                               # Request number of connected devices
    socket  = [dev for dev in devices if dev.has_socket_control] # Identify all connected devices that are wall plugs
    

    if(zig1.get_socket_toggle() == 0):
        api(socket[0].socket_control.set_state(1)) # Turn wall plug on
    else:
        api(socket[0].socket_control.set_state(0)) # Turn wall plug off
    zig1.set_socket_toggle(~zig1.get_socket_toggle()) # Toggle wall plug on-off state
  
    return actuators()
    
    
# Thermostat Temperature Mode Button Pressed
@app.route('/temperatureMode')
def temperatureMode():
    esp1.set_temp_mode(~esp1.get_temp_mode()) # Inverted temperature mode
    return actuators()

# Thermostat Automatic Mode Target Temperature User Input
@app.route('/temperatureInput', methods=["POST"])
def temperatureInput(): 
    esp1.set_temp_input(request.form['temp_input']) # Read user input from HTML file
    return actuators()
    
    
# NodeMCU ESP2866 Thermostat Button Toggle Pressed
@app.route('/espLEDToggle')
def espLEDToggle():
    
    if(esp1.get_temp_mode() == 0):           # If set to manual temperature mode
        if(esp1.get_esp_toggle() == 0):
            client.publish("thermostat","1") # Transmit instrustion to NodeMCU to turns on thermostat (LED)
        else:
            client.publish("thermostat","0") # Transmit instrustion to NodeMCU to turns off thermostat (LED)
            
        esp1.set_esp_toggle(~esp1.get_esp_toggle())  # Inverts esp toggle to indicate application button press
    return actuators()




# THREAD FUNCTIONS
# ESP2688 thermostat temperature control
def tempControl():

    while True:    
        # If thermostat set to automatic temperature mode
        if(esp1.get_temp_mode() != 0):    
            # If temperature is 10% less than  user selected temperature
            if(float(str(esp1.get_temp_input())) > float(lora1.get_temp())):
                client.publish("thermostat","1")                 # Send messgae to ESP, turning on thermostat         
                    
            # If temperature is 10% greater than user selected temperature
            elif(float(str(esp1.get_temp_input())) < float(lora1.get_temp())):
                client.publish("thermostat","0")                 # Send messgae to ESP, turning off thermostat
            time.sleep(5)

# Display data from LoRa node
def sensorDisplay():

    while True: 
        # Open and read data.csv file
        with open('data.csv','r') as csv_file:
            csv_reader = csv.reader(csv_file)        
            for line in csv_reader:
                lora1.set_date(line[0])     # Read date
                lora1.set_time(line[1])     # Read time
                lora1.set_identity(line[2]) # Read identity
                lora1.set_temp(line[3])     # Read temperature
                lora1.set_humidity(line[4]) # Read humidity
                lora1.set_blue(line[5])     # Read blue
                lora1.set_red(line[6])      # Read red

    

if __name__ == "__main__":
    
    lora1 = lora_node(0,0,0,0,0,0,0)    # Create LoRa node object
    bt1 = bt_devices(0,0)               # Create Bluetooth classic device object
    esp1 = esp_thermostat(0,0,0)        # Create NodeMCU thermostat object
    zig1 = zigbee_devices(0,0,0)        # Create zigbee devices object
    ble1 = ble_pi("0","0")              # Create BLE door system object
    disChart = display_chart(0,"a","a") # Create display charts object
    
    # Create MQTT client instance connected to local host IP
    client=mqtt.Client()                     # Create MQTT instance
    client.on_connect = on_connect           # Bind call back function
    client.connect('**.***.*.**', 1883, 60)  # Local host IP of IoT Hub, port 1883, keepalive 60
    client.loop_start()                      # Maintain network traffic flow with broker

    client.publish("thermostat","0")  # Turn thermostat off
    
    # Declare temperature control function as a thread
    thd1 = threading.Thread(target=tempControl,
                            args=())
    # Declare LoRa sensor data function as a thread
    thd2 = threading.Thread(target=sensorDisplay,
                            args=())                           
    thd1.start() # Start temperature control thread 
    thd2.start() # Start LoRa sensor data thread
    
    app.run(debug=True)  # Run Flask application on the local development server
