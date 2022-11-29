import os
import time
import subprocess


class SystemCommand:
	@classmethod
	def off(cls):
		answer = -1
		while answer != 'n' and answer != 'y':
			answer = input("Вы точно хотите отключить компьютер? (y - да, n - нет)")
			if answer != 'n' and answer != 'y':
				print("Неизвестная комнада")
		if answer == 'y':
			print("Выключение")
			os.system('systemctl poweroff')
		else:
			print("Отмена")
	@classmethod
	def reboot(cls):
		answer = -1
		while answer != 'n' and answer != 'y':
			answer = input("Вы точно хотите перезагрузить компьютер? (y - да, n - нет)")
			if answer != 'n' and answer != 'y':
				print("Неизвестная комнада")
		if answer == 'y':
			print("Перезагрузка")
			subprocess.check_call('reboot')
		else:
			print("Отмена")

SystemCommand.reboot()
SystemCommand.off()
