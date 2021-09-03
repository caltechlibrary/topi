# Change log for Topi

## Version 1.0.3

* Fix serious bugs in `tind.py`.
* Update test cases to account for changes in entries in Caltech's TIND catalog.


## Version 1.0.2

* Fix bugs in `tind_utils.py`.
* Update required version of [Sidetrack](https://github.com/caltechlibrary/sidetrack) to 2.0.


## Version 1.0.1

* Change approach for setting `tind_url` field on `TindRecord`. (Somehow the test cases previously didn't catch that it wasn't being set at all.)


## Version 1.0.0

* Removed build files accidentally committed during last release.
* Added more info to the [`README` file](README.md).
* Some internal code improvements.


## Version 0.0.2

Renamed the project to Topi (TIND Object Python Interface) to avoid a name clash on PyPI for the name "Potion".


## Version 0.0.1

First release.
