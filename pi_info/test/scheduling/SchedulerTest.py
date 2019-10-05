import time
import unittest

from pi_info.scheduling.SchedulingManager import SchedulingManager


class SchedulerTest(unittest.TestCase):
    scheduler = SchedulingManager()
    class Task():
        def __init__(self, id, a, delay):
            self.id = id
            self.delay = delay
            self.a = a
        def run(self):
            print("From task class ", self.a)

    def test_can_schedule_a_task(self):
        task1 = self.Task("1-2000-off", "1", 0.1)
        self.scheduler._schedule_task(task1)
        self.assertEqual(self.scheduler.is_empty, False)
        self.assertEqual(len(self.scheduler.schedules), 1)


def test_can_cancel_a_task(self):
        task1 = self.Task("1-1800-on", "1", 30)
        self.scheduler._schedule_task(task1)
        time.sleep(0.1)
        self.scheduler.cancel_task(task1.id)
        self.assertEqual(self.scheduler.is_empty, True)
        self.assertEqual(len(self.scheduler.schedules), 0)


if __name__ == '__main__':
    unittest.main()
