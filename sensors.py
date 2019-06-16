from enum import Enum


class SensorType(Enum):
    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    TEMPERATURE_AND_HUMIDITY = 'temperature and humidity'


class Room(Enum):
    LIVING_ROOM = 'living room'
    BALCONY = 'balcony'
    KITCHEN = 'kitchen'
    MASTER_BEDROOM = 'master bedroom'
    BEDROOM = 'bedroom'
    EN_SUITE_BATHROOM = 'en-suite bathroom'
    BATHROOM = 'bathroom'
    HALL = 'hall'


LIVING_ROOM1 = {"sensor_id": 100, "name": "Living Room 1", "location": Room.LIVING_ROOM.value, "type": SensorType.TEMPERATURE_AND_HUMIDITY}

SENSORS = [LIVING_ROOM1]


def get_sensor_by_id(sensor_id):
    return filter(lambda sensor: sensor["sensor_id"] == sensor_id, SENSORS).__next__()