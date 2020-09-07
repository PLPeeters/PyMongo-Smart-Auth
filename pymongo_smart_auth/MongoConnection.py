import logging
import os
import stat
import sys

from pymongo import MongoClient
from pymongo.errors import ConfigurationError

logging.basicConfig()
logger = logging.getLogger('pymongo_smart_auth')


class MongoConnection(MongoClient):
    USER_CREDENTIALS = '%s/.mongo_credentials' % os.path.expanduser('~')
    SERVER_CREDENTIALS = '/etc/mongo_credentials'
    __missing_credentials_warning_shown = False

    # On Unix systems, check the permissions of the credentials file
    if sys.platform in ('linux', 'linux2', 'darwin') and os.path.exists(USER_CREDENTIALS):
        # Get the file stats
        cred_file_stats = os.stat(USER_CREDENTIALS)

        # Issue a warning if the file is group readable
        if bool(cred_file_stats.st_mode & stat.S_IRGRP):
            logger.warning("{0} is readable by the group. It should only be readable by the user. Fix by running:\nchmod 600 \"{0}\"".format(USER_CREDENTIALS))

        # Issue a warning if the file is readable by others
        if bool(cred_file_stats.st_mode & stat.S_IROTH):
            logger.warning("{0} is readable by others. It should only be readable by the user. Fix by running:\nchmod 600 \"{0}\"".format(USER_CREDENTIALS))

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

        # If authentication is on for this connection
        if authenticate:
            # If no user was passed, try to get the credentials elsewhere
            if user is None:
                # If no credentials file was passed
                if credentials_file is None:
                    # Attempt to get the configuration from the environment
                    authenticated_mongodb_uri = os.environ.get('MONGO_AUTHENTICATED_URI') or None
                    authentication_database = os.environ.get('MONGO_AUTHENTICATION_DATABASE') or None
                    user = os.environ.get('MONGO_USERNAME') or None
                    password = os.environ.get('MONGO_PASSWORD') or None

                    values_to_check = {authentication_database, user, password}

                    # If there are undefined environment variables
                    if authenticated_mongodb_uri is None and None in values_to_check:
                        # If they aren't all undefined, raise a ConfigurationError
                        if len(values_to_check) > 1:
                            raise ConfigurationError("MONGO_AUTHENTICATED_URI environment variable not set and missing other environment variables.")

                        # Fall back to the first existing credentials file
                        # between the one in the user's home and the one in /etc
                        if os.path.exists(MongoConnection.USER_CREDENTIALS):
                            credentials_file = MongoConnection.USER_CREDENTIALS
                        elif os.path.exists(MongoConnection.SERVER_CREDENTIALS):
                            credentials_file = MongoConnection.SERVER_CREDENTIALS
                        elif not self.__missing_credentials_warning_shown:
                            logger.warning("MongoConnection is authenticated but no credential file was found at either '%s' or '%s' and environment variables were not defined." % (MongoConnection.USER_CREDENTIALS, MongoConnection.SERVER_CREDENTIALS))

                            self.__missing_credentials_warning_shown = True

                # If there is a credentials file to check
                if credentials_file is not None:
                    try:
                        # Try to open the credentials file
                        with open(credentials_file) as credentials_file_obj:
                            # Read the file
                            lines = [line.strip() for line in credentials_file_obj.readlines() if line.strip() != '']
                            num_lines = len(lines)

                            if num_lines not in {1, 3}:
                                raise ConfigurationError("Credential file '%s' is badly formatted (should contain 1 or 3 non-blank lines)." % credentials_file)

                            if num_lines == 3:
                                # Get the authentication database, user and password from the contents
                                authentication_database = lines[0] or None
                                user = lines[1] or None
                                password = lines[2] or None
                                authenticated_mongodb_uri = None
                            else:
                                # Get the URI from the contents
                                authenticated_mongodb_uri = lines[0]
                                authentication_database = None
                                user = None
                                password = None
                    except IOError:
                        raise ConfigurationError("Could not open '%s'." % credentials_file)
            elif password is None or authentication_database is None:
                raise ConfigurationError("You need to define a password and authentication database when setting a user.")

            if authenticated_mongodb_uri is None:
                authentication_parameters = {authentication_database, user, password}

                # If any of the authentication parameters is None
                if None in authentication_parameters:
                    # Raise a ConfigurationError if at least one of them was set
                    if len(authentication_parameters) > 1:
                        raise ConfigurationError("Credentials are missing at least one parameter (authentication database, username or password).")

                    # Return to prevent authentication if None of them were set
                    return
            else:
                if host is not None:
                    raise ValueError("Ambiguous connection: a host was passed to the constructor, but a URI was extracted from environment variables or a credential file.")

                host = authenticated_mongodb_uri
                port = None

            super(MongoConnection, self).__init__(host, port, document_class, tz_aware, connect, **kwargs)

            # Authenticate the connection manually if not using a URI
            if authenticated_mongodb_uri is None:
                self[authentication_database].authenticate(user, password)
