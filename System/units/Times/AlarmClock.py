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

class Alarm(TimeEvent):
    _regular = RegularDay.never
    _note = "Будильник" #заголвок или подпись к будильнику
    def SetNote(self, note: str):
        '''
        Задает будильнику заголовок
        :param note: заголвок
        '''
        _note = str


    def SetRegularMode(self, day = -1):
        _regular = day



