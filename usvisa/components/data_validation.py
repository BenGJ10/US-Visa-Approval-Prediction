import os
import sys
import json
import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

from usvisa.logger.logger import logging
from usvisa.utils.main_utils import read_yaml_file, write_yaml_file
from usvisa.exception.exception import UsVisaException
from usvisa.constants import SCHEMA_FILE_PATH

from usvisa.entity.config_entity import DataValidationConfig
from usvisa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact


class DataValidation:
    """
    DataValidation class is responsible for validating the data ingested by the Data Ingestion component.
    It checks for the presence of required columns, data types, and performs statistical tests to ensure
    that the data meets the expected schema and quality standards.
    """
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._scheme_config = read_yaml_file(SCHEMA_FILE_PATH) # Load schema configuration 
        
        except Exception as e:
            raise UsVisaException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        """
        Reads data from the specified file path and returns it as a pandas DataFrame.
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file {file_path} does not exist.")
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def validate_columns(self, dataframe: pd.DataFrame) -> bool:
        """
        Validates the number of columns.
        """
        try:
            status = len(dataframe.columns) == len(self._scheme_config["columns"])
            logging.info(f"Required number of columns: {len(self._scheme_config['columns'])}.")
            logging.info(f"Dataframe has {len(dataframe.columns)} in total.")
            return status
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def does_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        """
        Validates the existence of a numerical and categorical columns.
        """
        try:
            dataframe_columns = dataframe.columns
            missing_numerical_columns = []
            missing_categorical_columns = []
            
            for column in self._scheme_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)

            if len(missing_numerical_columns)>0:
                logging.info(f"Missing numerical column: {missing_numerical_columns}")

            for column in self._scheme_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)

            if len(missing_categorical_columns)>0:
                logging.info(f"Missing categorical column: {missing_categorical_columns}")

            return False if len(missing_categorical_columns)>0 or len(missing_numerical_columns)>0 else True
        
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold = 0.05) -> bool:
        """
        Detects dataset drift between a reference (base) dataset and a new (current) dataset
        using the Evidently library's metrics API. It compares the statistical properties of the two datasets to identify significant changes.
        If drift is detected, it generates a report and saves it in the specified file path.
        """
        try:
            # Use Evidently's DataDrift
            data_drift_profile = Profile(sections = [DataDriftProfileSection()])
            data_drift_profile.calculate(base_df, current_df) 
            
            report = data_drift_profile.json()
            json_report = json.loads(report)


            write_yaml_file(file_path = self.data_validation_config.drift_report_file_path, content = json_report)

            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]
            logging.info(f"{n_drifted_features}/{n_features} drift detected among features.")

            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]
            return drift_status
        
        except Exception as e:
            raise UsVisaException(e, sys)
        

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Performs initial data validation by checking the presence of required columns
        and detecting data drift between the training and testing datasets.
        """
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Reading data from the train and test file path
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            # Validating the number of columns
            status = self.validate_columns(dataframe = train_df)
            if not status:
                error_message = "Training dataframe does not contain all columns!\n"
                raise Exception(error_message)
            logging.info(f"All required columns present in training dataframe: {status}")

            status = self.validate_columns(dataframe = test_df)
            if not status:
                error_message = "Testing dataframe does not contain all columns!\n"
                raise Exception(error_message)
            logging.info(f"All required columns present in testing dataframe: {status}")

            # Validating numerical and categorical columns
            status = self.does_columns_exist(dataframe = train_df)
            if not status:
                raise Exception("Train data does not contain all valid columns.")

            status = self.does_columns_exist(dataframe = test_df)
            if not status:
                raise Exception("Test data does not contain all valid columns.")

            # Checking dataset drift
            validation_status = self.detect_dataset_drift(base_df = train_df, current_df = test_df)
            if validation_status:
                logging.info("Drift detected.")
            else:
                logging.info("No Drift detected.")

            # If no issue, save this as a csv file
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok = True)
            train_df.to_csv(self.data_validation_config.valid_train_file_path, index = False, header = True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index = False, header = True)

            data_validation_artifact = DataValidationArtifact(
                validation_status = validation_status,
                valid_train_file_path = self.data_validation_config.valid_train_file_path,
                valid_test_file_path = self.data_validation_config.valid_test_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        
        except Exception as e:
            raise UsVisaException(e, sys)