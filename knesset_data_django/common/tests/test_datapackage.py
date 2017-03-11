# -*- coding: utf-8 -*-
from django.test import SimpleTestCase
from ..scrapers.root_datapackage_scraper import RootDatapackageScraper
import os
from ...committees.models import Committee, CommitteeMeeting
from ..testing.mocks import MockLogger
import datetime


class DatapackageTestCase(SimpleTestCase):

    def given_clean_db(self):
        CommitteeMeeting.objects.filter(committee__knesset_id=2).delete()
        Committee.objects.filter(knesset_id=2).delete()

    def assert_clean_db(self):
        self.assertEqual(CommitteeMeeting.objects.filter(committee_id=2).count(), 0)
        self.assertEqual(Committee.objects.filter(id=2).count(), 0)

    def when_datapackage_was_scraped(self):
        root_datapackage_scraper = RootDatapackageScraper()
        root_datapackage_scraper.logger = logger = MockLogger()
        root_datapackage_scraper.unlock_datapackage()
        zip_file_name = os.path.join(os.path.dirname(__file__), "datapackage_last_120_days_2017-02-24.zip")
        root_datapackage_scraper.load_from_file(zip_file_name)
        self.assertEquals([r.getMessage() for r in logger.info_records],
                          ["loading from local zip file '{}'".format(zip_file_name)])
        root_datapackage_scraper.logger = logger = MockLogger()
        root_datapackage_scraper.log_scrape_return_value(root_datapackage_scraper.scrape_all(True))
        info_messages = [u"{}".format(r.getMessage()) for r in logger.info_records]
        self.assertIn("processed 100 items for scraper CommitteesScraper", info_messages)
        self.assertIn("processed 1468 items for scraper CommitteeMeetingsScraper", info_messages)
        self.assertIn("processed 566 items for scraper CommitteeMeetingProtocolsScraper", info_messages)
        print("\n".join([msg for msg in [u"{}: {}".format(r.levelname, r.getMessage()) for r in logger.all_records] if "2014012" in msg]))

    def assert_model(self, model_instance, expected_dict):
        for field, expected_value in expected_dict.items():
            if field.endswith(".strip"):
                actual_value = getattr(model_instance, field[:-6]).strip()
            else:
                actual_value = getattr(model_instance, field)
            self.assertEqual(actual_value, expected_value)
        return model_instance

    def assert_scraped_data(self):
        committee = self.assert_model(Committee.objects.get(knesset_id=2),
                                      {"knesset_id": 2, "name_eng": "Finance Committee"})
        committee_meeting = self.assert_model(CommitteeMeeting.objects.get(committee=committee, knesset_id="2014012"),
                                              {"date_string": "13/02/2017",
                                               "date": datetime.date(2017, 2, 13),
                                               "topics.strip": u"הוראות ליישום משטר כושר פירעון כלכלי של חברת ביטוח מבוסס Solvency II בהתאם לסעיף 35(ג) לחוק הפיקוח על שירותים פיננסיים (ביטוח), התשמ”א - 1981",
                                               "datetime": datetime.datetime(2017, 2, 13, 13, 30), # 2017-02-13T13:30:00
                                               "knesset_id": 2014012,
                                               "src_url": "http://fs.knesset.gov.il//20/Committees/20_ptv_368875.doc"})
        self.assertTrue(committee_meeting.protocol_text)

    def test(self):
        self.given_clean_db()
        self.assert_clean_db()
        self.when_datapackage_was_scraped()
        self.assert_scraped_data()
