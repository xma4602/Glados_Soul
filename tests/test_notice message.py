import datetime

from managers.data_manager import start

start()

from managers.message_manager import start as st

st()
from managers.message_manager import send
from src.entities.message import Message
from src.services.logger import start

start()

title = 'бот работает'
recipients_id = [441449409]
deadline = datetime.datetime(year=2023, month=9, day=7, hour=0, minute=9)
deadline1 = datetime.datetime(year=2023, month=9, day=7, hour=0, minute=8)
deadline3 = datetime.datetime(year=2023, month=9, day=7, hour=0, minute=7)
description = ['ура\n', ]
n = Message(title, recipients_id, deadline, description)
n1 = Message(title, recipients_id, deadline1, description)
n2 = Message(title, recipients_id, deadline3, description)
print(n.message_everyone())

send(n)
print('запуск 1')
send(n1)
print('запуск 2')
send(n2)
print('запуск 3')

while True:
    pass
# bot.send("hi", ('000000678', ))
# bot.send('normal message', ('441449409',))
