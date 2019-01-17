
from ..abs.io_abc import IoABC
from ..utils.adapters import ExecuteClient

__all__ = ["Edit"]

class Edit(IoABC):
    def __init__(self,client,**params):
        self.params = params
        self.mime_type = params.get('mime_type','str')
        self.client = client
        self.objs = [self]

    def __add__(self,obj):
        self.objs.append(obj)
        return self    

    def execute(self,shuttle):
        return ExecuteClient.run(client = self.client.edit,
                                    shuttle = shuttle,
                                    mime_type = self.mime_type, 
                                    params = self.params)