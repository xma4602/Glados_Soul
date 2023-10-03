import os
print(os.getcwd())
os.chdir('../')
os.chdir('../')

from System import config_manager
from System import data_manager
data_manager.start()
from System import command_manager
command_manager.start()

command_manager.parse("Напомни Мише, Саше\nЧерез 1 минуту\nБот работает", "463504482")
