import os
import time
import subprocess

class SystemCommand:
	@classmethod
	def off(cls):
		_answ = -1
		while _answ!=0 and _answ!=1:
			_answ = int(input("Вы точно хотите отключить компьютер? (1 - да, 0 - нет)"))
			if _answ!=0 and _answ!=1:
				print("Неизвестная комнада")
		
		if _answ==1:

			os.system('systemctl poweroff') 
		else:
			print("Отмена")
	@classmethod
	def reboot(cls):
		_answ = -1
		while _answ!=0 and _answ!=1:
			_answ = int(input("Вы точно хотите перезагрузить компьютер? (1 - да, 0 - нет)"))
			print(_answ)
			if _answ!=0 and _answ!=1:
				print("Неизвестная комнада")
		
		if _answ==1:
			subprocess.check_call('reboot')
		else:
			print("Отмена")
		
SystemCommand.reboot()
SystemCommand.off()


