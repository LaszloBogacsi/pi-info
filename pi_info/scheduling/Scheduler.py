import sched
import threading
import time


class Scheduler(object):
    def __init__(self) -> None:
        self.schedules = []
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def enter_sched(self):
        self.scheduler.enter(5, 1, lambda x: print("schedule ", x), argument=("running",))
        self.scheduler.run(blocking=True)


if __name__ == "__main__":
    s = Scheduler()
    t = threading.Thread(target=s.enter_sched)
    t.start()
    print("after scheduling")
