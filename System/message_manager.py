import asyncio
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from System import data_manager, config_manager
from System.modules import vk_bot, console
from System.units.message import Message
import logging
from System.units.time_event import TimeEvent

global nearest_event
global output
global input
scheduler: BackgroundScheduler


def start():
    logging.info('Запуск модуля message_manager')
    global nearest_event
    global output
    global input
    global scheduler
    # создание объекта шедулера, в который будем все планировать
    scheduler = BackgroundScheduler()

    input = config_manager.message_in()
    if input == 'vk':
        input = vk_bot
    else:
        input = console

    output = config_manager.message_in()
    if output == 'vk':
        output = vk_bot
    else:
        output = console

    input.start()
    if input != output:
        output.start()

    # получаем ближайшее событие
    event: TimeEvent = data_manager.get_nearest_event()
    if event is not None:
        # если событие есть, то планируем его
        _plan(event)
    scheduler.start()


async def listener(loop):
    await input.listener(loop)


async def sender():
    if nearest_event is not None:
        if nearest_event.time <= datetime.now():
            send_nearest_message()
    await asyncio.sleep(60)


def send_nearest_message():
    global nearest_event
    _send(nearest_event)
    nearest_event = data_manager.get_nearest_event(nearest_event)


def _send(notice: Message):
    """Исполняет запланированное событие"""
    # отправляем запланированное сообщение
    output.send(notice.message_somebody(), notice.peer_ids)
    # получаем ближайшее событие из бд
    event = data_manager.get_nearest_event(notice)
    if event is not None:
        # если оно есть, то планируем его
        _plan(event)


def send(msg: Message):
    """
    Отправляет или планирует отправку сообщения
    :param msg: сообщение
    """
    global scheduler
    if msg.time is None:
        # если время отправки не указано, то отправляем сейчас
        output.send(msg.message_somebody(), msg.peer_ids)
    else:
        # иначе сохраняем сообщение в бд
        data_manager.store_event(msg)
        # получаем список запланированных событий из sheduler
        job = scheduler.get_jobs()  # в списке должно оказаться одно событие или не быть его
        if len(job) != 0:
            # если список не пустой, то сравниваем время msg и события из sheduler
            if msg.time < job[0].next_run_time.replace(tzinfo=None):
                # replace(...) нужен чтобы убрать часовой пояс, иначе время не сравнивается
                # next_run_time возвращает время следующего запуска события из sheduler
                job[0].remove()  # если msg должен наступить раньше, то удаляем из sheduler старое событие
                _plan(msg)  # планируем msg
        else:
            _plan(msg)  # если ничего не запланировано, то планируем msg


def _plan(msg: Message):
    """Планирует событие в sheduler"""
    scheduler.add_job(_send,  # функция, которая выполнится по истечении времени
                      'date',  # тип триггера для определения времени срабатывания
                      run_date=msg.time,  # время срабатывания триггера datetime
                      args=(msg,),  # аргументы вызываемой функции
                      misfire_grace_time=60)  # время, в течение которого задача не будет считатья просроченной


def add_event(event):
    data_manager.store_event(event)
