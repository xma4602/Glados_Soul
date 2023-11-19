import asyncio
import time

import vk_api
from requests.exceptions import ConnectionError, ReadTimeout
from urllib3.exceptions import ReadTimeoutError
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.exceptions import ApiError

import logging
from managers import command_manager, config_manager, data_manager
from src.entities.message import Message

global __commands, __texts
global __vk, __keys, __longpoll, __api, __upload
global __keyboard_user, __keyboard_council, __keyboard_club


def start():
    logging.info('Запуск модуля vk_bot')
    global __commands, __texts
    global __vk, __keys, __api, __upload
    global __keyboard_user, __keyboard_council, __keyboard_club

    __keys = config_manager.get_vk_group_data()
    __vk = vk_api.VkApi(token=__keys['api_token'])
    __api = __vk.get_api()
    __upload = vk_api.VkUpload(__vk)

    __keyboard_user = __create_keyboard_user()
    __keyboard_council = __create_keyboard_council()
    __keyboard_club = __create_keyboard_club()

    __commands = {
        'back': 'Назад',
        'about_club': 'О клубе',
        'start': 'Начать'
    }
    __texts = {
        'back': 'Возвращаюсь к главному',
        'about_club': 'Что вы хотите о нас узнать?',
        'start': "Привет! "
                 "Я бот клуба Robotic! 🤖\n\n"
                 "С моей помощью вы можете узнать: \n"
                 "🔹 о нашем клубе\n"
                 "🔹 где мы находимся\n"
                 "🔹 открыта ли лаборатория\n"
                 "🔹 какие у нас ведутся проекты и мероприятия\n\n"
                 "❓ По остальным вопросам пишите заместителю председателя [id322610705|Маркарян Петросу]"
    }

    __connect()


def __connect():
    global __longpoll
    counter = 0
    not_connected = True
    while not_connected:
        try:
            __longpoll = VkBotLongPoll(__vk, __keys['group_id'])
            not_connected = False
            logging.info(f'Соединение с VK №{counter}: установлено')
        except ConnectionError or ReadTimeout or TimeoutError or ReadTimeoutError as err:
            counter += 1
            logging.error(f'Соединение с VK №{counter}: провалено', {'error': err})
            time.sleep(10)


async def listener(loop):
    while True:
        try:
            for event in __longpoll.listen():
                await asyncio.wait([loop.create_task(__handle(event))])
        except IOError as err:
            logging.error(f'Соединение с VK: провалено', {'error': err})
            __connect()


async def __handle(event):
    if event.type == VkBotEventType.MESSAGE_NEW:
        text = event.object.get('message').get('text')
        sender_id = str(event.object.get('message').get('from_id'))
        logging.info('Получено сообщение VK', {'message': text, 'sender_id': sender_id})

        if event.from_user:
            message, board = __pre_parse(text, sender_id)
            if board is None:
                command_manager.parse(text, sender_id)
            else:
                __change_board(message, sender_id, board)


def __pre_parse(text: str, sender_id):
    if text == __commands['start']:
        return __texts['start'], __get_base_keyboard(sender_id)
    elif text == __commands['about_club']:
        return __texts['about_club'], __keyboard_club
    elif text == __commands['back']:
        return __texts['back'], __get_base_keyboard(sender_id)
    else:
        return None, None


def __change_board(message, peer_id, board):
    try:
        __api.messages.send(
            message=message,
            peer_id=int(peer_id),
            random_id=0,
            keyboard=board.get_keyboard()
        )
    except ApiError as err:
        logging.error(
            'Не удалось отправить сообщение VK',
            {'message': message.replace('\n', ' '), 'id': id, 'error': err.__str__()}
        )


def send(message: Message):
    for id in message.peer_ids:
        try:
            __api.messages.send(
                message=message.message_somebody(),
                peer_id=int(id),
                random_id=0,
            )
            logging.info(
                'Отправлено сообщение VK',
                {'message': message.message_somebody().replace('\n', ' '), 'peer_id': id}
            )
        except ApiError as err:
            logging.error(
                'Не удалось отправить сообщение VK',
                {'message': message.message_somebody().replace('\n', ' '), 'id': id, 'error': err}
            )


def send_photo(peer_id, photo_path):
    try:
        photo = __upload.photo_messages(photo_path)[0]
        owner_id = photo['owner_id']
        photo_id = photo['id']
        access_key = photo['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        __vk.messages.send(peer_id=peer_id, random_id=0, attachment=attachment)
    except ApiError as err:
        logging.error(
            'Не удалось отправить фотографию VK',
            {'photo': photo_path, 'id': id, 'error': err}
        )


def __create_keyboard_user():
    keyboard = vk_api.keyboard.VkKeyboard(one_time=False)
    keyboard.add_button("Лаборатория открыта?", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("О клубе", color=VkKeyboardColor.SECONDARY)

    return keyboard


def __create_keyboard_council():
    keyboard = __create_keyboard_user()
    keyboard.add_line()
    keyboard.add_button("Закрыть", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button("Открыть", color=VkKeyboardColor.POSITIVE)

    return keyboard


def __create_keyboard_club():
    keyboard = vk_api.keyboard.VkKeyboard(one_time=False)
    keyboard.add_button("Что такое ROBOTIC?", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    # keyboard.add_button("Проекты и мероприятия", color=VkKeyboardColor.PRIMARY)
    # keyboard.add_line()
    keyboard.add_button("Как попасть в ROBOTIC?", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Назад", color=VkKeyboardColor.NEGATIVE)

    return keyboard


def __get_base_keyboard(id):
    if data_manager.is_council(id):
        return __keyboard_council
    else:
        return __keyboard_user
