from ..common.scrapers.simple_datapackage_scraper import SimpleDatapackageScraper
from .models import KnessetPerson, KnessetPersonToPosition, KnessetPosition


class PersonScraper(SimpleDatapackageScraper):

    DATAPACKAGE_RESOURCE_NAME = "persons-person"

    def _get_source_id(self, item_data):
        return item_data["id"]

    def _get_model_data(self, item_data):
        return {
            "last_name": item_data["last_name"],
            "first_name": item_data["first_name"],
            "gender_id": item_data["gender_id"],
            "gender_description": item_data["gender_description"],
            "email": item_data["email"],
            "is_current": item_data["is_current"],
            "last_update": item_data["last_update"]
        }

    def _get_model_class(self):
        return KnessetPerson

    def _get_source_id_attr(self):
        return "source_id"

    def _get_object_prefix(self, object):
        return u"person {} - {} {}".format(object.id, object.first_name, object.last_name)

class PersonPositionScraper(SimpleDatapackageScraper):

    DATAPACKAGE_RESOURCE_NAME = "persons-position"

    def _get_source_id(self, item_data):
        return item_data["id"]

    def _get_model_data(self, item_data):
        return {
            "description": item_data["description"],
            "gender_id": item_data["gender_id"],
            "gender_description": item_data["gender_description"],
            "last_update": item_data["last_update"]
        }

    def _get_model_class(self):
        return KnessetPosition

    def _get_source_id_attr(self):
        return "source_id"

    def _get_object_prefix(self, object):
        return u"person position {} - {}".format(object.id, object.description)

class PersonToPositionScraper(SimpleDatapackageScraper):

    DATAPACKAGE_RESOURCE_NAME = "persons-persons-to-positions"

    def _get_source_id(self, item_data):
        return item_data["id"]

    def _get_model_data(self, item_data):
        return {
            "person_id": item_data["person_id"],
            "position_id": item_data["position_id"],
            "knesset_num": item_data["knnesset_num"],
            "ministry_id": item_data["ministry_id"],
            "ministry_name": item_data["ministry_name"],
            "duty_description": item_data["duty_description"],
            "faction_id": item_data["faction_id"],
            "faction_name": item_data["faction_name"],
            "gov_num": item_data["gov_num"],
            "committee_id": item_data["committee_id"],
            "committee_name": item_data["committee_name"],
            "start_update": item_data["start_update"],
            "finish_update": item_data["finish_update"],
            "is_current": item_data["is_current"],
            "last_update": item_data["last_update"],
        }

    def _get_model_class(self):
        return KnessetPersonToPosition

    def _get_source_id_attr(self):
        return "source_id"

    def _get_object_prefix(self, object):
        return u"person to position {} - {} {}".format(object.id, object.person_id, object.position_id)
