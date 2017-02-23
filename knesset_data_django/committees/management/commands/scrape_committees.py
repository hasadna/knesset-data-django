# encoding: utf-8
from ...scrapers.committees import CommitteesScraper
from knesset_data_django.common.management_commands.base_datapackage_command import BaseDatapackageCommand


class Command(BaseDatapackageCommand):
    help = "Fetch the all the active committees information from the knesset and update existing"

    def handle_noargs(self, **options):
        load_from_datapackage, override_fetch_kwargs = super(Command, self).handle_noargs(**options)
        for committee, created in CommitteesScraper().scrape_active_committees():
            if created:
                self.logger.info(u"created committee {} - {}".format(committee.id, committee.name))
            else:
                self.logger.info(u'updated committee {} - {}'.format(committee.id, committee.name))
