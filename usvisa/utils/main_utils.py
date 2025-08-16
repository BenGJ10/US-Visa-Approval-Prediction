import os
import sys

import numpy as np
import pandas as pd
import dill
import yaml

from usvisa.logger.logger import logging
from usvisa.exception.exception import UsVisaException

def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise UsVisaException(e, sys) 



def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Writes content to a YAML file. If the file already exists and `replace` is True, it will be overwritten.
    If the file does not exist, it will be created along with any necessary directories.
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok = True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    
    except Exception as e:
        raise UsVisaException(e, sys) 



def load_object(file_path: str) -> object:
    """
    Loads an object from a specified file path using dill serialization.
    If the file does not exist or cannot be read, an exception is raised.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj)
        logging.info(f"Object loaded from {file_path}")
        return obj

    except Exception as e:
        raise UsVisaException(e, sys)
    


def save_object(file_path: str, obj: object) -> None:
    """
    Saves an object to a specified file path using dill serialization. If the directory does not exist, it will be created.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok = True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info(f"Object saved at {file_path}")

    except Exception as e:
        raise UsVisaException(e, sys) 



def save_numpy_array_data(file_path: str, array: np.array):
    """
    Saves a NumPy array to a specified file path. If the directory does not exist, it will be created.
    If the file already exists, it will be overwritten.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok = True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    
    except Exception as e:
        raise UsVisaException(e, sys)
    


def load_numpy_array_data(file_path: str) -> np.array:
    """
    Loads a NumPy array from a specified file path. If the file does not exist or cannot be read, an exception is raised.
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    
    except Exception as e:
        raise UsVisaException(e, sys)



def drop_columns(df: pd.DataFrame, cols: list)-> pd.DataFrame:
    """
    Drops specified columns from a DataFrame.
    """
    try:
        df = df.drop(columns = cols, axis = 1)
        logging.info(f"Dropped columns: {cols} from DataFrame")
        return df
    
    except Exception as e:
        raise UsVisaException(e, sys)