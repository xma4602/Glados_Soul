import json
import yaml

global __config
print('Запуск модуля config_manager')
with open('config.yaml', 'r') as file:
    __config = yaml.load(file, Loader=yaml.FullLoader)


def message_in():
    return __config['system']['in']


def message_out():
    return __config['system']['out']


def get_vk_group_data():
    with open(__config['vk']['keys'], 'r') as file:
        return json.load(file)


def council_file():
    return __config['data']['council']


def events_file():
    return __config['data']['events']


def fired_events_file():
    return __config['data']['fired']


def credentials_file():
    return __config['room']['keys']


def schedule_id():
    return __config['room']['schedule']['spreadsheet']


def schedule_enable():
    return __config['room']['schedule']['enable']


def log_out():
    return __config['logging']['out']


def log_file():
    return __config['logging']['file']


def log_level():
    return __config['logging']['level']


def about_club_file():
    return __config['data']['texts']['about']


def about_projects_file():
    return __config['data']['texts']['projects']


def join_club_file():
    return __config['data']['texts']['join']


def database_auth():
    with open(__config['database']['auth'], 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)
