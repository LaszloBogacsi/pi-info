from pi_info.data.DeviceType import DeviceType
from pi_info.data.room import Room


class Device(object):

    def __init__(self, device_id: int, name: str, location: Room, type: DeviceType) -> None:
        self.id = device_id
        self.name = name
        self.location = location
        self.type = type

