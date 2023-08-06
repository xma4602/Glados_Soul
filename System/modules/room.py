import json
import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime
from json import JSONDecodeError

opened = False
test_sheet_link = 'https://docs.google.com/spreadsheets/d/1SI-jXi1w74PJbuObw59MhZX6LgTyoTm_MFTbQ3bU8Us/edit#gid=0'  # ссылка на таблицу с расписанием
CREDENTIALS_FILE = 'files/google_token.json'
spreadsheet_id = '1SI-jXi1w74PJbuObw59MhZX6LgTyoTm_MFTbQ3bU8Us'
timetable_file = 'files/timetable.json'  # путь к файлу, где будет храниться спарсенная таблица


def load_timetable():
    """
    Загружает данные таблицы в файл
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets']
    )
    httpAuth = credentials.authorize(httplib2.Http())
    service = discovery.build('sheets', 'v4', http=httpAuth)
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='B1:B8',
        majorDimension='COLUMNS'
    ).execute()
    values = values['values'][0][1:]
    with open(timetable_file, 'w') as file:
        json.dump(values, file, indent=4)


def open_room():
    global opened
    opened = True


def close_room():
    global opened
    opened = False


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
