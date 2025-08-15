import os
import sys

import pandas as pd
from sklearn.model_selection import train_test_split
from usvisa.exception.exception import UsVisaException
from usvisa.logger.logger import logging
from usvisa.data_access.data import UsVisaData

from usvisa.entity.config_entity import DataIngestionConfig
from usvisa.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:
    """
    DataIngestion class is responsible for ingesting data from a MongoDB database,
    processing it, and exporting it into a feature store as well as splitting it into
    training and testing datasets. It handles the connection to the database,
    retrieves the data, and manages the file paths for the feature store and datasets.
    """
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def export_data_to_feature_store(self) -> pd.DataFrame:
        """ Export data retrieved from MongoDB database into csv format.
        This function creates a directory for the feature store file if it does not exist,
        and saves the dataframe as a CSV file in that directory.
        """
        try:
            logging.info(f"Exporting data from MongoDB")
            usvisadata = UsVisaData() # Getting data stored in MongoDB as DataFrame format
            df = usvisadata.export_collection_as_dataframe(collection_name = self.data_ingestion_config.collection_name)
            logging.info(f"Shape of dataframe: {df.shape}")

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok = True)
            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")

            df.to_csv(feature_store_file_path, index = False, header = True)
            return df
        
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def export_train_test_split(self, dataframe: pd.DataFrame):
        """Split the dataframe into training and testing datasets based on split ratio ."""
        try:
            logging.info("Entered training and testing split method of Data Ingestion class")
            train_set, test_set = train_test_split(
                dataframe, test_size = self.data_ingestion_config.train_test_split_ratio
            )
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok = True)

            logging.info("Exporting training and testing file path")
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index = False, header = True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index = False, header = True
            )
            logging.info("Exported training and testing file path.")

        except Exception as e:
            raise UsVisaException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Initiates the data ingestion components of training pipeline.
        """
        try:
            dataframe = self.export_data_to_feature_store()
            self.export_train_test_split(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path = self.data_ingestion_config.training_file_path,
                                        test_file_path = self.data_ingestion_config.testing_file_path)
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        
        except Exception as e:
            raise UsVisaException(e, sys)