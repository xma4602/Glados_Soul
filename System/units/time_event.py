from datetime import datetime


class TimeEvent:
    time_format = "%d.%m.%Y %H:%M:%S"
    __slots__ = ('__time',)

    def __init__(self, time: datetime):
        self.__time = time

    def __eq__(self, other):
        return self.__time == other.__time

    def __ne__(self, other):
        return self.__time != other.__time

    def __le__(self, other):
        return self.__time <= other.__time

    def __lt__(self, other):
        return self.__time < other.__time

    def __ge__(self, other):
        return self.__time >= other.__time

    def __gt__(self, other):
        return self.__time > other.__time

    @property
    def time(self):
        return self.__time

    @classmethod
    def from_dict(cls, event: dict):
        return TimeEvent(datetime.strptime(event['time'], TimeEvent.time_format))

    @classmethod
    def get_datetime(cls, event: dict):
        return datetime.strptime(event['time'], TimeEvent.time_format)

    @classmethod
    def datetime_to_str(cls, date: datetime):
        return date.strftime(TimeEvent.time_format)
