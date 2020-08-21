#!/usr/bin/env python

from pysense import Pysense         # Pysense development board library
from SI7006A20 import SI7006A20     # Humidity and temperature sensor library
from LTR329ALS01 import LTR329ALS01 # Light sensor library
from network import LoRa # LoRa library
#import machine # Machine library contains specific functions related to the hardware on a particular board
import socket  # Socket library
import time    # Time library
import pycom   # Pycom library

 #in memory that load libraries
py = Pysense()       # Create pysense object 
si = SI7006A20(py)   # Pass object to other libraries so they know how
lt = LTR329ALS01(py) # to connect through the board to the chip

# Initialise in LORA mode and set frequency 868.1MHz which is EU standard
lora = LoRa(mode=LoRa.LORA, frequency=868100000)   

# Create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

pycom.heartbeat(False)


print("Starting up Sensor...")
while True:
        # Set LED to Green
        pycom.rgbled(0x00FF00) 


        # Set blocking to send Data
        s.setblocking(True)

        # Display data from sensors to be sent
        print("Temperature: " + str(si.temperature())+ " deg C")
        print("Relative Humidity: " + str(si.humidity()) + " %RH")
        print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))
        
        # Define message contents
        id = str(1)                   # Set node identifier number
        temp  = str(si.temperature()) # Set temperature
        humid = str(si.humidity())    # Set humidity
        (blue, red) = lt.light()      # Find tuple containing blue and red 
        blueStr = str(blue)           # Set blue
        redStr = str(red)             # Set red

		# Construct message
        message = id + temp[:5] + humid[:5] + blueStr[:5] + redStr[:5]
		
		# Send message
        s.send(message)
		
        # Deep sleep mode 10 seconds
        py.setup_sleep(30)
        py.go_to_sleep(False)

