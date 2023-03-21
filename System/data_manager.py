import json

from System.units.alarm_clock import AlarmClock
from System.units.notice import Notice
from System.units.time_event import TimeEvent
from System.units.timer import Timer

event_file = "notice.json"


def store_event(event):
    events = []
    with open(event_file, 'r') as file:
        events = json.load(file)
        if len(events) == 0:
            event = event.to_dict()
            events.append(event)
        else:
            for index in range(len(events)):
                if event.time < TimeEvent.get_datetime(events[index]):
                    event = event.to_dict()
                    events.insert(index, event)
                    break

    with open(event_file, 'w') as file:
        json.dump(events, file, indent=4)


def get_nearest_event(old_event):
    events = []
    with open(event_file, 'r+') as file:
        events = json.load(file)
        if len(events) == 0:
            return None
        if old_event is not None:
            events.pop(0)
            json.dump(events, file, indent=4)
        nearest_event = events[0]


    if nearest_event['class_name'] == 'AlarmClock':
        return AlarmClock.from_dict(nearest_event)
    if nearest_event['class_name'] == 'Notice':
        return Notice.from_dict(nearest_event)
    if nearest_event['class_name'] == 'Timer':
        return Timer.from_dict(nearest_event)
