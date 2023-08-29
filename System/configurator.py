import json
import yaml

global config
with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


# with open('config.json', 'r') as file:
#    config = json.load(file)


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

