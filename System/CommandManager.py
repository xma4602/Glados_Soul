import System.units.System as sys
import System.units.Updating as upd
""" Файл, отвечающий за считывание команды из терминала и его запускание"""
commands = {
    0: 'help',
    #1: 'update',
    2: "system"
}


def _help():
    return ['[command]', 'where [command] is:', commands]


def execute(cmd, params):

    if cmd == commands.get(0):
        return _help()
    elif cmd == commands.get(1):
        return upd.update(params)
    elif cmd == commands.get(2):
        return sys.malina_control(params)
    else:
        return f'Не найдена команда {cmd}'