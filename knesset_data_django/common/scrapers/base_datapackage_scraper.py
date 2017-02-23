from .base_scraper import BaseScraper


class BaseDatapackageScraper(BaseScraper):

    def __init__(self):
        super(BaseDatapackageScraper, self).__init__()

    def _fetch_datapackage_resource_tempdir(self, resource_name, **kwargs):
        with TemporaryDirectory(prefix="knesset-data-django") as temp_data_root:
            temp_datapackage_root = os.path.join(temp_data_root, "datapackage")
            for row in RootDatapackage(temp_datapackage_root).get_resource(resource_name).fetch(**kwargs):
                yield row

    def _fetch_datapackage_resource_dataroot(self, resource_name, **kwargs):
        datapackage_root = os.path.join(settings.DATA_ROOT, "datapackage")
        if not os.path.exists(datapackage_root):
            os.mkdir(datapackage_root)
        for row in RootDatapackage(datapackage_root).get_resource(resource_name).fetch(**kwargs):
            yield row

    def _fetch_datapackage_resource(self, resource_name, **kwargs):
        if kwargs.get("load_from_datapackage"):
            return self._fetch_datapackage_resource_dataroot(resource_name, **kwargs)
        else:
            return self._fetch_datapackage_resource_tempdir(resource_name, **kwargs)
