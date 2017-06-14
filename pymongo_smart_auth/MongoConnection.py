import logging
import os
import stat
import sys

from pymongo import MongoClient
from pymongo.errors import ConfigurationError


class MongoConnection(MongoClient):
    USER_CREDENTIALS = '%s/.mongo_credentials' % os.path.expanduser('~')
    SERVER_CREDENTIALS = '/etc/mongo_credentials'

    # On Unix systems, check the permissions of the credentials file
    if sys.platform in ('linux', 'linux2', 'darwin') and os.path.exists(USER_CREDENTIALS):
        # Get the file stats
        cred_file_stats = os.stat(USER_CREDENTIALS)

        # Issue a warning if the file is group readable
        if bool(cred_file_stats.st_mode & stat.S_IRGRP):
            logging.warn("{0} is readable by the group. It should only be readable by the user. Fix by running:\nchmod 600 \"{0}\"".format(USER_CREDENTIALS))

        # Issue a warning if the file is readable by others
        if bool(cred_file_stats.st_mode & stat.S_IROTH):
            logging.warn("{0} is readable by others. It should only be readable by the user. Fix by running:\nchmod 600 \"{0}\"".format(USER_CREDENTIALS))

    def __init__(
            self,
            host=None,
            port=None,
            document_class=dict,
            tz_aware=False,
            connect=True,
            user=None,
            password=None,
            authentication_database=None,
            credentials_file=None,
            authenticate=True,
            **kwargs):
        """MongoDB connection with built-in authentication."""

        super(MongoConnection, self).__init__(host, port, document_class, tz_aware, connect, **kwargs)

        self.authenticate = authenticate

        # If authentication is on for this connection
        if authenticate:
            # If no user was passed, try to get the credentials from the filesystem
            if user is None:
                # If no credentials file was passed
                if credentials_file is None:
                    # Use the first existing credentials file between the one in the
                    # user's home and the one in /etc
                    if os.path.exists(MongoConnection.USER_CREDENTIALS):
                        credentials_file = MongoConnection.USER_CREDENTIALS
                    elif os.path.exists(MongoConnection.SERVER_CREDENTIALS):
                        credentials_file = MongoConnection.SERVER_CREDENTIALS
                    else:
                        raise ConfigurationError("No configuration file found at either '%s' or '%s'." % (MongoConnection.USER_CREDENTIALS, MongoConnection.SERVER_CREDENTIALS))

                try:
                    # Try to open the credentials file
                    with open(credentials_file) as credentials_file_obj:
                        try:
                            # Read the file
                            lines = credentials_file_obj.readlines()

                            # Get the authentication database, user and password from the contents
                            authentication_database = lines[0].strip()
                            user = lines[1].strip()
                            password = lines[2].strip()
                        except IndexError:
                            raise ConfigurationError("Credentials file '%s' is wrongly formatted." % credentials_file)
                except IOError:
                    raise ConfigurationError("Could not open '%s'." % credentials_file)
            elif password is None:
                raise ConfigurationError("A password is required.")

            self.user = user
            self.password = password
            self.authentication_database = authentication_database

    def __getitem__(self, name):
        """Get an authenticated database by name.

        Raises :class:`~pymongo.errors.InvalidName` if an invalid
        database name is used.

        :Parameters:
          - `name`: the name of the database to get
        """

        # Get the database object
        db = super(MongoConnection, self).__getitem__(name)

        # If authentication is turned on, authenticate before returning the database
        if self.authenticate:
            db.authenticate(self.user, self.password, self.authentication_database)

        return db
