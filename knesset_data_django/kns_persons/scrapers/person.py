from ...common.scrapers.base_datapackage_scraper import BaseDatapackageScraper
from knesset_data_django.common.exceptions import TooManyObjectsException
from ..models import KnessetPerson


class PersonScraper(BaseDatapackageScraper):
    DATAPACKAGE_RESOURCE_NAME = "person"

    def _handle_datapackage_item(self, person_data):
        """
        updates or create a committee object based on dataservice_person
        :param person_data: dataservice person object
        :return: tuple(person, created) the updated or created person model object and True/False if it was created
                """
        person_knesset_id = person_data["id"]
        person_model_data = {
            "last_name": person_data["last_name"],
            "first_name": person_data["first_name"],
            "gender_id": person_data["gender_id"],
            "gender_description": person_data["gender_description"],
            "email": person_data["email"],
            "is_current": person_data["is_current"],
            "last_update": person_data["last_update"]
        }
        person_qs = KnessetPerson.objects.filter(source_id=person_knesset_id)
        person_qs_count = person_qs.count()
        if person_qs_count == 1:
            person = person_qs.first()
            needs_update = False
            for attr, scraped_value in person_model_data.iteritems():
                db_value = getattr(person, attr)
                if db_value != scraped_value:
                    needs_update = True
                    break
            if needs_update:
                [setattr(person, k, v) for k, v in person_model_data.iteritems()]
                created, updated, message = False, True, "detected a change in one of the fields, updating person"
            else:
                created, updated, message = False, False, "existing person in DB, no change"
        elif person_qs_count == 0:
            person = KnessetPerson(knesset_id=person_knesset_id, **person_model_data)
            created, updated, message = True, False, "created person"
        else:
            raise TooManyObjectsException("committee_knesset_id={}, matching db ids: {}".format(person_knesset_id,
                                                                                                [c.id for c in
                                                                                                 person_qs]))
        if updated or created:
            person.save()
        return person, created, updated, message

    def log_return_value(self, person, created, updated, message):
        prefix = u"person {} - {} {}".format(person.id, person.first_name, person.last_name)
        if created or updated:
            self.logger.info(u"{}: {}".format(prefix, message))
        else:
            self.logger.debug(u'{}: {}'.format(prefix, message))
