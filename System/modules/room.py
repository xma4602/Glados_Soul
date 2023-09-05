import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from System import config_manager
import logging


def start():
    global schedule_enable, \
        credentials_file, \
        spreadsheet_id, \
        times, \
        statuses, \
        opened
    logging.info('Запуск модуля room')
    opened = False
    schedule_enable = config_manager.schedule_enable()
    spreadsheet_id = config_manager.spreadsheet_id()
    credentials_file = config_manager.credentials_file()
    times = ('08:00-09:35',
             '09:45-11:20',
             '11:30-13:05',
             '13:30-15:05',
             '15:15-16:50',
             '17:00-18:35',
             '18:45-20:15',
             '20:20-21:55')
    statuses = ('⛔ закрыто',
                '⚠ возможно открыто',
                '✅ открыто')


def load_timetable() -> list[str]:
    """
    Загружает данные таблицы в файл
    """
    logging.info('Запрос данных расписания')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_file,
        ['https://www.googleapis.com/auth/spreadsheets']
    )
    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('sheets', 'v4', http=http_auth)
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='P2:P116',
        majorDimension='COLUMNS'
    ).execute()
    return values['values'][0]


def open_room():
    global opened
    if opened:
        logging.warning('Повторная попытка перевести лабораторию в состояние ОТКРЫТО')
        return 'Лаборатория уже в состоянии ОТКРЫТО ✅'
    else:
        opened = True
        logging.info('Лаборатория переведена в состояние ОТКРЫТО')
        return 'Лаборатория переведена в состояние ОТКРЫТО ✅'


def close_room():
    global opened
    if opened:
        opened = False
        logging.info('Лаборатория переведена в состояние ЗАКРЫТО')
        return 'Лаборатория переведена в состояние ЗАКРЫТО ⛔'
    else:
        logging.warning('Повторная попытка перевести лабораторию в состояние ЗАКРЫТО')
        return 'Лаборатория уже в состоянии ЗАКРЫТО ⛔'


def is_opened():
    if datetime.now().hour < 8 or datetime.now().hour >= 21:  # с 21:00 по 8:00 лаборатория автоматически закрывается
        close_room()
    if opened:
        answer = '✅ Лаборатория открыта'
    else:
        answer = "⛔ Лаборатория закрыта"

    if schedule_enable:
        values = load_timetable()
        answer += parse_schedule(values)
    return answer


def current_week():
    today = datetime.now()

    if today.month >= 9:
        first_semester = datetime(year=today.year, month=9, day=1)
        return datetime.now().isocalendar().week - first_semester.isocalendar().week
    elif today.month < 2:
        first_semester = datetime(year=today.year - 1, month=9, day=1)
        return 52 - datetime.now().isocalendar().week + first_semester.isocalendar().week
    else:
        second_semester = datetime(year=today.year, month=9, day=1)
        return datetime.now().isocalendar().week - second_semester.isocalendar().week


def parse_schedule(values: list[str]) -> str:
    """Возвращает расписание лабы на сегодняшний день"""
    week = 1 - current_week() % 2
    day = datetime.now().weekday()
    schedule = "\n\nРасписание на сегодня\n"
    if datetime.now().hour > 21:
        day += 1
        schedule = "\n\nРасписание на завтра\n"

    num = (week * 7 + day) * 8
    stats = values[num:(num + 8)]
    for i in range(0, 8):
        schedule += f'{times[i]}: {statuses[int(stats[i])]}\n'
    return schedule
