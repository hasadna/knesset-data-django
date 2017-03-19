import logging


class BaseScraper(object):
    FUTURISTIC = False  # set to True for experiemental / not fully ready scrapers

    def __init__(self, logger=None, enable_the_future=False):
        self.logger = logging.getLogger(self.__module__) if not logger else logger
        self.enable_the_future = enable_the_future

    def __setattr__(self, key, value):
        if key == "logger":
            # if logger is set - we force it in scraper classes called as well
            self.force_logger = True
        super(BaseScraper, self).__setattr__(key, value)

    def get_child_scraper(self, scraper_class, *args, **kwargs):
        scraper_instance = scraper_class(*args, **kwargs)
        if getattr(self, "force_logger"):
            scraper_instance.logger = self.logger
        if self.enable_the_future or not scraper_instance.is_futuristic():
            return scraper_instance
        else:
            self.logger.info("skipping scraper {} because it's futuristic".format(scraper_class.__module__))
            return None

    def log_return_value(self, *args):
        """
        we want to allow callers of scraper methods to log the return values / actions done by scraper in different ways
        however, in many cases the actions should be logged to the logger as well
        so, callers (e.g. management command) should call this method to log the data to the logger in the correct way
        other callers might look at this implementation to understand how to log it to other outputs as well
        """
        raise NotImplementedError()

    def is_futuristic(self):
        return self.FUTURISTIC
