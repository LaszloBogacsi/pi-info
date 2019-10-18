#include "EspMQTTClient.h"
#include "DHTesp.h"
#include "secrets.h"

#define humidity_topic "sensor/humidity"
#define temperature_topic "sensor/temperature"

EspMQTTClient client(WIFI_SSID, WIFI_PASSWORD, MQTT_BROKER_IP, MQTT_USERNAME, MQTT_PASSWORD, "ESP8266_TEMP_Sensor2");

DHTesp dht;

void setup() {
  Serial.begin(74880);  
  client.enableDebuggingMessages(); // EspMQTTClient: Enable debugging messages sent to serial output
  // Start sensor
  dht.setup(4, DHTesp::DHT22); // Connect DHT sensor to GPIO 4 (D2)
}


long lastMsg = 0;
int sensor_id = 100;
long sleeptimeInSeconds = 1200; // 20 mins
void onConnectionEstablished() {
   float newTemp = dht.getTemperature();
   float newHum = dht.getHumidity();
   String status = dht.getStatusString();

   String jsonMsg = "{\"status\": \""+ status + "\", \"temperature\":" + newTemp + ", \"humidity\":" + newHum + ", \"sensor_id\":" + sensor_id + "}";
   Serial.println(jsonMsg);
   client.publish(temperature_topic, jsonMsg); // You can activate the retain flag by setting the third parameter to true
   Serial.println("About to go sleep for 20 mins...");
   delay(1000);
   ESP.deepSleep(sleeptimeInSeconds * 1000000); // D0 connected to RST
   delay(100);
}

void loop() {
  client.loop();
}
