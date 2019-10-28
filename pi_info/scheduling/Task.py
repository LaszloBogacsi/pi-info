class Task:

    def __init__(self, task_id: str, time: str, weekdays: str, delay_in_sec: int, actions: list) -> None:
        self.delay = delay_in_sec
        self.weekdays = weekdays
        self.actions = actions
        self.id = task_id
        self.time = time

    def run(self):
        for action in self.actions:
            if not callable(action):
                raise RuntimeError("action is not callable")
            else:
                action()
