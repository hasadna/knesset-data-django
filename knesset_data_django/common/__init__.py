import locale
import logging
import sys


def hebrew_strftime(dt, fmt=u'%A %d %B %Y  %H:%M'):
    locale.setlocale(locale.LC_ALL, 'he_IL.utf8')
    return dt.strftime(fmt).decode('utf8')


def simple_setup_logging(module_name, reset_loggers=False):
    logger = logging.getLogger(module_name)
    if reset_loggers:
        [logging.root.removeHandler(handler) for handler in tuple(logging.root.handlers)]
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(logging.Formatter("%(name)s:%(lineno)d\t%(levelname)s\t%(message)s"))
        stdout_handler.setLevel(logging.DEBUG)
        logging.root.addHandler(stdout_handler)
        logging.root.setLevel(logging.DEBUG)
    else:
        stdout_handler = None
    return logger, stdout_handler
