import os
import sys
from datetime import date
from dotenv import load_dotenv
"""
Defining common constant variables for training pipeline
"""
load_dotenv()
COLLECTION_NAME = "UsVisaData"
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
PIPELINE_NAME: str = "UsVisa"
ARTIFACT_DIR: str = "Artifacts" 
FILE_NAME: str = "usvisa.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
MODEL_FILE_NAME: str = "model.pkl"
TARGET_COLUMN = "case_status"
CURRENT_YEAR = date.today().year
SCHEMA_FILE_PATH = os.path.join('config', 'schema.yaml')
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = "ap-south-1"
APP_HOST = "0.0.0.0"
APP_PORT = 8000

"""
Data Ingestion related constants starts with DATA_INGESTION variable name
"""
DATA_INGESTION_COLLECTION_NAME: str = "UsVisaData"
DATA_INGESTION_DATABASE_NAME: str = "BenGJ"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
Data Validation related constants starts with DATA_VALIDATION varible name
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drfit_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

"""
Data Transformation related constants starts with DATA_TRANSFORMATION variable name
"""
DATA_TRANSFORAMTION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR : str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

"""
Model Trainer related constants starts with MODEL_TRAINER variable name
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")

"""
Model Evaluation related constants starts with MODEL_EVALUATION variable name
"""
MODEL_EVALUATION_THRESHOLD_SCORE_CHANGE: float = 0.05   
MODEL_BUCKET_NAME = "usvisa-proj-v1"
MODEL_PUSHER_S3_KEY = "model-registry"