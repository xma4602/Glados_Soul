import os
import time
import subprocess


class SystemCommand:
	@classmethod
	def off(cls):
		ans = -1
		while ans != 'n' and ans != 'y':
			ans = input("Вы точно хотите отключить компьютер? (y - да, n - нет)")
			if ans != 'n' and ans != 'y':
				print("Неизвестная комнада")
		if ans == 'y':
			os.system('systemctl poweroff')
		else:
			print("Отмена")
	@classmethod
	def reboot(cls):
		ans = -1
		while ans != 'n' and ans != 'y':
			ans = input("Вы точно хотите перезагрузить компьютер? (y - да, n - нет)")
			print(ans)
			if ans != 'n' and ans != 'y':
				print("Неизвестная комнада")
		if ans == 'y':
			subprocess.check_call('reboot')
		else:
			print("Отмена")

SystemCommand.reboot()
SystemCommand.off()
