from ..abs.client_abc import ClientABC
from ..utils.adapters import read_from_file
from ..utils.adapters import append_client_to_name
from ..utils.adapters import save_to_file

from PIL import Image

__all__ = ["ImageClient"]

class ImageClient(ClientABC):

    def read(self,shuttle):
        raise NotImplementedError('Use storage client to read image')

    def write(self,shuttle):
        raise NotImplementedError('Use storage client to write image')

    def edit(self,shuttle,crop_box):
        
        try:
            shuttle.client = self
            shuttle.name = append_client_to_name(shuttle=shuttle)

            image = shuttle.data
            shuttle.data = image.crop(crop_box)
            
            return shuttle

        except:
            raise 'Incorrect image data type: {}'.format(type(shuttle.data))

    def merge(self,shuttle):
        raise NotImplementedError('Use storage client to merge images')

    def delete(self,shuttle):
        pass       
                    