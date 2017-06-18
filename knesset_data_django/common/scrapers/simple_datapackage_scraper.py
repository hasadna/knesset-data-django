from .base_datapackage_scraper import BaseDatapackageScraper
from knesset_data_django.common.exceptions import TooManyObjectsException



class SimpleDatapackageScraper(BaseDatapackageScraper):

    # extending classes should define this with the name of the source resource from the datapackage
    # DATAPACKAGE_RESOURCE_NAME = ""

    def _get_source_id(self, item_data):
        return item_data["id"]

    def _get_model_data(self, item_data):
        raise NotImplementedError()

    def _get_model_class(self):
        raise NotImplementedError()

    def _get_source_id_attr(self):
        return "source_id"

    def _get_object_prefix(self, object):
        return str(object)

    def _handle_datapackage_item(self, item_data):
        """
        updates or create an object based on the data from the datapackage
        :param item_data: source data, conforms to the datapackage schema
        :return: tuple(object, created, updated, message) the created/updated db object, whether it was created or updated and a message
                """
        source_id = self._get_source_id(item_data)
        model_data = self._get_model_data(item_data)
        qs = self._get_model_class().objects.filter(**{self._get_source_id_attr(): source_id})
        qs_count = qs.count()
        if qs_count == 1:
            object = qs.first()
            needs_update = False
            for attr, scraped_value in model_data.iteritems():
                db_value = getattr(object, attr)
                if db_value != scraped_value:
                    self.logger.debug("change in field {} db_value {} scraped_value {}".format(attr, db_value, scraped_value))
                    needs_update = True
                    break
            if needs_update:
                [setattr(object, k, v) for k, v in model_data.iteritems()]
                created, updated, message = False, True, "detected a change in one of the fields, updating object"
            else:
                created, updated, message = False, False, "existing object in DB, no change"
        elif qs_count == 0:
            object = self._get_model_class()(**dict(model_data, **{self._get_source_id_attr(): source_id}))
            created, updated, message = True, False, "created object"
        else:
            raise TooManyObjectsException("source_id={0}, matching db ids: {1}".format(source_id, [o.id for o in qs]))
        if updated or created:
            object.save()
        return object, created, updated, message

    def log_return_value(self, object, created, updated, message):
        prefix = self._get_object_prefix(object)
        if created or updated:
            self.logger.info(u"{}: {}".format(prefix, message))
        else:
            self.logger.debug(u'{}: {}'.format(prefix, message))
