import json
import yaml

global config
print('Запуск модуля config_manager')
with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


def message_in():
    return config['system']['in']


def message_out():
    return config['system']['out']


def get_vk_group_data():
    with open(config['vk']['keys'], 'r') as file:
        return json.load(file)


def council_file():
    return config['data']['council']


def events_file():
    return config['data']['events']


def fired_events_file():
    return config['data']['fired']


def credentials_file():
    return config['room']['keys']


def timetable_file():
    return config['room']['timetable']


def spreadsheet_id():
    return config['room']['schedule']['spreadsheet']


def schedule_enable():
    return config['room']['schedule']['enable']


def log_out():
    return config['logging']['out']


def log_file():
    return config['logging']['file']


def log_level():
    return config['logging']['level']


def about_club_file():
    return config['data']['club']['about']


def about_projects_file():
    return config['data']['club']['projects']


def join_club_file():
    return config['data']['club']['join']
