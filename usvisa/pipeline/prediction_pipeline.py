import os
import sys
import numpy as np
import pandas as pd
from usvisa.logger.logger import logging
from usvisa.exception.exception import UsVisaException

from usvisa.entity.config_entity import UsVisaPredictorConfig
from usvisa.entity.s3_estimator import UsVisaEstimator
from usvisa.utils.main_utils import read_yaml_file

class UsVisaData:
    """
    Configuration class for the input data required for US Visa prediction.
    This class initializes the input data attributes based on the provided parameters.
    """
    def __init__(self, continent, education_of_employee, has_job_experience,
                requires_job_training, no_of_employees, region_of_employment,
                prevailing_wage, unit_of_wage, full_time_position, company_age):
        try:
            self.continent = continent
            self.education_of_employee = education_of_employee
            self.has_job_experience = has_job_experience
            self.requires_job_training = requires_job_training
            self.no_of_employees = no_of_employees
            self.region_of_employment = region_of_employment
            self.prevailing_wage = prevailing_wage
            self.unit_of_wage = unit_of_wage
            self.full_time_position = full_time_position
            self.company_age = company_age

        except Exception as e:
            raise UsVisaException(e, sys)
        
    def get_usvisa_input_data_frame(self)-> pd.DataFrame:
        """
        Converts the input data into a pandas DataFrame for prediction.
        This method constructs a DataFrame from the input data attributes, which can then be used for
        making predictions using the trained model.
        """
        try:    
            usvisa_input_dict = self.get_usvisa_data_as_dict()
            return pd.DataFrame(usvisa_input_dict)
        
        except Exception as e:
            raise UsVisaException(e, sys)

    def get_usvisa_data_as_dict(self):
        """
        Converts the input data into a dictionary format.
        This method prepares the input data as a dictionary, which can be used for model prediction.
        """
        try:
            input_data = {
                "continent": [self.continent],
                "education_of_employee": [self.education_of_employee],
                "has_job_experience": [self.has_job_experience],
                "requires_job_training": [self.requires_job_training],
                "no_of_employees": [self.no_of_employees],
                "region_of_employment": [self.region_of_employment],
                "prevailing_wage": [self.prevailing_wage],
                "unit_of_wage": [self.unit_of_wage],
                "full_time_position": [self.full_time_position],
                "company_age": [self.company_age],
            }
            return input_data
                
        except Exception as e:
            raise UsVisaException(e, sys)
        

class UsVisaClassifier:
    """
    A class for making predictions using the trained US Visa model.
    This class initializes the model configuration and provides a method to predict the visa status
    based on the input data.
    """
    def __init__(self, prediction_pipeline_config: UsVisaPredictorConfig = UsVisaPredictorConfig(),) -> None:
        try:
            # Initialize the configuration for the prediction pipeline
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise UsVisaException(e, sys)


    def predict(self, dataframe) -> str:
        """
        Predicts the visa status based on the input DataFrame.
        This method uses the trained model to make predictions on the provided DataFrame.
        """
        try:
            model = UsVisaEstimator(
                bucket_name = self.prediction_pipeline_config.model_bucket_name,
                model_path = self.prediction_pipeline_config.model_file_path,
            )
            result =  model.predict(dataframe)
            return result
        
        except Exception as e:
            raise UsVisaException(e, sys)