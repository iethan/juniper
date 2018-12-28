
from ..abs.io_abc import IoABC

__all__ = ["Read"]

class Read(IoABC):
    def __init__(self,client,**kwargs):
        self.client = client(**kwargs)
        self.objs = [self]

    def __add__(self,obj):
        self.objs.append(obj)
        return self    

    def execute(self,shuttle):
        return self.client.read(shuttle)