from System import DataManager
from System.bot.notice import Notice
from System.bot.task import Task
from datetime import datetime

nearest_notice = DataManager.get_nearest_notice()


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
