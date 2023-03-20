import json
import os
from System.units.notice import Notice
from System.units.time_event import TimeEvent
from System.units.alarm_clock import AlarmClock, RegularDay
from datetime import datetime

event_file = "notice.json"


# 2
def store_event(event: TimeEvent):
    events = []

    if os.path.getsize(event_file) != 0:
        with open(event_file, 'r') as file:
            events = json.loads(file)

    for i in range(len(events)):
        item = events[i].from_dict()
        if TimeEvent.compare(event, item) == 1:
            event = event.to_dict()
            events.insert(i+1, event)
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

    events.remove(nearest_event)

    with open(event_file, 'w') as file:
        json.dump(events, file, indent=4)

    return event.from_dict(nearest_event)
