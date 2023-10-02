from System.units.time_event import TimeEvent
from datetime import datetime


class Message(TimeEvent):
    """
    Атрибуты:
    """
    __slots__ = ('title', 'peer_ids', 'description', 'class_name')

    def __init__(self, title: str, peer_ids: list[str], time: datetime, description: list[str] = None):
        """
        Принимает список параметров и присваивает их полям
        :param title:  заголовок уведомления
        :param peer_ids: список id получателей
        :param time: время уведомления
        :param description: описание уведомления
        """
        super().__init__(time)
        self.title = title
        self.description = description if description is not None else []
        self.peer_ids = [peer_ids] if isinstance(peer_ids, str) else peer_ids
        self.class_name = self.__class__.__name__

    def __str__(self):
        """
        Отображает содержимое в строку
        :return: строка, представляющая экземпляр
        """
        return f"Message(title=\"{self.title}\", " \
               f"recipients_id={self.peer_ids}, " \
               f"time={self.__time}, " \
               f"description={self.description})"

    @classmethod
    def from_dict(cls, message_data: dict):
        time = TimeEvent.get_datetime(message_data)
        return Message(
            message_data['title'],
            message_data['peer_ids'],
            time,
            message_data['description'],
        )

    def message_somebody(self):
        """
        Формирует текст уведомления для одного получателя
        :return: строка текста уведомления
        """
        message = self.title + '\n\n'
        for des in self.description:
            message += des + '\n'
        return message

    def message_everyone(self):
        """
        Формирует текст уведомления для всех получателей
        :return: строка текста уведомления
        """
        message = ''
        for id in self.peer_ids:
            message += f'@{id}, '
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
