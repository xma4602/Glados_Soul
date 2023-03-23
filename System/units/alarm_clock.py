from datetime import datetime
import enum

from System.units.time_event import TimeEvent


class RegularDay(enum.Enum):
    never = -1
    everyday = 0
    monday = 1
    tuesday = 2
    wednesday = 3
    thursday = 4
    friday = 5
    saturday = 6
    sunday = 7


class AlarmClock(TimeEvent):
    count = 0

    def __init__(self, time: datetime, reg=[RegularDay.never], title=None):
        super().__init__(time)

        if RegularDay(-1) in reg and len(reg) > 1:
            raise ValueError("Недопустимые аргументы в списке повторений будильника reg")

        if title is None:
            title = f"Будильник {AlarmClock.count}"
            AlarmClock.count += 1

        self.regular = reg
        self.title = title
        self.class_name = self.__class__.__name__

    def __str__(self):
        """
        Отображает содержимое в строку
        :return: строка, представляющая экземпляр
        """
        return f"AlarmClock(title=\"{self.title}\", " \
               f"reg={self.regular}, " \
               f"time={self.time}, )"

    def postpone(self, time: datetime):
        pass

    def to_dict(self):
        dict_copy = self.__dict__.copy()
        list_of_regular = []
        for item in dict_copy['regular']:
            list_of_regular.append(item.value)
        dict_copy['regular'] = list_of_regular
        dict_copy['time'] = self.time.strftime(TimeEvent.time_format)
        return dict_copy

    @classmethod
    def from_dict(cls, alarm_data: dict):
        time = datetime.strptime(alarm_data['time'], TimeEvent.time_format)
        list_of_regular = []
        for item in alarm_data['regular']:
            list_of_regular.append(RegularDay(item))
        return AlarmClock(
            time,
            list_of_regular,
            alarm_data['title']
        )
