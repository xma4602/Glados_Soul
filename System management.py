import os
import subprocess

commands = ("off", "reboot", "clone", "update", "exit" )

state = True   # выключатель
while(state):

    print("\nВведите команду или help для просмотра доступных команд: ")
    ans = input()

    if (ans == "help"):
        print("\nДоступные команды:")
        for i in range (len(commands)):
            print(commands[i])

    elif (ans == "off"):
        os.system('systemctl poweroff')  # os.system('shutdown /p /f') на винде

    elif (ans == "reboot"):
        subprocess.check_call('reboot')   # os.system('shutdown -r -t 0') на винде

    elif (ans == "clone"):
        way = input("\nВведите путь для копирования репозитория: ")
        link = input("\nВведите ссылку на репозиторий GitHub: ")
        cmd = "git clone " + link
        
        os.chdir(way)
        p = subprocess.run(cmd, shell=True)

        if p.returncode == 0:
            print("\nУспех!!!")
        else: 
            print("\nЧто то пошло не так :(")

    elif(ans == "update"):
        way = input("\nВведите путь для обновления репозитория: ")
        cmd = "git pull"

        os.chdir(way)
        p = subprocess.run(cmd, shell=True)

        if p.returncode == 0:
            print("\nУспех!!!")
        else: 
            print("\nЧто то пошло не так :(")

    elif(ans == "exit"):
        state = False

    else:
        print("\nНеизвеcтная команда!!!\n")