from datetime import datetime


class TimeEvent:
    time_format = "%d.%m.%Y %H:%M:%S"

    def __init__(self, time: datetime):
        self.time = time

    @classmethod
    def compare(cls, event1, event2):
        if event1.time < event2.time:
            return -1
        if event1.time > event2.time:
            return 1
        if event1.time == event2.time:
            return 0


