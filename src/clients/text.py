from ..abs.client_abc import ClientABC
from ..utils.adapters import ShuttleAdapter

__all__ = ["Text"]

class Text(ClientABC):
    def __init__(self,data):
        self.data = data

    def read(self,shuttle):  
        shuttle.client = self

        shuttle.data = self.data 
        
        return ShuttleAdapter(shuttle=shuttle).shuttle

    def write(self,shuttle): 
        raise NotImplementedError('Use read method instead')

    def delete(self,shuttle):
        raise NotImplementedError