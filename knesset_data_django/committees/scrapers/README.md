# Committees data scrapers

## Logic of finding members who attended a committee

* get all the knesset member names
  * see [mks documentation](https://github.com/hasadna/knesset-data-django/tree/master/knesset_data_django/mks#getting-all-member-names-get_all_mk_names) for details
* go over the committee meeting protocol text and find member names from the list from previous step
  * uses logic from knesset-data-python to that, see [the relevant knesst-data-python docs](https://github.com/hasadna/knesset-data-python/blob/master/knesset_data/protocols/README.md#attending-members-logic) for details
