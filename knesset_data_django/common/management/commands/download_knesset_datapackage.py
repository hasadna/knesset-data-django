# encoding: utf-8
from knesset_data_django.common.management_commands.base_no_args_command import BaseNoArgsCommand
from optparse import make_option
from knesset_datapackage.root import RootDatapackage
from django.conf import settings


class Command(BaseNoArgsCommand):
    help = "Download a knesset datapackage zip and extract appropriately to be used by the scrapers"

    option_list = BaseNoArgsCommand.option_list + (
        make_option('--file', dest='file', default='', type=str,
                    help='path to datapackage.zip file'),
    )

    def handle_noargs(self, **options):
        super(Command, self).handle_noargs(**options)
        RootDatapackage.load_from_zip(options['file'], settings.DATA_ROOT)
