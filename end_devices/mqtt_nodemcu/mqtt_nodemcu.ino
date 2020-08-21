#include <ESP8266WiFi.h>           // ESP Library
#include <PubSubClient.h>          // MQTT Library

// MQTT COMMUNICATION SET-UP
const char* ssid = "VodafoneConnect28044518"; // WiFi service set identifier (SSID)
const char* password =  "8578j9vxkcbuffw";    // WiFi password
const char* mqttServer = "192.168.1.19";      // IP adress of Raspberry Pi
const int mqttPort = 1883;      // MQTT port number
const char* mqttUser = "";      // No MQTT username required to be defined
const char* mqttPassword = "";  // No MQTT password required to be defined

WiFiClient espClient;           // Initialise the ESP Client library
PubSubClient client(espClient); // Client library for MQTT communication

int thermostatState = 0; 


// Setup function called only once, at program startup
void setup() {

  // Passes 115200 baud rate to speed parameter between Serial monitor and device
  Serial.begin(115200);
  
  // Establish WiFi MQTT connection to Pi
  WiFi.begin(ssid, password); // Connect to WiFi network

  // Wait until WiFi connection established
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");

  
  client.setServer(mqttServer, mqttPort); // Set MQTT server details
  client.setCallback(callback);           // Sets the message callback function

  // Wait until connected to MQTT server on Raspberry Pi Hub
  while (!client.connected()) {
	  
    Serial.println("Connecting to MQTT...");

    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {
      Serial.println("connected");
    } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }	
  }

  pinMode(D5, OUTPUT);  // Set pinD5 as output, connected to thermostat represented
                        // by LED
}


// MQTT library code calls callback function when MQTT message on topic subscribed to received
void callback(char* topic, byte* payload, unsigned int length) {

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  char msg[length];
  
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
	  msg[i] = (char)payload[i];	     // Payload is state of thermostat
	  Serial.print((char)payload[i]);  // Print Message
  }

  thermostatState = atoi(msg);       // Received payload defines state of thermostat

}


// Loop function called consecutively
void loop() {

  client.subscribe("thermostat");  // Subscribe with topic 'esp8266'
  client.loop();                // Maintains connection and checks for incoming messages

  if(thermostatState == 0)
      digitalWrite(D5, LOW);    // Turn thermostat off
  if(thermostatState == 1)
      digitalWrite(D5, HIGH);   // Turn thermostat on

}
