from enum import Enum


class Status(Enum):
    ON = 'ON'
    OFF = 'OFF'


class DeviceStatus(object):

    def __init__(self, device_id: int, status: Status) -> None:
        self.device_id = device_id
        self.status = status


