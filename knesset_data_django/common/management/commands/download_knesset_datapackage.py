# encoding: utf-8
from knesset_data_django.common.management_commands.base_no_args_command import BaseNoArgsCommand
from optparse import make_option
from ...scrapers.root_datapackage_scraper import RootDatapackageScraper


class Command(BaseNoArgsCommand):
    help = "Download a knesset datapackage zip and extract appropriately to be used by the scrapers"

    option_list = BaseNoArgsCommand.option_list + (
        make_option('--file', dest='file', default='', type=str, help='path to datapackage.zip file'),
        make_option('--url', dest='url', default='', type=str, help='url to download datapackage.zip file from'),
        make_option('--remove-lock', action="store_true", help="remove the lock from the datapackage directory"),
        make_option('--scrape', action='store_true', help="run the relevant scrapers after extracting the datapackage"),
        make_option('--include', default="", type=str, help="include only resources that start with the given string/s (comma-separated)"),
        make_option('--exclude', default="", type=str, help="exclude resources that start with the given string/s (comma-separated)"),
        make_option('--future', action="store_true", help="include futuristic features, use with caution!"),
    )

    def handle_noargs(self, **options):
        super(Command, self).handle_noargs(**options)
        if not options['file'] and not options['url'] and not options['remove_lock'] and not options['scrape']:
            self.print_help("./manage.py", "download_knesset_datapackage")
        else:
            root_datapackage_scraper = RootDatapackageScraper(enable_the_future=options["future"])
            if options['remove_lock']:
                root_datapackage_scraper.unlock_datapackage()
                self.logger.info("datapackage forcefully unlocked!")
            if options['file']:
                root_datapackage_scraper.log_load_from_file_return_value(root_datapackage_scraper.load_from_file(options['file']))
            elif options['url']:
                root_datapackage_scraper.log_load_from_url_return_value(root_datapackage_scraper.load_from_url(options['url']))
            if options['scrape']:
                fetch_kwargs = {}
                if options.get("include"):
                    fetch_kwargs["include"] = options["include"].split(",")
                if options.get("exclude"):
                    fetch_kwargs["exclude"] = options["exclude"].split(",")
                root_datapackage_scraper.log_scrape_return_value(root_datapackage_scraper.scrape_all(True, fetch_kwargs))

