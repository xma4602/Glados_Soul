import json
import os
from System.units.notice import Notice
from System.units.time_event import TimeEvent
from System.units.alarm_clock import AlarmClock, RegularDay
from datetime import datetime

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

event_file = "notice.json"


# 2
def store_event(event: TimeEvent):
    event = event.to_dict()
    events = []

    if os.path.getsize(event_file) != 0:
        with open(event_file, 'r') as file:
            events = json.loads(file)

    for i in events:
        if TimeEvent.compare(events[i], events[i + 1]) == 1:
            events.insert(i, event)
            break

    with open(event_file, 'w') as file:
        json.dump(events, file, indent=4)


def get_nearest_event():
    if os.path.getsize(event_file) == 0:
        return None

    events = []
    with open(event_file, 'r') as file:
        events = json.load(file)

    nearest_event = events[0]
    nearest_time = datetime.strptime(nearest_event['time'], TimeEvent.time_format)
    for event in events:
        time = datetime.strptime(event['time'], TimeEvent.time_format)
        if time < nearest_event:
            nearest_event = event

    events.remove(nearest_event)

    with open(event_file, 'w') as file:
        json.dump(events, file, indent=4)

    return Notice.from_dict(nearest_event)
