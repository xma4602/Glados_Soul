import asyncio
import time

import vk_api
from requests.exceptions import ConnectionError, ReadTimeout
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.exceptions import ApiError

import logging
from System import command_manager, config_manager, data_manager

global vk, keys, longpoll, api, keyboard_user, keyboard_council


def start():
    logging.info('Запуск модуля vk_bot')
    global vk, keys, api, keyboard_user, keyboard_council
    keys = config_manager.get_vk_group_data()
    vk = vk_api.VkApi(token=keys['api_token'])
    api = vk.get_api()
    keyboard_user = create_keyboard_user()
    keyboard_council = create_keyboard_council()
    connect()


def connect():
    global longpoll
    counter = 0
    not_connected = True
    while not_connected:
        try:
            longpoll = VkBotLongPoll(vk, keys['group_id'])
            not_connected = False
            logging.info(f'Соединение с VK №{counter}: установлено')
        except ConnectionError or ReadTimeout as err:
            counter += 1
            logging.error(f'Соединение с VK №{counter}: провалено', {'error': err})
            time.sleep(10)


async def handle(event):
    if event.type == VkBotEventType.MESSAGE_NEW:
        message = event.object.get('message').get('text')
        sender_id = str(event.object.get('message').get('from_id'))
        logging.info('Получено сообщение VK', {'message': message, 'sender_id': sender_id})
        if event.from_user:
            command_manager.parse(message, sender_id)


async def listener(loop):
    while True:
        try:
            for event in longpoll.listen():
                await asyncio.wait([loop.create_task(handle(event))])
        except IOError as err:
            logging.error(f'Соединение с VK: провалено', {'error': err})
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
            logging.info('Отправлено сообщение VK', {'message': message.replace('\n', ' '), 'peer_id' :id})
        except ApiError as err:
            logging.error('Не удалось отправить сообщение VK',
                          {'message': message.replace('\n', ' '), 'id': id, 'error': err})


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
