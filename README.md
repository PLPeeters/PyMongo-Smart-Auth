# PyMongo-Smart-Auth

[![PyPI version](https://badge.fury.io/py/pymongo_smart_auth.svg)](https://badge.fury.io/py/pymongo_smart_auth)

## About

This package extends [PyMongo](https://github.com/mongodb/mongo-python-driver) to provide built-in smart authentication.

## Installation

    pip install pymongo_smart_auth

## Usage

The `MongoConnection` class is a drop-in replacement for the PyMongo `MongoClient` that simplifies authentication management and uses the singleton pattern. This means every unique set of parameters will only create one connection to MongoDB.

Three optional parameters have been added to the constructor:

* `user`: the user to authenticate with
* `password`: the password to authenticate with
* `credentials_file`: a file where credentials can be found
* `authenticate`: a boolean indicating whether the client should authenticate (defaults to `True`)

When using a credentials file, it should have the authentication database on the first line, the user on the second and the password on the third. Example:

    admin
    administrator
    P4ssw0rd

Upon initialisation, the client looks for credentials in the following order:

1. The `user` and `password` parameters
2. The passed `credentials_file`
3. The `.mongo_credentials` file in the user's home

Usage examples:

```python
from pymongo_smart_auth import MongoConnection

# Explicit user and password
mongo1 = MongoConnection(user='user', password='p4ssw0rd')
database1 = mongo1['database1'] # Automatically authenticated

# Explicit user and password with separate authentication database
mongo2 = MongoConnection(user='user', password='p4ssw0rd', authentication_database='mongo_users')
database2 = mongo2['database2'] # Automatically authenticated

# Will read /etc/.mongo_credentials
mongo3 = MongoConnection(credentials_file='/etc/.mongo_credentials')
database3 = mongo3['database3'] # Automatically authenticated

# Will read ~/.mongo_credentials
mongo4 = MongoConnection()
database4 = mongo4['database4'] # Automatically authenticated

# Will not authenticate
mongo5 = MongoConnection(authenticate=False)
database5 = mongo5['database5'] # Not authenticated
```

## License

This project is licensed under the terms of the MIT license.
