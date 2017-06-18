# -*- coding: utf-8 -*-
from django.test import SimpleTestCase
from ..scrapers.root_datapackage_scraper import RootDatapackageScraper
import os
from ...committees.models import Committee, CommitteeMeeting, ProtocolPart
from ..testing.mocks import MockLogger
import datetime
from ...mks.models import Member, Knesset, Party, Membership
from ...mks.scrapers.members import MembersScraper


#
#
# *** How to use, fix and extend this test ***
#
# This is a comprehensive end to end test of fetching data from a prepare knesset datapackage
#
# To test it we have a prepared datapackage file (which would be updated from time to time)
#
# We use it to load into the test db and then to test what was loaded / updated
#
# ** extracting the test datapackage
# knesset-data-django$ ./manage.py download_knesset_datapackage --file=knesset_data_django/common/tests/datapackage_last_120_days_2017-02-24.zip
# knesset_data_django.common.scrapers.root_datapackage_scraper:112	INFO	loading from local zip file 'knesset_data_django/common/tests/datapackage_last_120_days_2017-02-24.zip'
# knesset_data_django.common.scrapers.root_datapackage_scraper:145	INFO	datapackage available at /home/ori/knesset-data-django/data/datapackage
#
#
# ** examining it's content
# knesset-data-django$ ls data/datapackage/
#
#


class MockRootDatapackageScraper(RootDatapackageScraper):

    SCRAPERS = (
        "knesset_data_django.mks.scrapers.members.MembersScraper",
        "knesset_data_django.committees.scrapers.committees.CommitteesScraper",
        "knesset_data_django.committees.scrapers.committee_meetings.CommitteeMeetingsScraper",
        "knesset_data_django.committees.scrapers.committee_meeting_protocols.CommitteeMeetingProtocolsScraper",
    )

    def _scrape_instance_value(self, from_datapackage, fetch_kwargs, child_scraper_instance, return_value):
        if isinstance(child_scraper_instance, MembersScraper) and return_value[0] and return_value[1]:
            # add some fake data to allow committee meetings to detect it in attending members
            member = return_value[0]
            member.current_party = Party.objects.filter(name=u"העבודה").first()
            member.is_current = True
            member.save()
            membership = Membership(member=member, party=member.current_party, start_date=datetime.date(2000, 2, 2), position=6)
            membership.save()
        return return_value


