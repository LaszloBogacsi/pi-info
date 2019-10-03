from typing import List


class Task():
    def __init__(self, id: str, time: str, weekdays: str, delay_in_sec: int, actions: List) -> None:
        self.delay = delay_in_sec
        self.weekdays = weekdays
        self.actions = actions
        self.id = id
        self.time = time

    def run(self):
        for action in self.actions:
            if not callable(action):
                raise RuntimeError("action is not callable")
            else:
                action()
