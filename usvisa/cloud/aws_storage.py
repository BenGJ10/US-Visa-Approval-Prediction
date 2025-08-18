import os
import sys
import boto3
import pickle
import pandas as pd
from io import StringIO
from typing import List, Union
from mypy_boto3_s3.service_resource import Bucket
from botocore.exceptions import ClientError

from usvisa.exception.exception import UsVisaException
from usvisa.logger.logger import logging
from usvisa.configuration.aws_s3_connection import S3Client


class SimpleStorageService:
    """
    This class provides methods to interact with AWS S3 storage. It includes functionalities to check 
    if a key path is available, read objects, get bucket and file objects, load models, create folders, 
    upload files, upload dataframes as CSV, and read CSV files into dataframes.
    It uses the S3Client to establish a connection to AWS S3.
    The methods handle exceptions and log relevant information. The class is designed to be reusable and 
    modular, allowing for easy integration into larger applications that require AWS S3 storage operations.
    """
    def __init__(self):
        s3 = S3Client()
        self.s3_resource = s3.s3_resource
        self.s3_client = s3.s3_client

    def s3_key_path_available(self, bucket_name, s3_key)->bool:
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix = s3_key)]
            
            if len(file_objects) > 0:
                return True
            else:
                return False
        
        except Exception as e:
            raise UsVisaException(e, sys)
    
    @staticmethod
    def read_object(object_name: str, decode: bool = True, make_readable: bool = False) -> Union[StringIO, str]:
        """
        This method reads the object_name object with kwargs. 
        Reads the object from S3 and returns it as a string or StringIO object.
        """
        try:
            func = (
                lambda: object_name.get()["Body"].read().decode()
                if decode is True
                else object_name.get()["Body"].read()
            )
            conv_func = lambda: StringIO(func()) if make_readable is True else func()
            return conv_func()

        except Exception as e:
            raise UsVisaException(e, sys)
        
    def get_bucket(self, bucket_name: str) -> Bucket:
        """
        This method gets the bucket object based on the bucket_name.
        """
        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            return bucket
        
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def get_file_object( self, filename: str, bucket_name: str) -> Union[List[object], object]:
        """
        This method gets the file object from bucket_name bucket based on filename.
        """
        try:
            bucket = self.get_bucket(bucket_name)

            file_objects = [file_object for file_object in bucket.objects.filter(Prefix = filename)]
            func = lambda x: x[0] if len(x) == 1 else x
            file_objs = func(file_objects)
            return file_objs

        except Exception as e:
            raise UsVisaException(e, sys)
        
    def load_model(self, model_name: str, bucket_name: str, model_dir: str = None) -> object:
        """
        This method loads the model_name model from bucket_name bucket with kwargs.
        """
        try:
            func = (
                lambda: model_name
                if model_dir is None
                else model_dir + "/" + model_name
            )
            model_file = func()
            file_object = self.get_file_object(model_file, bucket_name)
            model_obj = self.read_object(file_object, decode = False)
            model = pickle.loads(model_obj)
            return model
        
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def create_folder(self, folder_name: str, bucket_name: str) -> None:
        """
        This method creates a folder_name folder in bucket_name bucket.
        """
        try:
            self.s3_resource.Object(bucket_name, folder_name).load()

        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                folder_obj = folder_name if folder_name.endswith("/") else folder_name + "/"
                self.s3_client.put_object(Bucket = bucket_name, Key = folder_obj)
            else:
                pass
            
    def upload_file(self, from_filename: str, to_filename: str,  bucket_name: str,  remove: bool = True):
        """
        This method uploads the from_filename file to bucket_name bucket with to_filename as bucket filename.
        """
        try:
            logging.info(
                f"Uploading {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )
            self.s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)

            logging.info(
                f"Uploaded {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )

            if remove is True:
                os.remove(from_filename)

        except Exception as e:
            raise UsVisaException(e, sys)
        
    def upload_df_as_csv(self,data_frame: pd.DataFrame,local_filename: str, bucket_filename: str,bucket_name: str,) -> None:
        """
        This method uploads the dataframe to bucket_filename csv file in bucket_name bucket
        """
        try:
            data_frame.to_csv(local_filename, index = None, header = True)

            self.upload_file(local_filename, bucket_filename, bucket_name)

        except Exception as e:
            raise UsVisaException(e, sys)
        
    
    def get_df_from_object(self, object_: object) -> pd.DataFrame:
        """
        This method gets the dataframe from the object_name object
        """
        try:
            content = self.read_object(object_, make_readable = True)
            df = pd.read_csv(content, na_values = "na")
            return df
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def read_csv(self, filename: str, bucket_name: str) -> pd.DataFrame:
        """
        This method gets the dataframe from the object_name object.
        """
        try:
            csv_obj = self.get_file_object(filename, bucket_name)
            df = self.get_df_from_object(csv_obj)
            return df
        
        except Exception as e:
            raise UsVisaException(e, sys)