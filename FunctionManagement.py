import functions.SystemManagement as SystemManagement

#список команд
Commands = ('system power off', 'system reboot',)

#функция, проверяющая наличие полученной команды в списке команд
def __CheckCommand(command=None):
    for keyPhrase in Commands:
        if keyPhrase in command:
            return True
    return False
def Function(command = None):
    if not __CheckCommand(command):
        return 'Неизвестная команда'
    if command == 'system power off':
        return(SystemManagement.SystemManagement('off'))
    elif command == 'system reboot':
        return(SystemManagement.SystemManagement('reboot'))

