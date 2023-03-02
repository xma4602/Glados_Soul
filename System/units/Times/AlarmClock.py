from datetime import datetime
from TimeEvent import TimeEvent
import enum


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
    _regular = [RegularDay.never, ]
    _note = "Будильник"  # заголвок или подпись к будильнику

    def set_note(self, note: str):
        '''
        Задает будильнику заголовок
        :param note: заголвок
        '''
        self._note = str

    def set_regular_mode(self, day=-1):
        self._regular.append(day)
