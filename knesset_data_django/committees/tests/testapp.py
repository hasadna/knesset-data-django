# -*- coding: utf-8 -*
import datetime

from ...persons.models import PersonAlias, Person
from ...mks.models import Knesset, Party, Member

ten_days_ago = datetime.datetime.today() - datetime.timedelta(days=10)
two_days_ago = datetime.datetime.today() - datetime.timedelta(days=2)


class TestApp(object):
    @classmethod
    def given_knesset_exists(cls, start_date=ten_days_ago, number=2, end_date=None):
        if Knesset.objects.filter(number=number).exists():
            return Knesset.objects.get(number=number)

        knesset = Knesset.objects.create(number=number,
                                         start_date=start_date, end_date=end_date)
        return knesset

    @classmethod
    def given_party_exists_in_knesset(cls, party_name, knesset):
        party, create = Party.objects.get_or_create(name='{0}_{1}'.format(party_name, knesset.number),
                                                    knesset=knesset,
                                                    start_date=knesset.start_date,
                                                    end_date=knesset.end_date)
        return party

    @classmethod
    def given_member_exists_in_knesset(cls, member_name, party, start_date=ten_days_ago.date(), end_date=None):
        member, create = Member.objects.get_or_create(name=member_name, start_date=ten_days_ago.date())
        # membership, create = Membership.objects.get_or_create(member=member, party=party,
        #                                                       start_date=party.knesset.start_date)
        # if end_date:
        #     membership.end_date = end_date
        #     membership.save()
        return member

    @classmethod
    def given_person_alias_exists(cls, alias_name, person):
        alias, create = PersonAlias.objects.get_or_create(name=alias_name, person=person)
        return alias
