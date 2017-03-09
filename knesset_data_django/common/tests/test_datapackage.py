# -*- coding: utf-8 -*-
from django.test import SimpleTestCase
from ..scrapers.root_datapackage_scraper import RootDatapackageScraper
import os
from ...committees.models import Committee, CommitteeMeeting
from django.conf import settings
import logging
from ..testing.mocks import MockLogger


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
        print("\n".join([msg for msg in [u"{}: {}".format(r.levelname, r.getMessage()) for r in logger.all_records] if "2014304" in msg]))


    def assert_scraped_data(self):
        # committee
        committee = Committee.objects.get(knesset_id=2)
        for field, expected_value in {"knesset_id": 2, "name_eng": "Finance Committee"}.items():
            self.assertEqual(getattr(committee, field), expected_value)
        # committee meeting
        committee_meeting = CommitteeMeeting.objects.get(committee=committee, knesset_id="2014012")
        print(committee_meeting)

    def test(self):
        self.given_clean_db()
        self.assert_clean_db()
        self.when_datapackage_was_scraped()
        self.assert_scraped_data()
