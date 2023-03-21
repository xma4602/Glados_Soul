from System.units.time_event import TimeEvent
from datetime import datetime


class Notice(TimeEvent):
    """
    Атрибуты:
    """


    def __init__(self, title: str, recipients_id: list, time: datetime, description: list):
        """
        Принимает список параметров и присваивает их полям
        :param notice_data: список параметров
        """
        super().__init__(time)
        self.title = title
        self.recipients_id = recipients_id
        self.description = description
        self.class_name = self.__class__.__name__


    def __str__(self):
        """
        Отображает содержимое в строку
        :return: строка, представляющая экземпляр
        """
        return f"Notice(title=\"{self.title}\", " \
               f"recipients_id={self.recipients_id}, " \
               f"time={self.time}, " \
               f"description={self.description})"

    @classmethod
    def from_dict(cls, notice_data: dict):
        time = TimeEvent.get_datetime(notice_data)
        return Notice(
            notice_data['title'],
            notice_data['recipients_id'],
            time,
            notice_data['description'],
        )

    def message_everyone(self):
        """
        Формирует текст уведомления для всех получателей
        :return: строка текста уведомления
        """
        message = ''
        for recipient in self.recipients_id:
            message += f'@{recipient}, '
        # удаление лишней пунктуации
        message = message[:-2] + '\n'
        message += self.title + '\n\n'
        for des in self.description:
            message += des + '\n'

        return message

    def to_dict(self):
        dict_copy = self.__dict__.copy()
        dict_copy['time'] = dict_copy['time'].strftime(TimeEvent.time_format)
        return dict_copy
