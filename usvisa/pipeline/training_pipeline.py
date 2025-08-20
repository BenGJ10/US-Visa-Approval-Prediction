import os
import sys
from usvisa.logger.logger import logging
from usvisa.exception.exception import UsVisaException

from usvisa.components.data_ingestion import DataIngestion
from usvisa.components.data_validation import DataValidation
from usvisa.components.data_transformation import DataTransformation
from usvisa.components.model_trainer import ModelTrainer
from usvisa.components.model_evaluation import ModelEvaluation
from usvisa.components.model_pusher import ModelPusher

from usvisa.entity.config_entity import (
    TrainingPipelineConfig, DataIngestionConfig, 
    DataValidationConfig, DataTransformationConfig, ModelTrainerConfig,
    ModelEvaluationConfig, ModelPusherConfig)

from usvisa.entity.artifact_entity import (
    DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact,
    ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact
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
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig() 

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
        
    def start_model_training(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        """
        This method of TrainPipeline class is responsible for starting the Model Training component.
        """
        try:
            logging.info("Started the model training method of the TrainPipeline class.")
            model_training = ModelTrainer(data_transformation_artifact = data_transformation_artifact,
                                          model_trainer_config = self.model_trainer_config)
            model_trainer_artifact = model_training.initiate_model_trainer()
            return model_trainer_artifact

        except Exception as e:
            raise UsVisaException(e, sys)
        
    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifact, model_trainer_artifact: ModelTrainerArtifact) -> ModelEvaluationArtifact:
        """
        This method of TrainPipeline class is responsible for starting the Model Evaluation component.
        """
        try:
            logging.info("Started the model evaluation method of the TrainPipeline class.")
            model_evaluation = ModelEvaluation(model_evaluation_config = self.model_evaluation_config,
                                               data_ingestion_artifact = data_ingestion_artifact,
                                               model_trainer_artifact = model_trainer_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        
        except Exception as e:
            raise UsVisaException(e, sys)   
        
    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        """
         This method of TrainPipeline class is responsible for starting the Model Pusher component.
        """
        try:
            logging.info("Started the model pusher method of the TrainPipeline class.")
            model_pusher = ModelPusher(model_evaluation_artifact = model_evaluation_artifact, 
                                       model_pusher_config = self.model_pusher_config)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        
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

            logging.info("Initiating Model training..")
            model_trainer_artifact = self.start_model_training(data_transformation_artifact = data_transformation_artifact)
            logging.info("Model training successfully completed.")

            logging.info("Initiating Model evaluation..")
            model_evaluation_artifact = self.start_model_evaluation(data_ingestion_artifact = data_ingestion_artifact,
                                                                    model_trainer_artifact = model_trainer_artifact)
            logging.info("Model evaluation successfully completed.")

            if not model_evaluation_artifact.is_model_accepted:
                logging.info("Model not accepted!")
                return None
            
            logging.info("Initiating Model pusher..")
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact = model_evaluation_artifact)
            logging.info("Model successfully pushed.")
        
        except Exception as e:
            raise UsVisaException(e, sys)