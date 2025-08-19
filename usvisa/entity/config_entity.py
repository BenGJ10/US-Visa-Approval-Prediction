"""
Config entities are used to store the configuration parameters for the data pipeline.
They mainly include the constants and settings that are used throughout the pipeline.
These entities are used to manage the configuration settings for data ingestion, data validation, data transformation,
and model training.
"""

import os
import sys
from datetime import datetime
from usvisa.constants import *
from dataclasses import dataclass

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

@dataclass
# A dataclass is used here so that the configuration can be easily instantiated and used throughout the pipeline. 
# We don't need to use a full class definition with an __init__ method, as dataclasses automatically generate it for us.
class TrainingPipelineConfig:
    """
    Sets up high-level configurations such as naming the pipeline and creating a timestamped artifact
    directory to store outputs
    """
    pipeline_name: str = PIPELINE_NAME
    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)
    timestamp: str = TIMESTAMP 

training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    """
    Configuration class for the data ingestion component of the pipeline.

    This includes:
    - Where to store raw and split data.
    - File paths for training/testing data.
    - Settings like train/test split ratio.
    - The MongoDB collection and database names from constants.
    """

    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)
    # File path where the full dataset (feature store) will be saved
    feature_store_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
    # Paths for the training and testing datasets after the split
    training_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
    testing_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    # MongoDB configurations
    collection_name:str = DATA_INGESTION_COLLECTION_NAME

@dataclass
class DataValidationConfig:
    """
    Configuration class for the data validation component of the pipeline.
    This includes:
    - Directories for valid and invalid data.
    - File paths for valid and invalid training/testing data.
    - Path for the drift report file.
    """

    data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME)

    valid_data_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_VALID_DIR)
    invalid_data_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_INVALID_DIR)

    valid_train_file_path: str = os.path.join(valid_data_dir, TRAIN_FILE_NAME)
    valid_test_file_path: str = os.path.join(valid_data_dir, TEST_FILE_NAME)

    invalid_train_file_path: str = os.path.join(invalid_data_dir, TRAIN_FILE_NAME)
    invalid_test_file_path: str = os.path.join(invalid_data_dir, TEST_FILE_NAME)
    # Path for the drift report file
    drift_report_file_path: str = os.path.join(data_validation_dir, 
                                               DATA_VALIDATION_DRIFT_REPORT_DIR, 
                                               DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)

@dataclass
class DataTransformationConfig:
    """
    Configuration class for the data transformation component of the pipeline.
    This includes:
    - Directory for data transformation artifacts.
    - Paths for transformed training and testing data.
    - Path for the preprocessing object file.
    """

    data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_TRANSFORAMTION_DIR_NAME)

    transformed_train_file_path: str = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                    TRAIN_FILE_NAME.replace("csv", "npy"))
    transformed_test_file_path: str = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                    TEST_FILE_NAME.replace("csv", "npy"))
    transformed_object_file_path: str = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, 
                                                     PREPROCSSING_OBJECT_FILE_NAME)

@dataclass
class ModelTrainerConfig:
    """
    Configuration class for the model trainer component of the pipeline.
    This includes:
    - Directory for model training artifacts.
    - Path for the trained model file.
    - Expected accuracy for the model.
    """
    
    model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME)
    trained_model_file_path: str = os.path.join(model_trainer_dir, MODEL_TRAINER_TRAINED_MODEL_DIR, MODEL_FILE_NAME)
    expected_accuracy: float = MODEL_TRAINER_EXPECTED_SCORE
    model_config_file_path: str = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH


@dataclass
class ModelEvaluationConfig:
    """
    Configuration class for the model evaluation component of the pipeline.
    This includes:
    - Threshold score change for model evaluation.
    - S3 bucket name for model storage.
    - S3 key path for the model file.
    """
    threshold_score_change: float = MODEL_EVALUATION_THRESHOLD_SCORE_CHANGE
    bucket_name: str = MODEL_BUCKET_NAME
    s3_model_key_path: str = MODEL_FILE_NAME



@dataclass
class ModelPusherConfig:
    """
    Configuration class for the model pusher component of the pipeline.
    This includes:
    - S3 bucket name for model storage.
    - S3 key path for the model file.
    """
    bucket_name: str = MODEL_BUCKET_NAME
    s3_model_key_path: str = MODEL_FILE_NAME