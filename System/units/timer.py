from datetime import datetime, timedelta
from System.units.time_event import TimeEvent


class Timer(TimeEvent):

    def __init__(self, time: timedelta):
        self.time = datetime.now() + time
        self.class_name = self.__class__.__name__


    def to_dict(self):
        dict_copy = self.__dict__.copy()
        dict_copy['timedata'] = self.time.strftime(TimeEvent.time_format)
        return dict_copy

    @classmethod
    def from_dict(cls, timer_data: dict):
        time = datetime.strptime(timer_data['time'], TimeEvent.time_format)
        return Timer(
            time
        )
