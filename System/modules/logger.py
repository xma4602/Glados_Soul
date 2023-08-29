import logging
import os
from logging import INFO, WARNING
import json
import sys
from typing import Union
from System.units import notice as nt

from System import configurator

_std_format = '%(asctime)s - %(levelname)s - %(message)s'
global message  # объект логирования сообщений
global data  # объект логирования записи данных
global notice  # объект логирования уведомлений


def start():
    print(f'Запуск модуля {os.path.basename(__file__)}')
    global message, data, notice

    if configurator.log_out() == 'console':
        message = create_logger('message')
        data = create_logger('data')
        notice = create_logger('notice')
    else:
        message = create_logger('message', configurator.log_message_file())
        data = create_logger('data', configurator.log_data_file())
        notice = create_logger('notice', configurator.log_notice_file())


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

    def add_console_handler(self, level, format_=_std_format, stream=sys.stdout) -> None:
        """Добавляет в логгер хэндлер для записи логов в консоль
        :param level: уровень минимального логирования хэндлера
        :param format_: формат записи логов, по умолчанию _std_format
        :param stream: поток вывода, по умолчанию - консоль"""
        message_handler = logging.StreamHandler(stream)
        message_handler.setLevel(level)
        message_handler.setFormatter(logging.Formatter(format_))
        self.logger.addHandler(message_handler)


def message_to_text(_type: str, _id: str, _message: str, _status: str) -> str:
    """
    Формирует текст лога сообщений
    :param _type: тип сообщения 'output' или 'input'
    :param _id: id отправителя/получателя
    :param _message: текст сообщения
    :param _status: 'fail' или 'success'
    """
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
    else:
        raise ValueError('Unexpected value for log out')

    return msg


def create_logger(name: str, log_out: str = 'console', file: str = None) -> Logger:
    """
    Возвращает объект Logger с одним хэндлером уровня INFO
    :param name: имя логгера
    :param log_out: путь вывода логов
    :param file: путь к файлу логирования
    """
    log = Logger(name, INFO)
    if log_out == 'file':
        log.add_file_handler(file, INFO)
    elif log_out == 'console':
        log.add_console_handler(INFO)
    else:
        raise ValueError('Unexpected value for log out')
    return log


def mess_output_info(text: str, _id: str):
    """
    Функция для записи лога исходящего сообщения уровня INFO
    :param text: текст сообщения
    :param _id: id получателя сообщения
    """
    global message
    text = message_to_text('output', _id, text, 'success')
    message.logger.info(text)


def mess_output_warning(text: str, _id: str) -> None:
    """
    Функция для записи лога исходящего сообщения уровня WARNING
    :param text: текст сообщения
    :param _id: id получателя сообщения
    """
    global message
    text = message_to_text('output', _id, text, 'fail')
    message.logger.warning(text)


def mess_input_info(text: str, _id: str) -> None:
    """
    Функция для записи лога входящего сообщения уровня INFO
    :param text: текст сообщения
    :param _id: id отправителя сообщения
    """
    global message
    text = message_to_text('input', _id, text, 'success')
    message.logger.info(text)


def mess_input_warning(text: str, _id: str):
    """
    Функция для записи лога входящего сообщения уровня WARNING
    :param text: текст сообщения
    :param _id: id отправителя сообщения
    """
    global message
    text = message_to_text('input', _id, text, 'fail')
    message.logger.warning(text)


def vk_connect_error(attempt_number: int, error):
    """
    Функция для записи лога попытки подключения уровня WARNING
    :param attempt_number: номер попытки подключения
    :param error: подробности ошибки подключения
    """
    global message
    text = f'Ошибка подключения к VK №{attempt_number}: {error}'
    message.logger.warning(text)


def vk_connect():
    """
    Функция для записи лога попытки подключения уровня WARNING
    """
    global message
    text = f'Подключение к VK: выполнено'
    message.logger.info(text)


def vk_listener_error(error):
    """
    Функция для записи лога попытки подключения уровня WARNING
    :param attempt_number: номер попытки подключения
    :param error: подробности ошибки подключения
    """
    global message
    text = f'Ошибка модуля vk_bot: {error}'
    message.logger.warning(text)


def data_log_read(file: str, _data: Union[dict, list]) -> None:
    global data
    pass


def data_log_write(file: str, _data: Union[dict, list]) -> None:
    pass


def data_event_del(file: str, event: dict) -> None:
    pass


def data_event_add(file: str, event: dict) -> None:
    pass


def notice_to_text(obj: dict) -> str:
    pass


def notice_create(obj) -> None:
    global notice
    txt = notice_to_text(obj.to_dict())
    notice.logger.info(txt)


def notice_send() -> None:
    pass
