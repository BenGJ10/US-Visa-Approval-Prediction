import sys
from usvisa.logger.logger import logging
from usvisa.exception.exception import UsVisaException

from usvisa.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from usvisa.entity.config_entity import TrainingPipelineConfig

from usvisa.components.data_ingestion import DataIngestion
from usvisa.components.data_validation import DataValidation
from usvisa.components.data_transformation import DataTransformation


if __name__ == "__main__":
    try:
        logging.info("Starting the ETL Pipeline")
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig()
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Initiating Data ingestion..")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion successfully completed.")
        print(data_ingestion_artifact)

        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info("Initiating Data validation..")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation successfully completed.")
        print(data_validation_artifact)

        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_ingestion_artifact, data_validation_artifact, data_transformation_config) 
        logging.info("Initiating Data transformation..")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data transformation successfully completed.")
        print(data_transformation_artifact)
        
    except Exception as e:
        raise UsVisaException(e, sys)