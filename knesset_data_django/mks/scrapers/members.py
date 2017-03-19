# encoding: utf-8
from knesset_data_django.common.exceptions import TooManyObjectsException
from ...common.scrapers.base_datapackage_scraper import BaseDatapackageScraper
from ..models import Member


class MembersScraper(BaseDatapackageScraper):
    FUTURISTIC=True  # scraper is experiemental / not ready for general use
    DATAPACKAGE_RESOURCE_NAME = "members"

    def _create_member(self, member_data):
        member = Member(id=member_data["id"],
                        name=u"{} {}".format(member_data["first_name"], member_data["name"]))
        member.save()
        return member, True, False, "Created".format(member.id)

    def _update_member(self, member, member_data):
        return member, False, False, "member already exists, not updating".format(member.id)

    def _handle_datapackage_item(self, member_data):
        """updates or create a member object based on the given member data form the datapackage"""
        # we assume and ensure that the knesset id is the same as the db id
        knesset_and_oknesset_id = member_data["id"]
        member_qs = Member.objects.filter(id=knesset_and_oknesset_id)
        member_qs_count = member_qs.count()
        if member_qs_count == 0:
            return self._create_member(member_data)
        elif member_qs_count == 1:
            return self._update_member(member_qs.first(), member_data)
        else:
            raise TooManyObjectsException()

    def log_return_value(self, member, created, updated, message):
        prefix = u"member {} - {}".format(member.id, member.name)
        if created or updated:
            self.logger.info(u"{}: {}".format(prefix, message))
        else:
            self.logger.debug(u'{}: {}'.format(prefix, message))
