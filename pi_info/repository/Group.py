class Group(object):
    def __init__(self, group_id: int or None, name: str, delay_in_ms: int, ids:[int]):
        self.group_id = group_id
        self.name = name
        self.delay_in_ms = delay_in_ms
        self.ids = ids
