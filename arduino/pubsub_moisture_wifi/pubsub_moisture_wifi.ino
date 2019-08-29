#include "EspMQTTClient.h"
#include "DHTesp.h"
#include "secrets.h"

#define moisture_topic "sensor/moisture"

EspMQTTClient client(WIFI_SSID, WIFI_PASSWORD, MQTT_BROKER_IP, MQTT_USERNAME, MQTT_PASSWORD, "ESP8266_MOISTURE_Sensor1");

void setup() {
  Serial.begin(74880);  
  client.enableDebuggingMessages(); // EspMQTTClient: Enable debugging messages sent to serial output
  // Start sensor
}


long lastMsg = 0;
int sensor_id = 200;
long sleeptimeInSeconds = 1200; // 20 mins
void onConnectionEstablished() {
   String newMoisture = "s";
   String jsonMsg = "{\"moisture\":" + newMoisture + ", \"sensor_id\":" + sensor_id + "}";
   Serial.println(jsonMsg);
   client.publish(moisture_topic, jsonMsg); // You can activate the retain flag by setting the third parameter to true
   Serial.println("About to go sleep for 20 mins...");
   delay(1000);
   ESP.deepSleep(sleeptimeInSeconds * 1000000); // D0 connected to RST
   delay(100);
}

void loop() {
  // client.loop();
  int sensorValue = 1024 - analogRead(A0);
  Serial.println(sensorValue);

  int outputValue = map(sensorValue, 0, 511, 0, 100);

  Serial.println(outputValue);
  delay(1000);
}
