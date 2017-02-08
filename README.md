# Django-specific APis and modules for working with Knesset data

[![Build Status](https://travis-ci.org/hasadna/knesset-data-django.svg?branch=master)](https://travis-ci.org/hasadna/knesset-data-django)

Part of [Knesset data project](https://github.com/hasadna/knesset-data/)

APIs and Python modules specific to usage with Django.

Specifically, it means usage by Open Knesset, but we try to be as separate from it as possible.

Generally, it is meant to contain well documented and tested code that handles the following aspects of the knesset data:

* Scrapers - which allow to get the data and store it in DB
* Export data from the DB
* Provide insights / calculations on top of the data in DB
* Logic to support viewing the data from the DB (but not actually rendering any views)

### Documentation

* [Development guide](/DEVELOPMENT.md)
* [Scrapers guide](/SCRAPERS.md)
