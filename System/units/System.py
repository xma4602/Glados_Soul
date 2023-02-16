import os
import subprocess

actions = {
    1: 'power-off',
    2: 'reboot',
    3: 'exit'
}


def power_off():
    return os.system('systemctl poweroff')  # os.system('shutdown /p /f') на винде


def reboot():
    return subprocess.check_call('reboot')  # os.system('shutdown -r -t 0') на винде


def exit():
    #Launcher.state = False
    return True


def help():
    return ['system [action]', 'where [action] is:', actions]
