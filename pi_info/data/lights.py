from enum import Enum

from pi_info.data.room import Room


class LightType(Enum):
    TABLE_LAMP = 'table_lamp'


class LightStatus(Enum):
    ON = 'ON'
    OFF = 'OFF'


light1 = {"light_id": 1, "name": "Light 1", "location": Room.LIVING_ROOM, "type": LightType.TABLE_LAMP, "current_status": LightStatus.OFF}
light2 = {"light_id": 2, "name": "Light 2", "location": Room.LIVING_ROOM, "type": LightType.TABLE_LAMP, "current_status": LightStatus.OFF}
LIGHTS = [light1, light2]


def get_light_by_id(light_id):
    return filter(lambda light: light["light_id"] == light_id, LIGHTS).__next__()


def get_lights_by_room(room):
    return list(filter(lambda light: light["location"] == room, LIGHTS))