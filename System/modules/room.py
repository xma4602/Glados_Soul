import apiclient
from pprint import pprint
import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import gspread

opened = False
CREDENTIALS_FILE = 'C:/Users/regis/Glados_Soul/System/google_token.json'
spreadsheet_id = '1SI-jXi1w74PJbuObw59MhZX6LgTyoTm_MFTbQ3bU8Us'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets']
)
httpAuth = credentials.authorize(httplib2.Http())
service = discovery.build('sheets', 'v4', http=httpAuth)
values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='A1:B3',
    majorDimension='ROWS'
).execute()

pprint(values)
pprint(values['values'][0][0:])


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
        pass
