from enum import Enum

from pi_info.data.DeviceType import DeviceType
from pi_info.data.room import Room


class Device(object):

    def __init__(self, device_id: int, name: str, location: Room, device_type: DeviceType) -> None:
        self.device_id = device_id
        self.name = name
        self.location = location
        self.device_type = device_type

    def as_dict(self):
        new_dict = {}
        for k, v in vars(self).items():
            new_dict[k] = self._conv(v)
        return new_dict

    @staticmethod
    def _conv(v):
        if isinstance(v, Enum):
            return v.value
        return v



