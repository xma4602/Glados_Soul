from System import DataManager
from System.bot.notice import Notice
from System.bot.task import Task
from datetime import datetime
import System.ConsoleManager as ConsoleManager
import re
from System.units.time.AlarmClock import AlarmClock
from System.units.time.Notice import Notice
from System.units.time.Timer import Timer

nearest_event = DataManager.get_nearest_event()

def check_time():
    return nearest_notice.time <= datetime.now()


def send_nearest_notice():
    global nearest_notice
    if nearest_notice is not None:
        send(nearest_notice)
        nearest_notice = DataManager.get_nearest_notice()


def new_task(task: Task):
    send(task.notice_recipients())
    plan(task.notice_deadlines())


def send(notice: Notice):
    # vk_bot.send(notice.message_everyone())
    pass


def plan(notices: list):
    for notice in notices:
        DataManager.store_notice(notice)




def parse(time: str):
    # регуляркой находим дату
    date = re.search(r'(\d{1,2})\.(\d{1,2})(.(\d{2,4}))?', time)
    # удаляем дату из текста
    time = time.replace(date[0], '')
    # регуляркой находим время
    time = re.search(r'(\d{1,2})([: ](\d{1,2}))?', time)
    # проверяем наличие года и дообрабатываем его
    year = date.group(4)
    if year is None:
        year = datetime.today().year
    else:
        if len(year) == 4:
            year = int(year)
        else:
            year = int(year) + 2000

    # проверяем наличие минут и дообрабатываем их
    minute = int(time.group(2)) if len(time.groups()) == 2 else 0

    # возвращаем экземпляр даты-времени
    return datetime(
        year=year,
        month=int(date.group(2)),
        day=int(date.group(1)),
        hour=int(time.group(1)),
        minute=minute
    )

def start(self):
    while True:
        if self.nearest_event < datetime.now():
            ConsoleManager.show(self.nearest_event)
            self.nearest_event = DataManager.get_nearest_event()


def add_timer(self, timer: Timer):
    pass


def add_alarmclock(self, alarmclock: AlarmClock):
    pass


def add_notice(self, notice: Notice):
    pass
