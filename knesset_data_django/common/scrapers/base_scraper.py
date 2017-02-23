import logging
import os
from backports.tempfile import TemporaryDirectory
from django.conf import settings
from knesset_datapackage.root import RootDatapackage


class BaseScraper(object):

    def __init__(self, logger=None):
        self.logger = logging.getLogger(self.__module__) if not logger else logger
