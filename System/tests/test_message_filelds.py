from datetime import datetime

from System.units.message import Message

msg = Message("заголовок", "12345", datetime.now())

print(msg.__dict__())
