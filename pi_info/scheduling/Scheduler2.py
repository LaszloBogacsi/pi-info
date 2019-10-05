import datetime
import logging
import sched
import threading
import time
from typing import List

from pi_info.repository.Schedule import Schedule
from pi_info.scheduling.Task import Task
from pi_info.scheduling.Time import Time

logger = logging.getLogger('Scheduler')


class Scheduler2(object):

    def __init__(self, timefunc, delayfunc) -> None:
        self.scheduler = sched.scheduler(timefunc, delayfunc)
        self.event = None

    def worker(self, task: Task, rescheduler):
        deadline = 0
        self.event = self.scheduler.enter(task.delay, 0, task.run)
        logger.debug(('Event scheduled with id: {} in {} seconds'.format(task.id, task.delay)))

        while deadline is not None:
            deadline = self.scheduler.run(blocking=False)
            print(deadline, threading.current_thread().name)
            time.sleep(1)
        print("finished")
        rescheduler(self, task) # all tasks to be rescheduled until canceled

    def cancel_task(self):
        self.scheduler.cancel(self.event)
        logger.debug('Event canceled with id: %s', self.event)
