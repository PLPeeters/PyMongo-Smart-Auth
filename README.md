# PyMongo-Smart-Auth

[![PyPI version](https://badge.fury.io/py/pymongo_smart_auth.svg)](https://badge.fury.io/py/pymongo_smart_auth)

## About

This package extends [PyMongo](https://github.com/mongodb/mongo-python-driver)'s `MongoClient` to provide built-in smart authentication. It simplifies authentication by:

* automatically authenticating when creating the connection instead of having to manually call `authenticate` on the authentication database
* if an authenticated client was created without passing any credentials, it authenticates by:
    1. looking for a `MONGO_CREDENTIAL_FILE` environment variable and associated kwargs in the constructor to format it, if applicable
    2. looking for a `MONGO_AUTHENTICATED_URI` environment variable
    3. looking for credentials in the `MONGO_AUTHENTICATION_DATABASE`, `MONGO_USERNAME` and `MONGO_PASSWORD` environment variables
    4. looking for a `.mongo_credentials` file in the user's home
    5. looking for a `mongo_credentials` file in the `/etc` folder

It also allows the user to specify the path to another credentials file or pass credentials directly.

## Installation

    pip install pymongo_smart_auth

## Usage

The `MongoConnection` class is a drop-in replacement for PyMongo's `MongoClient` that simplifies authentication management.

The constructor works in the same way as the `MongoClient` constructor, with four additional, optional parameters:

* `user`: the user to authenticate with
* `password`: the password to authenticate with
* `credentials_file`: a file where credentials can be found
* `authenticate`: a boolean indicating whether the client should authenticate (defaults to `True`)

When using a credentials file, it should either have a single line with a fully authenticated URI or have the authentication database on the first line, the user on the second and the password on the third. Empty lines are ignored. Example:

    admin
    administrator
    P4ssw0rd

Upon initialisation with the default `authenticate=True`, the client looks for credentials in the following order:

1. The `user` and `password` parameters
2. The passed `credentials_file`
3. The `MONGO_CREDENTIAL_FILE` environment variable formatted with the kwargs of the constructor, if applicable
4. The `MONGO_AUTHENTICATED_URI` environment variable
5. The `MONGO_AUTHENTICATION_DATABASE`, `MONGO_USERNAME` and `MONGO_PASSWORD` environment variables
6. The `.mongo_credentials` file in the user's home
7. The `mongo_credentials` file in the `/etc` folder

Usage examples:

```python
from pymongo_smart_auth import MongoConnection

# Explicit user and password
mongo1 = MongoConnection(user='user', password='p4ssw0rd')
database1 = mongo1['database1'] # Automatically authenticated

# Explicit user and password with separate authentication database
mongo2 = MongoConnection(user='user', password='p4ssw0rd', authentication_database='mongo_users')
database2 = mongo2['database2'] # Automatically authenticated

# Will read /some/path/mongo_credentials
mongo3 = MongoConnection(credentials_file='/some/path/mongo_credentials')
database3 = mongo3['database3'] # Automatically authenticated

# Will read the environment variables if they exist, otherwise ~/.mongo_credentials if it exists, otherwise /etc/mongo_credentials
mongo4 = MongoConnection()
database4 = mongo4['database4'] # Automatically authenticated

# Will authenticate with a file defined in the environment with a keyword argument
# Assuming MONGO_CREDENTIAL_FILE=/etc/credentials_{group}
mongo5 = MongoConnection(group='my_group')
database5 = mongo6['my_group_database'] # Automatically authenticated

# Will not authenticate
mongo6 = MongoConnection(authenticate=False)
database6 = mongo5['database5'] # Not authenticated
```

## License

This project is licensed under the terms of the MIT license.
