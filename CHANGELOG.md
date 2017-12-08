Changelog
=========

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
