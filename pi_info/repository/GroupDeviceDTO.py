from pi_info.repository.Device import Device
from pi_info.repository.Group import Group


class GroupDeviceDTO(object):

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
            return cls(entity.group_id, ",".join(map(str, entity.ids)), entity.name, True, "None", entity.delay_in_ms)
        if isinstance(entity, Device):
            return cls(entity.device_id, entity.device_id, entity.name, False, entity.location.value, 0)

