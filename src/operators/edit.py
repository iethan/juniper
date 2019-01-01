
from ..abs.io_abc import IoABC

__all__ = ["Edit"]

class Edit(IoABC):
    def __init__(self,client,**kwargs):
        self.kwargs = kwargs
        self.client = client
        self.objs = [self]

    def __add__(self,obj):
        self.objs.append(obj)
        return self    

    def execute(self,shuttle):
        return self.client.edit(shuttle,**self.kwargs)