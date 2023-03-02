from datetime import datetime


class TimeEvent:
    timedata = datetime()
    def __init__(self, _year=0, _month=0, _day=0, _hour=0, _minute=0, _second=0, _microsecond=0):
        timedata = datetime(_year, _month, _day, _hour, _minute, _second, _microsecond)


