import asyncio
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.exceptions import ApiError
from requests.exceptions import ReadTimeout

from System import command_manager, data_manager
import System.modules.logger as log


def start():
    global api
    global longpoll
    keys = data_manager.get_vk_group_data()
    vk = vk_api.VkApi(token=keys['api_token'])
    longpoll = VkBotLongPoll(vk, keys['group_id'])
    api = vk.get_api()


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
        except ReadTimeout:
            start()


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
