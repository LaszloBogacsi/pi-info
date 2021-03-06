class Schedule(object):
    group_id: str
    schedule_id: int or None
    device_id: [int]
    status: str
    days: str
    time: str

    def __init__(self, schedule_id: int or None, group_id: str, device_id: [int], status: str, days: str, time: str):
        self.group_id = group_id
        self.schedule_id = schedule_id
        self.device_id = device_id
        self.status = status
        self.days = days
        self.time = time

    def __repr__(self) -> str:
        return "time: {}, status: {}, days: {}, device_id: {}".format(
            self.time, self.status, self.days, self.device_id)
