import json
import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime
from json import JSONDecodeError

from System import configurator

opened = False
# test_sheet_link = 'https://docs.google.com/spreadsheets/d/1SI-jXi1w74PJbuObw59MhZX6LgTyoTm_MFTbQ3bU8Us/edit#gid=0'  # ссылка на таблицу с расписанием
spreadsheet_id = configurator.spreadsheet_id()
timetable_file = configurator.timetable_file()  # путь к файлу, где будет храниться спарсенная таблица
credentials_file = configurator.credentials_file()
times = ('08:00 - 09:35',
         '09:45 - 11:20',
         '11:30 - 13:05',
         '13:30 - 15:05',
         '15:15 - 16:50',
         '17:00 - 18:35',
         '18:45 - 20:15',
         '20:20 - 21:55')
statuses = ('Лаборатория закрыта',
            'Есть небольшой шанс на то, что в лабе кто-то есть',
            'Лаборатория открыта')


def load_timetable():
    """
    Загружает данные таблицы в файл
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_file,
        ['https://www.googleapis.com/auth/spreadsheets']
    )
    httpAuth = credentials.authorize(httplib2.Http())
    service = discovery.build('sheets', 'v4', http=httpAuth)
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='P2:P116',
        majorDimension='COLUMNS'
    ).execute()
    values = values['values'][0]
    with open(timetable_file, 'w') as file:
        json.dump(values, file, indent=4)


def open_room():
    global opened
    opened = True


def close_room():
    global opened
    opened = False


def curr_week():
    cdate = datetime.now()
    month = cdate.month

    if month >= 9:
        first_semester = datetime(year=cdate.year, month=9, day=1)
        return datetime.now().isocalendar().week - first_semester.isocalendar().week
    elif month < 2:
        first_semester = datetime(year=cdate.year - 1, month=9, day=1)
        return 52 - datetime.now().isocalendar().week + first_semester.isocalendar().week
    else:
        second_semester = datetime(year=cdate.year, month=9, day=1)
        return datetime.now().isocalendar().week - second_semester.isocalendar().week


def get_rasp(values: list[str]) -> str:
    """Возвращает расписание лабы на сегодняшний день"""
    week = 1 - curr_week() % 2
    day = datetime.now().weekday()
    rasp_day = week * 7 + day
    num = rasp_day * 8
    stats = values[num:(num + 8)]
    rasp = ""
    for i in range(0, 7):
        rasp += times[i] + ': ' + statuses[int(stats[i])] + '\n'
    return rasp


def is_opened():
    if opened:
        return 'Лаборатория открыта'
    else:
        # return 'Лаборатория закрыта'
        day = datetime.now().isoweekday()
        timetable = {}
        try:
            with open(timetable_file, 'r') as file:
                timetable = json.load(file)
            return f"Лаба откроется по расписанию в {timetable[day - 1]}"
        except FileNotFoundError:
            # лог на ошибку отсутствия файла
            return "Лаборатория закрыта"
        except JSONDecodeError:
            # лог на ошибку декодирования json
            return "Лаборатория закрыта"

# load_timetable()
