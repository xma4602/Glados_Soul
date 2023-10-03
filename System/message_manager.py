import asyncio
import logging

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from System import data_manager, config_manager
from System.modules import vk_bot, console
from System.units.message import Message
from System.data_manager import _check_fired_events

global __nearest_event
global __output
global __input
__scheduler: BackgroundScheduler


def start():
    logging.info('Запуск модуля message_manager')
    global __nearest_event
    global __output
    global __input
    global __scheduler
    # создание объекта шедулера, в который будем все планировать
    _check_fired_events()
    __scheduler = BackgroundScheduler()

    __input = config_manager.message_in()
    if __input == 'vk':
        __input = vk_bot
    else:
        __input = console

    __output = config_manager.message_in()
    if __output == 'vk':
        __output = vk_bot
    else:
        __output = console

    __input.start()
    if __input != __output:
        __output.start()

    __nearest_event = data_manager.get_nearest_event()
    # получаем ближайшее событие
    # event: TimeEvent = data_manager.get_nearest_event()
    # if event is not None:
    # если событие есть, то планируем его
    #   _plan(event)
    # scheduler.start()


async def listener(loop):
    await __input.listener(loop)


async def sender():
    global __nearest_event
    if __nearest_event is not None:
        if __nearest_event.time <= datetime.now():
            __output.send(__nearest_event)
            __nearest_event = data_manager.get_nearest_event(__nearest_event)
    await asyncio.sleep(30)


def send(msg: Message):
    if msg <= datetime.now():
        __output.send(msg)
    else:
        global __nearest_event
        if __nearest_event is None or msg <= __nearest_event:
            __nearest_event = msg
        data_manager.store_event(msg)

# def send_nearest_message():
#     global nearest_event
#     _send(nearest_event)
#     nearest_event = data_manager.get_nearest_event(nearest_event)
#
#
# def _send(message: Message):
#     """Исполняет запланированное событие"""
#     # отправляем запланированное сообщение
#     output.send(message)
#     # получаем ближайшее событие из бд
#     event = data_manager.get_nearest_event(message)
#     if event is not None:
#         # если оно есть, то планируем его
#         _plan(event)
#
#
# def send(msg: Message):
#     """
#     Отправляет или планирует отправку сообщения
#     :param msg: сообщение
#     """
#     global scheduler
#     if msg.time is None:
#         # если время отправки не указано, то отправляем сейчас
#         output.send(msg.message_somebody(), msg.peer_ids)
#     else:
#         data_manager.store_event(msg)  # иначе сохраняем сообщение в бд
#         jobs = scheduler.get_jobs()  # получаем список запланированных событий из scheduler
#
#         if len(jobs) != 0:  # в списке должно оказаться одно событие или не быть его
#             # если список не пустой, то сравниваем время msg и события из scheduler
#             if msg.time < jobs[0].next_run_time.replace(tzinfo=None):
#                 # next_run_time возвращает время следующего запуска события из scheduler
#                 # replace(...) нужен чтобы убрать часовой пояс, иначе время не сравнивается.
#                 jobs[0].remove()  # если msg должен наступить раньше, то удаляем из scheduler старое событие
#                 _plan(msg)  # планируем msg
#         else:
#             _plan(msg)  # если ничего не запланировано, то планируем msg
#
#
# def _plan(msg: Message):
#     """Планирует событие в scheduler"""
#     scheduler.add_job(_send,  # функция, которая выполнится по истечении времени
#                       'date',  # тип триггера для определения времени срабатывания
#                       run_date=msg.time,  # время срабатывания триггера datetime
#                       args=(msg,),  # аргументы вызываемой функции
#                       misfire_grace_time=60)  # время, в течение которого задача не будет считаться просроченной
