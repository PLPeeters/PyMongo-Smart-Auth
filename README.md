# PyMongo-Smart-Auth

[![PyPI version](https://badge.fury.io/py/pymongo-smart-auth.svg)](https://badge.fury.io/py/pymongo-smart-auth)

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

    pip install pymongo-smart-auth

## Usage

The `MongoClient` class from the `PyMongo-Smart-Auth` package is a drop-in replacement for PyMongo's `MongoClient` that simplifies authentication management.

The constructor works in the same way as the `MongoClient` constructor with four additional parameters, all optional:

* `username`: the username to authenticate with
* `password`: the password to authenticate with
* `credentials_file`: a file where credentials can be found
* `authenticate`: a boolean indicating whether the client should authenticate (defaults to `True`)

### Credentials file

When using a credentials file, it should either have:

* a single line with a fully authenticated URI
* the authentication database on the first line, the user on the second and the password on the third. Empty lines are ignored. Example file:

        admin
        administrator
        P4ssw0rd

### Credential lookup order

Upon initialisation with the default `authenticate=True`, the client looks for credentials in the following order:

1. The `username` and `password` parameters
2. The passed `credentials_file`
3. The `MONGO_CREDENTIAL_FILE` environment variable formatted with the kwargs of the constructor, if applicable
4. The `MONGO_AUTHENTICATED_URI` environment variable
5. The `MONGO_AUTHENTICATION_DATABASE`, `MONGO_USERNAME` and `MONGO_PASSWORD` environment variables
6. The `.mongo_credentials` file in the user's home
7. The `mongo_credentials` file in the `/etc` folder

### Usage examples

```python
from pymongo_smart_auth import MongoClient

# Explicit user and password
mongo1 = MongoClient(username='user', password='p4ssw0rd')
database1 = mongo1['database1'] # Automatically authenticated

# Explicit user and password with separate authentication database
mongo2 = MongoClient(username='user', password='p4ssw0rd', authentication_database='mongo_users')
database2 = mongo2['database2'] # Automatically authenticated

# Will read /some/path/mongo_credentials
mongo3 = MongoClient(credentials_file='/some/path/mongo_credentials')
database3 = mongo3['database3'] # Automatically authenticated

# Will read the file in the MONGO_CREDENTIAL_FILE environment variable if set,
# then the file in MONGO_CREDENTIAL_FILE environment variable if set,
# then the MONGO_AUTHENTICATION_DATABASE, MONGO_USERNAME and MONGO_PASSWORD environment variables if set,
# then ~/.mongo_credentials if it exists,
# otherwise /etc/mongo_credentials
mongo4 = MongoClient()
database4 = mongo4['database4'] # Automatically authenticated

# Will authenticate with a file defined in the environment with a keyword argument
# Assuming MONGO_CREDENTIAL_FILE=/etc/credentials_{group},
# this will authenticate with the credentials in /etc/credentials_my_group
mongo5 = MongoClient(group='my_group')
database5 = mongo6['my_group_database'] # Automatically authenticated

# Will not authenticate
mongo6 = MongoClient(authenticate=False)
database6 = mongo5['database5'] # Not authenticated
```

## License

This project is licensed under the terms of the MIT license.
