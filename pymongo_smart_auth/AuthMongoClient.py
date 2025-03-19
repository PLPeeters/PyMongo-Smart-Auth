import pymongo

from .SmartAuth import SmartAuth

PYMONGO_VERSION_TUPLE = tuple(map(int, pymongo.__version__.split('.')[:2]))


class AuthMongoClient(pymongo.MongoClient, SmartAuth):
    def __init__(  # noqa: C901
        self,
        host=None,
        port=None,
        document_class=dict,
        tz_aware=False,
        connect=True,
        credentials_file=None,
        authenticate=True,
        **kwargs,
    ):
        host, port, kwargs = self.get_host_port_and_updated_kwargs(host, port, credentials_file, authenticate, kwargs)
        super().__init__(host, port, document_class, tz_aware, connect, **kwargs)
