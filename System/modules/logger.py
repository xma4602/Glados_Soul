import logging
from logging import INFO, WARNING
import json
import sys
from typing import List

_std_format = '%(asctime)s - %(levelname)s - %(message)s'
global message


class Logger:
    """
    Класс для удобного создания объекта лога
    """

    def __init__(self, log_name: str, level):
        self.logger = logging.getLogger(log_name)  # создание логгера
        self.logger.setLevel(level)  # задание минимального уровня логирования

    def set_formatters(self, format_: str) -> None:
        """
        Устанавливает для всех хэндлеров логгера формат записи
        """
        formatter = logging.Formatter(format_)  # создание объекта формата
        for elem in self.logger.handlers:
            elem.setFormatter(formatter)  # установка формата для каждого хэндлера

    def add_file_handler(self, file: str, level: int, format_: str = _std_format) -> None:
        """Добавляет в логгер хэндлер для записи логов в файл
        :param file: путь к файлу для записи логов
        :param level: уровень минимального логирования хэндлера
        :param format_: формат записи логов, по умолчанию _std_format"""
        message_handler = logging.FileHandler(file)
        message_handler.setLevel(level)
        message_handler.setFormatter(logging.Formatter(format_))
        self.logger.addHandler(message_handler)

    def add_console_handler(self, level, format_=_std_format, stream=sys.stdout):
        """Добавляет в логгер хэндлер для записи логов в консоль
        :param level: уровень минимального логирования хэндлера
        :param format_: формат записи логов, по умолчанию _std_format
        :param stream: поток вывода, по умолчанию - консоль"""
        message_handler = logging.StreamHandler(stream)
        message_handler.setLevel(level)
        message_handler.setFormatter(logging.Formatter(format_))
        self.logger.addHandler(message_handler)


def log_message(_type: str, _id: str, _message: str, _status: str) -> str:
    mess_dict = {
        "type": _type,
        "user_id": _id,
        "message": _message,
        "status": _status
    }
    text = json.dumps(mess_dict, ensure_ascii=False)
    return text


def init_message(log_out: str, file_info: str, file_warning: str) -> Logger:
    """
    Создает логгер для сообщений
    :param log_out: вывод логов 'console' или 'file'
    :param file_info: путь к файлу для записи логов info
    :param file_warning: путь к файлу для записи логов warning
    """
    msg = Logger('message', INFO)
    if log_out == 'file':
        msg.add_file_handler(file_info, INFO)
        msg.add_file_handler(file_warning, WARNING)
    elif log_out == 'console':
        msg.add_console_handler(INFO)

    return msg


def mess_send_info(text: str, id):
    global message
    text = log_message('output', id, text, 'success')
    message.logger.info(text)


def mess_send_warning(text: str, id):
    global message
    text = log_message('output', id, text, 'success')
    message.logger.warning(text)


def mess_parse_info(text: str, id):
    global message
    text = log_message('input', id, text, 'success')
    message.logger.info(text)


def mess_parse_warning(text: str, id):
    global message
    text = log_message('input', id, text, 'success')
    message.logger.warning(text)


def start():
    global message

    with open('config.json', 'r') as config_file:
        configs = json.load(config_file)
        log_out = configs['logger_output']
        if log_out == 'file':
            message_file_info = configs['message_info']
            message_file_warning = configs['message_warning']

    message = init_message(log_out, message_file_info, message_file_warning)
