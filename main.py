import sys
from usvisa.logger.logger import logging
from usvisa.exception.exception import UsVisaException

from usvisa.entity.config_entity import DataIngestionConfig
from usvisa.entity.config_entity import TrainingPipelineConfig

from usvisa.components.data_ingestion import DataIngestion


if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig()
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Initiating Data ingestion..")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion successfully completed.")
        print(data_ingestion_artifact)

    except Exception as e:
        raise UsVisaException(e, sys)