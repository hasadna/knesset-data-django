from .base_scraper import BaseScraper


class BaseDatapackageScraper(BaseScraper):
    DATAPACKAGE_RESOURCE_NAME = None

    def __init__(self, datapackage=None):
        super(BaseDatapackageScraper, self).__init__()
        self._datapackage = datapackage

    def _get_datapackage(self):
        return self._datapackage

    def _get_datapackage_resource(self):
        return self._get_datapackage().get_resource(self.DATAPACKAGE_RESOURCE_NAME)

    def _get_datapackage_resource_path(self, relpath=None):
        return self._get_datapackage_resource().get_path(relpath)

    def _handle_datapackage_item(self, item_data):
        raise NotImplementedError()

    def log_return_value(self, *args):
        """
        logs the return value of _handle_datapackage_item
        """
        raise NotImplementedError()

    def scrape_from_datapackage(self, **kwargs):
        return (self._handle_datapackage_item(item_data) for item_data in self._get_datapackage_resource().fetch_from_datapackage(**kwargs))

    def scrape(self, **kwargs):
        return (self._handle_datapackage_item(item_data) for item_data in self._get_datapackage_resource().fetch(**kwargs))
