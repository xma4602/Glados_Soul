import datetime

from System.data_manager import start
start()

from System.message_manager import start as st
st()
from System.message_manager import send
from System.units.message import Message
from System.modules.logger import start
start()


title = 'бот работает'
recipients_id = [441449409, 2, 3]
deadline = datetime.datetime.today()
description = ('ура\n',
               'наконец-то\n',
               'бот\n',
               'работает ')
n = Message(title, recipients_id, deadline, description)
print(n.message_everyone())


send(n)
# bot.send("hi", ('000000678', ))
# bot.send('normal message', ('441449409',))
