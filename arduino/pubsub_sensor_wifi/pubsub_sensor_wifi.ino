#include "EspMQTTClient.h"
#include "DHTesp.h"
#include "secrets.h"

#define humidity_topic "sensor/humidity"
#define temperature_topic "sensor/temperature"

EspMQTTClient client(WIFI_SSID, WIFI_PASSWORD, MQTT_BROKER_IP, MQTT_USERNAME, MQTT_PASSWORD, "ESP8266_TEMP_Sensor");

DHTesp dht;

void setup() {
  Serial.begin(115200);  
  client.enableDebuggingMessages(); // EspMQTTClient: Enable debugging messages sent to serial output
  // Start sensor
  dht.setup(4, DHTesp::DHT22); // Connect DHT sensor to GPIO 4 (D2)
}


long lastMsg = 0;

void onConnectionEstablished() {
 
   float newTemp = dht.getTemperature();
   float newHum = dht.getHumidity();
   String status = dht.getStatusString();

   String jsonMsg = "{\"status\": \""+ status + "\", \"temperature\":" + newTemp + ", \"humidity\":" + newHum + "}";
   Serial.println(jsonMsg);
   client.publish(temperature_topic, jsonMsg); // You can activate the retain flag by setting the third parameter to true
  
}
void loop() {
  client.loop();
  long now = millis();
  if (client.isConnected() && (now - lastMsg > 3000))  {
    lastMsg = now;
     float newTemp = dht.getTemperature();
     float newHum = dht.getHumidity();
     String status = dht.getStatusString();
     String jsonMsg = "{\"status\": \""+ status + "\", \"temperature\":" + newTemp + ", \"humidity\":" + newHum + "}";
     client.publish(temperature_topic, jsonMsg); // You can activate the retain flag by setting the third parameter to true
  }
  
}
