import inspect
import logging
import os
import stat
import sys
from string import Formatter
from typing import Optional, Tuple

import pymongo

logging.basicConfig()
logger = logging.getLogger('pymongo_smart_auth')

PYMONGO_VERSION_TUPLE = tuple(map(int, pymongo.__version__.split('.')[:2]))


class SmartAuth:
    USER_CREDENTIALS = '{}/.mongo_credentials'.format(os.path.expanduser('~'))
    SERVER_CREDENTIALS = '/etc/mongo_credentials'
    __missing_credentials_warning_shown = False
    __PYMONGO_ARGS = set(inspect.getfullargspec(pymongo.MongoClient).args)

    # On Unix systems, check the permissions of the credential file
    if sys.platform in ('linux', 'linux2', 'darwin') and os.path.exists(USER_CREDENTIALS):
        # Get the file stats
        cred_file_stats = os.stat(USER_CREDENTIALS)

        # Issue a warning if the file is group readable
        if bool(cred_file_stats.st_mode & stat.S_IRGRP):
            logger.warning("{0} is readable by the group. It should only be readable by the user. Fix by running:\nchmod 600 \"{0}\"".format(USER_CREDENTIALS))

        # Issue a warning if the file is readable by others
        if bool(cred_file_stats.st_mode & stat.S_IROTH):
            logger.warning("{0} is readable by others. It should only be readable by the user. Fix by running:\nchmod 600 \"{0}\"".format(USER_CREDENTIALS))

    def get_host_port_and_updated_kwargs(  # noqa: C901
        self,
        host=None,
        port=None,
        credentials_file=None,
        authenticate=True,
        kwargs: dict = None,
    ) -> Tuple[Optional[str], Optional[int], dict]:
        # If authentication is off for this connection, just initialise
        if not authenticate:
            return

        if not kwargs:
            kwargs = {}

        username = kwargs.get('username')
        password = kwargs.get('password')
        authSource = kwargs.get('authSource')
        authenticated_mongodb_uri = None

        # If no user was passed, try to get the credentials elsewhere
        if username is None:
            # If no credential file was passed
            if credentials_file is None:
                # Check if a specific credential file was requested
                logger.debug('Checking environment for credential file path...')

                credentials_file = os.environ.get('MONGO_CREDENTIAL_FILE') or None

                if credentials_file is not None:
                    logger.debug(f'Got MONGO_CREDENTIAL_FILE = {credentials_file}')

                    # Check if the path is a format string
                    field_references = {field for _, field, _, _ in Formatter().parse(credentials_file) if field}

                    # If the string contains field references
                    if len(field_references) > 0:
                        logger.debug(f'Fields in file path = {field_references}')

                        # Create a set with the known arguments from PyMongo and our library
                        # and check that the fields do not clash with those
                        constructor_args = self.__PYMONGO_ARGS.union(set(inspect.getargspec(self).args))
                        name_clashes = field_references.intersection(constructor_args)

                        logger.debug(f'Constructor args = {constructor_args}')

                        # If there are name clashes, raise a ConfigurationError
                        if len(name_clashes) > 0:
                            raise pymongo.errors.ConfigurationError('The following variables in your MONGO_CREDENTIAL_FILE environment variable clash with the variables of either the AuthMongoClient or MongoClient constructor: {}.'.format(', '.join(name_clashes)))

                        # Check that the kwargs contain the necessary fields
                        missing_kwargs = field_references - set(kwargs)

                        # If fields are missing, raise a ConfigurationError
                        if len(missing_kwargs) > 0:
                            raise pymongo.errors.ConfigurationError('The following variables were found in your MONGO_CREDENTIAL_FILE environment variable but were not in the kwargs for the AuthMongoClient constructor: {}.'.format(', '.join(missing_kwargs)))

                        # Pop the format string arguments from the kwargs
                        format_string_arguments = {}

                        for field in field_references:
                            format_string_arguments[field] = kwargs.pop(field)

                        # Build the final path to the credential file
                        logger.info(f'Formatting credential file {credentials_file!r} found in environment with arguments: {format_string_arguments}.')
                        credentials_file = credentials_file.format(**format_string_arguments)
                    else:
                        logger.info(f'Using credential file found in environment: {credentials_file!r}.')
                else:
                    logger.debug('Got no credential file from the environment (MONGO_CREDENTIAL_FILE).')

            if credentials_file is None:
                # Attempt to get the configuration from the environment
                logger.debug('Checking environment for authenticated URI...')

                authenticated_mongodb_uri = os.environ.get('MONGO_AUTHENTICATED_URI') or None

                # If the environment does not contain a URI, check it for credentials
                if authenticated_mongodb_uri is None:
                    logger.debug('Got no URI from the environment (MONGO_AUTHENTICATED_URI); checking environment for credentials...')

                    authSource = os.environ.get('MONGO_AUTHENTICATION_DATABASE') or None
                    username = os.environ.get('MONGO_USERNAME') or None
                    password = os.environ.get('MONGO_PASSWORD') or None

                    logger.debug(f'Got MONGO_AUTHENTICATION_DATABASE = {authSource}')
                    logger.debug(f'Got MONGO_USERNAME = {username}')
                    logger.debug(f'MONGO_PASSWORD present and non-empty: {password is not None}')

                    values_to_check = {authSource, username, password}

                    # If there are undefined environment variables
                    if None in values_to_check:
                        # If they aren't all undefined, raise a ConfigurationError
                        if len(values_to_check) > 1:
                            raise pymongo.errors.ConfigurationError('MONGO_AUTHENTICATED_URI environment variable not set and missing other environment variables.')

                        logger.debug('Got no credentials from environment; falling back to static credential files.')

                        # Fall back to the first existing credential file
                        # between the one in the user's home and the one in /etc
                        if os.path.exists(self.USER_CREDENTIALS):
                            credentials_file = self.USER_CREDENTIALS
                        elif os.path.exists(self.SERVER_CREDENTIALS):
                            credentials_file = self.SERVER_CREDENTIALS
                        elif not self.__missing_credentials_warning_shown:
                            logger.warning(f"Mongo client is authenticated but no credential file was found at either '{self.USER_CREDENTIALS}' or '{self.SERVER_CREDENTIALS}' and environment variables were not defined.")

                            self.__missing_credentials_warning_shown = True

                        if credentials_file is not None:
                            logger.info(f'Using static credential file: {credentials_file!r}.')
                    else:
                        logger.info('Using credentials found in environment.')
                else:
                    logger.info('Using URI found in environment.')

            # If there is a credential file to check
            if credentials_file is not None:
                try:
                    # Try to open the credential file
                    with open(credentials_file) as credentials_file_obj:
                        # Read the file
                        lines = [line.strip() for line in credentials_file_obj.readlines() if line.strip() != '']
                        num_lines = len(lines)

                        # Verify the file has the expected number of lines
                        if num_lines not in {1, 3}:
                            raise pymongo.errors.ConfigurationError(f"Credential file '{credentials_file}' is badly formatted (should contain 1 or 3 non-blank lines).")

                        if num_lines == 3:
                            # Get the authentication database, user and password from the contents
                            authSource = lines[0] or None
                            username = lines[1] or None
                            password = lines[2] or None
                            authenticated_mongodb_uri = None
                        else:
                            # Get the URI from the contents
                            authenticated_mongodb_uri = lines[0]
                            authSource = None
                            username = None
                            password = None
                except OSError:
                    raise pymongo.errors.ConfigurationError(f'Could not open credential file: {credentials_file!r}.')
        elif password is None or authSource is None:
            raise pymongo.errors.ConfigurationError('You need to define a password and authSource when setting a user.')

        can_manually_authenticate = False

        if authenticated_mongodb_uri is None:
            authentication_parameters = {authSource, username, password}

            # If any of the authentication parameters is None
            if None in authentication_parameters:
                # Raise a ConfigurationError if at least one of them was set
                if len(authentication_parameters) > 1:
                    raise pymongo.errors.ConfigurationError('Credentials are missing at least one parameter (authentication database, username or password).')
            else:
                can_manually_authenticate = True
        else:
            if not authenticated_mongodb_uri.startswith('mongodb://'):
                raise pymongo.errors.ConfigurationError('Mongo URI should start with mongodb://')

            logger.info('Authenticating with Mongo URI.')

            if host is not None:
                raise ValueError('Ambiguous connection: a host was passed to the constructor, but a URI was extracted from environment variables or a credential file.')

            host = authenticated_mongodb_uri
            port = None

        if PYMONGO_VERSION_TUPLE >= (4, 0):
            if authSource is not None:
                kwargs['authSource'] = authSource

            if username is not None:
                kwargs['username'] = username

            if password is not None:
                kwargs['password'] = password
        elif can_manually_authenticate:
            logger.info('Authenticating with extracted credentials.')
            self[authSource].authenticate(username, password)

        return host, port, kwargs
