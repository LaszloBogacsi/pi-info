import logging
import sched
import threading
import time

from pi_info.scheduling.Task import Task

logger = logging.getLogger('Scheduler')


class Scheduler(object):

    def __init__(self) -> None:
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.schedules = []

    def worker(self, task: Task):

        deadline = 0
        event = self.scheduler.enter(task.delay, 0, task.run)
        logger.debug('Event scheduled with id: %s', task.id)
        self.schedules.append((task.id, event))

        while deadline is not None:
            deadline = self.scheduler.run(blocking=False)

    def schedule_task(self, task: Task):
        t = threading.Thread(target=self.worker, args=(task,))
        t.start()
        return t

    def cancel_task(self, id_task):
        self.scheduler.cancel(id_task[1])
        self.schedules.remove(id_task)
        logger.debug('Event canceled with id: %s', id_task[0])

    @property
    def is_empty(self):
        return self.scheduler.empty()
