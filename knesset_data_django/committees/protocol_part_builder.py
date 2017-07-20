# -*- coding: utf-8 -*

from knesset_data.protocols.protocol_header_parser import ProtocolHeaderParser
from collections import namedtuple

from ..persons.models import Person, PersonAlias
from .models import ProtocolPart

ProtocolPartResult = namedtuple('ProtocolPartResult', ['meeting', 'order', 'header', 'body', 'speaker'])


def create_person_name_mk_id_map(mks):
    persons = Person.objects.filter(mk__in=mks).select_related()
    aliases = PersonAlias.objects.filter(person__in=persons).select_related()
    persons_map = dict()
    for person in persons:
        persons_map[person.name] = person.mk.id

    for alias in aliases:
        persons_map[alias.name] = alias.person.mk.id

    return persons_map


class CommitteeProtocolPartBuilder(object):
    def __init__(self, meeting, order, header, body, mks):
        self.mks = mks
        self.committee_meeting = meeting
        self.order = order
        self.header = header

        self.body = body

    def build(self):
        # mapped_names_ids = create_person_name_mk_id_map(self.mks)
        # header_text, speaker_id = ProtocolHeaderParser(self.header, mapped_names_ids).parse()
        return ProtocolPart(meeting=self.committee_meeting,
                            order=self.order,
                            body=self.body,
                            # speaker_id=speaker_id,
                            header=self.header)
