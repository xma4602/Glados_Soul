import asyncio
import time

import vk_api
from requests.exceptions import ConnectionError, ReadTimeout
from urllib3.exceptions import ReadTimeoutError
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.exceptions import ApiError

import logging
from System import command_manager, config_manager, data_manager

global vk, keys, longpoll, api
global keyboard_user, keyboard_council, keyboard_club


def start():
    logging.info('Запуск модуля vk_bot')
    global vk, keys, api
    global keyboard_user, keyboard_council, keyboard_club

    keys = config_manager.get_vk_group_data()
    vk = vk_api.VkApi(token=keys['api_token'])
    api = vk.get_api()

    keyboard_user = create_keyboard_user()
    keyboard_council = create_keyboard_council()
    keyboard_club = create_keyboard_club()

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
        except ConnectionError or ReadTimeout or TimeoutError or ReadTimeoutError as err:
            counter += 1
            logging.error(f'Соединение с VK №{counter}: провалено', {'error': err})
            time.sleep(10)


async def listener(loop):
    while True:
        try:
            for event in longpoll.listen():
                await asyncio.wait([loop.create_task(handle(event))])
        except IOError as err:
            logging.error(f'Соединение с VK: провалено', {'error': err})
            connect()


async def handle(event):
    if event.type == VkBotEventType.MESSAGE_NEW:
        message = event.object.get('message').get('text')
        sender_id = str(event.object.get('message').get('from_id'))
        logging.info('Получено сообщение VK', {'message': message, 'sender_id': sender_id})

        if event.from_user:
            msg, board = change_board(message, sender_id)
            if board is None:
                command_manager.parse(message, sender_id)
            else:
                send(msg, [sender_id], board)


def change_board(text: str, sender_id):
    if text == 'О клубе':
        return 'Что вы хотите о нас узнать?', keyboard_club
    elif text == 'Начать':
        return "Привет! " \
               "Я бот клуба Robotic! 🤖\n\n" \
               "С моей помощью вы можете узнать: \n" \
               "🔹 о нашем клубе\n" \
               "🔹 где мы находимся\n" \
               "🔹 открыта ли лаборатория\n" \
               "🔹 какие у нас ведутся проекты и мероприятия\n\n" \
               "❓ По остальным вопросам пишите заместителю председателя [id322610705|Маркарян Петросу]", \
            get_base_keyboard(sender_id)
    elif text == 'Назад':
        return 'Возвращаюсь к главному', get_base_keyboard(sender_id)
    else:
        return None, None


def get_base_keyboard(id):
    if data_manager.is_council(id):
        return keyboard_council
    else:
        return keyboard_user


def send(message: str, ids: list, board=None):
    for id in ids:
        try:
            if board is None:
                api.messages.send(
                    message=message,
                    peer_id=int(id),
                    random_id=0,
                )
            else:
                api.messages.send(
                    message=message,
                    peer_id=int(id),
                    random_id=0,
                    keyboard=board.get_keyboard()
                )

            logging.info('Отправлено сообщение VK', {'message': message.replace('\n', ' '), 'peer_id': id})
        except ApiError as err:
            logging.error('Не удалось отправить сообщение VK',
                          {'message': message.replace('\n', ' '), 'id': id, 'error': err})


def create_keyboard_user():
    keyboard = vk_api.keyboard.VkKeyboard(one_time=False)
    keyboard.add_button("Лаборатория открыта?", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("О клубе", color=VkKeyboardColor.SECONDARY)

    return keyboard


def create_keyboard_council():
    keyboard = create_keyboard_user()
    keyboard.add_line()
    keyboard.add_button("Закрыть", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button("Открыть", color=VkKeyboardColor.POSITIVE)

    return keyboard


def create_keyboard_club():
    keyboard = vk_api.keyboard.VkKeyboard(one_time=False)
    keyboard.add_button("Что такое ROBOTIC?", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    # keyboard.add_button("Проекты и мероприятия", color=VkKeyboardColor.PRIMARY)
    # keyboard.add_line()
    keyboard.add_button("Как попасть в ROBOTIC?", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Назад", color=VkKeyboardColor.NEGATIVE)

    return keyboard
