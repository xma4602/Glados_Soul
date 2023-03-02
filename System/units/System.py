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
        power_off()
    elif action == 'reboot':
        reboot()
    elif action == 'exit':
        exit()

def power_off():
    return os.system('systemctl poweroff')  # os.system('shutdown /p /f') на винде


def reboot():
    return subprocess.check_call('reboot')  # os.system('shutdown -r -t 0') на винде


def exit():
    #Launcher.state = False
    return True