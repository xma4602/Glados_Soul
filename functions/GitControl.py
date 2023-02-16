import subprocess
import os


commands = ("clone", "update")
way = "/home/pi/Desktop/Glados_Soul" #путь к проекту
repositoryLink = "https://github.com/xma4602/Glados_Soul"


def Git(command=None, branch=None):
    """
    Обновляет или клонирует репозиторий
    :param command: команда
    :param branch: ветка репозитория
    :return: результат выполнения
    """
    try:
        os.chdir(way) #изменяет текущий рабочий каталог
    except FileNotFoundError:
        return "Файл или каталог не найден"
    except PermissionError:
        return "Отсутствуют необходимые права доступа"
    except NotADirectoryError:
        return "Путь не является каталогом"
    except OSError:
        return "Системная ошибка"

    if command == "clone":
        cmd = "git clone " + repositoryLink
        p = subprocess.run(cmd, shell=True)

        if p.returncode == 0:
            return ("\nРепозиторий успешно склонирован")
        else:
            return("\nКлонирование не удалось")
    elif command == "update":
        branches = ("mechanics_test", "recognition_test", "system_test",)
        branch = branch.strip()

        if branch in branches:
            subprocess.run("git stash", shell=True)
            subprocess.run(f"git checkout {branch}", shell=True)
            p = subprocess.run(f"git pull --ff-only origin {branch}", shell=True)
            if p.returncode == 0:
                return(f"Ветка {branch} обновлена")
            else:
                return("\nПроизошла ошибка.")
        elif branch == 'None':
            return("Вы не указали ветку обновления")
        else:
            return("Такой ветки не существует")
    else:
        return("Неизвестная команда")
