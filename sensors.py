from enum import Enum


class SensorType(Enum):
    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    TEMPERATURE_AND_HUMIDITY = 'temperature and humidity'


LIVING_ROOM1 = {"name": "Living Room 1", "location": "living room", "type": SensorType.TEMPERATURE_AND_HUMIDITY}

SENSORS = [LIVING_ROOM1]