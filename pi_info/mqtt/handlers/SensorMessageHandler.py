from pi_info.mqtt.handlers import AbstractMessageHandler
from pi_info.repository.sensor_data_repository import save_sensor_data


class SensorMessageHandler(AbstractMessageHandler):

    @property
    def topic(self):
        return "sensor/temperature"

    def parse_message(self, message):
        return {"timestamp": message['timestamp'],
                "values" : [
                    {"type": "temperature", "value":  message['temperature']},
                    {"type": "humidity", "value":  message['humidity']}
                ],
                "status": message['status'],
                "sensor_id": message['sensor_id']}

    def handle(self, parsed_message):
        save_sensor_data(parsed_message)

