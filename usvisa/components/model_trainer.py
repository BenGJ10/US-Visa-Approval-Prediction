import sys
import numpy as np
import pandas as pd
from typing import Tuple
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from neuro_mf  import ModelFactory

from usvisa.logger.logger import logging
from usvisa.exception.exception import UsVisaException
from usvisa.utils.main_utils import load_numpy_array_data, read_yaml_file, load_object, save_object
from usvisa.entity.config_entity import ModelTrainerConfig
from usvisa.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from usvisa.entity.estimator import UsVisaModel

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_object_and_report(self, train: np.array, test: np.array) -> Tuple[object, object]:
        """
        This function uses neuro_mf to get the best model object and report of the best model.
        """
        try:
            logging.info("Using neuromf library to get best model object and report")
            model_factory = ModelFactory(model_config_path = self.model_trainer_config.model_config_file_path)

            X_train, Y_train, X_test, Y_test = train[:, :-1], train[:, -1], test[:, :-1], test[:, -1]

            # Get the best model detail using the model factory
            best_model_detail = model_factory.get_best_model(
                X = X_train, y = Y_train, base_accuracy = self.model_trainer_config.expected_accuracy 
            )
            # Save the best model object
            model_obj = best_model_detail.best_model
            Y_pred = model_obj.predict(X_test)

            accuracy = accuracy_score(Y_test, Y_pred) 
            f1 = f1_score(Y_test, Y_pred) 
            precision = precision_score(Y_test, Y_pred) 
            recall = recall_score(Y_test, Y_pred) 
            logging.info(f"Model accuracy: {accuracy}, F1 score: {f1}, Precision: {precision}, Recall: {recall}")
            metric_artifact = ClassificationMetricArtifact(f1_score = f1, precision_score = precision, recall_score = recall)
            
            return best_model_detail, metric_artifact
        
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def initiate_model_trainer(self, ) -> ModelTrainerArtifact:
        """
        This function initiates the model training process by loading the transformed data.
        It then trains the model using the best model from the neuro_mf library and saves the trained model.
        """
        try:
            train_arr = load_numpy_array_data(file_path = self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path = self.data_transformation_artifact.transformed_test_file_path)

            best_model_detail ,metric_artifact = self.get_model_object_and_report(train = train_arr, test = test_arr)

            preprocessing_obj = load_object(file_path = self.data_transformation_artifact.transformed_object_file_path)

            if best_model_detail.best_score < self.model_trainer_config.expected_accuracy:
                logging.info("No model found with score more than expected accuracy score")
                raise Exception("No best model found with score more than base score")
            
            usvisamodel = UsVisaModel(preprocessing_object = preprocessing_obj, 
                                      trained_model_object = best_model_detail.best_model)
            logging.info("Created UsVisaModel object with preprocessor and model")
            save_object(self.model_trainer_config.trained_model_file_path, usvisamodel)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path = self.model_trainer_config.trained_model_file_path,
                metric_artifact = metric_artifact
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        
        except Exception as e:
            raise UsVisaException(e, sys)