from datetime import datetime, timedelta
from System.units.time.time_event import TimeEvent


class Timer(TimeEvent):

    def __init__(self, time: timedelta):
        self.time = datetime.now() + time

    def to_dict(self):
        dict_copy = self.__dict__.copy()
        dict_copy['timedata'] = self.time.strftime(TimeEvent.time_format)
        return dict_copy

    @classmethod
    def from_dict(cls, timer_data: dict):
        time = timer_data['time'].strptime(TimeEvent.time_format)
        return Timer(
            time
        )
