from enum import Enum

from pi_info.data.room import Room


class SensorType(Enum):
    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    TEMPERATURE_AND_HUMIDITY = 'temperature and humidity'



LIVING_ROOM1 = {"sensor_id": 100, "name": "Living Room 1", "location": Room.LIVING_ROOM, "type": SensorType.TEMPERATURE_AND_HUMIDITY, "sampling_rate_mins": 20}
MASTER_BEDROOM1 = {"sensor_id": 101, "name": "Master BedRoom 1", "location": Room.MASTER_BEDROOM, "type": SensorType.TEMPERATURE_AND_HUMIDITY, "sampling_rate_mins": 20}

SENSORS = [LIVING_ROOM1, MASTER_BEDROOM1]


def get_sensor_by_id(sensor_id):
    return filter(lambda sensor: sensor["sensor_id"] == sensor_id, SENSORS).__next__()


def get_sensors_by_room(room):
    return list(filter(lambda sensor: sensor["location"] == room, SENSORS))