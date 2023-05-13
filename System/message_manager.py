import asyncio
from datetime import datetime

from System import data_manager
from System.modules import vk_bot
from System.units.notice import Notice
from System.modules.logger import Logger

# nearest_event = data_manager.start()
nearest_event = None
output = vk_bot
input = vk_bot


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
