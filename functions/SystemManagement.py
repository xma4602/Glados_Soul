import os
import subprocess
def SystemManagement(command = None):
    """
    Выключает.перезагружает компьютер
    :param command: команда
    """
    if command == "off":
        os.system('systemctl poweroff')  # os.system('shutdown /p /f') на винде
        return 'Завершение работы'
    elif command == "reboot":
        subprocess.check_call('reboot')  # os.system('shutdown -r -t 0') на винде
        return 'Перезагрузка'
    else:
        return 'Неизвестная команда'
