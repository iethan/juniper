from ..abs.client_abc import ClientABC
from ..utils.adapters import ShuttleAdapter

from PIL import Image

class ImageClient(ClientABC):
    def __init__(self,file_path,crop_box=None):
        self._file_path = file_path
        self._crop_box = crop_box

    @property
    def crop_box(self,):
        return self._crop_box

    @property
    def file_path(self,):
        return self._file_path

    def read(self,shuttle):
        shuttle.client = self
        shuttle.write_path = self.file_path
        return ShuttleAdapter(shuttle=shuttle).read()

    def write(self,shuttle):
        shuttle.client = self
        shuttle.write_path = self.file_path
        return ShuttleAdapter(shuttle=shuttle).write()

    def edit(self,shuttle):
        
        shuttle.client = self
        shuttle.write_path = self.file_path
        
        img = Image.open(self.file_path)
        
        shuttle.data = img.crop(self.crop_box) 

        return ShuttleAdapter(shuttle=shuttle).shuttle


    def delete(self,shuttle):
        pass       
                    