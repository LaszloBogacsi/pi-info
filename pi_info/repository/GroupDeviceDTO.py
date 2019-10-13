class GroupDeviceDTO:

    def __init__(self, group_id, device_id, name, is_group, location, delay) -> None:
        self.group_id = group_id
        self.device_id = device_id
        self.name = name
        self.is_group = is_group
        self.location = location
        self.delay = delay