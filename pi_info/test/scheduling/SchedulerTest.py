import unittest

from pi_info.scheduling.Scheduler import Scheduler


class SchedulerTest(unittest.TestCase):
    scheduler = Scheduler()
    class Task():
        def __init__(self, id, a, delay):
            self.id = id
            self.delay = delay
            self.a = a
        def run(self):
            print("From task class ", self.a)

    def test_can_schedule_a_task(self):
        task1 = self.Task("1-2000-off", "1", 0.1)
        t = self.scheduler.schedule_task(task1)
        self.assertEqual(self.scheduler.is_empty, False)

    def test_can_cancel_a_task(self):
            task1 = self.Task("1-1800-on", "1", 30)
            self.scheduler.schedule_task(task1)
            task = next(task for task in self.scheduler.schedules if task[0] == task1.id)[1]
            self.scheduler.cancel_task(task)
            self.assertEqual(self.scheduler.is_empty, True)


if __name__ == '__main__':
    unittest.main()
