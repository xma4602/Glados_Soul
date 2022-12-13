import os
import subprocess

commands = ("off", "reboot", "clone", "update", "exit")
way = "/home/pi/Desktop/Glados_Soul"
state = True  # выключатель
while (state):
    answer = input("\nВведите команду или help для просмотра доступных команд: ")
    answer.strip()
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
    elif answer.split()[0] == "update":
        if len(answer) == 6:
            print("Существуют ветки:\nmechanics_test\nrecognition_test\nsystem_test")
            cmd = "git pull origin "
            cmd += input("Введите ветку, которую надо обновить: ").strip()
        else:
            cmd = "git pull origin "
            cmd += answer.split()[1].strip()
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
