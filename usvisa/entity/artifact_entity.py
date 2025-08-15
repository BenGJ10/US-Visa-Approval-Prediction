"""
Artifact entities are the outputs we get from various steps in the data pipeline.
These entities are used to store the results of data ingestion, data validation, data transorformation, and model training.
"""

from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    """
    Data class for storing paths related to data ingestion artifacts.
    This class holds the file paths for training and testing datasets
    after they have been processed and split from the original dataset.    
    """
    train_file_path: str
    test_file_path: str