import asyncio
import socket
from threading import Thread

from System import message_manager, data_manager, command_manager
from System.modules import logger


def sender():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        try:
            loop.run_until_complete(message_manager.sender())
        except socket.timeout:
            continue


def listener():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        try:
            loop.run_until_complete(message_manager.listener(loop))
        except socket.timeout:
            continue


if __name__ == '__main__':
    data_manager.start()
    message_manager.start()
    command_manager.start()
    logger.start()

    listen = Thread(target=listener)
    listen.start()
    print(f"Поток прослушивания сообщений: запущен")

    send = Thread(target=sender)
    send.start()
    print(f"Поток отправки сообщений: запущен")
    print()

    for thread in [listen, send]:
        thread.join()
