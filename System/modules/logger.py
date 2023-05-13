import logging


class Logger:
    _log_folder = 'files\\log\\'
    _format = '%(asctime)s - %(levelname)s - %(message)s'
    message_file_info = _log_folder + 'message_info.log'
    message_file_warning = _log_folder + 'message_warning.log'
    notice_file = _log_folder + 'notice.log'

    message = logging.getLogger('message')
    notice = logging.getLogger('notice')

    message.setLevel(logging.INFO)
    notice.setLevel(logging.INFO)

    message_handlers = []
    message_handlers.append(logging.FileHandler(message_file_info))
    message_handlers[0].setLevel(logging.INFO)
    message_handlers.append(logging.FileHandler(message_file_warning))
    message_handlers[1].setLevel(logging.WARNING)

    notice_handler = logging.FileHandler(notice_file)
    notice_handler.setLevel(logging.INFO)
    notice_handler.setFormatter(logging.Formatter(_format))

    for handler in message_handlers:
        message.addHandler(handler)
        handler.setFormatter(logging.Formatter(_format))
    notice.addHandler(notice_handler)
    notice_handler.setFormatter(logging.Formatter(_format))
