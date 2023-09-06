import asyncio
from datetime import datetime

from System import data_manager, config_manager
from System.modules import vk_bot, console
from System.units.message import Message
import logging
global nearest_event
global output
global input


def start():
    logging.info('Запуск модуля message_manager')
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
            send_nearest_message()
    await asyncio.sleep(60)


def send_nearest_message():
    global nearest_event
    send(nearest_event)
    nearest_event = data_manager.get_nearest_event(nearest_event)


def send(message: Message):
    output.send(message)


def plan(messages: list):
    for message in messages:
        data_manager.store_event(message)


def add_event(event):
    data_manager.store_event(event)
