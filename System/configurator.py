import json

from System.modules import vk_bot, console


def start():
    global config
    with open('config.json', 'r') as file:
        config = json.load(file)


def message_in():
    messanger = config['message_in']
    if messanger == 'vk':
        return vk_bot
    if messanger == 'console':
        return console


def message_out():
    messanger = config['message_out']
    if messanger == 'vk':
        return vk_bot
    if messanger == 'console':
        return console


def get_vk_group_data():
    with open(config['vk_keys'], 'r') as file:
        data = json.load(file)
    return data


def council_file():
    return config['council']


def events_file():
    return config['events']


def fired_events_file():
    return config['fired']
