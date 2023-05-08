import asyncio
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from System import command_manager, data_manager


keys = data_manager.get_vk_group_data()
vk = vk_api.VkApi(token=keys['api_token'])
longpoll = VkBotLongPoll(vk, keys['group_id'])
api = vk.get_api()

'''
vk_session = vk_api.VkApi(
    token='vk1.a.fW6xhIXyLDwog_FX1fRTMiyEoVZL_b0ENm2J4y5lBKZ0hefDhJylNknLzd4I72GJ6--1rNhspg41efbhbJYPX1osNLmRCi9QBKo5v2AhBszehAZKPFUCby-7EeOkHOXXl_2Cp6Z8-0Hqo3yU9FF-B5811qznwiJq-uFEq_rOmUXkHde-9RvMTvm_T4WyFFNWsCd1baqaZA1mwaB69y9TSg')
longpoll = VkBotLongPoll(vk_session, '218320118')
vk = vk_session.get_api()
'''


async def handle(event):
    if event.type == VkBotEventType.MESSAGE_NEW:
        message = event.object.get('message').get('text')
        sender_id = str(event.object.get('message').get('from_id'))
        if event.from_user:
            command_manager.parse(message, sender_id)


async def listener(loop):
    while True:
        for event in longpoll.listen():
            try:
                await asyncio.wait([loop.create_task(handle(event))])
            except Exception:
                continue
            '''            
            except urllib3.exceptions.ReadTimeoutError:
                continue
            except vk_api.exceptions.ApiError:
                continue
            except requests.exceptions.ReadTimeout:
                continue
                '''


def send(message: str, ids: list):
    for ID in ids:
        api.messages.send(
            message=message,
            peer_id=int(ID),
            random_id=0,
        )
        '''
        api.messages.send(
            key=tuple('f25124946931a230031d57ddd73e4e0efcec4b7b'),
            server=tuple('https://lp.vk.com/wh218320118'),
            ts=tuple('42'),
            
            message=message,
            peer_id=int(ID),
        )
        '''
