import os

from ..abs.client_abc import ClientABC
from ..utils.adapters import ShuttleAdapter

__all__ = ["LocalFileSystem"]

class LocalFileSystem(ClientABC):

    def __init__(self,file_path):
        self.file_path = file_path

    def read(self,shuttle):     
        
        #used for naming in ShuttleAdapter
        shuttle.client = self

        shuttle.write_path = self.file_path

        return ShuttleAdapter(shuttle=shuttle).read()

    def write(self, shuttle):

        #used for naming in ShuttleAdapter
        shuttle.client = self

        shuttle.write_path = self.file_path 

        return ShuttleAdapter(shuttle=shuttle).write()

    def delete(self,shuttle):

        os.remove(self.file_path)

        shuttle.client = self

        shuttle = ShuttleAdapter(shuttle=shuttle)

        shuttle.write_path = self.file_path

        return shuttle