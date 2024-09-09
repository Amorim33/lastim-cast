from pymongo.errors import CollectionInvalid

from lib.database import db
from lib.collections import collections_granularity

for collection_name, granularity in collections_granularity.items():
    try:
        db.create_collection(
            collection_name,
            timeseries={
                "timeField": "Datetime",
                "metaField": "Date",
                "granularity": granularity
            }
        )
    except CollectionInvalid as err:
        print(err)
        if err._message == f'collection {collection_name} already exists':
            print(err._message)
        else:
            raise err

    print(f"Created time series collection: {collection_name} with granularity: {granularity}")
