import subprocess
import os


commands = ("clone", "update")
way = "/home/pi/Desktop/Glados_Soul" #путь к проекту


def Git(command=None, branch=None):
    """
    Обновляет или клонирует репозиторий
    :param command: команда
    :param branch: ветка репозитория
    :return: результат выполнения
    """
    os.chdir(way) #изменяет текущий рабочий каталог
    if command == "clone":
        cmd = "git clone " + input("\nВведите ссылку на репозиторий GitHub: ").strip()
        p = subprocess.run(cmd, shell=True)
        if p.returncode == 0:
            return ("\nРепозиторий успешно склонирован")
        else:
            return("\nКлонирование не удалось")
    elif command == "update":
        branches = ("mechanics_test", "recognition_test", "system_test",)

        if branch in branches:
            subprocess.run("git stash", shell=True)
            subprocess.run(f"git checkout {branch}", shell=True)
            p = subprocess.run(f"git pull --ff-only origin {branch}", shell=True)
            if p.returncode == 0:
                return(f"Ветка {branch} обновлена")
            else:
                return("\nПроизошла ошибка")
        else:
            return("Такой ветки не существует")
    else:
        return("Неизвестная команда")
