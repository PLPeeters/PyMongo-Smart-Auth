Changelog
=========

**2.1.0**

* Added AsyncMongoClient for supported PyMongo versions (≥ 4.9)

**2.0.0**

* Added support for PyMongo >= 4.0
* Renamed the `user` parameter to `username` to be consistent with the PyMongo 4.0 interface
* Dropped support for Python < 3.6

**1.3.0**

* Added support for Python 3.10
* Renamed the import to `MongoClient` to make the package truly drop-in, meaning you can just change your import to `from pymongo_smart_auth import MongoClient` when transitioning from PyMongo and _voilà_ (to avoid breaking compatibility with older code, `MongoConnection` can still be imported)

**1.2.1**

* Fixed client not properly initialising when authentication is disabled.

**1.2.0**

* Added support for `MONGO_CREDENTIAL_FILE` environment variable that should contain a string with a path to a credential file to use. The string may be a format string, in which case it will be formatted using the `kwargs` passed to the constructor.

**1.1.0**

* Added support for a `MONGO_AUTHENTICATED_URI` environment variable that should contain a fully authenticated MongoDB URI
* Added support for single-line credential files, which are assumed to contain a fully authenticated URI
* Tweaked credential file parser to ignore blank lines

**1.0.3**

* Updated `__init__.py` to avoid crashing with Python 3

**1.0.2**

* Added a class variable to prevent showing the warning for authenticated connections without credentials more than once

**1.0.0**

* When no credentials are provided for an authenticated connection, the client now logs a warning instead of raising an exception
* Switched to a specific logger instead of using the root logger
* Removed unnecessary instance attributes

**0.6.0**

* Added the ability to fetch credentials from environment variables

**0.5.1**

* Moved the username, password and authentication database to instance variables

**0.5.0**

* Moved authentication to the initialisation instead of authenticating only when fetching a database

**0.4.0**

* Made the MongoClient a regular class instead of a singleton, because the singleton pattern broke things such as forking

**0.3.0**

* Added support for server credentials in /etc/mongo_credentials

**0.2.1**

* Fixed singleton not working properly due to overridden `__init__` method

**0.2.0**

* Added init parameter to allow disabling authentication

**0.1.6**

* Added warnings when `~/.mongo_credentials` file is readable by the group or others

**0.1.5**

* Added support for a separate authentication database

**0.1**

* Initial commit
