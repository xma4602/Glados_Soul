import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, time

from System import configurator

opened = False
# test_sheet_link = 'https://docs.google.com/spreadsheets/d/1SI-jXi1w74PJbuObw59MhZX6LgTyoTm_MFTbQ3bU8Us/edit#gid=0'  # ссылка на таблицу с расписанием
spreadsheet_id = configurator.spreadsheet_id()
credentials_file = configurator.credentials_file()
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
    return values['values'][0]


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
    rasp = "\n\nРасписание на сегодня\n"
    if datetime.now().time() > time(hour=21):
        day += 1
        rasp = "\n\nРасписание на завтра\n"

    rasp_day = week * 7 + day
    num = rasp_day * 8
    stats = values[num:(num + 8)]
    for i in range(0, 8):
        rasp += times[i] + ': ' + statuses[int(stats[i])] + '\n'
    return rasp


def is_opened():
    values = load_timetable()
    answer = ""
    if datetime.now().time() > time(hour=21):
        close_room()
    if opened:
        answer = '✅ Лаборатория открыта'
    else:
        answer = "⛔ Лаборатория закрыта"
    answer += get_rasp(values)
    return answer
