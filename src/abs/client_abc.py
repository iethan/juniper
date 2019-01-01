
from abc import ABCMeta
from abc import abstractmethod

__all__ = ["ClientABC"]

class ClientABC(metaclass=ABCMeta):
    
    @abstractmethod
    def read(self):
        """Read from source"""

    @abstractmethod
    def write(self):
        """Read to source"""

    @abstractmethod
    def delete(self):
        """Delete from source"""