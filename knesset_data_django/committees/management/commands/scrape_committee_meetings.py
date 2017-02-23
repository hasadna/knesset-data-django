# encoding: utf-8
from ....common.management_commands.base_no_args_command import BaseNoArgsCommand
from optparse import make_option
from django.utils.timezone import now, timedelta
from ...scrapers.committee_meetings import CommitteeMeetingsScraper


class Command(BaseNoArgsCommand):
    help = "Scrape latest committee meetings data from the knesset"

    option_list = BaseNoArgsCommand.option_list + (
        make_option('--datapackage', dest='datapackage', action="store_true",
                    help="load from the downloaded datapackage"),
        make_option('--days', dest='days', default=5, type=int,
                    help="scrape meetings with dates from today minus X days"),
        make_option('--committee-ids', dest='committeeids', default='', type=str,
                    help='comma-separated list of committee ids to iterate over (default=all active committees)')
    )

    def handle_noargs(self, **options):
        super(Command, self).handle_noargs(**options)
        if options['datapackage'] and not options['days'] and not options['committeeids']:
            kwargs = {"load_from_datapackage": True}
        else:
            kwargs = {"days": options['days'],
                      "committee_ids": options['committeeids'].split(',') if options['committeeids'] != '' else None}
        self.logger.info('Scraping committee meetings...')
        for committee, update_meeting_results in CommitteeMeetingsScraper().scrape(**kwargs):
            self.logger.info(u'Updating committee: {} ({})'.format(committee.name, committee.knesset_id))
            for meeting_data, meeting_model, error in update_meeting_results:
                if meeting_model:
                    self.logger.info(u'updated meeting {} ({})'.format(meeting_data["id"], meeting_data["datetime"]))
                else:
                    self.logger.info(u'did not update meeting {} ({}): {}'.format(meeting_data["id"], meeting_data["datetime"], error))
