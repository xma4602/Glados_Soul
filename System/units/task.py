from datetime import datetime
from datetime import timedelta

from System import data_manager
from System.units.message import Message


class Task:
    """
    Класс реализующий хранение атрибутов задачи.

    Атрибуты:

    * title: заголовок - string
    * manager_id: id создателя int
    * performers_id: id исполнителей int[]
    * deadline: дедлайн выполнения datetime
    * description: описание string[]

    """

    def __init__(self, title: str, manager_id: str, performers_id: list, deadline: datetime, description: list):
        self.title = title
        self.manager_id = manager_id
        self.performers_id = performers_id
        self.deadline = deadline
        self.description = description

    def __str__(self):
        """
        Отображает содержимое в строку
        :return: строка, представляющая экземпляр
        """
        return f"Task(title=\"{self.title}\", " \
               f"manager_id={self.manager_id}, " \
               f"performers_id={self.performers_id}, " \
               f"deadline={self.deadline}, " \
               f"description={self.description})"

    def notice_recipients(self) -> Message:
        return Message(
            title='Вам поступила новая задача от ' + data_manager.id_to_names([self.manager_id])[0],
            recipients_id=self.performers_id,
            time=datetime.now(),
            description=[self.title] + self.description
        )

    def notice_deadlines(self) -> list:
        notices = []

        # если остаток больше часа, ставим напоминание за час
        remaining = (self.deadline - datetime.now()).total_seconds() // 3600
        if remaining >= 1:
            notices.append(
                Message(
                    title=f'Остался один час до окончания задачи \"{self.title}\"',
                    recipients_id=self.performers_id,
                    time=self.deadline - timedelta(hours=1),
                    description=[self.title] + self.description
                )
            )

            # если остаток больше дня, ставим напоминание за день
            remaining = (self.deadline - datetime.now()).days
            if remaining >= 1:
                notices.append(
                    Message(
                        title=f'Остался один день до окончания задачи \"{self.title}\"',
                        recipients_id=self.performers_id,
                        time=self.deadline - timedelta(days=1),
                        description=[self.title] + self.description
                    )
                )
                # если остаток больше недели, ставим напоминание за неделю
                if remaining >= 7:
                    notices.append(
                        Message(
                            title=f'Осталась одна неделя до окончания задачи \"{self.title}\"',
                            recipients_id=self.performers_id,
                            time=self.deadline - timedelta(days=7),
                            description=[self.title] + self.description
                        )
                    )

        return notices
