import json

from System.modules import vk_bot, console

global config


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

