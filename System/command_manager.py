import re
from datetime import datetime, timedelta
import logging
from System import data_manager, message_manager

from System.modules import room, timing
from System.units.message import Message
from System.units.task import Task

global __commands


def start():
    logging.info('Запуск модуля command_manager')
    global __commands
    __commands = {
        'task': 'задач',
        'hello': 'прив|здрав',
        'open': 'открыть',
        'close': 'закрыть',
        'is_open': '(.*открыт.*лаб.*)|(.*лаб.*открыт.*)|(.*закрыт.*лаб.*)|(.*лаб.*закрыт.*)|(.*лаб.*ест.*)|(.*ест.*лаб.*)',
        'about_club': 'что такое robotic?',
        'projects': 'проекты и мероприятия',
        'join_club': 'как попасть в robotic?',
        'remind': 'напомни'
    }


# главный метод парсинга сообщения
def parse(text: str, sender_id: str):
    """
    Получает и текст сообщения и обрабатывает его.
    Не возвращает результат.
    :param sender_id: айди отправителя сообщения
    :param text: string текст сообщения
    """

    # разбиваем на строки и очищаем от пробелов
    text = text.split('\n')
    for i in range(len(text)):
        text[i] = text[i].strip(' ')
        text[i] = " ".join(text[i].split())

    title = text[0].lower()
    # если в заголовке тег задачи, отправляем на парсинг задачи
    # ответ на начать
    if re.search(__commands['task'], title) is not None:
        __new_task(sender_id, text[1:])
    # приветствие
    elif re.search(__commands['hello'], title) is not None:
        __hello(sender_id)
    # команда открытия лабы
    elif re.search(__commands['open'], title) is not None:
        __open_room(sender_id)
    # команда закрытия лабы
    elif re.search(__commands['close'], title) is not None:
        __close_room(sender_id)
    # вопрос, открыта ли лаба
    elif re.search(__commands['is_open'], title) is not None:
        __is_opened(sender_id)
    # общая инфа о клубе
    elif re.search(__commands['about_club'], title) is not None:
        __about_club(sender_id)
    # инфа о проектах клуба
    elif re.search(__commands['projects'], title) is not None:
        __about_projects(sender_id)
    # как попасть в клуб
    elif re.search(__commands['join_club'], title) is not None:
        __join_club(sender_id)
    # напоминание
    elif re.search(__commands['remind'], title) is not None:
        __remind(sender_id, text)


def __new_task(sender_id: str, task_data: list):
    """
    Получает и парсит данные о задаче
    :param sender_id: айди отправителя сообщения
    :param task_data: массив данных задачи.
    task_data = [заголовок, организатор, список исполнителей, дедлайн, описание]
    :return: экземпляр Task
    """

    # вызываем методы парсинга для каждого поля
    task_data[1] = data_manager.names_to_id(task_data[1].replace(',', '').split())
    task_data[2] = pasrse_date(task_data[2])

    return Task(
        title=task_data[0],
        manager_id=sender_id,
        performers_id=task_data[1],
        deadline=task_data[2],
        description=task_data[3:]
    )


def __unknown_command(sender_id: str):
    message = Message(
        'Неизвестная команда',
        [sender_id],
        datetime.now(),
        []
    )
    message_manager.send(message)


def __is_opened(sender_id: str):
    message = Message(
        room.is_opened(),
        [sender_id],
        datetime.now(),
        []
    )
    message_manager.send(message)


def __open_room(sender_id: str):
    if data_manager.is_council(sender_id):
        message = room.open_room()
        message = Message(
            message,
            [sender_id],
            datetime.now(),
            []
        )
    else:
        logging.warning('Попытка получить доступ к команде совета клуба', {'id': sender_id})
        message = Message(
            'У вас нет доступа к этой команде',
            [sender_id],
            datetime.now(),
            []
        )

    message_manager.send(message)


def __close_room(sender_id):
    if data_manager.is_council(sender_id):
        message = room.close_room()
        message = Message(
            message,
            [sender_id],
            datetime.now(),
            []
        )
    else:
        logging.warning('Попытка получить доступ к команде совета клуба', {'id': sender_id})
        message = Message(
            'У вас нет доступа к этой команде',
            [sender_id],
            datetime.now(),
            []
        )

    message_manager.send(message)


def __hello(sender_id):
    message = Message(
        'Привет!',
        [sender_id],
        datetime.now(),
        []
    )
    message_manager.send(message)


def __about_club(sender_id):
    about_club = data_manager.about_club()
    message = Message(
        about_club[0],
        [sender_id],
        datetime.now(),
        about_club[1:]
    )
    message_manager.send(message)


def __about_projects(sender_id):
    about_projects = data_manager.about_projects()
    message = Message(
        about_projects[0],
        [sender_id],
        datetime.now(),
        about_projects[1:]
    )
    message_manager.send(message)


def __join_club(sender_id):
    join_club = data_manager.join_club()
    message = Message(
        join_club[0],
        [sender_id],
        datetime.now(),
        join_club[1:]
    )
    message_manager.send(message)


def __remind(sender_id, text):
    try:
        peer = __parse_peer(sender_id, re.sub(r'напомни\s*', '', text[0].lower()))
        time = __parse_datetime(text[1].lower())

        message = Message(text[2], peer, time, text[3:])
        message_manager.send(message)
        logging.info('Создано напоминание', {'notice': message.__str__()})

        message_manager.send(Message(
            'Напоминание создано',
            [sender_id],
            datetime.now(),
            []
        ))
    except ValueError as err:
        message_manager.send(Message(
            err.__str__(),
            [sender_id],
            datetime.now(),
            []
        ))


def __parse_peer(sender_id, peer):
    if peer == '':
        return [sender_id]
    if re.search(r'совет[а-я]*\s*', peer) is not None:
        return data_manager.council_ids()
    raise ValueError('Неверный формат получателя напоминания')


def __parse_datetime(string):
    result = datetime.now()
    if string.startswith('через'):
        string, delta = time_parser.parse_time(re.sub(r'через\s*', '', string))
        result += delta
        if len(string) != 0:
            result = __parse_time_in(result, string)
    elif string.startswith('в'):
        result = __parse_time_in(result, string)
    else:
        string, delta = time_parser.parse_date(string)
        result = delta
        if len(string) != 0:
            result = __parse_time_in(result, string)

    return result


def __parse_time_in(result, string):
    string, delta = time_parser.parse_time(re.sub(r'в\s*', '', string))
    result = result.replace(
        hour=int(delta.total_seconds() // 3600),
        minute=int(delta.total_seconds() % 60)
    )
    return result
