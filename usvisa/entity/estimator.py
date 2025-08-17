import sys
import pandas as pd
from sklearn.pipeline import Pipeline
from usvisa.logger.logger import logging
from usvisa.exception.exception import UsVisaException


class TargetValueMapping:
    """
    TargetValueMapping class is used to map target values for visa application statuses.
    It provides a way to define and retrieve the mapping of target values to their corresponding
    status labels, which can be useful for model training and evaluation.
    """
    def __init__(self):
        self.Certified: int = 0
        self.Denied: int = 1

    def _asdict(self):
        """Convert the class attributes to a dictionary."""
        return self.__dict__
    
    def reverse_mapping(self):
        """Reverse the mapping of target values to status labels."""
        mapping_response = self._asdict
        return dict(zip(mapping_response.values(), mapping_response.keys()))
    
    
class UsVisaModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Function accepts raw inputs and then transformed raw input using preprocessing_object
        which guarantees that the inputs are in the same format as the training data.
        At last it performs prediction on transformed features.
        """
        
        try:
            logging.info("Using the trained model to get predictions")
            transformed_feature = self.preprocessing_object.transform(dataframe)
            return self.trained_model_object.predict(transformed_feature)
        
        except Exception as e:
            raise UsVisaException(e, sys) 
        
    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"