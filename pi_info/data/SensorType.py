from enum import Enum


class SensorType(Enum):
    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    TEMPERATURE_AND_HUMIDITY = 'temperature and humidity'
    SOIL_MOISTURE = 'soil moisture'
