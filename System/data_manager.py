import json
from datetime import datetime, timedelta
from System.units.time_event import TimeEvent
from System.units.message import Message
import logging
from System import config_manager


def start():
    logging.info('Запуск модуля data_manager')
    global __fired_events_file
    global __events_file
    global __council_file

    __fired_events_file = config_manager.fired_events_file()
    __events_file = config_manager.events_file()
    __council_file = config_manager.council_file()


def __save_json(file_name, *args):
    # logger.info('Сохранены данные', data=args)
    with open(file_name, 'w') as file:
        json.dump(args, file, indent=4, ensure_ascii=False)


def __load_json(file_name: str):
    with open(file_name, 'r') as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            return None
        # logger.info('Загружены данные', data=data)
        return data


def __load_txt(file_name: str) -> list[str]:
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.readlines()


def is_council(id: str) -> bool:
    users = __load_json(__council_file)
    return id in users.keys()


def council_ids() -> list[str]:
    global __council_file
    return __load_json(__council_file).keys()


def store_event(event):
    """
    Сохраняет событие в файл
    :param event: объект события
    """
    events = __load_json(__events_file)
    if len(events) == 0:
        events = [event.to_dict()]
    else:
        flag = False
        for index in range(len(events)):
            ev = TimeEvent.get_datetime(events[index])
            if event.__time < ev:
                flag = True
                event = event.to_dict()
                events.insert(index, event)
                break
        if not flag:
            events.append(event.to_dict())
    __save_json(__events_file, events)


def get_nearest_event(old_event=None) -> TimeEvent:
    """
    Возвращает ближайшее событие
    :params old_event: исполнившееся событие
    """
    events = __load_json(config_manager.events_file())  # считывает список событий из файла
    if events is None or len(events) == 0:  # если событий нет, то возвращает None
        return None
    else:
        if old_event is not None:  # если передано старое событие, то удаляет его из списка
            events.pop(0)
            __save_json(config_manager.events_file(), events)  # записывает измененный список обратно в файл
        if len(events) == 0:
            return None
        nearest_event = events[0]  # получаем ближайшее событие
        event_class = eval(nearest_event['class_name'])  # создаем объект того же класса, что и nearest_event

        return event_class.from_dict(nearest_event)


def _check_fired_events():
    """
    Используется единожды при запуске, возвращает ближайшее не просроченное событие
    """

    events = __load_json(config_manager.events_file())  # считываем список событий
    if len(events) != 0:
        fired_events = []  # список просроченных событий
        event = events[0]  # получаем ближайшее событие
        delta = datetime.now() - TimeEvent.get_datetime(event)  # вычисляем разницу между сейчас и временем события
        while delta > timedelta(minutes=1):
            fired_events.append(event)  # если событие просрочено, добавляем его в список
            events.pop(0)  # удаляем просроченное из списка запланированных событий
            if len(events) == 0:  # если список событий закончился, значит все события просрочены
                event = []
                break
            event = events[0]
            delta = datetime.now() - TimeEvent.get_datetime(event)

        __save_json(config_manager.events_file(),
                    events)  # записываем в файл список запланированных событий без просрочек

        if len(fired_events) != 0:
            load_fired_events = __load_json(config_manager.fired_events_file())  # загружаем список просрочек из файла
            load_fired_events += fired_events  # добавляем в список новые просрочки
            __save_json(config_manager.fired_events_file(), load_fired_events)  # загружаем все обратно в файл


def get_fired_events():
    """
    Возвращает список просроченных событий
    """
    fired_events = __load_json(__fired_events_file)

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
    users = __load_json(__council_file)
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
    users = __load_json(__council_file)
    for i in range(len(users_surnames)):
        for id, name in users.items():
            if users_surnames[i] == name:
                users_surnames[i] = id
    return users_surnames


def about_club():
    return __load_txt(config_manager.about_club_file())


def about_projects():
    return __load_txt(config_manager.about_projects_file())


def join_club():
    return __load_txt(config_manager.join_club_file())
