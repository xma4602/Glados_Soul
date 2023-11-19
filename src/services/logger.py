import logging
from managers import config_manager
import sys


def start():
    print('Запуск логгера')
    # формат вывода логов
    log_format = '%(asctime)s - %(levelname)s - %(message)s - %(args)s'

    output = config_manager.log_out()
    if output == 'file':
        file_handler = logging.FileHandler(config_manager.log_file())
        file_handler.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.ERROR)
        handlers = [file_handler, stream_handler]
    elif output == 'console':
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        handlers = [stream_handler]
    else:
        raise ValueError('Unexpected value for log out')

    logging.basicConfig(
        handlers=handlers,
        level=config_manager.log_level(),
        format=log_format
    )
