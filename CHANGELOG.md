Changelog
=========

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
