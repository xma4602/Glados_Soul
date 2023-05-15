import asyncio
import socket
from threading import Thread

from System import message_manager
from System import data_manager
from System import command_manager

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

    threads = []
    print(f"Поток прослушивания сообщений: запущен")
    t = Thread(target=listener)
    threads.append(t)
    t.start()

    print(f"Поток отправки сообщений: запущен")
    t = Thread(target=sender)
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
