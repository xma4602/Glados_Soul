from datetime import datetime

from System import data_manager
from System.modules import console
from System.units.notice import Notice
from System.units.task import Task

nearest_event = data_manager.start()
output = console


def check_time():
    if nearest_event is None:
        return False
    else:
        return nearest_event.time <= datetime.now()


def send_nearest_notice():
    global nearest_event
    send(nearest_event)
    nearest_event = data_manager.get_nearest_event(nearest_event)


def new_task(task: Task):
    send(task.notice_recipients())
    plan(task.notice_deadlines())


def send(notice: Notice):
    output.send(notice.message_everyone())


def plan(notices: list):
    for notice in notices:
        data_manager.store_event(notice)


def add_event(event):
    data_manager.store_event(event)
