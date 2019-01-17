from abc import ABCMeta
from abc import abstractmethod



__all__ = ["IoABC"]

class IoABC(metaclass=ABCMeta):
    
    @abstractmethod
    def execute(self,shuttle):
        """Executes clients"""