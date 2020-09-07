# PyMongo-Smart-Auth

[![PyPI version](https://badge.fury.io/py/pymongo_smart_auth.svg)](https://badge.fury.io/py/pymongo_smart_auth)

## About

This package extends [PyMongo](https://github.com/mongodb/mongo-python-driver)'s `MongoClient` to provide built-in smart authentication. It simplifies authentication by:

* automatically authenticating when creating the connection instead of having to manually call `authenticate` on the authentication database
* if an authenticated client was created without passing any credentials, it authenticates by:
    1. looking for a `MONGO_AUTHENTICATED_URI` environment variable
    2. looking for credentials in the `MONGO_AUTHENTICATION_DATABASE`, `MONGO_USERNAME` and `MONGO_PASSWORD` environment variables
    3. looking for a `.mongo_credentials` file in the user's home
    4. looking for a `mongo_credentials` file in the `/etc` folder

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
3. The `MONGO_AUTHENTICATED_URI` environment variable
4. The `MONGO_AUTHENTICATION_DATABASE`, `MONGO_USERNAME` and `MONGO_PASSWORD` environment variables
5. The `.mongo_credentials` file in the user's home
6. The `mongo_credentials` file in the `/etc` folder

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

# Will not authenticate
mongo5 = MongoConnection(authenticate=False)
database5 = mongo5['database5'] # Not authenticated
```

## License

This project is licensed under the terms of the MIT license.
