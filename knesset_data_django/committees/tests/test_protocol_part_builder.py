# -*- coding: utf-8 -*
import datetime
import factory
from django.test import TestCase
from ..models import CommitteeMeeting
from knesset_data_django.committees.protocol_part_builder import CommitteeProtocolPartBuilder
from .testapp import TestApp


class CommitteeMeetingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommitteeMeeting

    committee_id = 1
    date = datetime.datetime.now().date()


class ProtocolPartBuilderTestCase(TestCase):
    def setUp(self):
        super(ProtocolPartBuilderTestCase, self).setUp()

    def tearDown(self):
        super(ProtocolPartBuilderTestCase, self).tearDown()

    def when_committee_protocol_part_builder_is_called_with_part_data(self, header, body, mks, meeting=None,
                                                                      order=None):
        order = order or 2
        meeting = meeting or CommitteeMeetingFactory()
        return CommitteeProtocolPartBuilder(meeting=meeting, order=order, header=header, body=body, mks=mks).build()

    def verify_protocol_part_created_with_expected_body_header_and_speaker_id(self, part_to_check, expected_body,
                                                                              expected_header, expected_speaker_id):
        self.assertEqual(part_to_check.speaker_id, expected_speaker_id)
        self.assertEqual(part_to_check.body, expected_body)
        self.assertEqual(part_to_check.header, expected_header)

    def test_protocol_part_builder_creates_protocl_parts_with_speaker_id(self):
        knesset = TestApp.given_knesset_exists(number=19)
        party = TestApp.given_party_exists_in_knesset('labor', knesset)
        mk = TestApp.given_member_exists_in_knesset(u'סתיו שפיר', party=party)
        TestApp.given_person_alias_exists(u'בוגי בוגי', mk.person.get())

        part = self.when_committee_protocol_part_builder_is_called_with_part_data(header=u'חברת הכנסת סתיו שפיר',
                                                                                  body=u'אמרה הערב כך וגם אחרת',
                                                                                  mks=[mk])
        self.verify_protocol_part_created_with_expected_body_header_and_speaker_id(part,
                                                                                   expected_body=u'אמרה הערב כך וגם אחרת',
                                                                                   expected_header=u'חברת הכנסת סתיו שפיר',
                                                                                   expected_speaker_id=mk.person.get().id)
