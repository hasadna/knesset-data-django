import logging, os


from django_nose import NoseTestSuiteRunner


class KnessetDataDjangoTestRunner(NoseTestSuiteRunner):

    def setup_test_environment(self, **kwargs):
        # Disabling debug/info in testing
        logging.disable(logging.WARNING)
        return super(KnessetDataDjangoTestRunner, self).setup_test_environment(**kwargs)

    def teardown_databases(self, old_config, **kwargs):
        if os.environ.get("REUSE_DB") != "1" and os.environ.get("KEEP_DB") != "1":
            return super(KnessetDataDjangoTestRunner, self).teardown_databases(old_config, **kwargs)
