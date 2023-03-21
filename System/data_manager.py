import json
from datetime import datetime, time, timedelta
from System.units.alarm_clock import AlarmClock
from System.units.notice import Notice
from System.units.time_event import TimeEvent
from System.units.timer import Timer

event_file = "notice.json"
fired_events_file = "fired_event.json"


def store_event(event):
    events = []
    with open(event_file, 'r') as file:
        events = json.load(file)
        if len(events) == 0:
            event = event.to_dict()
            events.append(event)
        else:
            for index in range(len(events)):
                ev = TimeEvent.get_datetime(events[index])
                if event.time < ev:
                    event = event.to_dict()
                    events.insert(index, event)
                    break

    with open(event_file, 'w') as file:
        json.dump(events, file, indent=4)


def get_nearest_event(old_event=None):
    events = []
    with open(event_file, 'r+') as file:
        events = json.load(file)

    if len(events) == 0:
        return None
    else:
        if old_event is not None:
            events.pop(0)
            json.dump(events, file, indent=4)

        nearest_event = events[0]
        event_class = eval(nearest_event['class_name'])

        return event_class.from_dict(nearest_event)


def start():
    events = []
    with open(event_file, 'r+') as file:
        events = json.load(file)

    if len(events) == 0:
        return None

    fired_events = []

    event = events[0]
    delta = datetime.now() - TimeEvent.get_datetime(event)
    while delta > timedelta(hours = 1):
        fired_events.append(event)
        events.pop(0)
        if len(events) == 0:
            event = None
            break
        event = events[0]
        delta = datetime.now() - TimeEvent.get_datetime(event)

    with open(event_file, 'w') as file:
        json.dump(events, file, indent=4)

    load_fired_events = []
    if len(fired_events) != 0:
        with open(fired_events_file, 'r') as file:
            load_fired_events = json.load(file)
        with open(fired_events_file, 'w') as file:
            load_fired_events += fired_events
            json.dump(load_fired_events, file, indent=4)

    return event

store_event(AlarmClock(datetime.now() - timedelta(hours = 3)))
event = start()
print(event)
