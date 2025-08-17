import os
import sys
from usvisa.logger.logger import logging
from usvisa.exception.exception import UsVisaException

from usvisa.components.data_ingestion import DataIngestion
from usvisa.components.data_validation import DataValidation
from usvisa.components.data_transformation import DataTransformation

from usvisa.entity.config_entity import (
    TrainingPipelineConfig, DataIngestionConfig, 
    DataValidationConfig, DataTransformationConfig)

from usvisa.entity.artifact_entity import (
    DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
)


class TrainingPipeline:
    """
    The TrainingPipeline class orchestrates the entire machine learning pipeline,
    from data ingestion to model training. It initializes the pipeline configuration,
    manages the sequence of operations, and handles exceptions that may arise during the process.
    """

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()    

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        This method of TrainPipeline class is responsible for starting the Data Ingestion component.
        """
        try:
            logging.info("Entered the data ingestion initiation method of the TrainPipeline class.")
            data_ingestion = DataIngestion(data_ingestion_config = self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        This method of TrainPipeline class is responsible for starting the Data Valdiation component.
        """
        try:
            logging.info("Entered the data validation initiation method of the TrainPipeline class.")
            data_validation = DataValidation(data_ingestion_artifact = data_ingestion_artifact, 
                                             data_validation_config = self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact

        except Exception as e:
            raise UsVisaException(e, sys)
        
    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        """
        This method of TrainPipeline class is responsible for starting the Data Transformation component.
        """
        try:
            logging.info("Entered the data transformation initiation method of the TrainPipeline class.")
            data_transformation = DataTransformation(data_ingestion_artifact = data_ingestion_artifact, 
                                                     data_validation_artifact = data_validation_artifact,
                                                     data_transformation_config = self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        
        except Exception as e:
            raise UsVisaException(e, sys)
        

    def run_pipeline(self, ) -> None:
        """
        This method of TrainPipeline class is responsible for running the complete ML pipeline.
        """
        try:
            logging.info("Starting the ETL Pipeline")
            logging.info("Initiating Data ingestion..")
            data_ingestion_artifact = self.start_data_ingestion()
            logging.info("Data ingestion successfully completed.")
            logging.info("Initiating Data validation..")
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact = data_ingestion_artifact)
            logging.info("Data validation successfully completed.")
            logging.info("Initiating Data transformation..")
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact = data_ingestion_artifact, data_validation_artifact = data_validation_artifact)
            logging.info("Data transformation successfully completed.")
            
        except Exception as e:
            raise UsVisaException(e, sys)