import datetime

from src.bot.Notice import Notice

title = 'бот работает'
recipients_id = [1, 2, 3]
deadline = datetime.datetime.today()
description = 'ура\n' \
              'наконец-то\n' \
              'бот\n' \
              'работает '
n = Notice([title, recipients_id, deadline, description])
print(n.message_everyone())
