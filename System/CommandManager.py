import units.System as sys
import units.Updating as upd

commands = {
    0: 'help',
    1: 'update',
    2: 'system'
}


def _help():
    return ['[command]', 'where [command] is:', commands]


def execute(cmd, params):

    if cmd.isdigit():
        cmd = commands.get(int(cmd))

    if cmd == commands.get(0):
        return _help()
    elif cmd == commands.get(1):
        return _executeUpdating(params)
    elif cmd == commands.get(2):
        return _executeSystem(params)
    else:
        return f'Не найдено команды {cmd}'


def _executeSystem(params):
    cmd = params[0]
    commands = sys.actions

    if cmd == commands.get(0):
        return _help()
    elif cmd == commands.get(1):
        return sys.reboot()
    elif cmd == commands.get(2):
        return sys.power_off()


def _executeUpdating(params):
    return upd.update(params)
