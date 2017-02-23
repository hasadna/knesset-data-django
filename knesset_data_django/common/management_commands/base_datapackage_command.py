from .base_no_args_command import BaseNoArgsCommand
from optparse import make_option


class BaseDatapackageCommand(BaseNoArgsCommand):
    """
    should be used as base class for commands which interact with datapackages
    """

    option_list = BaseNoArgsCommand.option_list + (
        make_option('--datapackage', dest='load_from_datapackage', action="store_true",
                    help='Load data from the last downloaded datapackage (using download_knesset_datapackage management command)'),
        make_option('--fetch-kwargs', dest='fetch_kwargs', type=str,
                    help='Override the kwargs used to make the datapackage with the given JSON object'),
    )

    def handle_noargs(self, **options):
        super(BaseDatapackageCommand, self).handle_noargs(**options)
        load_from_datapackage = options.get("load_from_datapackage")
        override_fetch_kwargs = options.get("fetch_kwargs")
        if load_from_datapackage and override_fetch_kwargs:
            raise Exception("you must choose either to load from datapackage or override fetch kwargs, not both")
        return load_from_datapackage, override_fetch_kwargs
