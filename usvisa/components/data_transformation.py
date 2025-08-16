import os
import sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer

from usvisa.logger.logger import logging
from usvisa.exception.exception import UsVisaException
from usvisa.entity.estimator import TargetValueMapping
from usvisa.constants import TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR
from usvisa.utils.main_utils import save_numpy_array_data, save_object, drop_columns, read_yaml_file

from usvisa.entity.config_entity import DataTransformationConfig
from usvisa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact

class DataTransformation:
    """
    DataTransformation class is responsible for transforming the data after it has been validated.
    It also prepares the artifacts for further processing in the pipeline.
    """
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, 
                       data_validation_artifact: DataValidationArtifact,
                       data_transformation_config: DataTransformationConfig):
        
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self._schema_config = read_yaml_file(file_path = SCHEMA_FILE_PATH)

        except Exception as e:
            raise UsVisaException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise UsVisaException(e, sys)
        
         
    def get_data_transformer_object(self) -> Pipeline:
        """
        Create a data transformation pipeline that includes scaling, encoding, and transformation.
        This method initializes the necessary transformers and returns a pipeline object that can be used
        to preprocess the data. 
        """
        try:
            standard_scaler = StandardScaler()
            onehot_encoder = OneHotEncoder()
            ordinal_encoder = OrdinalEncoder()
            logging.info("Initialized StandardScaler, OneHotEncoder, OrdinalEncoder")

            oh_columns = self._schema_config['oh_columns']
            or_columns = self._schema_config['or_columns']
            transform_columns = self._schema_config['transform_columns']
            num_features = self._schema_config['num_features']

            logging.info("Initialized PowerTransformer")
            transform_pipeline = Pipeline(steps = [
                ('transformer', PowerTransformer(method = 'yeo-johnson'))
            ])

            preprocessor = ColumnTransformer(
                [
                    ("OneHotEncoder", onehot_encoder, oh_columns),
                    ("Ordinal_Encoder", ordinal_encoder, or_columns),
                    ("Transformer", transform_pipeline, transform_columns),
                    ("StandardScaler", standard_scaler, num_features)
                ]
            )
            logging.info("Created preprocessor object from ColumnTransformer")
            return preprocessor
        
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def initiate_data_transformation(self):
        """
        Initiates the data transformation process by applying the preprocessor to the training and testing datasets.
        It also handles the addition of new features, such as 'company_age', and applies data balancing techniques like SMOTEENN.
        The transformed data is saved as numpy arrays, and the preprocessor object is saved for future use.
        """
        try:
            # Check if data validation was successful
            if self.data_validation_artifact.validation_status:
                preprocessor = self.get_data_transformer_object()
                logging.info("Got the preprocessor object")

                # Read the training and testing data
                train_df = DataTransformation.read_data(file_path = self.data_ingestion_artifact.train_file_path)
                test_df = DataTransformation.read_data(file_path = self.data_ingestion_artifact.test_file_path)

                input_feature_train_df = train_df.drop(columns = [TARGET_COLUMN], axis = 1)
                target_feature_train_df = train_df[TARGET_COLUMN]
                logging.info("Got the input features and target features of training dataset")

                input_feature_train_df['company_age'] = CURRENT_YEAR - input_feature_train_df['yr_of_estab']
                logging.info("Added company_age column to the training dataset")
                drop_cols = self._schema_config['drop_columns']
                logging.info("Dropped the columns in drop_cols of training dataset")
                input_feature_train_df = drop_columns(df = input_feature_train_df, cols = drop_cols)
                
                target_feature_train_df = target_feature_train_df.replace(
                    TargetValueMapping()._asdict()
                )

                input_feature_test_df = test_df.drop(columns = [TARGET_COLUMN], axis = 1)
                target_feature_test_df = test_df[TARGET_COLUMN]
                logging.info("Got the input features and target features of testing dataset")

                input_feature_test_df['company_age'] = CURRENT_YEAR - input_feature_test_df['yr_of_estab']
                logging.info("Added company_age column to the testing dataset")
                logging.info("Dropped the columns in drop_cols of testing dataset")
                input_feature_test_df = drop_columns(df = input_feature_test_df, cols = drop_cols)
                
                target_feature_test_df = target_feature_test_df.replace(
                    TargetValueMapping()._asdict()
                )
                # Apply the preprocessor to the training and testing data
                logging.info("Applying preprocessing object on training and testing dataframe")
                input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
                input_feature_test_arr = preprocessor.transform(input_feature_test_df)

                # Data balancing using SMOTEENN
                logging.info("Applying SMOTEENN on training dataset")
                smoteen = SMOTEENN(sampling_strategy = "minority")

                input_feature_train_final, target_feature_train_final = smoteen.fit_resample(input_feature_train_arr, target_feature_train_df)
                input_feature_test_final, target_feature_test_final = smoteen.fit_resample(input_feature_test_arr, target_feature_test_df)
                logging.info("Applied SMOTEENN on training and testing dataset")

                # Save the preprocessor and transformed data
                train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
                test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]

                save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array = train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array = test_arr)
                logging.info("Saved the preprocessor object")

                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
                )
                return data_transformation_artifact
            
            else:
                raise Exception(self.data_validation_artifact.validation_status)

        except Exception as e:
            raise UsVisaException(e, sys)