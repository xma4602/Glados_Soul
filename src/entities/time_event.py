from datetime import datetime


class TimeEvent:
    time_format = "%d.%m.%Y %H:%M:%S"
    __slots__ = ['__time']

    def __init__(self, time: datetime):
        self.__time = time

    def __eq__(self, other):
        if isinstance(other, TimeEvent):
            return self.__time == other.__time
        if isinstance(other, datetime):
            return self.__time == other

    def __le__(self, other):
        if isinstance(other, TimeEvent):
            return self.__time <= other.__time
        if isinstance(other, datetime):
            return self.__time <= other

    def __lt__(self, other):
        if isinstance(other, TimeEvent):
            return self.__time <= other.__time
        if isinstance(other, datetime):
            return self.__time <= other

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
