from ...common.scrapers.base_datapackage_scraper import BaseDatapackageScraper
from ...common import hebrew_strftime
from ..models import CommitteeMeeting, Committee
from ...common.exceptions import TooManyObjectsException
from django.utils.functional import cached_property


class CommitteeMeetingsScraper(BaseDatapackageScraper):
    DATAPACKAGE_RESOURCE_NAME = "committee-meetings"

    def _get_committee(self, meeting_data):
        qs = Committee.objects.filter(knesset_id=meeting_data["committee_id"])
        cnt = qs.count()
        if cnt == 1:
            return qs.first()
        elif cnt == 0:
            raise Exception("All meetings must have a valid committee id. You should ensure committees scraper runs before the meetings scraper")
        else:
            raise TooManyObjectsException()

    def _has_existing_meeting(self, meeting_data):
        committee = self._get_committee(meeting_data)
        qs = CommitteeMeeting.objects.filter(committee=committee)
        if qs.filter(knesset_id=meeting_data["id"]).exists():
            return True, "there is an existing meeting with the same src knesset id"
        elif qs.filter(date=meeting_data["datetime"], knesset_id=None).exists():
            # there is an existing meeting on the same date but without a src knesset id
            # this meeting was scraped before the knesset-data improvements so we can't know for sure
            # if it's not the same meeting
            # for this case we assume it's the same meeting to prevent duplicated meetings
            return True, "there is an existing meeting on same date ({})".format(meeting_data["datetime"])
        else:
            # no existing meeting
            return False, None

    def _create_meeting(self, meeting_data):
        committee = self._get_committee(meeting_data)
        meeting_model_data = self._get_committee_meeting_fields_from_dataservice(meeting_data)
        meeting = CommitteeMeeting.objects.create(committee=committee, **meeting_model_data)
        return meeting, "created meeting id {}".format(meeting.pk)

    def _get_committee_meeting_fields_from_dataservice(self, meeting_data):
        meeting_model_data = {
            "date_string": hebrew_strftime(meeting_data["datetime"], fmt=u'%d/%m/%Y'),
            "date": meeting_data["datetime"],
            "topics": meeting_data["title"],
            "datetime": meeting_data["datetime"],
            "knesset_id": meeting_data["id"],
            "src_url": meeting_data["url"],
        }
        if meeting_model_data['topics'] is None or meeting_model_data['topics'] == '':
            meeting_model_data['topics'] = meeting_data["session_content"]
        return meeting_model_data

    def _handle_datapackage_item(self, meeting_data):
        created_meeting = None
        if not meeting_data["url"]:
            message = "missing meeting url"
        else:
            has_existing_meeting, message = self._has_existing_meeting(meeting_data)
            if not has_existing_meeting:
                created_meeting, message = self._create_meeting(meeting_data)
        return meeting_data, created_meeting, message

    def log_return_value(self, meeting_data, meeting_model, message):
        prefix = u"committee {} meeting {}".format(meeting_data["committee_id"], meeting_data["id"])
        if meeting_model:
            self.logger.info(u'{}: {}'.format(prefix, message))
        else:
            self.logger.debug(u'{}: did not update: {}'.format(prefix, message))
