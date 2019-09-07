class Schedule(object):
    def __init__(self, schedule_id, device_id, status, days, time):
        self.schedule_id = schedule_id
        self.device_id = device_id
        self.status = status
        self.days = days
        self.time = time


    def __repr__(self) -> str:
        return "time: {}, status: {}, days: {}, device_id: {}".format(
            self.time.isoformat(), self.status, self.days, self.device_id)
