import functions.SystemManagement as SystemManagement
import functions.GitControl as GitControl

#список команд
Commands = ('system power off', 'system reboot', 'git update', 'git clone',)


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

#блок SystemManagement
    if command == 'system power off':
        return(SystemManagement.SystemManagement('off'))
    elif command == 'system reboot':
        return(SystemManagement.SystemManagement('reboot'))

#блок GitControl
    elif command[:10] == 'git update':
        return(GitControl.Git('update', command[10:]))
    elif command[:9] == 'git clone':
        return(GitControl.Git('clone', command[9:]))