class DatapackageTestCase(SimpleTestCase):

    TEST_MKS = {896: u'מיקי רוזנטל',
                35: u'משה גפני',
                939: u'רחל עזריה',
                943: u'נאוה בוקר',
                951: u'עודד פורר',
                862: u'מיכל בירן', }

    def given_clean_db(self):
        # import ipdb;ipdb.set_trace()
        Member.objects.filter(id__in=self.TEST_MKS.keys()).delete()
        ProtocolPart.objects.filter(meeting__in=CommitteeMeeting.objects.filter(committee__knesset_id=2)).delete()
        CommitteeMeeting.objects.filter(committee__knesset_id=2).delete()
        Committee.objects.filter(knesset_id=2).delete()

    def given_db_initialized_with_required_data(self):
        knesset = Knesset.objects.current_knesset()
        self.assertTrue(knesset.number > 18)
        if Party.objects.filter(name=u"העבודה").count() == 0:
            party = Party(name=u"העבודה", start_date=datetime.date(2000, 1, 1),
                          number_of_members=60, number_of_seats=3,
                          knesset=knesset)
            party.save()


    def assert_clean_db(self):
        self.assertEqual(Member.objects.filter(id__in=self.TEST_MKS.keys()).count(), 0)
        self.assertEqual(ProtocolPart.objects.filter(meeting__in=CommitteeMeeting.objects.filter(committee__knesset_id=2)).count(), 0)
        self.assertEqual(CommitteeMeeting.objects.filter(committee_id=2).count(), 0)
        self.assertEqual(Committee.objects.filter(id=2).count(), 0)

    def when_datapackage_was_scraped_with_future_enabled(self):
        root_datapackage_scraper = MockRootDatapackageScraper(enable_the_future=True)
        if os.environ.get("SKIP_EXTRACT", "") != "1":
            root_datapackage_scraper.logger = logger = MockLogger()
            root_datapackage_scraper.unlock_datapackage()
            root_datapackage_scraper.load_from_directory(os.path.join(os.path.dirname(__file__), "datapackage"))
            self.assertEquals([r.getMessage() for r in logger.info_records],
                              ["loading from local directory '{}'".format(os.path.join(os.path.dirname(__file__), "datapackage"))])
        root_datapackage_scraper.logger = logger = MockLogger()
        root_datapackage_scraper.log_scrape_return_value(root_datapackage_scraper.scrape_all(True))
        info_messages = [u"{}".format(r.getMessage()) for r in logger.info_records]
        self.assertIn("processed 946 items for scraper MembersScraper", info_messages)
        self.assertIn("processed 100 items for scraper CommitteesScraper", info_messages)
        self.assertIn("processed 34 items for scraper CommitteeMeetingsScraper", info_messages)
        self.assertIn("processed 6 items for scraper CommitteeMeetingProtocolsScraper", info_messages)
        # for debugging (add -s to see output when tests pass)
        print("\n".join([msg for msg in [u"{}: {}".format(r.levelname, r.getMessage()) for r in logger.all_records] if "2014012" in msg or "896" in msg]))

    def assert_model(self, model_instance, expected_dict):
        for field, expected_value in expected_dict.items():
            if field.endswith(".strip"):
                actual_value = getattr(model_instance, field[:-6]).strip()
            else:
                actual_value = getattr(model_instance, field)
            self.assertEqual(actual_value, expected_value)
        return model_instance

    def assert_scraped_data(self):
        # members
        members = Member.objects.filter(id__in=self.TEST_MKS.keys())
        self.assertEqual(members.count(), len(self.TEST_MKS))
        for member in members:
            self.assert_model(member, {"name": self.TEST_MKS[member.id]})

        # committees
        committee = self.assert_model(Committee.objects.get(knesset_id=2),
                                      {"knesset_id": 2, "name_eng": "Finance Committee"})

        # committee meetings
        committee_meeting = self.assert_model(CommitteeMeeting.objects.get(committee=committee, knesset_id="2014012"),
                                              {"date_string": "13/02/2017",
                                               "date": datetime.date(2017, 2, 13),
                                               "topics.strip": u"הוראות ליישום משטר כושר פירעון כלכלי של חברת ביטוח מבוסס Solvency II בהתאם לסעיף 35(ג) לחוק הפיקוח על שירותים פיננסיים (ביטוח), התשמ”א - 1981",
                                               "datetime": datetime.datetime(2017, 2, 13, 13, 30), # 2017-02-13T13:30:00
                                               "knesset_id": 2014012,
                                               "src_url": "http://fs.knesset.gov.il//20/Committees/20_ptv_368875.doc"})

        # committee meeting protocol text and parts
        self.assertTrue("Solvency II" in committee_meeting.protocol_text)
        self.assertTrue(u"פרוטוקול מס' 647" in committee_meeting.parts.get(order=1).body)
        self.assertTrue(u"סדר-היום" == committee_meeting.parts.get(order=2).header)

        # committee meeting attending members
        self.assertEqual({mk.id: mk.name             for mk   in committee_meeting.mks_attended.all()},
                         {mkid : self.TEST_MKS[mkid] for mkid in [35, 862, 896, 939, 943, 951]})

    def test(self):
        self.given_clean_db()
        self.given_db_initialized_with_required_data()
        self.assert_clean_db()
        self.when_datapackage_was_scraped_with_future_enabled()  # we have to enable future to get MKs
        self.assert_scraped_data()
