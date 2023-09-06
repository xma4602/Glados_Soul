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

    event: TimeEvent = data_manager.get_nearest_event()
    if event is not None:
        _plan(event)
    scheduler.start()


async def listener(loop):
    await input.listener(loop)


async def sender():
    if nearest_event is not None:
        if nearest_event.time <= datetime.now():
            send_nearest_notice()
    await asyncio.sleep(60)


def send_nearest_notice():
    global nearest_event
    _send(nearest_event)
    nearest_event = data_manager.get_nearest_event(nearest_event)


def _send(notice: Message):
    output.send(notice.message_somebody(), notice.recipients_id)
    event = data_manager.get_nearest_event(notice)
    if event is not None:
        _plan(event)


def send(msg: Message):
    global scheduler
    if msg.time is None:
        output.send(msg.message_somebody(), msg.recipients_id)
    else:
        data_manager.store_event(msg)
        job = scheduler.get_jobs()
        if len(job)!=0:
            if msg.time < job[0].next_run_time.replace(tzinfo=None):
                job[0].remove()
        _plan(msg)


def _plan(msg: Message):
    scheduler.add_job(_send, 'date', run_date=msg.time, args=(msg,), misfire_grace_time=60)


def add_event(event):
    data_manager.store_event(event)
