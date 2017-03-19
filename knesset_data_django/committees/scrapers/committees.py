# encoding: utf-8
from knesset_data_django.common.exceptions import TooManyObjectsException
from ...common.scrapers.base_datapackage_scraper import BaseDatapackageScraper
from ..models import Committee


class CommitteesScraper(BaseDatapackageScraper):
    DATAPACKAGE_RESOURCE_NAME = "committees"

    def _handle_datapackage_item(self, committee_data):
        """
        updates or create a committee object based on dataservice_committee
        :param dataservice_committee: dataservice committee object
        :return: tuple(committee, created) the updated or created committee model object and True/False if it was created
        """
        committee_knesset_id = committee_data["id"]
        committee_model_data = {
            "name": committee_data["name"],
            "knesset_type_id": committee_data["type_id"],
            "knesset_parent_id": committee_data["parent_id"],
            "name_eng": committee_data["name_eng"],
            "name_arb": committee_data["name_arb"],
            "start_date": committee_data["begin_date"],
            "end_date": committee_data["end_date"],
            "knesset_description": committee_data["description"],
            "knesset_description_eng": committee_data["description_eng"],
            "knesset_description_arb": committee_data["description_arb"],
            "knesset_note": committee_data["note"],
            "knesset_note_eng": committee_data["note_eng"],
            "knesset_portal_link": committee_data["portal_link"],
        }
        committee_qs = Committee.objects.filter(knesset_id=committee_knesset_id)
        committee_qs_count = committee_qs.count()
        if committee_qs_count == 1:
            committee = committee_qs.first()
            needs_update = False
            for attr, scraped_value in committee_model_data.iteritems():
                db_value = getattr(committee, attr)
                if db_value != scraped_value:
                    needs_update=True
                    break
            if needs_update:
                [setattr(committee, k, v) for k, v in committee_model_data.iteritems()]
                created, updated, message = False, True, "detected a change in one of the fields, updating committee"
            else:
                created, updated, message = False, False, "existing meeting in DB, no change"
        elif committee_qs_count == 0:
            committee = Committee(knesset_id=committee_knesset_id, **committee_model_data)
            created, updated, message = True, False, "created meeting"
        else:
            raise TooManyObjectsException("committee_knesset_id={}, matching db ids: {}".format(committee_knesset_id, [c.id for c in committee_qs]))
        if updated or created:
            committee.save()
        return committee, created, updated, message

    def log_return_value(self, committee, created, updated, message):
        prefix = u"committee {} - {}".format(committee.id, committee.name)
        if created or updated:
            self.logger.info(u"{}: {}".format(prefix, message))
        else:
            self.logger.debug(u'{}: {}'.format(prefix, message))
