import json
import re
import os
from System.units.time.Notice import Notice
from System.units.time.TimeEvent import TimeEvent
from System.units.time.Timer import Timer
from System.units.time.AlarmClock import AlarmClock, RegularDay
from datetime import datetime, timedelta

time_file = "time.json"
time_format = "%d.%m.%y %H:%M:%S"



"""def store_time_event(obj: TimeEvent):
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

        file.write(json.dumps(dict_copy))"""

a = AlarmClock(datetime.now(), reg=(RegularDay.tuesday, RegularDay.friday))

notice_file = "notice.json"

#2
def store_notice(notice: Notice):
    notice = notice.to_dict()
    notices = []

    if os.path.getsize(notice_file) != 0:
        with open(notice_file, 'r') as file:
            notices = json.load(file)

    notices.append(notice)

    with open(notice_file, 'w') as file:
        json.dump(notices, file, indent=4)


def get_nearest_notice():

    if os.path.getsize(notice_file) == 0:
        return None
    else:
        notices = []
        with open(notice_file, 'r') as file:
            notices = json.load(file)

        nearest_notice = notices[0]
        nearest_time = datetime.strptime(nearest_notice['time'], Notice.time_format)
        for notice in notices:
            time = datetime.strptime(notice['time'], Notice.time_format)
            if time < nearest_time:
                nearest_notice = notice

        notices.remove(nearest_notice)

        with open(notice_file, 'w') as file:
            json.dump(notices, file, indent=4)

        return Notice.from_dict(nearest_notice)
