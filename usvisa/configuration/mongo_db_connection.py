import os
import sys
import pymongo
import certifi
from usvisa.logger.logger import logging
from usvisa.exception.exception import UsVisaException
from usvisa.constants import MONGO_DB_URL, DATA_INGESTION_DATABASE_NAME

ca = certifi.where()

class MongoDBClient:
    """
    This class exports the dataframe from mongodb into the feature store.
    """
    client = None
    def __init__(self, database_name = DATA_INGESTION_DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = MONGO_DB_URL
                if mongo_db_url is None:
                    raise Exception(f"Environment key: MONGO_DB_URL is not set.")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile = ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection succesfull")
        
        except Exception as e:
            raise UsVisaException(e, sys)
        
if __name__ == "__main__":
    try:
        mongo_client = MongoDBClient()
        print("Databases:", mongo_client.client.list_database_names())
        print(f"Connected to database: {mongo_client.database_name}")
    except UsVisaException as e:
        print("Custom Exception:", e)
    except Exception as e:
        print("General Exception:", e)