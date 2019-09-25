class Task():
    def __init__(self, id: str, time: str, weekdays: str, delay_in_sec: int, action) -> None:
        self.delay = delay_in_sec
        self.weekdays = weekdays
        self.run = action
        self.id = id
        self.time = time
        if not callable(action):
            raise RuntimeError("action is not callable")
