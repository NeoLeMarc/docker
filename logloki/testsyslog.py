import logging
import logging.handlers

my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = ('127.0.0.1',514))

my_logger.addHandler(handler)

my_logger.debug('this is debug')
my_logger.critical('this is critical')
