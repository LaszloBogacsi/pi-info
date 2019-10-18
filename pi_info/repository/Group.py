from pi_info.repository.DeviceStatus import Status


class Group(object):
    group_id: str
    status: Status
    name: str
    delay_in_ms: int
    ids: [int]

    def __init__(self, group_id: str, name: str, delay_in_ms: int, ids:[int], status: Status):
        self.status = status
        self.group_id = group_id
        self.name = name
        self.delay_in_ms = delay_in_ms
        self.ids = ids

