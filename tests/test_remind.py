import os
print(os.getcwd())
os.chdir('../src/')
os.chdir('../src/')

data_manager.start()
from managers import command_manager

command_manager.start()

command_manager.parse("Напомни Мише, Саше\nЧерез 1 минуту\nБот работает", "463504482")
