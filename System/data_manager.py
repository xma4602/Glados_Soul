import json
from datetime import datetime, timedelta
from System.units.time_event import TimeEvent
from System.units.notice import Notice


def start():
    pass


def save(file_name, *args):
    with open(file_name, 'w') as file:
        json.dump(args, file, indent=4, ensure_ascii=False)


def load(str: file_name):
    with open(file_name, 'r') as file:
        return json.load(file)


def is_council(id: str):
    users = load(config['council'])
    return id in users.keys()


def store_event(event):
    """
    Сохраняет событие в файл
    :param event: объект события
    """
    events = load(config['events'])
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
    save(config['events'], events)


def get_nearest_event(old_event=None):
    """
    Возвращает ближайшее событие
    :params old_event: исполнившееся событие
    """
    events = load(config['events'])  # считывает список событий из файла
    if len(events) == 0:  # если событий нет, то возвращает None
        return None
    else:
        if old_event is not None:  # если передано старое событие, то удаляет его из списка
            events.pop(0)
            save(config['events'], events)  # записывает измененный список обратно в файл
        if len(events) == 0:
            return None
        nearest_event = events[0]  # получаем ближайшее событие
        event_class = eval(nearest_event['class_name'])  # создаем объект того же класса, что и nearest_event

        return event_class.from_dict(nearest_event)


def check_fired_events():
    """
    Используется единожды при запуске, возвращает ближайшее не просроченное событие
    """

    events = load(config['events'])  # считываем список событий

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

    save(config['events'], events) # записываем в файл список запланированных событий без просрочек

    if len(fired_events) != 0:
        load_fired_events = load(config['fired']) # загружаем список просрочек из файла
        load_fired_events += fired_events  # добавляем в список новые просрочки
        save(config['fired'], load_fired_events) # загружаем все обратно в файл


def get_fired_events():
    """
    Возвращает список просроченных событий
    """
    fired_events = load(config['fired'])

    if len(fired_events) == 0:
        return None

    for i in (range(len(fired_events))):
        event_class = eval(fired_events[i]['class_name'])
        fired_events[i] = event_class.from_dict(fired_events[i])

    return fired_events


def id_to_names(users_id: list):
    """
    Получиет имена пользователей и возвращает их id
    :param users_id: список фамилий пользователей
    :return: список соответствующих фамилиям id
    """
    names = []
    for user_id in users_id:
        for name, id in users.items():
            if int(id) == user_id:
                names.append(name)
                break

    return names


def names_to_id(users_surnames: list):
    """
    Получиет имена пользователей и возвращает их id
    :param users_surnames: список фамилий пользователей
    :return: список соответствующих фамилиям id
    """
    # по ключам фамилий из словаря users формируем список id
    for i in range(len(users_surnames)):
        for id, name in users.items():
            if users_surnames[i] == name:
                users_surnames[i] = id
    return users_surnames



