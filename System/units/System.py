import os
import subprocess

actions = {
    1: 'power-off',
    2: 'reboot',
    3: 'exit'
}

def malina_control(params):
    if len(params) == 0:
        return ['system [action]', 'where [action] is:', actions]
    elif params[0] in actions.values():
        action = params[0]
    else:
        return "Нет такой команды"

    if action == 'power-off':
        return os.system('systemctl poweroff')
    elif action == 'reboot':
        return subprocess.check_call('reboot')
    elif action == 'exit':
        return "exit"