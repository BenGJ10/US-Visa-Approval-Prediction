import sys
from typing import Optional
import numpy as np
import pandas as pd
from usvisa.configuration.mongo_db_connection import MongoDBClient
from usvisa.constants import DATA_INGESTION_DATABASE_NAME
from usvisa.exception.exception import UsVisaException


class UsVisaData:
    """
    This class helps to export entire MongoDB records as pandas dataframe.
    """

    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name = DATA_INGESTION_DATABASE_NAME)
        except Exception as e:
            raise UsVisaException(e, sys)
        

    def export_collection_as_dataframe(self,collection_name:str, database_name:Optional[str] = None)->pd.DataFrame:
        try:
            """Read data from MongoDB database.\n
            This function connects to the MongoDB database using the provided URL,
            retrieves the specified collection, and converts it into a pandas DataFrame.
            It also handles the removal of the "_id" column if it exists in the DataFrame."
            """
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            
            if "_id" in df.columns.to_list():
                df = df.drop(columns = ["_id"], axis = 1)
            
            df.replace({"na":np.nan},inplace = True)
            return df
        
        except Exception as e:
            raise UsVisaException(e, sys)