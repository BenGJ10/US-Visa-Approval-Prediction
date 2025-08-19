import sys
from usvisa.logger.logger import logging
from usvisa.exception.exception import UsVisaException

from usvisa.entity.config_entity import(DataIngestionConfig, DataValidationConfig, 
                                        DataTransformationConfig, ModelTrainerConfig, 
                                        ModelEvaluationConfig, ModelPusherConfig)
from usvisa.entity.config_entity import TrainingPipelineConfig

from usvisa.components.data_ingestion import DataIngestion
from usvisa.components.data_validation import DataValidation
from usvisa.components.data_transformation import DataTransformation
from usvisa.components.model_trainer import ModelTrainer
from usvisa.components.model_evaluation import ModelEvaluation
from usvisa.components.model_pusher import ModelPusher

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

        data_validation_config = DataValidationConfig()
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info("Initiating Data validation..")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation successfully completed.")
        print(data_validation_artifact)

        data_transformation_config = DataTransformationConfig()
        data_transformation = DataTransformation(data_ingestion_artifact, data_validation_artifact, data_transformation_config) 
        logging.info("Initiating Data transformation..")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data transformation successfully completed.")
        print(data_transformation_artifact)
        
        model_trainer_config = ModelTrainerConfig()
        model_trainer = ModelTrainer(data_transformation_artifact, model_trainer_config)
        logging.info("Initiating Model Training..")
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model training successfully completed.")
        print(model_trainer_artifact)
        
        model_evaluation_config = ModelEvaluationConfig()
        model_evaluation = ModelEvaluation(model_evaluation_config, data_ingestion_artifact, model_trainer_artifact)
        logging.info("Initiating Model Evaluation..")
        model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
        logging.info("Model evaluation successfully completed.")
        print(model_evaluation_artifact)
        
        model_pusher_config = ModelPusherConfig()
        model_pusher = ModelPusher(model_evaluation_artifact, model_pusher_config)
        logging.info("Initiating Model Pusher..")
        model_pusher_artifact = model_pusher.initiate_model_pusher()
        logging.info("Model pushing successfully completed.")
        print(model_pusher_artifact)

    except Exception as e:
        raise UsVisaException(e, sys)