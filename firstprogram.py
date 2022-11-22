import os
import time
import subprocess

class SystemCommand:
	@classmethod
	def off(cls, tttime=0):
		if type(tttime) is not int:
			raise TypeError("Аргумент должен быть целым числом")
		_answ = -1
		while _answ!=0 and _answ!=1:
			_answ = int(input("Вы точно хотите отключить компьютер? (1 - да, 0 - нет)"))
			if _answ!=0 and _answ!=1:
				print("Неизвестная комнада")
		
		if _answ==1:
			time.sleep(tttime)
			os.system('systemctl poweroff') 
		else:
			print("Отмена")
	@classmethod
	def reboot(cls, tttime=0):
		if type(tttime) is not int:
			raise TypeError("Аргумент должен быть целым числом")
		_answ = -1
		while _answ!=0 and _answ!=1:
			_answ = int(input("Вы точно хотите перезагрузить компьютер? (1 - да, 0 - нет)"))
			print(_answ)
			if _answ!=0 and _answ!=1:
				print("Неизвестная комнада")
		
		if _answ==1:
			time.sleep(tttime)
			subprocess.check_call('reboot')
		else:
			print("Отмена")
		
SystemCommand.reboot(10)
SystemCommand.off(10)


