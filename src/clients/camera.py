from ..abs.client_abc import ClientABC

from ..utils.adapters import append_client_to_name

from PIL import Image

try:

    from picamera import PiCamera

except ModuleNotFoundError:
    # import warnings
    # warnings.warn('PiCamera could not found, loading mock')
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
    def __init__(self,sleep):
        self._sleep = sleep

    @property
    def sleep(self,):
        return self._sleep

    def read(self,shuttle):

        shuttle.client = self
        shuttle.name = append_client_to_name(shuttle=shuttle)

        tmp_file = '{}/{}.jpg'.format(shuttle.staging_path,shuttle.name.lower())

        camera = PiCamera()
        camera.start_preview()
        time.sleep(self.sleep) #allows picamera start
        camera.capture(tmp_file)
        camera.close()

        shuttle.data = Image.open(tmp_file)

        os.remove(tmp_file)

        return shuttle

    
    def write(self,shuttle):
        raise NotImplementedError('Cannot write an image with a camera. \
                                    Use read instead')

    def delete(self,shuttle):
        raise NotImplementedError('Use the storage client to delete')

    def edit(self,shuttle):
        raise NotImplementedError('Use the image client to edit')                     