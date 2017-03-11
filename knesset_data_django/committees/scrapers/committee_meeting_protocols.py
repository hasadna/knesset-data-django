from ...common.scrapers.base_datapackage_scraper import BaseDatapackageScraper
from ...mks.utils import get_all_mk_names
from ..models import CommitteeMeeting, ProtocolPart
from datetime import datetime
import os
import csv


class CommitteeMeetingProtocolsScraper(BaseDatapackageScraper):
    DATAPACKAGE_RESOURCE_NAME = "committee-meetings-protocols"

    def _get_all_mk_names(self):
        if not getattr(self, 'loaded_mk_names', False):
            self.mks, self.mk_names = get_all_mk_names()
            setattr(self, 'loaded_mk_names', True)
        return self.mks, self.mk_names

    def _validate_datapackage_item(self, text_file_path, parts_file_path, meetings_cnt):
        if meetings_cnt == 0:
            return False, "could not find meeting in DB"
        elif meetings_cnt > 1:
            return False, "found more then 1 matching meeting in DB"
        elif "ERROR: " in text_file_path:
            return False, "missing text file due to error in datapackage creation: {}".format(text_file_path.split("ERROR: ")[1])
        elif "ERROR: " in parts_file_path:
            return False, "missing parts file due to error in datapackage creation: {}".format(parts_file_path.split("ERROR: ")[1])
        elif not os.path.exists(text_file_path):
            return False, "missing text file {}".format(text_file_path)
        elif not os.path.exists(parts_file_path):
            return False, "missing parts file {}".format(parts_file_path)
        elif os.path.getsize(text_file_path) < 5:
            return False, "too small text file {}".format(text_file_path)
        elif os.path.getsize(parts_file_path) < 5:
            return False, "too small parts file {}".format(parts_file_path)
        else:
            return True, ""

    def _get_meetings(self, committee_id, meeting_id):
        qs = CommitteeMeeting.objects.filter(committee__knesset_id=committee_id, knesset_id=meeting_id)
        cnt = qs.count()
        return cnt, qs

    def _save_protocol_text(self, meeting, protocol_text):
        meeting.protocol_text = protocol_text
        meeting.protocol_text_update_date = datetime.now()
        meeting.save()

    def _update_protocol_text(self, meeting, text_file_path):
        if not meeting.protocol_text:
            with open(text_file_path) as f:
                protocol_text = f.read().decode('utf8')
            self._save_protocol_text(meeting, protocol_text)
            return True, "added protocol text to the meeting"
        else:
            return False, "meeting already has protocol text, will not update"

    def _save_protocol_parts(self, meeting, protocol_parts):
        ProtocolPart.objects.bulk_create(protocol_parts)
        meeting.protocol_parts_update_date = datetime.now()
        meeting.save()

    def _update_protocol_parts(self, meeting, parts_file_path):
        if meeting.parts.count() > 0:
            return False, "meeting has existing protocol parts, will not reparse"
        else:
            with open(parts_file_path) as f:
                parts = csv.reader(f)
                assert parts.next() == ['header', 'body']
                protocol_parts = [ProtocolPart(meeting=meeting, order=i + 1,
                                               header=part[0].decode('utf8'), body=part[1].decode('utf8'))
                                  for i, part in enumerate(parts)]
            self._save_protocol_parts(meeting, protocol_parts)
            return True, "inserted protocol parts"

    def _handle_datapackage_item(self, meeting_data):
        text_file_path = self._get_datapackage_resource_path(meeting_data["text"])
        parts_file_path = self._get_datapackage_resource_path(meeting_data["parts"])
        cnt, qs = self._get_meetings(meeting_data["committee_id"], meeting_data["meeting_id"])
        ok, error = self._validate_datapackage_item(text_file_path, parts_file_path, cnt)
        if not ok:
            return False, error, meeting_data, None, None, None, None
        else:
            meeting = qs.first()
            text_updated, text_message = self._update_protocol_text(meeting, text_file_path)
            if not text_updated:
                parts_updated, parts_message = False, "protocol text not updated, so skipping parts updating as well"
            else:
                parts_updated, parts_message = self._update_protocol_parts(meeting, parts_file_path)
            return True, None, meeting_data, text_updated, text_message, parts_updated, parts_message

    def log_return_value(self, ok, error, meeting_data, text_updated, text_message, parts_updated, parts_message):
        if ok:
            self.logger.debug(text_message)
            self.logger.debug(parts_message)
            if text_updated and parts_updated:
                self.logger.info("committee {} meeting {}: updated committee meeting protocol text and parts".format(meeting_data["committee_id"], meeting_data["meeting_id"]))
            elif text_updated:
                self.logger.error("committee {} meeting {}: updated committee meeting protocol text only".format(meeting_data["committee_id"], meeting_data["meeting_id"]))
            elif parts_updated:
                self.logger.error("committee {} meeting {}: updated committee meeting protocol parts only".format(meeting_data["committee_id"], meeting_data["meeting_id"]))
            else:
                self.logger.debug("committee {} meeting {}: no update to protocol text or parts".format(meeting_data["committee_id"], meeting_data["meeting_id"]))
        else:
            self.logger.info("committee {} meeting {}: error scraping committee meeting protocol: {}".format(meeting_data["committee_id"], meeting_data["meeting_id"], error))
