import System.modules.logger as l
import System.modules.vk_bot as vk
import System.data_manager as dm
dm.start()
l.start()
vk.start()


l.mess_send_warning('hello', 3)
l.mess_parse_warning('hi', 986898797)
l.mess_send_info('info', 8)

