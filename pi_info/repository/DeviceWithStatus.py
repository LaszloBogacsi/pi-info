from pi_info.data.DeviceType import DeviceType
from pi_info.data.room import Room
from pi_info.repository.Device import Device
from pi_info.repository.DeviceStatus import Status


class DeviceWithStatus(Device):

    def __init__(self, device_id: int, name: str, location: Room, device_type: DeviceType, status: Status) -> None:
        super().__init__(device_id, name, location, device_type)
        self.status = status

    def as_dict(self):
        return super().as_dict()


