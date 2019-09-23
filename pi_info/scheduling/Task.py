class Task():
    def __init__(self, id, delay_in_sec, action) -> None:
        self.run = action
        self.id = id
        self.delay = delay_in_sec
        if not callable(action):
            raise RuntimeError("action is not callable")
