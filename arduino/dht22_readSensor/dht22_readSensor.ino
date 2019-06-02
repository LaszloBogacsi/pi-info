#include "DHTesp.h"

DHTesp dht;
void setup() {
Serial.begin(115200);
  Serial.println();
  Serial.println("Status\tHumidity (%)\tTemperature (C)\tHeatIndex (C)");
  String thisBoard= ARDUINO_BOARD;
  Serial.println(thisBoard);

  dht.setup(4, DHTesp::DHT22); // Connect DHT sensor to GPIO 4 (D2)
}

void loop() {
delay(dht.getMinimumSamplingPeriod()); // 2000 ms

  float humidity = dht.getHumidity();
  float temperature = dht.getTemperature();
  String status = dht.getStatusString();
  String jsonMsg = "{\"status\":"+ status + ", \"temperature\":" + temperature + ", \"humidity\":" + humidity + "}";
  Serial.print(jsonMsg);
  Serial.print(dht.getStatusString());
  Serial.print("\t");
  Serial.print(humidity, 1);
  Serial.print("\t\t");
  Serial.print(temperature, 1);
  Serial.print("\t\t");
  Serial.println(dht.computeHeatIndex(temperature, humidity, false), 1);

}
