import os

from ...abs.client_abc import ClientABC

from ...utils.adapters import convert_to_string
from ...utils.adapters import read_from_file
from ...utils.adapters import save_to_file

from ...utils.adapters import append_client_to_name

__all__ = ["LocalFileSystem"]

class LocalFileSystem(ClientABC,Exception):


    def read(self, shuttle, file_path):     

        shuttle.client = self

        shuttle.data = read_from_file(file_path)
        shuttle.name = append_client_to_name(shuttle=shuttle)

        return shuttle

    def write(self, shuttle, file_path=None):

        shuttle.client = self

        #file_path can ride on the shuttle
        if not file_path:
            blob_name = shuttle.data['file_path']
            del shuttle.data['file_path']
            shuttle.data = shuttle.data['data']
        
        save_to_file(data=shuttle.data,file_path=file_path)
        
        shuttle.name = append_client_to_name(shuttle=shuttle)
        
        return shuttle

    def edit(self,shuttle, file_path):
        raise NotImplementedError('Use image or text clients for editing')

    def merge(self,shuttle, file_path):
        raise NotImplementedError('#TODO')

    def delete(self,shuttle, file_path):

        os.remove(file_path)

        shuttle.client = self

        shuttle.name = append_client_to_name(shuttle=shuttle)

        return shuttle