from datetime import datetime


class TimeEvent:
    time_format = "%d.%m.%Y %H:%M:%S"

    def __init__(self, time: datetime):
        self.time = time

    def end(self):
        pass
