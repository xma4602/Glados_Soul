from System import command_manager
from System import data_manager, message_manager
from System.modules import logger, room
id = '441449409'
command_manager.start()
data_manager.start()
message_manager.start()
logger.start()
room.load_timetable()
command_manager.parse('Открыл', id)
command_manager.parse('А лаба сейчас открыта?', id)
command_manager.parse('Закрыл', id)
command_manager.parse('А лаба сейчас открыта?', id)
