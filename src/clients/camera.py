from ..abs.client_abc import ClientABC
from ..utils.adapters import ShuttleAdapter

from PIL import Image

try:

    from picamera import PiCamera

except ModuleNotFoundError:
    import warnings
    warnings.warn('PiCamera could not found, loading mock')
    #mocking camera if not found
    
    class PiCamera:
        def start_preview(self,): pass
        def capture(self,file_name):
            img = Image.new('RGB', (640,480), color = 'red')
            img.save(file_name)
        def close(self,): pass

import time
import os

__all__ = ["CameraClient"]

class CameraClient(ClientABC):
    def __init__(self,file_path):
        self._file_path = file_path

    @property
    def file_path(self,):
        return self._file_path

    def read(self,shuttle):
        raise NotImplementedError('Cannot read an image with a camera. \
                                  Use write(shuttle) instead')

    def write(self,shuttle):

        shuttle.client = self
        shuttle.write_path = self.file_path        

        camera = PiCamera()
        camera.start_preview()
        time.sleep(2) #allows picamera start
        camera.capture(self.file_path)
        camera.close()
        
        shuttle.data = Image.open(self.file_path)

        return ShuttleAdapter(shuttle=shuttle).shuttle

    def delete(self,shuttle):

        raise NotImplementedError('Use the Filesystem delete')
                     