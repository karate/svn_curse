import logging
import logging.config

APP_NAME = 'svn_curse'
LOGFILE = APP_NAME + '.log'

logging.basicConfig(level=logging.INFO, filename=LOGFILE)


def get_logger():
    log = logging.getLogger(APP_NAME)
    return log


def debug_start_done(func):
    def inner(*args, **kwargs):
        log = get_logger()
        log.debug('{} Start'.format(func.__name__))
        func(*args, **kwargs)
        log.debug('{} Done'.format(func.__name__))
    return inner
