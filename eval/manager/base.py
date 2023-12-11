"""base file"""
from abc import ABC, abstractmethod

class EvalBase(ABC):
    """base class"""
    @abstractmethod
    def evaluate(self, data_obj: dict):
        """Abstract method to evaluate"""
