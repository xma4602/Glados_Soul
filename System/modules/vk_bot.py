import asyncio
import os
import time
from http.client import RemoteDisconnected

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.exceptions import ApiError
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError

from System import command_manager, configurator
import System.modules.logger as log

global vk, keys, longpoll, api


def start():
    print(f'Запуск модуля {os.path.basename(__file__)}')
    global vk, keys, api
    keys = configurator.get_vk_group_data()
    vk = vk_api.VkApi(token=keys['api_token'])
    api = vk.get_api()
    connect()


def connect():
    global longpoll
    connection_try_counter = 0
    not_connected = True
    while not_connected:
        try:
            longpoll = VkBotLongPoll(vk, keys['group_id'])
            not_connected = False
            log.vk_connect()
        except ConnectionError as err:
            connection_try_counter += 1
            log.vk_connect_error(connection_try_counter, err)
            time.sleep(10)


async def handle(event):
    if event.type == VkBotEventType.MESSAGE_NEW:
        message = event.object.get('message').get('text')
        sender_id = str(event.object.get('message').get('from_id'))
        log.mess_input_info(message, sender_id)
        if event.from_user:
            command_manager.parse(message, sender_id)


async def listener(loop):
    while True:
        try:
            for event in longpoll.listen():
                await asyncio.wait([loop.create_task(handle(event))])
        except IOError as err:
            log.vk_listener_error(err)
            connect()


def send(message: str, ids: list):
    for ID in ids:
        try:
            api.messages.send(
                message=message,
                peer_id=int(ID),
                random_id=0,
            )
            message = message.replace('\n', ' ')
            log.mess_output_info(message, ID)
        except ApiError:
            log.mess_output_warning(message, ID)
