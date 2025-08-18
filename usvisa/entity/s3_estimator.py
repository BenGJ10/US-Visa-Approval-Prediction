import sys
import pandas as pd
from usvisa.cloud.aws_storage import SimpleStorageService
from usvisa.exception.exception import UsVisaException
from usvisa.entity.estimator import UsVisaModel

class UsVisaEstimator:
    """
    This class is used to save and retrieve usvisa models in the S3 bucket for the prediction.
    It provides methods to check if a model is present, load the model, save the model, and make predictions.
    The class uses SimpleStorageService to interact with AWS S3 storage.
    It is designed to be reusable and modular, allowing for easy integration into larger applications that require
    AWS S3 storage operations for model management.
    """
    def __init__(self, bucket_name, model_path,):
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService()
        self.model_path = model_path
        self.loaded_model: UsVisaModel = None


    def is_model_present(self,model_path):
        """
        This method checks if the model is present in the S3 bucket.
        It returns True if the model is present, otherwise returns False.
        """
        try:
            return self.s3.s3_key_path_available(bucket_name = self.bucket_name, s3_key = model_path)
        
        except UsVisaException as e:
            print(e)
            return False
        
    def load_model(self) -> UsVisaModel:
        """
        This method loads the model from the S3 bucket.
        It returns the loaded model object.
        If the model is not present, it raises an exception.
        """
        return self.s3.load_model(self.model_path, bucket_name = self.bucket_name)
    
    def save_model(self, from_file, remove:bool = False) -> None:
        """
        This method saves the model to the S3 bucket.
        It takes the file to be saved and a flag to remove the local file after saving.
        If the save operation fails, it raises an exception.
        """
        try:
            self.s3.upload_file(from_file,
                                to_filename = self.model_path,
                                bucket_name = self.bucket_name,
                                remove = remove
                                )
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def predict(self, dataframe: pd.DataFrame):
        """
        This method predicts the output using the loaded model.
        It takes a pandas DataFrame as input and returns the prediction.
        If the model is not loaded, it loads the model first.
        """
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe = dataframe)
        
        except Exception as e:
            raise UsVisaException(e, sys)