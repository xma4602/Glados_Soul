import json
from pprint import pprint
import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime

opened = False
test_sheet_link = 'https://docs.google.com/spreadsheets/d/1SI-jXi1w74PJbuObw59MhZX6LgTyoTm_MFTbQ3bU8Us/edit#gid=0'
CREDENTIALS_FILE = 'C:/Users/regis/Glados_Soul/System/google_token.json'
spreadsheet_id = '1SI-jXi1w74PJbuObw59MhZX6LgTyoTm_MFTbQ3bU8Us'
timetable_file = 'timetable.json'


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
    with open(timetable_file, 'w') as file:
        json.dump(values, file, indent=4)
    return


def open_room():
    global opened
    opened = True


def close_room():
    global opened
    opened = False


def is_opened():
    if opened:
        return True
    else:
        day = datetime.now().isoweekday()
        timetable = {}
        with open(timetable_file, 'r') as file:
            timetable = json.load(file)
        return f"Лаба откроется по расписанию в {timetable['values'][0][day]}"


load_timetable()
print(is_opened())
