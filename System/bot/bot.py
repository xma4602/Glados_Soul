import asyncio
import socket
from threading import Thread

import requests
import urllib3
import vk_api, vk
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from System.bot import message_manager

vk_session = vk_api.VkApi(
    token='vk1.a.fW6xhIXyLDwog_FX1fRTMiyEoVZL_b0ENm2J4y5lBKZ0hefDhJylNknLzd4I72GJ6--1rNhspg41efbhbJYPX1osNLmRCi9QBKo5v2AhBszehAZKPFUCby-7EeOkHOXXl_2Cp6Z8-0Hqo3yU9FF-B5811qznwiJq-uFEq_rOmUXkHde-9RvMTvm_T4WyFFNWsCd1baqaZA1mwaB69y9TSg')
longpoll = VkBotLongPoll(vk_session, '218320118')
vk = vk_session.get_api()


def send(message: str, ids: list):
    for ID in ids:
        vk.messages.send(
            key=tuple('f25124946931a230031d57ddd73e4e0efcec4b7b'),
            server=tuple('https://lp.vk.com/wh218320118'),
            ts=tuple('42'),
            random_id=0,
            message=message,
            peer_id=int(ID),
        )


async def bot(event):
    if event.type == VkBotEventType.MESSAGE_NEW:
        message = event.object.message.get('text').lower()
        sender_id = list(event.object.values())[0].get('from_id')
        if event.from_user:
            message_manager.new_message(message, sender_id)


async def sender():
    pass

    await asyncio.sleep(60)
async def listener(loop):
    while True:
        for event in longpoll.listen():
            try:
                await asyncio.wait([loop.create_task(bot(event))])
            except socket.timeout:
                continue
            except urllib3.exceptions.ReadTimeoutError:
                continue
            except vk_api.exceptions.ApiError:
                continue
            except requests.exceptions.ReadTimeout:
                continue


def main(func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        try:
            if func == 0:
                loop.run_until_complete(listener(loop))
            if func == 1:
                loop.run_until_complete(sender())
        except socket.timeout:
            continue
        except urllib3.exceptions.ReadTimeoutError:
            continue
        except vk_api.exceptions.ApiError:
            continue
        except requests.exceptions.ReadTimeout:
            continue


if __name__ == '__main__':
    threads = []
    for i in range(0, 2):
        print(f"Запускаю поток {i}")
        t = Thread(target=main, args=[i])
        threads.append(t)
        t.start()
    for i in threads:
        i.join()
