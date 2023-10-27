from System.units.time_event import TimeEvent
from datetime import datetime


class Message(TimeEvent):
    """
    Атрибуты:
    """
    __slots__ = ['__title', '__peer_ids', '__description']

    def __init__(self, title: str, peer_ids: list[str], time: datetime, description: list[str] = None):
        """
        Принимает список параметров и присваивает их полям
        :param title:  заголовок уведомления
        :param peer_ids: список id получателей
        :param time: время уведомления
        :param description: описание уведомления
        """
        super().__init__(time)
        self.__title = title
        self.__description = description if description is not None else []
        self.__peer_ids = [peer_ids] if isinstance(peer_ids, str) else peer_ids

    def __str__(self):
        """
        Отображает содержимое в строку
        :return: строка, представляющая экземпляр
        """
        return f"Message(title=\"{self.__title}\", " \
               f"__peer_ids={self.__peer_ids}, " \
               f"time={super().time}, " \
               f"description={self.__description})"

    def __dict__(self):  # ОСТОРОЖНО КОСТЫЛЬ
        return {
            'time': TimeEvent.datetime_to_str(self.time),
            'title': self.title,
            'peer_ids': self.peer_ids,
            'description': self.description,
            'class_name': self.__class__.__name__,
        }

    @property
    def time(self):
        return super().time

    @property
    def title(self):
        return self.__title

    @property
    def peer_ids(self):
        return self.__peer_ids

    @property
    def description(self):
        return self.__description

    @classmethod
    def from_dict(cls, message_data: dict):
        time = TimeEvent.get_datetime(message_data)
        return Message(
            message_data['title'],
            message_data['peer_ids'],
            time,
            message_data['description'],
        )

    def message_somebody(self) -> str:
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
