import json
import os
from datetime import datetime
from src.bot.notice import Notice

notice_file = "notice.json"


def store_notice(notice: Notice):
    notice = notice.to_dict()
    notices = []

    if os.path.getsize(notice_file) != 0:
        with open(notice_file, 'r') as file:
            notices = json.load(file)

    notices.append(notice)

    with open(notice_file, 'w') as file:
        json.dump(notices, file, indent=4)


def get_nearest_notice():
    if os.path.getsize(notice_file) == 0:
        return None
    else:
        notices = []
        with open(notice_file, 'r') as file:
            notices = json.load(file)

        nearest_notice = notices[0]
        nearest_time = datetime.strptime(nearest_notice['time'], Notice.time_format)
        for notice in notices:
            time = datetime.strptime(notice['time'], Notice.time_format)
            if time < nearest_time:
                nearest_notice = notice

        notices.remove(nearest_notice)

        with open(notice_file, 'w') as file:
            json.dump(notices, file, indent=4)

        return Notice.from_dict(nearest_notice)

