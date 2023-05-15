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

    @classmethod
    def from_dict(cls, event: dict):
        time = datetime.strptime(event['time'], TimeEvent.time_format)
        return TimeEvent(time)

    @classmethod
    def get_datetime(cls, event: dict):
        return datetime.strptime(event['time'], TimeEvent.time_format)

    @classmethod
    def datetime_to_str(cls, date: datetime):
        return datetime.strftime(TimeEvent.time_format)

