import functions.SystemManagement as SystemManagement

#список команд
Commands = ('system power off', 'system reboot',)

#функция, проверяющая наличие полученной команды в списке команд
def __CheckCommand(command=None):
    global Commands
    for keyPhrase in Commands:
        if all(word in command.split() for word in keyPhrase.split()):
            return True
    return False
def Function(command = None):
    if not __CheckCommand(command):
        return 0
    if command == 'system power off':
        return(SystemManagement.SystemManagement('off'))
    elif command == 'system reboot':
        return(SystemManagement.SystemManagement('reboot'))


