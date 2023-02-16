import functions.SystemManagement as SystemManagement

#список команд
Commands = ('system power off', 'system reboot',)


def __CheckCommand(command=None):
    """
    Проверяет наличие заданной команды в списке команд
    :param command: заданная команда
    """
    for keyPhrase in Commands:
        if keyPhrase in command:
            return True
    return False


def Function(command = None):
    """
    Вызывает заданную команду
    :param command: заданная команда
    :return: результат выполнения
    """
    if not __CheckCommand(command):
        return 'Неизвестная команда'
    if command == 'system power off':
        return(SystemManagement.SystemManagement('off'))
    elif command == 'system reboot':
        return(SystemManagement.SystemManagement('reboot'))
