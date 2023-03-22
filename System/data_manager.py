import json
from datetime import datetime, time, timedelta
from System.units.alarm_clock import AlarmClock
from System.units.notice import Notice
from System.units.time_event import TimeEvent
from System.units.timer import Timer

event_file = "notice.json"
fired_events_file = "fired_event.json"


def store_event(event):
    """
    Сохраняет событие в файл
    :param event: объект события
    """
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
    """
    Возвращает ближайшее событие
    :params old_event: исполнившееся событие
    """
    events = []
    with open(event_file, 'r+') as file:
        events = json.load(file)  # считывает список событий из файла

    if len(events) == 0:  # если событий нет, то возвращает None
        return None
    else:
        if old_event is not None:  # если передано старое событие, то удаляет его из списка
            events.pop(0)
            with open(event_file, 'w') as file:
                json.dump(events, file, indent=4)  # записывает измененный список обратно в файл

        nearest_event = events[0]  # получаем ближайшее событие
        event_class = eval(nearest_event['class_name'])  # создаем объект того же класса, что и nearest_event

        return event_class.from_dict(nearest_event)


def start():
    """
    Используется единожды при запуске, возвращает ближайшее не просроченное событие
    """

    events = []
    with open(event_file, 'r+') as file:  # считываем список событий
        events = json.load(file)

    if len(events) == 0:  # возвращаем none, если событий нет
        return None

    fired_events = []  # список просроченных событий

    event = events[0]  # получаем ближайшее событие
    delta = datetime.now() - TimeEvent.get_datetime(event)  # вычисляем разницу между сейчас и временем события
    while delta > timedelta(hours=1):
        fired_events.append(event)  # если событие просрочено, добавляем его в список
        events.pop(0)  # удаляем просроченное из списка запланированных событий
        if len(events) == 0:  # если список событий закончился, значит все события просрочены
            event = None
            break
        event = events[0]
        delta = datetime.now() - TimeEvent.get_datetime(event)

    with open(event_file, 'w') as file:  # записываем в файл список запданированных событий без просрочек
        json.dump(events, file, indent=4)

    load_fired_events = []  # список из файла просроченных событий
    if len(fired_events) != 0:
        with open(fired_events_file, 'r') as file:
            load_fired_events = json.load(file)  # загружаем список просрочек из файла
        with open(fired_events_file, 'w') as file:
            load_fired_events += fired_events  # добавляем в список новые просрочки
            json.dump(load_fired_events, file, indent=4)  # загружаем все обратно в файл

    if event is None:  # если ближайших непросроченных событий нет, то возвращаем none
        return None

    event_class = eval(event['class_name'])  # создаем объект того же класса, что и event
    return event_class.from_dict(event)
