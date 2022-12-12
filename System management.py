import os
import subprocess

commands = ("off", "reboot", "clone", "update", "exit" )

state = True   # выключатель
while(state):

    print("\nВведите команду или help для просмотра доступных команд: ")
    answer = input()
    match answer:
        case "help":
            print("\nДоступные команды:")
            for i in range(len(commands)):
                print(commands[i])
        case "off":
            print("Завершение работы")
            os.system('systemctl poweroff')  # os.system('shutdown /p /f') на винде
        case "reboot":
            subprocess.check_call('reboot')  # os.system('shutdown -r -t 0') на винде
        case "clone":
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
        case "update":
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

        case "exit":
            state = False
        case _:
            print("Неизвестная команда!")

