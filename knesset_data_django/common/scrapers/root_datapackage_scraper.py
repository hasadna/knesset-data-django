from .base_scraper import BaseScraper
from django.conf import settings
import os
from knesset_datapackage.root import RootDatapackage
from importlib import import_module
import shutil
from tempfile import mktemp
import requests


class RootDatapackageScraper(BaseScraper):

    # list of scraper classes which extend the BaseDatapackageScraper class
    # will call these scrapers one by one in tuple order to load the data from the datapackage
    SCRAPERS = (
        "knesset_data_django.mks.scrapers.members.MembersScraper",
        "knesset_data_django.committees.scrapers.committees.CommitteesScraper",
        "knesset_data_django.committees.scrapers.committee_meetings.CommitteeMeetingsScraper",
        "knesset_data_django.committees.scrapers.committee_meeting_protocols.CommitteeMeetingProtocolsScraper",
        "knesset_data_django.kns_persons.scrapers.PersonScraper",
        "knesset_data_django.kns_persons.scrapers.PersonPositionScraper",
        "knesset_data_django.kns_persons.scrapers.PersonToPositionScraper",
    )

    def __init__(self, **kwargs):
        super(RootDatapackageScraper, self).__init__(**kwargs)
        self.datapackage_dir = os.path.join(settings.DATA_ROOT, "datapackage")
        self.datapackage_lock = os.path.join(self.datapackage_dir, "LOCK")

    def _validate_and_lock_datapackage(self):
        if not os.path.exists(self.datapackage_dir):
            return False, "you must load a datapackage first"
        else:
            datapackage_lock = os.path.join(self.datapackage_dir, "LOCK")
            if os.path.exists(datapackage_lock):
                return False, "datapackage directory is already locked, either another scraper is working in parallel or you need to remove the lock"
            else:
                with open(datapackage_lock, "w") as f:
                    f.write(".")
                return True, "datapackage directory was successfully locked"

    def _scrape_instance_value(self, from_datapackage, fetch_kwargs, child_scraper_instance, return_value):
        # can be used to override scraper functionality during the return generator stream
        # used for automated testing
        return return_value

    def _scrape_instance(self, from_datapackage, fetch_kwargs, child_scraper_instance):
        scrape_func = getattr(child_scraper_instance, "scrape_from_datapackage" if from_datapackage else "scrape")
        for return_value in scrape_func(**fetch_kwargs):
            yield self._scrape_instance_value(from_datapackage, fetch_kwargs, child_scraper_instance, return_value)

    def _scrape_class(self, from_datapackage, scraper_class, datapackage, fetch_kwargs):
        """
        creates a scraper instance and scrapes from a single scraper class
        returns: (scraper_instance, scraper_item_return_values_generator)
        """
        child_scraper_instance = self.get_child_scraper(scraper_class, datapackage=datapackage)
        return child_scraper_instance, self._scrape_instance(from_datapackage, fetch_kwargs, child_scraper_instance) if child_scraper_instance else None

    def _scrape_classes(self, from_datapackage, scraper_classes, datapackage, fetch_kwargs):
        """
        iterates over the scraper_classes, calling _scrape_class for each one
        returns a generator which generates: (scraper_class, is_ok, scrape_class_return_value)
        if is_ok is False, scrape_class_return_value will contain the exception
        """
        for scraper_class in scraper_classes:
            try:
                yield scraper_class, True, self._scrape_class(from_datapackage, scraper_class, datapackage, fetch_kwargs)
            except Exception, e:
                yield scraper_class, False, e

    def _scrape(self, from_datapackage, scraper_classes, fetch_kwargs=None, with_dependencies=True):
        """
        iterates over the scraper_classes and calls the relevant scrape function for each
        :param from_datapackage: bool - if True fetches from a previously downloaded and extracted datapackage
                                        otherwise - fetches online from the source data
        :param scraper_classes: list of scraper classes to fetch from
        :param fetch_kwargs: relevant only if from_datapackage is False, can contain kwargs to change the fetching from source data
        :param with_dependencies: some scrapers might depend on other scrapers, default behavior is to call dependant scrapers as well
        :return: return value from _scrape_classes function, raises exceptions on errors
        """
        fetch_kwargs = {} if not fetch_kwargs else fetch_kwargs
        validated, validate_message = self._validate_and_lock_datapackage()
        if validated:
            self.logger.debug(validate_message)
            try:
                datapackage = RootDatapackage(self.datapackage_dir, with_dependencies)
                return self._scrape_classes(from_datapackage, scraper_classes, datapackage, fetch_kwargs)
            finally:
                self.unlock_datapackage()
        else:
            raise Exception(validate_message)

    def unlock_datapackage(self):
        """
        unlocks the datapackage directory if needed
        no return values or expected exceptions
        """
        if os.path.exists(self.datapackage_lock):
            self.logger.debug("removing lock file {}".format(self.datapackage_lock))
            os.remove(self.datapackage_lock)

    def scrape(self, from_datapackage, scraper_class, fetch_kwargs=None, with_dependencies=True):
        """
        scrape a single scraper class
        see _scrape function for parameters and return value
        """
        return self._scrape(from_datapackage, [scraper_class], fetch_kwargs, with_dependencies)

    def scrape_all(self, from_datapackage, fetch_kwargs=None, with_dependencies=True):
        """
        scrapers from all the scrpaer classes (using self.SCRAPERS)
        see _scrape function for parameters and return value
        """
        get_scraper_class = lambda module_class: getattr(import_module(".".join(module_class.split('.')[:-1])), module_class.split('.')[-1])
        scraper_classes = [get_scraper_class(module_class) for module_class in self.SCRAPERS]
        return self._scrape(from_datapackage, scraper_classes, fetch_kwargs, with_dependencies)

    def load_from_file(self, datapackage_zip_file):
        """
        extract the zip file into the datapackage directory (DATA_ROOT/datapackage)
        raises exception if directory exists and is locked (usually meaning scrape process is in progress)
        returns the datapackage directory the zip file was extracted into (will always be DATA_ROOT/datapackage)
        """
        self.logger.info("loading from local zip file '{}'".format(datapackage_zip_file))
        if os.path.exists(self.datapackage_lock):
            raise Exception("datapackage directory is locked, cannot load another datapackage zip before lock is removed")
        else:
            if os.path.exists(self.datapackage_dir):
                shutil.rmtree(self.datapackage_dir)
            return RootDatapackage.load_from_zip(datapackage_zip_file, settings.DATA_ROOT)

    def load_from_directory(self, directory, symlink=True):
        if not symlink:
            raise NotImplementedError()
        else:
            self.logger.info("loading from local directory '{}'".format(directory))
            if os.path.exists(self.datapackage_lock):
                raise Exception("datapackage directory is locked, cannot load another datapackage before lock is removed")
            else:
                if os.path.exists(self.datapackage_dir):
                    if os.path.islink(self.datapackage_dir):
                        os.remove(self.datapackage_dir)
                    else:
                        shutil.rmtree(self.datapackage_dir)
                os.symlink(directory, os.path.join(settings.DATA_ROOT, "datapackage"))
                if os.path.exists(self.datapackage_lock):
                    os.remove(self.datapackage_lock)
                return os.path.join(settings.DATA_ROOT, "datapackage")

    def load_from_url(self, datapackage_zip_url):
        """
        download a zip file from the url and call load_from_file to extract it into the datapackage directory
        returns a tuple (zip_file_name, load_from_file_return_value)
        """
        self.logger.info("downloading datapackage zip file from url '{}'".format(datapackage_zip_url))
        # we download first to a temporary file, and after download succeeded rename it to the correct place
        # this is to support cases where download was interrupted, or when zip file should be overwritten
        temp_file = mktemp()
        with open(temp_file, "wb") as f:
            for chunk in requests.get(datapackage_zip_url, stream=True):
                f.write(chunk)
        # url looks someting like this: https://s3.amazonaws.com/knesset-data/datapackage_last_5_days_2017-02-23.zip
        # output path will look something like this: data/datapackage_last_5_days_2017-02-23.zip
        zip_file_name = os.path.join(settings.DATA_ROOT, datapackage_zip_url.split('/')[-1])
        shutil.move(temp_file, zip_file_name)
        return zip_file_name, self.load_from_file(zip_file_name)

    def log_load_from_url_return_value(self, load_from_url_return_value):
        zip_file_name, load_from_file_return_value = load_from_url_return_value
        self.logger.info("zip file saved at {}".format(zip_file_name))
        self.log_load_from_file_return_value(load_from_file_return_value)

    def log_load_from_file_return_value(self, load_from_file_return_value):
        datapackage_dir = load_from_file_return_value
        self.logger.info("datapackage available at {}".format(datapackage_dir))

    def log_scrape_return_value(self, scrape_classes_return_value):
        for scraper_class, is_ok, scrape_class_return_value in scrape_classes_return_value:
            if is_ok:
                scraper_instance, scrape_return_values = scrape_class_return_value
                if scraper_instance:
                    i = 0
                    try:
                        for scrape_return_value in scrape_return_values:
                            scraper_instance.log_return_value(*scrape_return_value)
                            i += 1
                    except Exception as e:
                        message = "unexpected exception parsing return value for {}".format(scraper_class)
                        self.logger.exception(message)
                        raise Exception(message)
                    self.logger.info("processed {} items for scraper {}".format(i, scraper_class.__name__))
                else:
                    self.logger.debug("skipping scraper {}".format(scraper_class.__name__))
            else:
                self.logger.error("exception in scraper '{}', continuing to next scraper class".format(scraper_class.__name__))
                self.logger.exception(scrape_class_return_value)
