import sched
import threading
import time


class Scheduler(object):
    def __init__(self) -> None:
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.schedules = []

    def worker(self, task):

        deadline = 0
        event = self.scheduler.enter(task.delay, 0, task.run)
        self.schedules.append((task.id, event))

        while deadline is not None:
            deadline = self.scheduler.run(blocking=False)

    def schedule_task(self, task):
        t = threading.Thread(target=self.worker, args=(task,))
        t.start()
        return t

    def cancel_task(self, task):
        self.scheduler.cancel(task)

    @property
    def is_empty(self):
        return self.scheduler.empty()
