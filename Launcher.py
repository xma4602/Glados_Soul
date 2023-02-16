import os
import System.CommandManager as cm
import System.Display as disp

_way = "/home/pi/Desktop/Glados_Soul"
# os.chdir(_way)
state = True  # выключатель

while (state):
    answer = input("\nВведите команду: ").strip()
    answer = " ".join(answer.split()).split()

    if len(answer) == 1:
        res = cm.execute(answer[0], [])
    else:
        res = cm.execute(answer[0], answer[1:])

    disp.show(res)
