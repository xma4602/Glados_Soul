import asyncio
import os
import time

import vk_api
from requests.exceptions import ConnectionError
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.exceptions import ApiError

import System.modules.logger as log
from System import command_manager, configurator, data_manager

global vk, keys, longpoll, api, keyboard_user, keyboard_council


def start():
    print(f'Запуск модуля {os.path.basename(__file__)}')
    global vk, keys, api, keyboard_user, keyboard_council
    keys = configurator.get_vk_group_data()
    vk = vk_api.VkApi(token=keys['api_token'])
    api = vk.get_api()
    keyboard_user = create_keyboard_user()
    keyboard_council = create_keyboard_council()
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
    for id in ids:
        if data_manager.is_council(id):
            board = keyboard_council
        else:
            board = keyboard_user
        try:
            api.messages.send(
                message=message,
                peer_id=int(id),
                random_id=0,
                keyboard=board.get_keyboard()
            )
            message = message.replace('\n', ' ')
            log.mess_output_info(message, id)
        except ApiError as err:
            print(err)
            log.mess_output_warning(message, id)


def create_keyboard_user():
    keyboard = vk_api.keyboard.VkKeyboard(one_time=False)
    # False Если клавиатура должна оставаться открытой после нажатия на кнопку
    # True если она должна закрываться

    keyboard.add_button("Лаборатория открыта?", color=VkKeyboardColor.PRIMARY)

    return keyboard


def create_keyboard_council():
    keyboard = create_keyboard_user()
    keyboard.add_line()  # Обозначает добавление новой строки
    keyboard.add_button("Закрыть", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button("Открыть", color=VkKeyboardColor.POSITIVE)

    return keyboard
