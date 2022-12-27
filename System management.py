import os
import subprocess

commands = ("off", "reboot", "clone", "update", "exit")
way = "/home/pi/Desktop/Glados_Soul"
os.chdir(way)
state = True  # выключатель
while (state):
    answer = input("\nВведите команду: ")
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
        cmd = "git clone " + input("\nВведите ссылку на репозиторий GitHub: ").strip()
        p = subprocess.run(cmd, shell=True)
        if p.returncode == 0:
            print("\nРепозиторий успешно склонирован")
        else:
            print("\nКлонирование не удалось")
    elif answer == "update":
        branches = {1: "mechanics_test", 2: "recognition_test", 3: "system_test"}
        for i in branches.items():
            print(f"{i[0]}: {i[1]}")
        branch = int(input("Введите номер ветки: "))
        branch = branches.get(branch, None)
        if branch != None:
            subprocess.run("git stash", shell=True)
            subprocess.run(f"git checkout {branch}", shell=True)
            p = subprocess.run(f"git pull --ff-only origin {branch}", shell=True)
            if p.returncode == 0:
                print("\nВетка обновлена")
            else:
                print("\nПроизошла ошибка")
        else:
            print("Неверно введен номер ветки")
    elif answer == "exit":
        print("Выход из программы")
        state = False
    else:
        print("Неизвестная команда")
