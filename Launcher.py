import System.command_manager as cm
import System.units.console as disp
""" Включение лаунчера - включает гладос """
_way = "/home/pi/Desktop/Glados_Soul"
# os.chdir(_way)
global state
state = True# выключатель

while (state):
    answer = input("\nВведите команду: ").strip()
    answer = " ".join(answer.split()).split()

    if len(answer) == 0:
        continue
    elif len(answer) == 1:
        res = cm.execute(answer[0], [])
    else:
        res = cm.execute(answer[0], answer[1:])

    if res == "exit":
        disp.show("Гладос остановлен")
        state = False
    else:
        disp.show(res)
