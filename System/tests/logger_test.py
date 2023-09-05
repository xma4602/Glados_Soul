import System.modules.logger as l
import logging
#l.start()

logging.info('Все работает', {'firts arg': 3, 'type': 'test'})
try:
    a = 1/0
except Exception:
    logging.error('Ошибка', stack_info=True)
#logging.basicConfig(force=True, filename=r'System\files\log\')

