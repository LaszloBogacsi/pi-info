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


class Scheduler(object):

    def __init__(self) -> None:
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.schedules = []

    def schedule_task_from_db(self, schedule: Schedule, action):
        id = "{}-{}".format(schedule.device_id, schedule.schedule_id)
        delay = self._delay_until_run(schedule.time, schedule.days)
        self.schedule_task(Task(id, schedule.time, schedule.days, delay, action))

    def schedule_task_from_form(self, device_id, schedule_id, s_time, weekdays, action):
        id = "{}-{}".format(device_id, schedule_id)
        delay = self._delay_until_run(s_time, weekdays)
        self.schedule_task(Task(id, s_time, weekdays, delay, action))

    def schedule_task(self, task: Task):
        task_exists = len([s for s in self.schedules if s[0] == task.id]) > 0
        if task_exists:
            print("will cancel task")
            self.cancel_task(task.id)
            print("will cancel task")
        t = threading.Thread(target=self._worker, args=(task,))
        t.start()

    def cancel_task(self, task_id):
        id_task = [sched for sched in self.schedules if sched[0] == task_id][0]
        self.scheduler.cancel(id_task[1])
        self.schedules.remove(id_task)
        logger.debug('Event canceled with id: %s', id_task[0])

    @property
    def is_empty(self):
        return self.scheduler.empty()

    @staticmethod
    def _calculate_next_run(current_time: datetime, current_weekday: int, weekdays: List[int], time: Time) -> datetime:
        one_week_offset = 7
        scheduled_time = current_time.replace(hour=time.hour, minute=time.minute, second=0, microsecond=0)
        if current_weekday in weekdays and current_time < scheduled_time:
            return scheduled_time
        else:
            deltas = []
            for day in weekdays:
                deltas.append(abs(day - current_weekday) if day - current_weekday != 0 else 7)
            closest_day_diff = weekdays[max([i for i, v in enumerate(deltas) if v == min(deltas)])] - current_weekday
        return scheduled_time.replace(day=current_time.day) + datetime.timedelta(days=closest_day_diff if closest_day_diff > 0 else closest_day_diff + one_week_offset)

    def _reschedule_task(self, task):
        new_delay = self._delay_until_run(task.time, task.weekdays)
        logger.debug(('Event will reschedule with id: {} in {} seconds'.format(task.id, new_delay)))
        self._worker(Task(task.id, task.time, task.weekdays, new_delay, task.run))

    def _worker(self, task: Task):
        deadline = 0
        event = self.scheduler.enter(task.delay, 0, task.run)
        logger.debug(('Event scheduled with id: {} in {} seconds'.format(task.id, task.delay)))
        self.schedules.append((task.id, event))

        while deadline is not None:
            deadline = self.scheduler.run(blocking=False)
            time.sleep(1)

        self._reschedule_task(task)

    def _find_closest_time(self, time, days) -> datetime:
        time_to_run = time.split(':')
        schedule_time = Time(int(time_to_run[0]), int(time_to_run[1]))
        weekdays = list(int(day) for day in days.split(','))
        return self._calculate_next_run(datetime.datetime.now(), datetime.datetime.today().weekday() + 1, weekdays, schedule_time)

    def _delay_until_run(self, time, weekdays) -> int:
        current_time = datetime.datetime.now()
        closest_time = self._find_closest_time(time, weekdays)
        return (closest_time - current_time).seconds