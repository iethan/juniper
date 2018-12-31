import os

from ..abs.client_abc import ClientABC

from ..utils.adapters import convert_to_string
from ..utils.adapters import read_from_file
from ..utils.adapters import save_to_file

from ..utils.adapters import append_client_to_name

__all__ = ["LocalFileSystem"]

class LocalFileSystem(ClientABC,Exception):

    def __init__(self,file_path):
        self.file_path = file_path

    def read(self,shuttle):     

        shuttle.client = self

        shuttle.data = read_from_file(self.file_path)
        shuttle.name = append_client_to_name(shuttle=shuttle)

        return shuttle

    def write(self, shuttle):

        shuttle.client = self
        
        save_to_file(data=shuttle.data,file_path=self.file_path)
        
        shuttle.name = append_client_to_name(shuttle=shuttle)
        
        return shuttle

    def edit(self,shuttle):
        raise NotImplementedError('Use image or text clients for editing')

    def merge(self,shuttle):
        raise NotImplementedError('#TODO')

    def delete(self,shuttle):

        os.remove(self.file_path)

        shuttle.client = self

        shuttle.name = append_client_to_name(shuttle=shuttle)

        return shuttle