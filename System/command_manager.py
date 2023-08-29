import re
import os
from datetime import datetime

from System import data_manager, message_manager

from System.modules import room
from System.units.notice import Notice
from System.units.task import Task

global commands


def start():
    print(f'Запуск модуля {os.path.basename(__file__)}')
    global commands
    commands = {
        'task': 'задач',
        'hello': 'прив|здрав',
        'open': 'открыть',
        'close': 'закрыть',
        'is_open': '(.*открыт.*лаб.*)|(.*лаб.*открыт.*)|(.*закрыт.*лаб.*)|(.*лаб.*закрыт.*)|(.*лаб.*ест.*)|(.*ест.*лаб.*)'
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
    if re.search(commands['task'], title) is not None:
        new_task(sender_id, text[1:])
    if re.search(commands['hello'], title) is not None:
        hello(sender_id)
    # команда открытия лабы
    elif re.search(commands['open'], title) is not None:
        open_room(sender_id)
    # команда закрытия лабы
    elif re.search(commands['close'], title) is not None:
        close_room(sender_id)
    # вопрос, открыта ли лаба
    elif re.search(commands['is_open'], title) is not None:
        is_opened(sender_id)
    # ответ на нераспознанную команду
    else:
        unknown_command(sender_id)


def new_task(sender_id: str, task_data: list):
    """
    Получает и парсит данные о задаче
    :param sender_id: айди отправителя сообщения
    :param task_data: массив данных задачи.
    task_data = [заголовок, организатор, список исполнителей, дедлайн, описание]
    :return: экземпляр Task
    """

    # вызываем методы парсинга для каждого поля
    task_data[1] = data_manager.names_to_id(task_data[1].replace(',', '').split())
    task_data[2] = pasrse_time(task_data[2])

    return Task(
        title=task_data[0],
        manager_id=sender_id,
        performers_id=task_data[1],
        deadline=task_data[2],
        description=task_data[3:]
    )


def pasrse_time(date_time):
    """
    Получает и парсит данные о времени
    :param date_time: дата и время
    :return: экземпляр datetime
    """
    # регуляркой находим дату
    date = re.search(r'(\d{1,2})\.(\d{1,2})(.(\d{2,4}))?', date_time)
    # удаляем дату из текста
    date_time = date_time.replace(date[0], '')
    # регуляркой находим времяя
    time = re.search(r'(\d{1,2})([: ](\d{1,2}))?', date_time)

    # проверяем наличие года и дообрабатываем его
    year = date.group(4)
    if year is None:
        year = datetime.today().year
    else:
        if len(year) == 4:
            year = int(year)
        else:
            year = int(year) + 2000

    minute = time.group(3)
    # проверяем наличие минут и дообрабатываем их
    minute = int(minute) if len(minute) == 2 else 0

    # возвращаем экземпляр даты-времени
    return datetime(
        year=year,
        month=int(date.group(2)),
        day=int(date.group(1)),
        hour=int(time.group(1)),
        minute=minute
    )


def unknown_command(sender_id: str):
    message = Notice(
        'Неизвестная команда',
        [sender_id],
        datetime.now(),
        []
    )
    message_manager.send(message)


def is_opened(sender_id: str):
    message = Notice(
        room.is_opened(),
        [sender_id],
        datetime.now(),
        []
    )
    message_manager.send(message)


def open_room(sender_id: str):
    if data_manager.is_council(sender_id):
        room.open_room()
        message = Notice(
            'Лаборатория переведена в состояние ОТКРЫТО',
            [sender_id],
            datetime.now(),
            []
        )
    else:
        message = Notice(
            'У вас нет доступа к этой команде',
            [sender_id],
            datetime.now(),
            []
        )

    message_manager.send(message)


def close_room(sender_id):
    if data_manager.is_council(sender_id):
        room.close_room()
        message = Notice(
            'Лаборатория переведена в состояние ЗАКРЫТО',
            [sender_id],
            datetime.now(),
            []
        )
    else:
        message = Notice(
            'У вас нет доступа к этой команде',
            [sender_id],
            datetime.now(),
            []
        )

    message_manager.send(message)


def hello(sender_id):
    message = Notice(
        'Привет!',
        [sender_id],
        datetime.now(),
        []
    )
    message_manager.send(message)
