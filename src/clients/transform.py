from ..abs.client_abc import ClientABC

from ..utils.adapters import append_client_to_name


__all__ = ["Transform"]

class Transform(ClientABC,Exception):
    def __init__(self,exec_func):
        self.exec_func = exec_func

    def edit(self, shuttle):
        
        shuttle.client = self
        
        func_result = self.exec_func(shuttle.data,**shuttle.meta)

        shuttle.data = func_result

        shuttle.name = append_client_to_name(shuttle=shuttle)

        return shuttle

    def read(self,shuttle): 
        raise NotImplementedError('Use a storage client to reads data')

    def write(self,shuttle): 
        raise NotImplementedError('Use a storage client to write data')

    def delete(self,shuttle):
        raise NotImplementedError('Use a storage client to delete data')

    def merge(self,shuttle,exec_func):
        raise NotImplementedError
