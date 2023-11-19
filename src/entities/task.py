from datetime import datetime
from datetime import timedelta

from managers import data_manager
from src.entities.message import Message
from src.entities.time_event import TimeEvent


class Task(TimeEvent):
    """
    Класс реализующий хранение атрибутов задачи.

    Атрибуты:

    * title: заголовок - string
    * manager_id: id создателя int
    * performers_id: id исполнителей int[]
    * time: дедлайн выполнения datetime
    * description: описание string[]

    """
    __slots__ = ('__title', '__manager_id', '__performers_id', '__description')

    def __init__(self, title: str, manager_id: str, performers_id: list[str], time: datetime, description: list[str]):
        super().__init__(time)
        self.__title = title
        self.__manager_id = manager_id
        if isinstance(performers_id, str):
            performers_id = [performers_id]
        self.__performers_id = performers_id
        self.__description = description

    @property
    def title(self):
        return self.__title

    @property
    def manager_id(self):
        return self.__manager_id

    @property
    def performers_id(self):
        return self.__performers_id

    @property
    def description(self):
        return self.__description

    def __str__(self):
        """
        Отображает содержимое в строку
        :return: строка, представляющая экземпляр
        """
        return f"Task(title=\"{self.title}\", " \
               f"manager_id={self.manager_id}, " \
               f"performers_id={self.performers_id}, " \
               f"time={self.__time}, " \
               f"description={self.__description})"

    def message_recipients(self) -> Message:
        return Message(
            title='Вам поступила новая задача от ' + data_manager.id_to_names([self.manager_id])[0],
            peer_ids=self.performers_id,
            time=datetime.now(),
            description=[self.title] + self.__description
        )

    def message_deadlines(self) -> list:
        messages = []

        # если остаток больше часа, ставим напоминание за час
        remaining = (self.__time - datetime.now()).total_seconds() // 3600
        if remaining >= 1:
            messages.append(
                Message(
                    title=f'Остался один час до окончания задачи \"{self.title}\"',
                    peer_ids=self.performers_id,
                    time=self.__time - timedelta(hours=1),
                    description=[self.title] + self.__description
                )
            )

            # если остаток больше дня, ставим напоминание за день
            remaining = (self.__time - datetime.now()).days
            if remaining >= 1:
                messages.append(
                    Message(
                        title=f'Остался один день до окончания задачи \"{self.title}\"',
                        peer_ids=self.performers_id,
                        time=self.__time - timedelta(days=1),
                        description=[self.title] + self.__description
                    )
                )
                # если остаток больше недели, ставим напоминание за неделю
                if remaining >= 7:
                    messages.append(
                        Message(
                            title=f'Осталась одна неделя до окончания задачи \"{self.title}\"',
                            peer_ids=self.performers_id,
                            time=self.__time - timedelta(days=7),
                            description=[self.title] + self.__description
                        )
                    )

        return messages
