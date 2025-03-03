import pymongo

from .AuthMongoClient import AuthMongoClient


class AsyncAuthMongoClient(pymongo.AsyncMongoClient, AuthMongoClient):
    pass
