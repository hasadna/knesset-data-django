from django.core.management.base import NoArgsCommand
import logging
from django.conf import settings
import sys
from knesset_data_django.common import simple_setup_logging


class BaseNoArgsCommand(NoArgsCommand):
    """
    root class for management commands

    all extending classes must call super class handle_noargs

    provides common functionality:

    * logging
        * when running this management command all existing django loggers will be removed (configurable)
        * they will be replaced with single logger to stdout
        * also, additional loggers can be added (for example, to track scrapers progress / status)
    """

    def __init__(self):
        super(BaseNoArgsCommand, self).__init__()
        app_name = self.__module__.split('.')[-4]
        command_name = self.__module__.split('.')[-1]
        self.command_name = "{app_name}.{command_name}".format(app_name=app_name, command_name=command_name)
        reset_loggers = getattr(settings, 'KNESSET_DATA_DJANGO_RESET_LOGGERS', True)
        self.logger, self.stdout_handler = simple_setup_logging(self.__module__, reset_loggers=reset_loggers)

    def handle_noargs(self, **options):
        if self.stdout_handler:
            self.stdout_handler.setLevel({"3": logging.DEBUG,
                                          "2": logging.DEBUG,
                                          "1": logging.INFO,
                                          "0": logging.ERROR}[options['verbosity']])
