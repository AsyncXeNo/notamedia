from env import get_var
from models import collections

from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from loguru import logger


def setup() -> (MongoClient, Database):
    uri = f'mongodb+srv://{get_var("MONGODB_USERNAME")}:{get_var("MONGODB_PASSWORD")}@notamedia.83rwaqu.mongodb.net/?retryWrites=true&w=majority'

    logger.info('connecting to mongodb')

    client = MongoClient(uri)
    database: Database = client.get_database(get_var('DATABASE_NAME'))

    for name in collections.values():
        try:
            database.create_collection(name)
            logger.warning(f'couldn\'t find an existing {name} collection, creating a new one')
        except:
            logger.debug(f'{name} collection already exists')

    return client, database
