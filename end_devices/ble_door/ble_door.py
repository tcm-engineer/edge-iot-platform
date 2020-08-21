#!/usr/bin/python3

import dbus              # D-Bus message bus system library
import RPi.GPIO as GPIO  # Raspberry Pi GPIO library
import time              # Time library

from advertisement import Advertisement 
from service import Application, Service, Characteristic, Descriptor

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"   # Gatt characteristic interface access
NOTIFY_TIMEOUT = 5000                               # Notification timeout constant

# Advertisement class
class PiAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("RaspberryPi")
        self.include_tx_power = True

# Service class
class PiService(Service):
    PI_SERVICE_UUID = "00000001-710e-4a5b-8d75-3e5b444bc3cf"    # Service UUID

    def __init__(self, index):
        Service.__init__(self, index, self.PI_SERVICE_UUID, True)
        self.add_characteristic(PiCharacteristic(self))


# Characteristic class
class PiCharacteristic(Characteristic):
    PI_CHARACTERISTIC_UUID = "00000002-710e-4a5b-8d75-3e5b444bc3cf"    # Characteristic UUID

    def __init__(self, service):
        self.notifying = False      # Initalise notification off

        Characteristic.__init__(
                self, self.PI_CHARACTERISTIC_UUID,
                ["notify", "read"], service)


    def get_pi(self):
        pirPin = 18     # Input pin from PIR sensor
        reedPin = 17    # Input pin from reed switch
        
        value = []      # Characteristic list
        
        # Set first character of characteristic to 1 if PIR triggered, otherwise 0
        if GPIO.input(pirPin):
            value.append(dbus.Byte("1".encode()))
        else:
            value.append(dbus.Byte("0".encode()))
 
         # Set second character of characteristic to 1 if reed switch triggered, otherwise 0           
        if GPIO.input(reedPin):
            value.append(dbus.Byte("1".encode()))
        else:
            value.append(dbus.Byte("0".encode()))

        return value
    
    # Determine if characteristics change value
    def set_pi_callback(self):
        if self.notifying:
            value = self.get_pi()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    # Start notification
    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_pi()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_pi_callback)

    # End notification
    def StopNotify(self):
        self.notifying = False

    # Read characteristics
    def ReadValue(self, options):
        value = self.get_pi()

        return value

# Pin Setup
pirPin = 18
reedPin = 17

GPIO.setmode(GPIO.BCM)       # Broadcom pin-numbering scheme
GPIO.setup(pirPin, GPIO.IN)  # PIR pin as input
GPIO.setup(reedPin, GPIO.IN) # Reed switch pin as input       
                
# Define BLE service application
app = Application()
app.add_service(PiService(0))
app.register()

# Define and register BLE advertisement
adv = PiAdvertisement(0)
adv.register()

try:
    app.run()   # Start application
except KeyboardInterrupt:
    app.quit()  # End application
