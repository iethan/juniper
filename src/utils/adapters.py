import os
import zlib
from PIL import Image
from .converters import convert_to_string

__all__ = ["ShuttleAdapter"]

class ShuttleAdapter:
    def __init__(self,shuttle):
        self._shuttle = shuttle
        self._original_name = self._shuttle.name
        self._client_name = self._shuttle.client.__class__.__name__

    @property
    def shuttle(self):
        #append client to operator name
        self._shuttle.name = '-'.join([self._original_name,
                self._client_name])
        return self._shuttle

    @shuttle.setter
    def shuttle(self,value):
        self._shuttle = value
        return value

    def write(self):
        try:
            with open(self.shuttle.write_path,'+w') as f:
                data = convert_to_string(self.shuttle.data)
                f.write(data)

        except TypeError: #implementing PIL image save
            self.shuttle.data.save(self.shuttle.write_path)

        return self.shuttle

    def read(self):
        
        try:
            with open(self.shuttle.write_path,'r') as f:
                self.shuttle.data = f.read()

        except UnicodeDecodeError:
            self.shuttle.data = Image.open(self.shuttle.write_path)
        
        except FileNotFoundError:
            pass

        return self.shuttle