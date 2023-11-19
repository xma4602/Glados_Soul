# -*- coding: utf-8 -*-
import logging
from logging import INFO, ERROR
import sys

from managers import config_manager


class Logger:
    """
    Класс для удобного создания объекта лога
    """
    log_format = '%(asctime)s - %(levelname)s - %(message)s - %(args)s'

    def __init__(self, name: str, level, log_out: str, file_path: str):
        self.logger = logging.getLogger(name)  # создание логгера
        self.logger.setLevel(level)  # задание минимального уровня логирования

        if log_out == 'file':
            self.add_file_handler(INFO, file_path)
            self.add_console_handler(ERROR)
        elif log_out == 'console':
            self.add_console_handler(INFO)
        else:
            raise ValueError('Unexpected value for log out')

    def add_file_handler(self, level: int, file: str, ) -> None:
        """Добавляет в логгер хэндлер для записи логов в файл
        :param file: путь к файлу для записи логов
        :param level: уровень минимального логирования хэндлера
        """
        handler = logging.FileHandler(file)
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(self.log_format))

        self.logger.addHandler(handler)

    def add_console_handler(self, level, stream=sys.stdout) -> None:
        """Добавляет в логгер хэндлер для записи логов в консоль
        :param level: уровень минимального логирования хэндлера
        :param stream: поток вывода, по умолчанию - консоль"""
        handler = logging.StreamHandler(stream)
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(self.log_format))

        self.logger.addHandler(handler)


print('Запуск модуля logger')
log = Logger('main_logger',
             config_manager.log_level(),
             config_manager.log_out(),
             config_manager.log_file()
             )


def info(massage: str, **data) -> None:
    global log
    if len(data) == 0:
        log.logger.info(massage)
    else:
        log.logger.info(massage, data)


def warning(massage: str, **data) -> None:
    global log
    if len(data) == 0:
        log.logger.warning(massage)
    else:
        log.logger.warning(massage, data)


def error(massage: str, **data) -> None:
    global log
    if len(data) == 0:
        log.logger.error(massage)
    else:
        log.logger.error(massage, data)
