# encoding: utf-8
from knesset_data_django.common.exceptions import TooManyObjectsException
from ...common.scrapers.base_scraper import BaseScraper
from ..models import Committee


class CommitteesScraper(BaseScraper):

    def _get_all_active_committees_data(self, has_portal_link):
        kwargs = {"include": ["committees"]}
        if has_portal_link:
            kwargs["main_committees"] = True
        else:
            kwargs["active_committees"] = True
        return self._fetch_datapackage_resource("committees", **kwargs)

    def _update_or_create(self, committee_data):
        """
        updates or create a committee object based on dataservice_committee
        :param dataservice_committee: dataservice committee object
        :return: tuple(committee, created) the updated or created committee model object and True/False if it was created
        """
        committee_id = committee_data["id"]
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
        committee_qs = Committee.objects.filter(id=committee_id)
        committee_qs_count = committee_qs.count()
        if committee_qs_count == 1:
            committee = committee_qs.first()
            [setattr(committee, k, v) for k, v in committee_model_data.iteritems()]
            created = False
        elif committee_qs_count == 0:
            committee = Committee(id=committee_id, **committee_model_data)
            created = True
        else:
            raise TooManyObjectsException()
        committee.save()
        return committee, created

    def scrape_active_committees(self):
        """
        updates the active committees in the DB
        creates new committees / updates data for existing committees
        :return: generator of return values from _update_or_create_from_dataservice
        """
        return (self._update_or_create(committee_data)
                for committee_data
                in self._get_all_active_committees_data(has_portal_link=False))
