import asyncio
from datetime import datetime

from System import data_manager, config_manager
from System.modules import vk_bot, console, logger
from System.units.notice import Notice

global nearest_event
global output
global input


def start():
    logger.info('Запуск модуля message_manager')
    global nearest_event
    global output
    global input

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

    nearest_event = data_manager.get_nearest_event()


async def listener(loop):
    await input.listener(loop)


async def sender():
    if nearest_event is not None:
        if nearest_event.time <= datetime.now():
            send_nearest_notice()
    await asyncio.sleep(60)


def send_nearest_notice():
    global nearest_event
    send(nearest_event)
    nearest_event = data_manager.get_nearest_event(nearest_event)


def send(notice: Notice):
    output.send(notice.message_somebody(), notice.recipients_id)


def plan(notices: list):
    for notice in notices:
        data_manager.store_event(notice)


def add_event(event):
    data_manager.store_event(event)
