import os
import subprocess

commands = ("off", "reboot", "clone", "update", "exit")

state = True  # выключатель
while (state):

    print("\nВведите команду или help для просмотра доступных команд: ")
    answer = input()
    if answer == "help":
        print("\nДоступные команды:")
        for i in range(len(commands)):
            print(commands[i])
    elif answer == "off":
        print("Завершение работы")
        os.system('systemctl poweroff')  # os.system('shutdown /p /f') на винде
    elif answer == "reboot":
        print("Перезагрузка")
        subprocess.check_call('reboot')  # os.system('shutdown -r -t 0') на винде
    elif answer == "clone":
        way = input("\nВведите путь для копирования репозитория: ")
        link = input("\nВведите ссылку на репозиторий GitHub: ")
        cmd = "git clone " + link
        try:
            os.chdir(way)
            p = subprocess.run(cmd, shell=True)
            print("\nУспех!!!")
        except FileNotFoundError:
            print("\nФайл не найден!")
        except BaseException:
            print("\nЧто-то пошло не так... :(")
    elif answer == "update":
        way = input("\nВведите путь для обновления репозитория: ")
        cmd = "git pull"
        try:
            os.chdir(way)
            p = subprocess.run(cmd, shell=True)
            print("\nУспех!!!")
        except FileNotFoundError:
            print("\nФайл не найден!")
        except BaseException:
            print("\nЧто-то пошло не так... :(")

    elif answer == "exit":
        print("Выход из программы")
        state = False
    else:
        print("Неизвестная команда!")
