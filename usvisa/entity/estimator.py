import sys

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