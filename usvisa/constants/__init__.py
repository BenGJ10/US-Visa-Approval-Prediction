import os
import sys
from datetime import date

"""
Defining common constant variables for training pipeline
"""
COLLECTION_NAME = "UsVisaData"
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
PIPELINE_NAME: str = "UsVisa"
ARTIFACT_DIR: str = "Artifacts" 
FILE_NAME: str = "usvisa.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
MODEL_FILE_NAME: str = "model.pkl"

"""
Data Ingestion related constants starts with DATA_INGESTION variable name
"""
DATA_INGESTION_COLLECTION_NAME: str = "UsVisaData"
DATA_INGESTION_DATABASE_NAME: str = "BenGJ"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2
