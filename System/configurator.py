import json


def start():
    global config
    with open('config.json', 'r') as file:
        config = json.load(file)


def message_in():
    return config['system']['in']


def message_out():
    return config['system']['out']


def get_vk_group_data():
    return config['vk']['keys']


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
    return config['room']['spreadsheet']
