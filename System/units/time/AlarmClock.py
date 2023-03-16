import datetime
import enum

from TimeEvent import TimeEvent


class RegularDay(enum.Enum):
    never = -1
    everyday = 0
    monday = 1
    tuesday = 2
    wednesday = 3
    thursday = 4
    friday = 5
    saturday = 6
    sunday = 7


class AlarmClock(TimeEvent):
    count = 0

    def __init__(self, time: datetime, reg=[RegularDay.never], title=None):
        super().__init__(time)

        if RegularDay(-1) in reg and reg.size() > 0:
            raise ValueError("Недопустимые аргументы в списке повторений будильника reg")

        if title is None:
            title = f"Будильник {AlarmClock.count}"
            AlarmClock.count += 1

        self.regular = reg
        self.title = title

    def postpone(self, time: datetime):
        pass
