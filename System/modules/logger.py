import logging
import os
from logging import INFO, WARNING, ERROR
import json
import sys
from typing import Union
from System.units import notice as nt

from System import configurator

_std_format = '%(asctime)s - %(levelname)s - %(message)s'
global log


def start() -> None:
    print(f'Запуск модуля {os.path.basename(__file__)}')
    global log
    if configurator.log_out() == 'console':
        log = create_logger('message')
    else:
        log = create_logger('message', configurator.log_file())


def info(msg: str, **data) -> None:
    global log
    text = log.format_text(msg, **data)
    log.logger.info(text)


def warning(msg: str, **data) -> None:
    global log
    text = log.format_text(msg, **data)
    log.logger.warning(text)


def error(msg: str, **data) -> None:
    global log
    text = log.format_text(msg, **data)
    log.logger.error(text)


class Logger:
    """
    Класс для удобного создания объекта лога
    """

    def __init__(self, log_name: str, level):
        self.logger = logging.getLogger(log_name)  # создание логгера
        self.logger.setLevel(level)  # задание минимального уровня логирования

    def format_text(self, msg: str, **data) -> str:
        return f"msg: {msg}; data: {json.dumps(data)}"

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

    def add_console_handler(self, level, format_=_std_format, stream=sys.stdout) -> None:
        """Добавляет в логгер хэндлер для записи логов в консоль
        :param level: уровень минимального логирования хэндлера
        :param format_: формат записи логов, по умолчанию _std_format
        :param stream: поток вывода, по умолчанию - консоль"""
        message_handler = logging.StreamHandler(stream)
        message_handler.setLevel(level)
        message_handler.setFormatter(logging.Formatter(format_))
        self.logger.addHandler(message_handler)


def create_logger(name: str, log_out: str = 'console', file: str = None) -> Logger:
    """
    Возвращает объект Logger с одним хэндлером уровня INFO
    :param name: имя логгера
    :param log_out: путь вывода логов
    :param file: путь к файлу логирования
    """
    log = Logger(name, INFO)
    log.add_console_handler(ERROR)
    if log_out == 'file':
        log.add_file_handler(file, INFO)
        log.add_file_handler(file, WARNING)
        log.add_file_handler(file, ERROR)
    elif log_out == 'console':
        log.add_console_handler(INFO)
    else:
        raise ValueError('Unexpected value for log out')
    return log
