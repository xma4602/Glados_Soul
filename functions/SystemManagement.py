import os
import subprocess
def SystemManagement(command = None):
    if command == "off":
        os.system('systemctl poweroff')  # os.system('shutdown /p /f') на винде
        return 'success'
    elif command == "reboot":
        subprocess.check_call('reboot')  # os.system('shutdown -r -t 0') на винде
        return 'success'
    else:
        return 'unknown command'
