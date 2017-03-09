import logging


class MockDataserviceObject(object):

    def __init__(self, dataservice_class, **kwargs):
        for field_name, field in dataservice_class.get_fields().iteritems():
            setattr(self, field_name, kwargs.get(field_name, None))


class MockLogger(logging.Logger):

    def __init__(self, is_debug=False):
        self.is_debug = is_debug
        super(MockLogger, self).__init__("MockLogger")
        self.setLevel(logging.DEBUG)
        self.debug_records = []
        self.info_records = []
        self.all_records = []

    def isEnabledFor(self, level):
        return True

    def handle(self, record):
        if record.levelno == logging.DEBUG:
            self.debug_records.append(record)
        elif record.levelno == logging.INFO:
            self.info_records.append(record)
        self.all_records.append(record)
        if self.is_debug:
            print(record.getMessage())
