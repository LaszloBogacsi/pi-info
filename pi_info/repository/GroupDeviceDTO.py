from pi_info.repository.Device import Device
from pi_info.repository.Group import Group


class GroupDeviceDTO(object):
    group_id: str
    device_id: str
    name: str
    is_group: bool
    location: str
    delay: int

    def __init__(self, group_id, device_id, name, is_group, location, delay) -> None:
        self.group_id = group_id
        self.device_id = device_id
        self.name = name
        self.is_group = is_group
        self.location = location
        self.delay = delay

    @classmethod
    def convert_from(cls, entity):
        if isinstance(entity, Group):
            return cls(entity.group_id, ",".join(map(str, entity.ids)), entity.name.lower(), True, "None", entity.delay_in_ms)
        if isinstance(entity, Device):
            return cls(str(entity.device_id), str(entity.device_id), entity.name.lower(), False, entity.location.value.lower(), 0)

