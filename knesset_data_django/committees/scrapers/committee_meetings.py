from ...common.scrapers.base_scraper import BaseScraper
from ...common import hebrew_strftime
from ..meetings import reparse_protocol
from ...mks.utils import get_all_mk_names
from ..models import Committee, CommitteeMeeting
import os
from django.conf import settings
from knesset_datapackage.root import RootDatapackage
from backports.tempfile import TemporaryDirectory


class CommitteeMeetingsScraper(BaseScraper):

    def _get_meetings(self, committee_id, days=5, **kwargs):
        # self._fetch_datapackage_resource("committee-meetings", days=days)
        # return DataserviceCommitteeMeeting.get(committee_id, days=days)
        return self._fetch_datapackage_resource("committee-meetings", days=days, **kwargs)


    def _has_existing_meeting(self, meeting_data):
        qs = CommitteeMeeting.objects.filter(
            committee__knesset_id=meeting_data["committee_id"])
        if qs.filter(knesset_id=meeting_data["id"]).exists():
            # there is an existing meeting with the same src knesset id
            self.logger.debug('there is an existing meeting with same src knesset id ({})'.format(meeting_data["id"]))
            return True
        elif qs.filter(date=meeting_data["datetime"], knesset_id=None).exists():
            # there is an existing meeting on the same date but without a src knesset id
            # this meeting was scraped before the knesset-data improvements so we can't know for sure
            # if it's not the same meeting
            # for this case we assume it's the same meeting to prevent duplicated meetings
            self.logger.debug('there is an existing meeting on same date ({}) but without id'.format(meeting_data["datetime"]))
            return True
        else:
            # no existing meeting
            return False

    def _reparse_protocol(self, meeting):
        mks, mk_names = get_all_mk_names()
        reparse_protocol(meeting, mks=mks, mk_names=mk_names)

    def _create_meeting(self, meeting_data, committee):
        meeting_model_data = self._get_committee_meeting_fields_from_dataservice(meeting_data)
        meeting = CommitteeMeeting.objects.create(committee=committee,
                                                                     **meeting_model_data)
        self.logger.debug('created meeting {}'.format(meeting.pk))
        self._reparse_protocol(meeting)
        return meeting

    def _update_meeting(self, committee, meeting_data):
        if not meeting_data["url"]:
            return (meeting_data, None, "missing meeting url")
        elif self._has_existing_meeting(meeting_data):
            return (meeting_data, None, "meeting exists in DB")
        else:
            return (meeting_data, self._create_meeting(meeting_data, committee), "")

    def _update_committee_meetings(self, committee, days=5, **kwargs):
        return (self._update_meeting(committee, meeting_data)
                for meeting_data in self._get_meetings(committee.knesset_id, days=days, **kwargs))

    def _get_committees(self, committee_ids):
        return Committee.objects.filter(knesset_id__gt=0, pk__in=committee_ids)

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

    def scrape(self, days=5, committee_ids=None, **kwargs):
        if not kwargs.get("load_from_datapackage") and not committee_ids:
            committee_ids = Committee.objects.all().values_list('pk', flat=True)
        return ((committee, self._update_committee_meetings(committee, days=days, **kwargs))
                for committee in self._get_committees(committee_ids))
