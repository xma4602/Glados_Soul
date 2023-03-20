import json
import os
from System.units.notice import Notice
from System.units.time_event import TimeEvent
from System.units.alarm_clock import AlarmClock, RegularDay
from System.units.timer import Timer
from datetime import datetime

event_file = "notice.json"


# 2
def store_event(event):
    events = []
    with open(event_file, 'r') as file:
        events = json.loads(file)
        if len(events) == 0:
            events.append(event)
        else:
            for i in range(len(events)):
                item = TimeEvent.from_dict(events[i])
                if TimeEvent.compare(event, item) == 1:
                    event = event.to_dict()
                    events.insert(i + 1, event)
                    break

    with open(event_file, 'w') as file:
        json.dump(events, file, indent=4)


def get_nearest_event():
    events = []
    with open(event_file, 'r') as file:
        events = json.load(file)
        if len(events) == 0:
            return None

        nearest_event = events[0]
        nearest_time = datetime.strptime(nearest_event['time'], TimeEvent.time_format)

        events.remove(nearest_event)

    with open(event_file, 'w') as file:
        json.dump(events, file, indent=4)
    if nearest_event['class_name'] == 'AlarmClock':
        return AlarmClock.from_dict(nearest_event)
    if nearest_event['class_name'] == 'Notice':
        return Notice.from_dict(nearest_event)
    if nearest_event['class_name'] == 'Timer':
        return Timer.from_dict(nearest_event)



