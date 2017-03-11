# Using the Knesset-data-django from Open Knesset

This document assumes you have a properly installed Open Knesset environment and you would like to use knesset-data-django features from it.

## Available commands

* `./manage.py download_knesset_datapackage`
  * Supports downloading or extracing a previously prepared datapackage file
  * The knesset-data-datapackage project creates a package every day, you can download those packages
     * for example - https://s3.amazonaws.com/knesset-data/datapackage_last_120_days_2017-03-10.zip
     * check the [knesset-data-datapackage project](https://github.com/hasadna/knesset-data-datapackage/blob/master/README.md) for more details
  * to download directly from a url, use the following command:
    * `./manage.py download_knesset_datapackage --url=https://s3.amazonaws.com/knesset-data/datapackage_last_120_days_2017-03-10.zip`
  * you can add the --scrape parameter to also start the relevant scrapers to update from the downloaded datapackage
  * run with --help to see the available options

* `make_knesset_datapackage`
  * available from the knesset_data_datapackage project - allows to create a datapackage with different parameters then the one uploaded to S3
  * bear in mind that Knesset might block your IP and is generally buggy, so it might not always work
  * it creates the datapackage in data/datapackage directory
