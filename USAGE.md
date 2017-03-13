# Using the Knesset-data-django from Open Knesset

This document assumes you have a properly installed Open Knesset environment and you would like to use knesset-data-django features from it.

## how to fetch updated data form the Knesset

Best way is to download a prepared datapackage, knesset-data-datapackage project does that and uploads to S3, for example - `https://s3.amazonaws.com/knesset-data/datapackage_last_120_days_2017-03-10.zip`

Alternatively, you can make a datapackage locally, but bear in mind that Knesset blocks some IPs sometimes, so it might not always work.

* To create a datapackage, you can use the `make_knesset_datapackage` command which is available from knesset-data-datapackage module.
* To download a prepared datapackage, use the `./manage.py download_knesset_datapackage` command with --url param

See Available commands section below for more details.

## Available commands

* `make_knesset_datapackage`
  * creates the datapackage in data/datapackage directory
  * check the options (`--help`) to see how you can modify the datapackage creation
  * if you don't pass the --zip option it will create the datapackage ready to be scraped:
    * `./manage.py download_knesset_datapackage --scrape`

* `./manage.py download_knesset_datapackage`
  * Supports downloading or extracing a previously prepared datapackage file
  * The knesset-data-datapackage project creates a package every day, you can download those packages
     * for example - https://s3.amazonaws.com/knesset-data/datapackage_last_120_days_2017-03-10.zip
     * check the [knesset-data-datapackage project](https://github.com/hasadna/knesset-data-datapackage/blob/master/README.md) for more details
  * to download a prepared datapackage from a url, use the following command:
    * `./manage.py download_knesset_datapackage --url=https://s3.amazonaws.com/knesset-data/datapackage_last_120_days_2017-03-10.zip`
  * you can add the --scrape parameter to also start the relevant scrapers to update from the downloaded datapackage
  * run with --help to see the available options
