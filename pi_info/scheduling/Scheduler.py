import logging
import sched
import threading
import time

from pi_info.scheduling.Task import Task

logger = logging.getLogger('Scheduler')


class Scheduler(object):

    def __init__(self, timefunc, delayfunc) -> None:
        self.scheduler = sched.scheduler(timefunc, delayfunc)
        self.event = None
        self.should_reschedule = True

    def worker(self, task: Task, rescheduler):
        deadline = 0
        self.event = self.scheduler.enter(task.delay, 0, task.run)
        logger.debug(('Event scheduled with id: {} in {} seconds'.format(task.id, task.delay)))

        while deadline is not None:
            deadline = self.scheduler.run(blocking=False)
            time.sleep(1)
        if self.should_reschedule:
            rescheduler(self, task)  # all tasks to be rescheduled until canceled

    def cancel_task(self):
        self.should_reschedule = False
        self.scheduler.cancel(self.event)
        logger.debug('Event canceled with id: %s', self.event)
