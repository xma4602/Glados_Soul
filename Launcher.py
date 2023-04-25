import asyncio
import socket
from threading import Thread

import requests
import urllib3
from vk_api import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from System import command_manager, message_manager
from System.modules.bot import longpoll


async def handle(event):
    if event.type == VkBotEventType.MESSAGE_NEW:
        message = event.object.get('message').get('text')
        sender_id = str(event.object.get('message').get('from_id'))
        if event.from_user:
            command_manager.parse(message, sender_id)


async def sender():
    if message_manager.check_time():
        message_manager.send_nearest_notice()
    await asyncio.sleep(60)


async def listener(loop):
    while True:
        for event in longpoll.listen():
            try:
                await asyncio.wait([loop.create_task(handle(event))])
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

    print(f"Запускаю поток прослушивания сообщений")
    t = Thread(target=main, args=[0])
    threads.append(t)
    t.start()

    print(f"Запускаю поток отправки сообщений")
    t = Thread(target=main, args=[1])
    threads.append(t)
    t.start()

    for thread in threads:
        thread.join()

'''
import System.command_manager as cm
import System.modules.console as disp
""" Включение лаунчера - включает гладос """
_way = "/home/pi/Desktop/Glados_Soul"
# os.chdir(_way)
global state
state = True# выключатель

while (state):
    answer = input("\nВведите команду: ").strip()
    answer = " ".join(answer.split()).split()

    if len(answer) == 0:
        continue
    elif len(answer) == 1:
        res = cm.execute(answer[0], [])
    else:
        res = cm.execute(answer[0], answer[1:])

    if res == "exit":
        disp.show("Гладос остановлен")
        state = False
    else:
        disp.show(res)
'''
