import datetime
import logging
import threading
import time
from typing import List

from pi_info.repository.Schedule import Schedule
from pi_info.scheduling.Scheduler import Scheduler
from pi_info.scheduling.Task import Task
from pi_info.scheduling.Time import Time

logger = logging.getLogger('SchedulingManager')


class SchedulingManager:
    schedulers: [(int, Scheduler)]

    def __init__(self) -> None:
        self.schedulers = []

    def schedule_task_from_db(self, schedule: Schedule, actions):
        task_id = "{}-{}".format(schedule.group_id, schedule.schedule_id)
        delay = self._delay_until_next_run(schedule.time, schedule.days)
        self._schedule_task(Task(task_id, schedule.time, schedule.days, delay, actions))

    def schedule_task_from_form(self, device_id, schedule_id, s_time, weekdays, actions):
        task_id = "{}-{}".format(device_id, schedule_id)
        delay = self._delay_until_next_run(s_time, weekdays)
        task = Task(task_id, s_time, weekdays, delay, actions)
        self._schedule_task(task)
        return task

    def update_task_from_form(self, device_id, schedule_id, s_time, weekdays, action):
        task_id = "{}-{}".format(device_id, schedule_id)
        self.cancel_task(task_id)
        self.schedule_task_from_form(device_id, schedule_id, s_time, weekdays, action)

    def cancel_task(self, task_id):
        id_to_scheduler = next((scheduler for scheduler in self.schedulers if scheduler[0] == task_id), None)
        if id_to_scheduler is not None:
            scheduler: Scheduler = id_to_scheduler[1]
            self.schedulers.remove(id_to_scheduler)
            scheduler.cancel_task()
        else:
            logger.debug('Can not find scheduler to cancel with id: {}'.format(task_id))

    def _schedule_task(self, task: Task):
        scheduler = Scheduler(time.time, time.sleep)
        t = threading.Thread(target=scheduler.worker, args=(task, self._reschedule_task))
        t.start()

        self.schedulers.append((task.id, scheduler))

    def _reschedule_task(self, scheduler, task):
        new_delay = self._delay_until_next_run(task.time, task.weekdays)
        logger.debug(('Event will reschedule with id: {} in {} seconds'.format(task.id, new_delay)))
        scheduler.worker(Task(task.id, task.time, task.weekdays, new_delay, task.run), self._reschedule_task,)

    def _find_closest_schedule_time(self, time, days) -> datetime:
        time_to_run = time.split(':')
        schedule_time = Time(int(time_to_run[0]), int(time_to_run[1]))
        weekdays = list(int(day) for day in days.split(','))
        return self._calculate_next_run(datetime.datetime.now(), datetime.datetime.today().weekday() + 1, weekdays, schedule_time)

    def _delay_until_next_run(self, time, weekdays) -> int:
        current_time = datetime.datetime.now()
        closest_time = self._find_closest_schedule_time(time, weekdays)
        return int((closest_time - current_time).total_seconds())

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

