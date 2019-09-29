from enum import Enum


class Weekday(Enum):
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
    Sun = 7

    @staticmethod
    def get_all_weekdays():
        return [dict(key=v.value, value=v.name) for k, v in enumerate(Weekday)]

    def weekdays(self):
        pass

    def weekends(self):
        pass