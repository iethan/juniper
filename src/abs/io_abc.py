from abc import ABCMeta
from abc import abstractmethod


class IoABC(metaclass=ABCMeta):
    
    @abstractmethod
    def execute(self):
        """Executes clients"""