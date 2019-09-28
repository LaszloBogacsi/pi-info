#include "secrets.h"
#include "EspMQTTClient.h"
#include "ESP8266WiFi.h"
#include "ArduinoJson.h"

#define relay_topic "switch/relay"
#define relay_status_topic "switch/status"

EspMQTTClient client(WIFI_SSID, WIFI_PASSWORD, MQTT_BROKER_IP, MQTT_USERNAME, MQTT_PASSWORD, "ESP8266_Relay_1_2");
StaticJsonDocument<200> doc;

int RELAY1 = 0; //D3; // GPIO0 
int RELAY2 = 2; //D4; // GPIO2
void setup() {
  Serial.begin(74880);  
 
  pinMode(RELAY1, OUTPUT);
  pinMode(RELAY2, OUTPUT);
  digitalWrite(RELAY1, HIGH);
  digitalWrite(RELAY2, HIGH);
  client.enableDebuggingMessages(); // EspMQTTClient: Enable debugging messages sent to serial output
}
bool isOn = false;
long lastExec;

void onMessageCallback(const String &payload) {
    // Deserialize the JSON document
  DeserializationError error = deserializeJson(doc, payload);
    // Test if parsing succeeds.
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.c_str());
    return;
  }
  const char* stat = doc["status"]; 
  const char* rel_id = doc["device_id"];
  Serial.println(stat);
  Serial.println(rel_id);
 Serial.println(payload); 
 if (String(stat) == "OFF") {
  turnOff(String(rel_id));
 }
 if (String(stat) == "ON") {
  turnOn(String(rel_id));
 }
 
}

void onConnectionEstablished() {
  Serial.println("connected..."); 
  client.subscribe(relay_topic, onMessageCallback);
}

void loop() {
  client.loop();
}

void turnOn(String relay_id){
    isOn = true;
    if (relay_id == "1") {
      digitalWrite(RELAY1, LOW);  
    }
    if (relay_id == "2") {
      digitalWrite(RELAY2, LOW);  
    }
    
    String jsonMsg =  "{\"status\": \"ON\", \"device_id\":\"" + relay_id + "\"}";
    Serial.println(jsonMsg);
    client.publish(relay_status_topic, jsonMsg); // You can activate the retain flag by setting the third parameter to true 
}

void turnOff(String relay_id){
    isOn = false;
    if (relay_id == "1") {
      digitalWrite(RELAY1, HIGH);  
    }
    if (relay_id == "2") {
      digitalWrite(RELAY2, HIGH);  
    }
     String jsonMsg = "{\"status\": \"OFF\", \"device_id\":\"" + relay_id + "\"}";
    Serial.println(jsonMsg);
    client.publish(relay_status_topic, jsonMsg); // You can activate the retain flag by setting the third parameter to true 
 
}
