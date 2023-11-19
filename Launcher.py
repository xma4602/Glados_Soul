import asyncio
import logging
import socket
from threading import Thread
from managers import command_manager, data_manager, message_manager
from src.services import room, logger


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
    logger.start()
    room.start()
    logging.info('запуск лаунчера')
    data_manager.start()
    message_manager.start()
    command_manager.start()

    listen = Thread(target=listener)
    listen.start()
    print(f"\nПоток прослушивания сообщений: запущен")

    send = Thread(target=sender)
    send.start()
    print(f"Поток отправки сообщений:      запущен")
    print()

    for thread in [listen, send]:
        thread.join()
