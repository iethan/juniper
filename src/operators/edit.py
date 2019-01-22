
from ..abs.io_abc import IoABC
from ..utils.adapters import ParamAdapter

__all__ = ["Edit"]

class Edit(IoABC):
    def __init__(self,client,**params):
        self.params = params
        self.client = client
        self.objs = [self]

    def __add__(self,obj):
        self.objs.append(obj)
        return self    

    def execute(self,shuttle):
        shuttle = ParamAdapter(shuttle,self.params,self.client).run()
        shuttle = self.client.edit(shuttle)     
        return shuttle