from datetime import datetime, timedelta
from System.units.time.TimeEvent import TimeEvent


class Timer(TimeEvent):

    def __init__(self, time: timedelta):
        self.time = datetime.now() + time

    def to_dict(self):
        dict_copy = slf.__dict__.copy()