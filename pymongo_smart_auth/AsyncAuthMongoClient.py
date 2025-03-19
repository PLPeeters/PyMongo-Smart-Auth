import pymongo

from .SmartAuth import SmartAuth


class AsyncAuthMongoClient(pymongo.AsyncMongoClient, SmartAuth):
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
