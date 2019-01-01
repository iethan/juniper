import os
import shutil

__all__ = [
    "Shuttle",
    "Juniper",
]

class Cache: pass    

class Shuttle:
    def __init__(self,name=None):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        self._name = value
        return value

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self,value):
        self._client = value
        return value

    @property
    def staging_path(self):
        return self._staging_path

    @staging_path.setter
    def staging_path(self,value):
        self._staging_path = value
        return value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self,value):
        self._data = value
        return value
       
        
class Juniper:

    def __init__(self,staging_path='staging',cache=None,logging=None):        
        self.staging_path = staging_path
        #todo implement 
        self.cache = cache
        self.logging = logging
    
    def __rshift__(self,io):
        
        shuttle = Shuttle()

        if not os.path.exists(self.staging_path):
            os.makedirs(self.staging_path)

        for step,obj in enumerate(io.objs):            
            step = '{0:03d}'.format(step)
            shuttle.name = '-'.join([step,obj.__class__.__name__])
            shuttle.staging_path = self.staging_path
            shuttle = obj.execute(shuttle)

            print(shuttle.name)

        os.rmdir(self.staging_path)