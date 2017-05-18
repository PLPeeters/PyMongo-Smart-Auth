import os

from pymongo import MongoClient
from pymongo.errors import ConfigurationError


class MongoConnection(MongoClient):
    USER_CREDENTIALS = '%s/.mongo_credentials' % os.path.expanduser('~')

    def __new__(cls, *args, **kwargs):
        """Create or return the singleton for the provided arguments."""

        # Create a unique key for the instance
        kwd_mark = object()  # Sentinel to separate args from kwargs
        key = args + (kwd_mark,) + tuple(sorted(kwargs.items()))
        self = str(key)

        # If the class doesn't have an instance for the current set of parameters yet, create it now
        if not hasattr(cls, self):
            instance = object.__new__(cls)
            instance.__init__(*args, **kwargs)

            setattr(cls, self, instance)

        # Return the instance
        return getattr(cls, self)

    def __init__(
            self,
            host=None,
            port=None,
            document_class=dict,
            tz_aware=False,
            connect=True,
            user=None,
            password=None,
            credentials_file=None,
            **kwargs):
        """Singleton MongoDB connection with built-in authentication."""

        super(MongoConnection, self).__init__(host, port, document_class, tz_aware, connect, **kwargs)

        # If no user was passed, try to get the credentials from the filesystem
        if user is None:
            # If no credentials file was passed, use the one in the user's home folder
            if credentials_file is None:
                credentials_file = MongoConnection.USER_CREDENTIALS

            try:
                # Try to open the credentials file
                with open(credentials_file) as credentials_file_obj:
                    try:
                        # Read the file
                        lines = credentials_file_obj.readlines()

                        # Get the user and password from the contents
                        user = lines[0].strip()
                        password = lines[1].strip()
                    except IndexError:
                        raise ConfigurationError("User credentials file '%s' is wrongly formatted." % credentials_file)
            except IOError:
                raise ConfigurationError("Could not open '%s'." % credentials_file)
        elif password is None:
            raise ConfigurationError("A password is required.")

        self.user = user
        self.password = password

    def __getitem__(self, name):
        """Get an authenticated database by name.

        Raises :class:`~pymongo.errors.InvalidName` if an invalid
        database name is used.

        :Parameters:
          - `name`: the name of the database to get
        """

        # Get the database object
        db = super(MongoConnection, self).__getitem__(name)

        # Authenticate before returning it
        db.authenticate(self.user, self.password)

        return db

    def __getattr__(self, name):
        """Get an authenticated database by name.

        Raises :class:`~pymongo.errors.InvalidName` if an invalid
        database name is used.

        :Parameters:
          - `name`: the name of the database to get
        """

        return self.__getitem__(name)
