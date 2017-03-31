# Committees data scrapers

## Logic of finding members who attended a committee

* get all the knesset member names (using get_all_mk_names function)
  * gets all the members which are in the current knesset
  * add additional / alternate names for each members (from Person tables)
* go over the committee meeting protocol text
  * uses logic from knesset-data-python for finding members in the protocol
