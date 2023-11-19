import logging
import sys

from managers import command_manager
from src.entities.message import Message


def start():
    logging.info('Запуск модуля console')


def send(msg: Message):
    print(msg.message_somebody())


async def listener(loop):
    command = ''
    while True:
        try:
            input_str = await loop.run_in_executor(None, sys.stdin.read)
            if input_str == '    \n':
                command_manager.parse(command, '0')
                command = ''
            else:
                command += input_str
        except IOError as err:
            logging.error(f'Ошибка потока ввода', {'error': err})
