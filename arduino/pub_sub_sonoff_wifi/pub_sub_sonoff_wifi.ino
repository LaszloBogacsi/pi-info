#include "secrets.h"
#include "EspMQTTClient.h"
#include "ESP8266WiFi.h"
#include "ArduinoJson.h"

#define relay_topic "switch/relay"
#define relay_status_topic "switch/status"

EspMQTTClient client(WIFI_SSID, WIFI_PASSWORD, MQTT_BROKER_IP, MQTT_USERNAME, MQTT_PASSWORD, "Sonoff_5");

int gpio_13_led = 13;
int gpio_12_relay = 12;
String sonoffRelayId = "504";

void setup() {
  Serial.begin(74880);  
  
  pinMode(gpio_13_led, OUTPUT);
  digitalWrite(gpio_13_led, HIGH);
  
  pinMode(gpio_12_relay, OUTPUT);
  digitalWrite(gpio_12_relay, LOW);
  
  client.enableDebuggingMessages(); // EspMQTTClient: Enable debugging messages sent to serial output
}

void loop() {
  client.loop();
}

void onMessageCallback(const String &payload) {
    Serial.println(payload); 

    const size_t capacity = JSON_OBJECT_SIZE(2) + 30;
    DynamicJsonDocument doc(capacity);

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
  int blinkTime = 500;
  blink(5, blinkTime);

}

void turnOn(String relay_id){
    if (relay_id == sonoffRelayId) {
      digitalWrite(gpio_13_led, LOW);
      digitalWrite(gpio_12_relay, HIGH);
      String jsonMsg =  "{\"status\": \"ON\", \"device_id\":\"" + relay_id + "\"}";
      Serial.println(jsonMsg);
      client.publish(relay_status_topic, jsonMsg);
    }
}

void turnOff(String relay_id){
    if (relay_id == sonoffRelayId) {
      digitalWrite(gpio_13_led, HIGH);
      digitalWrite(gpio_12_relay, LOW);
      String jsonMsg = "{\"status\": \"OFF\", \"device_id\":\"" + relay_id + "\"}";
      Serial.println(jsonMsg);
      client.publish(relay_status_topic, jsonMsg); // You can activate the retain flag by setting the third parameter to true
    }
}

void blink(int repeats, int time) {
  for (int i = 0; i < repeats; i++) {
    digitalWrite(gpio_13_led, LOW);
    delay(time);
    digitalWrite(gpio_13_led, HIGH);
    delay(time);
  }
}
