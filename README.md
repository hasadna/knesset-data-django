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

**Just want to use the project from Open Knesset?** [Check out the usage guide](/USAGE.md)

### Known issues / FAQ / Common problems
* [Why does this project have a setting file?](https://github.com/hasadna/knesset-data-django/issues/5)

### Documentation

* [Usage guide](/USAGE.md) - How to use the knesset-data-django in other projects (e.g. open knesset)
* [Development guide](/DEVELOPMENT.md) - Details for developers intending to work on Knesset-data-django.
* [Scrapers guide](/SCRAPERS.md) - Scraping is a main part of this project, this document provides details about the scraping architecture, how to add new scrapers or modify existing scrapers.
