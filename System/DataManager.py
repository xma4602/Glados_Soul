import json
import re

from System.units.time.Notice import Notice
from System.units.time.TimeEvent import TimeEvent
from System.units.time.Timer import Timer
from System.units.time.AlarmClock import AlarmClock, RegularDay
from datetime import datetime, timedelta

time_file = "time.json"
time_format = "%d.%m.%y %H:%M:%S"


def get_nearest_event(self):
    pass


def store_time_event(obj: TimeEvent):
    """Записывает в json файл уведомление, таймер или будильник"""
    dict_copy = obj.__dict__.copy()
    list_of_regular = []

    if 'regular' in dict_copy:
        for item in dict_copy['regular']:
            list_of_regular.append(item.value)
        dict_copy['regular'] = list_of_regular
    dict_copy['timedata'] = obj.time.strftime(time_format)

    with open(time_file, "r+") as file:
        event = load_next_time_event(file)
        timedata = datetime.strptime(event['timedata'], time_format)

        while obj.time < timedata:
            event = load_next_time_event(file)
            timedata = datetime.strptime(event['timedata'], time_format)

        file.write(json.dumps(dict_copy))


def load_next_time_event(file):
    print(file.tell())
    a = file.readline()
    return json.loads(a)


a = AlarmClock(datetime.now(), reg=(RegularDay.tuesday, RegularDay.friday))
print(store_time_event(a))
