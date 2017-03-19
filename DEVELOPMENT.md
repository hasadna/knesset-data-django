# knesset-data-django development guide

## Testing / using the project directly

The project includes a testing django app which replicates Open Knesset app -
this can be used for testing and also provides documentation.

##### Preconditions

* You have the following directories as siblings under the same root directory:
  * knesset-data-python - clone of knesset-data-python repository
  * knesset-data-django - clone of knesset-data-django repository
  * Open-Knesset - clone of Open Knesset repository
* You are running inside knesset-data-django python virtualenv

##### Install requiremnets

* `(knesset-data-django) $ pip install -r dev_requirements.txt`

##### Create the DB and migrate (uses Sqlite3 by default)

* `(knesset-data-django) $ ./manage.py syncdb`
* `(knesset-data-django) $ ./manage.py migrate`

##### Running management commands

For example, the following commands will fill in committees data in your DB

* `(knesset-data-django) $ ./manage.py scrape_committees -v2`
* `(knesset-data-django) $ ./manage.py scrape_committee_meetingss --from_days=60 -v2`

##### Using shell-plus to interact with the data

* `(knesset-data-django) $ ./manage.py shell_plus`
* `> CommitteeMeeting.objects.count()`

## Running the automated tests

* `(knesset-data-django) $ ./manage.py test`

If you want to save time on tests or inspect the test db, you can use REUSE_DB parameter:

* First time, run:
  * `KEEP_DB=1 ./manage.py test`

* This keeps the db at test.db and you can re-run the tests on the same DB using:
  * `REUSE_DB=1 ./manage.py test`

* Some changes require creating a fresh DB, you can just delete test.db and run `KEEP_DB=1 ./manage.py test`

## Integrating with existing Django project (AKA Open Knesset)

##### preconditions / assumptions

* existing project is in directory /home/user/Open-Knesset
* existing project is inside a virtualenv called "oknesset"
* clone of knesset-data-django git repo is in /home/user/knesset-data-django

##### installation

* install knesset-data and knesset-data-django in the existing project virtualenv
  * `(oknesset) ~/Open-Knesset$ pip install -e ../knesset-data-python`
  * `(oknesset) ~/Open-Knesset$ pip install -e ../knesset-data-django`
* add the relevant knesset-data-django apps to INSTALLED_APPS in your project's django settings
  * `from knesset_data_django import KNESSET_DATA_DJANGO_APPS`
  * `INSTALLED_APPS += KNESSET_DATA_DJANGO_APPS`

## See also

* [Scrapers guide](/SCRAPERS.md)
