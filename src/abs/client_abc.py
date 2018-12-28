
from abc import ABCMeta
from abc import abstractmethod


class ClientABC(metaclass=ABCMeta):
    
    @abstractmethod
    def read(self):
        """Read from Google Cloud Platform services"""

    @abstractmethod
    def write(self):
        """Write to Google Cloud Platform services"""

    @abstractmethod
    def delete(self):
        """Write to Google Cloud Platform services"""