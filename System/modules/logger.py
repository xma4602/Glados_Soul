import logging
from logging import INFO, WARNING
import json
import sys

mess_in_file = False

_log_folder = 'System\\files\\log\\'
_std_format = '%(asctime)s - %(levelname)s - %(message)s'
message_file_info = _log_folder + 'message_info.log'
message_file_warning = _log_folder + 'message_warning.log'
notice_file = _log_folder + 'notice.log'


class Logger:
    def __init__(self, log_name: str, level):
        self._logger = logging.getLogger(log_name)
        self._log_name = log_name
        self._logger.setLevel(level)

    def add_handlers(self, handlers: list):
        for elem in handlers:
            self._logger.addHandler(elem)

    def set_formatters(self, format_: str):
        formatter = logging.Formatter(format_)
        for elem in self._logger.handlers:
            elem.setFormatter(formatter)

    def add_file_handler(self, file: str, level, format_=_std_format):
        message_handler = logging.FileHandler(file)
        message_handler.setLevel(level)
        message_handler.setFormatter(logging.Formatter(format_))
        self._logger.addHandler(message_handler)

    def add_console_handler(self, level, format_=_std_format, stream=sys.stdout):
        message_handler = logging.StreamHandler(stream)
        message_handler.setLevel(level)
        message_handler.setFormatter(logging.Formatter(format_))
        self._logger.addHandler(message_handler)


def mess_start():
    global message
    if mess_in_file:
        message.add_file_handler(message_file_info, INFO)
        message.add_file_handler(message_file_warning, WARNING)
    else:
        message.add_console_handler(INFO)
    return message


def start():
    mess_start()


def mess_info(text: str, ID):
    global message
    text = f"'{text}' send to id:{ID}"
    message._logger.info(text)


def mess_warning(text: str, ID):
    global message
    text = f"'{text}' FAILED send to id:{ID}"
    message._logger.warning(text)


message = Logger('message', INFO)
# notice = logging.getLogger('notice')
#
#
# notice.setLevel(logging.INFO)
#
# message_handlers = []
# message_handlers.append(logging.FileHandler(message_file_info))
# message_handlers[0].setLevel(logging.INFO)
# message_handlers.append(logging.FileHandler(message_file_warning))
# message_handlers[1].setLevel(logging.WARNING)
#
# notice_handler = logging.FileHandler(notice_file)
# notice_handler.setLevel(logging.INFO)
#     notice_handler.setFormatter(logging.Formatter(_format))
#
# for handler in message_handlers:
#     message.addHandler(handler)
#     handler.setFormatter(logging.Formatter(_format))
# notice.addHandler(notice_handler)
# notice_handler.setFormatter(logging.Formatter(_format))
