from pymongo_smart_auth.AuthMongoClient import PYMONGO_VERSION_TUPLE, AuthMongoClient

__all__ = ['MongoClient', 'MongoConnection']

MongoClient = AuthMongoClient

if PYMONGO_VERSION_TUPLE >= (4, 9):
    from pymongo_smart_auth.AsyncAuthMongoClient import AsyncAuthMongoClient

    AsyncMongoClient = AsyncAuthMongoClient
    __all__.append('AsyncMongoClient')

# Legacy
MongoConnection = AuthMongoClient
